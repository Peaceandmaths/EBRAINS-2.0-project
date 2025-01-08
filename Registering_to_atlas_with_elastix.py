import SimpleITK as sitk
from time import time
# Count the time taken for registration


# Load images
fimg = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_64_DIMENSIONS.nii'  # Atlas 
#mimg = '/data/golubeka/EBRAINS/Nifti_T1_images/ToF-3D-multi-s2_anevrisme_-_6.nii.gz' # TOF image
mimg = '/data/golubeka/data2024-mock/Processed_v1_nifti/CT_converted_brain_cropped/ANGIO_20150709144655_5.nii.gz' # CTA
result_path = '/data/golubeka/EBRAINS/Atlases/registered_difumo_atlas_to_cta_brain_cropped.nii.gz'

fixedImage = sitk.ReadImage(fimg)
movingImage = sitk.ReadImage(mimg)

# Set up the ElastixImageFilter for registration
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage)
elastixImageFilter.SetMovingImage(movingImage)

# Define parameter maps (e.g., translation, rigid, affine) for multi-stage registration
parameterMap1 = sitk.GetDefaultParameterMap("translation")
parameterMap2 = sitk.GetDefaultParameterMap("rigid")
parameterMap3 = sitk.GetDefaultParameterMap("affine")

# Add the parameter maps to the ElastixImageFilter
elastixImageFilter.SetParameterMap(parameterMap1)
elastixImageFilter.AddParameterMap(parameterMap2)
elastixImageFilter.AddParameterMap(parameterMap3)

# Time the registration
start_time = time()
# Execute the registration
elastixImageFilter.Execute()

# Get the result image
resultImage = elastixImageFilter.GetResultImage()

# Save the result image
sitk.WriteImage(resultImage, result_path)

# Print the time taken for registration
end_time = time()
print(f"Registration completed in {end_time - start_time:.2f} seconds")
print(f"Registration completed. Result saved to {result_path}")
