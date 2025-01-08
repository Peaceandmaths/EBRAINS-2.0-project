import SimpleITK as sitk
import matplotlib.pyplot as plt
import os

# Function to display images
def display_images(fixed, moving, registered):
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    axes[0].imshow(sitk.GetArrayViewFromImage(fixed), cmap='gray')
    axes[0].set_title('Fixed Image')
    axes[0].axis('off')
    
    axes[1].imshow(sitk.GetArrayViewFromImage(moving), cmap='gray')
    axes[1].set_title('Moving Image')
    axes[1].axis('off')
    
    axes[2].imshow(sitk.GetArrayViewFromImage(registered), cmap='gray')
    axes[2].set_title('Registered Image')
    axes[2].axis('off')
    
    plt.show()

# Paths to fixed (T1) and moving (TOF) images
base_dir = '/data/golubeka/EBRAINS/Nifti_T1_images'
fimg = 'sT1W_3D_TFE_tra_HR_GADO_-_1401.nii.gz'  # T1-weighted image
mimg = 'WILLIS_4min_-_501.nii.gz'               # TOF image
ffixedImage = os.path.join(base_dir, fimg)
fmovingImage = os.path.join(base_dir, mimg)

# Load images
fixedImage = sitk.ReadImage(ffixedImage)
movingImage = sitk.ReadImage(fmovingImage)

# Register images using SimpleElastix
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage)
elastixImageFilter.SetMovingImage(movingImage)
elastixImageFilter.LogToConsoleOn()
elastixImageFilter.SetParameterMap(sitk.GetDefaultParameterMap("rigid"))
elastixImageFilter.Execute()

# Get the registered image
registeredImage = elastixImageFilter.GetResultImage()

# Display the images
display_images(fixedImage, movingImage, registeredImage)