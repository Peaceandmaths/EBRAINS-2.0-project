import SimpleITK as sitk
import os
from time import time
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(filename='registration_errors.log', level=logging.ERROR)

# Base directory for your images
base_dir = '/data/golubeka/EBRAINS/Nifti_T1_images'

# Function to register TOF to T1-weighted image
def register_images():
    # Paths to fixed (T1) and moving (TOF) images
    fimg = 'sT1W_3D_TFE_tra_HR_GADO_-_1401.nii.gz'  # T1-weighted image
    mimg = 'WILLIS_4min_-_501.nii.gz'               # TOF image
    ffixedImage = os.path.join(base_dir, fimg)
    fmovingImage = os.path.join(base_dir, mimg)

    try:
        # Load images
        fixedImage = sitk.ReadImage(ffixedImage)
        movingImage = sitk.ReadImage(fmovingImage)

        # Set up parameter maps for multi-stage registration
        parameterMap1 = sitk.GetDefaultParameterMap('translation')
        parameterMap1['MaximumNumberOfIterations'] = ['256']
        parameterMap1['FinalBSplineInterpolationOrder'] = ['4']

        parameterMap2 = sitk.GetDefaultParameterMap('rigid')
        parameterMap2['MaximumNumberOfIterations'] = ['512']
        parameterMap2['FinalBSplineInterpolationOrder'] = ['4']

        parameterMap3 = sitk.GetDefaultParameterMap('affine')
        parameterMap3['MaximumNumberOfIterations'] = ['512']
        parameterMap3['FinalBSplineInterpolationOrder'] = ['4']

        parameterMap4 = sitk.GetDefaultParameterMap('bspline')
        parameterMap4['MaximumNumberOfIterations'] = ['512']
        parameterMap4['FinalBSplineInterpolationOrder'] = ['4']

        # Initialize ElastixImageFilter for registration
        elastixImageFilter = sitk.ElastixImageFilter()
        elastixImageFilter.LogToConsoleOn()
        elastixImageFilter.SetFixedImage(fixedImage)
        elastixImageFilter.SetMovingImage(movingImage)

        # Add parameter maps for different stages
        elastixImageFilter.SetParameterMap(parameterMap1)
        elastixImageFilter.AddParameterMap(parameterMap2)
        elastixImageFilter.AddParameterMap(parameterMap3)
        # Uncomment the next line if bspline transformation is needed
        # elastixImageFilter.AddParameterMap(parameterMap4)

        # Print parameter maps for verification
        elastixImageFilter.PrintParameterMap()

        # Execute registration
        start_time = time()
        elastixImageFilter.Execute()
        end_time = time()
        print(f"Registration completed in {end_time - start_time:.2f} seconds")

        # Save the result image
        resultImage = elastixImageFilter.GetResultImage()
        resultFile = os.path.join(base_dir, 'registered_TOF_to_T1_201033417.nii.gz')
        sitk.WriteImage(resultImage, resultFile)

    except Exception as e:
        logging.error(f"Error during registration: {e}")
        print(f"An error occurred: {e}")

# Run the registration process
if __name__ == '__main__':
    with tqdm(total=1, desc="Registering TOF to T1") as pbar:
        register_images()
        pbar.update(1)
