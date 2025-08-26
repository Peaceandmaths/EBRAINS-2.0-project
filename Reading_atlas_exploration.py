import nibabel as nib
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import os

# =========================
# Define file paths
# =========================
registered_atlas_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_64_DIMENSIONS.nii'  # Path to your labeled atlas file
tof_path = "/data/golubeka/EBRAINS/Nifti_T1_images/ToF-3D-multi-s2_anevrisme_-_6.nii.gz"                # Path to the registered TOF file

# =========================
# Load the registered files
# =========================
# Load NIfTI files
registered_atlas = nib.load(registered_atlas_path)
registered_atlas_data = registered_atlas.get_fdata()

tof = nib.load(tof_path)
tof_data = tof.get_fdata()

# Print basic information
print(f"Atlas shape: {registered_atlas_data.shape}")
print(f"TOF shape: {tof_data.shape}")

# Check if dimensions match
if registered_atlas_data.shape != tof_data.shape:
    print("Warning: Dimensions of the atlas and TOF image do not match!")

# =========================
# Visualize the Atlas and TOF
# =========================

# Function to display two images side by side
def plot_side_by_side(slice_index, atlas_data, tof_data, title1="Atlas", title2="TOF"):
    plt.figure(figsize=(12, 6))
    
    # Atlas slice
    plt.subplot(1, 2, 1)
    plt.imshow(atlas_data[:, :, slice_index], cmap="nipy_spectral", interpolation="nearest")
    plt.colorbar(label="Label")
    plt.title(f"{title1} (Slice {slice_index})")
    
    # TOF slice
    plt.subplot(1, 2, 2)
    plt.imshow(tof_data[:, :, slice_index], cmap="gray", interpolation="nearest")
    plt.colorbar(label="Intensity")
    plt.title(f"{title2} (Slice {slice_index})")
    
    plt.show()

# Choose a slice index to visualize
slice_index = registered_atlas_data.shape[2] // 2  # Middle slice
plot_side_by_side(slice_index, registered_atlas_data, tof_data)

# =========================
# Overlay the Atlas on TOF
# =========================
def overlay_atlas_on_tof(slice_index, atlas_data, tof_data, alpha=0.5):
    plt.figure(figsize=(8, 8))
    
    # TOF background
    plt.imshow(tof_data[:, :, slice_index], cmap="gray", interpolation="nearest", alpha=1.0)
    
    # Atlas overlay
    plt.imshow(atlas_data[:, :, slice_index], cmap="nipy_spectral", interpolation="nearest", alpha=alpha)
    
    plt.colorbar(label="Atlas Labels")
    plt.title(f"Overlay: TOF with Atlas (Slice {slice_index})")
    plt.show()

# Visualize overlay with transparency
overlay_atlas_on_tof(slice_index, registered_atlas_data, tof_data, alpha=0.5)


############# Visualize only coregistered image 

import nibabel as nib
import matplotlib.pyplot as plt

# =========================
# Define file path
# =========================
coregistered_image_path = "/data/golubeka/EBRAINS/Nifti_T1_images/registered_difumo_atlas_to_tof.nii.gz"  # Replace with your file path

# =========================
# Load the Coregistered Image
# =========================
coregistered_image = nib.load(coregistered_image_path)
coregistered_data = coregistered_image.get_fdata()

# Print basic information
print(f"Coregistered image shape: {coregistered_data.shape}")

# =========================
# Visualize the Coregistered Image
# =========================
def visualize_coregistered(slice_index, data, title="Coregistered Image"):
    plt.figure(figsize=(8, 8))

    # Show the selected slice
    plt.imshow(data[:, :, slice_index], cmap="nipy_spectral", interpolation="nearest")
    plt.colorbar(label="Intensity/Labels")
    plt.title(f"{title} (Slice {slice_index})")
    plt.show()

# Choose a slice index to visualize
slice_index = coregistered_data.shape[2] // 3  # Middle slice
visualize_coregistered(slice_index, coregistered_data)


################### Last version ? No, I still can't see vessels 

import SimpleITK as sitk
from time import time

# ==========================
# Define file paths
# ==========================

fixed_image_path = "/data/golubeka/EBRAINS/Nifti_T1_images/ToF-3D-multi-s2_anevrisme_-_6.nii.gz"   # TOF image (Fixed)
moving_image_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_64_DIMENSIONS.nii'     # Atlas (Moving)
result_registered_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_REGISTERED.nii'  # Output path for registered atlas

# ==========================
# Load the Images
# ==========================
fixedImage = sitk.ReadImage(fixed_image_path)  # TOF image (intensity-based)
movingImage = sitk.ReadImage(moving_image_path)  # Atlas (categorical labels)

# Set up ElastixImageFilter for registration
elastixImageFilter = sitk.ElastixImageFilter()
elastixImageFilter.SetFixedImage(fixedImage)  # TOF image as fixed
elastixImageFilter.SetMovingImage(movingImage)  # Atlas as moving

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
# Resample the Atlas with Nearest-Neighbor Interpolation
# ==========================
# Use Transformix to resample the moving image
transformixImageFilter = sitk.TransformixImageFilter()
transformixImageFilter.SetMovingImage(movingImage)
transformixImageFilter.SetTransformParameterMap(elastixImageFilter.GetTransformParameterMap())
transformixImageFilter.Execute()

# Retrieve the registered atlas
registeredAtlas = transformixImageFilter.GetResultImage()

# Save the registered atlas
sitk.WriteImage(registeredAtlas, result_registered_path)
print(f"Registered atlas saved to: {result_registered_path}")

# ==========================
# Visualize the Results
# ==========================
import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# Load the TOF and registered atlas
tof_image = sitk.GetArrayFromImage(fixedImage)  # Convert TOF to NumPy array
registered_atlas = sitk.GetArrayFromImage(registeredAtlas)  # Convert atlas to NumPy array

# Choose a slice index
slice_index = tof_image.shape[0] // 2  # Middle slice

# Plot TOF and registered atlas side by side
plt.figure(figsize=(12, 6))

# TOF image
plt.subplot(1, 2, 1)
plt.imshow(tof_image[slice_index, :, :], cmap="gray", interpolation="nearest")
plt.title("TOF Image (Slice)")
plt.colorbar(label="Intensity")

# Registered atlas
plt.subplot(1, 2, 2)
plt.imshow(registered_atlas[slice_index, :, :], cmap="nipy_spectral", interpolation="nearest")
plt.title("Registered Atlas (Slice)")
plt.colorbar(label="Labels")

plt.show()


################# Visualizing the coregistered image 

import nibabel as nib
import matplotlib.pyplot as plt
import numpy as np

# ==========================
# Define file path
# ==========================
registered_image_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_REGISTERED.nii'  # Path to the co-registered image

# ==========================
# Load the Co-Registered Image
# ==========================
registered_img = nib.load(registered_image_path)
registered_data = registered_img.get_fdata()

# Print basic information about the image
print(f"Co-registered image shape: {registered_data.shape}")
print(f"Intensity range: {np.min(registered_data)} to {np.max(registered_data)}")

# ==========================
# Visualize the Co-Registered Image
# ==========================
def visualize_registered(slice_index, data, cmap="nipy_spectral", title="Co-Registered Image"):
    plt.figure(figsize=(8, 8))
    plt.imshow(data[:, :, slice_index], cmap=cmap, interpolation="nearest")
    plt.colorbar(label="Intensity/Labels")
    plt.title(f"{title} (Slice {slice_index})")
    plt.show()

# Choose a slice index for visualization
slice_index = registered_data.shape[2] // 2  # Middle slice
# see a different slice 
slice_index = 50
visualize_registered(slice_index, registered_data, cmap="nipy_spectral")


# Plot intensity histogram
plt.figure(figsize=(10, 6))
plt.hist(registered_data.flatten(), bins=100, color="blue", alpha=0.7)
plt.title("Intensity Distribution of Co-Registered Image")
plt.xlabel("Intensity")
plt.ylabel("Frequency")
plt.show()


## Overlay tof to registered atlas 

import nibabel as nib
import numpy as np
import matplotlib.pyplot as plt

# ==========================
# Define file paths
# ==========================
tof_path = '/data/golubeka/EBRAINS/Nifti_T1_images/ToF-3D-multi-s2_anevrisme_-_6.nii.gz'            # Path to TOF image
registered_atlas_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_REGISTERED.nii'  # Path to registered atlas

# ==========================
# Load images
# ==========================
tof_img = nib.load(tof_path)
tof_data = tof_img.get_fdata()

registered_atlas_img = nib.load(registered_atlas_path)
registered_atlas_data = registered_atlas_img.get_fdata()

# Ensure dimensions match
if tof_data.shape != registered_atlas_data.shape:
    raise ValueError("TOF image and registered atlas dimensions do not match!")

# ==========================
# Visualize Overlay
# ==========================
def overlay_tof_with_labels(tof, labels, slice_index, alpha=0.5):
    plt.figure(figsize=(8, 8))

    # TOF image as background
    plt.imshow(tof[:, :, slice_index], cmap="gray", interpolation="nearest", alpha=1.0)

    # Registered atlas as overlay
    plt.imshow(labels[:, :, slice_index], cmap="nipy_spectral", interpolation="nearest", alpha=alpha)

    plt.colorbar(label="Labels")
    plt.title(f"Overlay of TOF and Registered Atlas (Slice {slice_index})")
    plt.show()

# Choose a slice index
slice_index = tof_data.shape[2] // 2  # Middle slice
slice_index = 80
overlay_tof_with_labels(tof_data, registered_atlas_data, slice_index, alpha=0.5)

##### Visualize 3D with SLicer 


# ==========================
# Interactive Slider
# ==========================

from matplotlib.widgets import Slider
import matplotlib
import matplotlib
matplotlib.use('Agg')

# ==========================
# Visualization Function
# ==========================
# Ensure interactive mode is enabled
plt.ion()

def plot_slice(slice_index):
    """Function to plot a single slice with TOF and atlas overlay."""
    plt.clf()  # Clear the current figure
    plt.imshow(tof_data[:, :, slice_index], cmap="gray", alpha=1.0)  # TOF as background
    plt.imshow(registered_atlas_data[:, :, slice_index], cmap="nipy_spectral", alpha=0.5)  # Labels overlay
    plt.title(f"Slice {slice_index}")
    plt.colorbar(label="Labels")
    plt.draw()
    plt.pause(0.01)

# Set up the figure and slider
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2)  # Space for the slider

# Display the initial slice
initial_slice = tof_data.shape[2] // 2  # Start with the middle slice
plot_slice(initial_slice)


# Add a slider for slice navigation
ax_slider = plt.axes([0.2, 0.1, 0.6, 0.03])  # Slider position
slice_slider = Slider(ax_slider, 'Slice', 0, tof_data.shape[2] - 1, valinit=initial_slice, valstep=1)

# Update function for the slider
def update(val):
    slice_index = int(slice_slider.val)
    plot_slice(slice_index)

# Connect the slider to the update function
slice_slider.on_changed(update)
plt.show()


### Visualize 3D volume rendering using pyvista 
import nibabel as nib
import numpy as np
import pyvista as pv


# Ensure dimensions match
if tof_data.shape != registered_atlas_data.shape:
    raise ValueError("TOF image and registered atlas dimensions do not match!")

# ==========================
# Preprocess Data for Visualization
# ==========================
# Normalize TOF intensity data for better visualization
tof_data_normalized = (tof_data / np.max(tof_data)) * 255  # Scale to [0, 255]

# Create a combined volume
# Assign atlas labels a higher intensity range to make them visually distinct
combined_volume = np.copy(tof_data_normalized)
atlas_intensity_offset = 300  # Offset to distinguish labels
combined_volume[registered_atlas_data > 0] = atlas_intensity_offset + registered_atlas_data[registered_atlas_data > 0]

# ==========================
# Create a PyVista Uniform Grid
# ==========================
grid = pv.UniformGrid()
grid.dimensions = combined_volume.shape  # Match dimensions to the volume
grid.origin = (0, 0, 0)  # Origin at (0, 0, 0)
grid.spacing = (1, 1, 1)  # Set grid spacing (adjust if necessary)
grid.point_data["values"] = combined_volume.flatten(order="F")  # Add volume data

# ==========================
# Volume Rendering
# ==========================
# Set up the PyVista plotter
plotter = pv.Plotter()
opacity = [0, 0.1, 0.3, 0.6, 0.9, 1]  # Define opacity transfer function
plotter.add_volume(grid, scalars="values", cmap="nipy_spectral", opacity=opacity, shade=True)

# Add axes and grid for reference
plotter.add_axes()
plotter.show_grid()

# Show the rendered volume
plotter.show()

import nibabel as nib

# Path to your labeled atlas file
registered_atlas_path = '/data/golubeka/EBRAINS/Atlases/DIFUMO_ATLAS_64_DIMENSIONS.nii'

# Load the atlas file
atlas_img = nib.load(registered_atlas_path)

# Get the header information
header = atlas_img.header

# Print the resolution (voxel dimensions)
print("Resolution (voxel dimensions):", header.get_zooms())
