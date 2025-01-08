import SimpleITK as sitk
import time
import nibabel as nib
import numpy as np
import os
from tqdm import tqdm

# Simple elastix doens't do skull stripping so we need to do it manually (?) or use TotalSegmentator 
# For CTA we need to crop the image to the brain first before registering.

# Paths
cta_path = '/data/golubeka/data2024-mock/Processed_v1_nifti/CT_converted/ANGIO_CT._20160310130837_4.nii.gz'
brain_mask_path = '/data/golubeka/data2024-mock/Processed_v1_nifti/CT_converted_brain/ANGIO_CT._20160310130837_4_brain_seg.nii.gz/brain.nii.gz'
output_path = '/data/golubeka/EBRAINS/CTA/cta_brain_cropped.nii.gz'
os.makedirs('/data/golubeka/EBRAINS/CTA/', exist_ok=True)

# Timer start
start_time = time.time()

try:
    # Load the images
    print("Loading CTA and brain mask...")
    cta_img = nib.load(cta_path)
    brain_mask_img = nib.load(brain_mask_path)
    
    cta_data = cta_img.get_fdata()
    brain_mask_data = brain_mask_img.get_fdata()
    
    # Keep only brain voxels
    print("Applying brain mask to keep only brain voxels...")
    brain_only_cta_data = cta_data * brain_mask_data  # Element-wise multiplication
    
    # Create a new NIfTI image with the brain-only data
    brain_only_cta_img = nib.Nifti1Image(brain_only_cta_data, affine=cta_img.affine)
    
    # Save the brain-only image
    print("Saving brain-only CTA image...")
    nib.save(brain_only_cta_img, output_path)
    
    print(f"Brain-only CTA image saved to {output_path}")
except Exception as e:
    print(f"An error occurred: {e}")

# Timer end
end_time = time.time()
print(f"Processing completed in {end_time - start_time:.2f} seconds.")



######################################### Coregistration #########################################
import SimpleITK as sitk

# Load images
fixedImage = sitk.ReadImage('/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_64_DIMENSIONS.nii')
movingImage = sitk.ReadImage('/data/golubeka/EBRAINS/CTA/cta_brain_cropped.nii.gz')

# Set up ElastixImageFilter
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage)
elastixImageFilter.SetMovingImage(movingImage)

# Add parameter maps (translation, rigid, affine)
parameterMap1 = sitk.GetDefaultParameterMap("translation")
parameterMap2 = sitk.GetDefaultParameterMap("rigid")
parameterMap3 = sitk.GetDefaultParameterMap("affine")

# If you want to include an initial transform, configure the parameter maps accordingly
parameterMap1["InitialTransform"] = ["NoInitialTransform"]  # Default; no initial transform
# Uncomment below if there's a precomputed transform:
# parameterMap1["InitialTransform"] = ["path/to/initial/transform.txt"]

# Add the parameter maps
elastixImageFilter.SetParameterMap(parameterMap1)
elastixImageFilter.AddParameterMap(parameterMap2)
elastixImageFilter.AddParameterMap(parameterMap3)

# Execute the registration
print("Starting registration...")
elastixImageFilter.Execute()

# Save the result
resultImage = elastixImageFilter.GetResultImage()
sitk.WriteImage(resultImage, '/data/golubeka/EBRAINS/Atlases/registered_difumo_atlas_to_cta_brain_cropped.nii.gz')
print("Registration completed and saved.")
