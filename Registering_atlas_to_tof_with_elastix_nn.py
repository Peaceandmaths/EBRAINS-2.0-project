import SimpleITK as sitk
from time import time

# ==========================
# Define file paths
# ==========================
fixed_image_path = '/data/golubeka/EBRAINS/Nifti_T1_images/ToF-3D-multi-s2_anevrisme_-_6.nii.gz'  # TOF image (Fixed)
moving_image_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_64_DIMENSIONS.nii'  # Atlas (Moving)
result_path = '/data/golubeka/EBRAINS/Nifti_T1_images/registered_difumo_atlas_to_tof.nii.gz'

# ==========================
# Load images
# ==========================
fixedImage = sitk.ReadImage(fixed_image_path)
movingImage = sitk.ReadImage(moving_image_path)

# Set up ElastixImageFilter for registration
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage)
elastixImageFilter.SetMovingImage(movingImage)

# Define parameter maps for registration
parameterMap1 = sitk.GetDefaultParameterMap("translation")
parameterMap2 = sitk.GetDefaultParameterMap("rigid")
parameterMap3 = sitk.GetDefaultParameterMap("affine")

# Add parameter maps to the ElastixImageFilter
elastixImageFilter.SetParameterMap(parameterMap1)
elastixImageFilter.AddParameterMap(parameterMap2)
elastixImageFilter.AddParameterMap(parameterMap3)

# Time the registration
start_time = time()
elastixImageFilter.Execute()

# ==========================
# Resample Moving Image Using Transformix
# ==========================
# Set up TransformixImageFilter for resampling
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())
transformixImageFilter.SetMovingImage(movingImage)

# Execute Transformix to apply the transform
transformixImageFilter.Execute()

# Get the resampled (registered) atlas
resultImage = transformixImageFilter.GetResultImage()

# Save the registered atlas
sitk.WriteImage(resultImage, result_path)

# ==========================
# Print execution time
# ==========================
end_time = time()
print(f"Registration completed in {end_time - start_time:.2f} seconds")
print(f"Result saved to {result_path}")
