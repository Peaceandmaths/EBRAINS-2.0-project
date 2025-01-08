""" Equivalent of this script is the command line 
sftp://160.85.79.231/data/golubeka/data2024-mock/dcm2niix -z y -f t1_se_tra_4mm_-_13 -o /data/golubeka/EBRAINS/Nifti_T1_images /data/golubeka/EBRAINS/Patient_1712/t1_se_tra_4mm_-_13"""

import os
import subprocess
import time
from tqdm import tqdm
import logging

# Set paths
base_path = "/data/golubeka/EBRAINS/Patient_1712"  # Replace with the base directory path containing patient folders
output_path = "/data/golubeka/EBRAINS/Nifti_T1_images"  # Replace with the directory where you want to save the NIfTI files
os.makedirs(output_path, exist_ok=True)

# Configure logging
logging.basicConfig(filename="conversion_errors.log", level=logging.ERROR, format="%(asctime)s - %(message)s")

# Time tracking
start_time = time.time()

# Function to convert DICOM to NIfTI
def convert_dicom_to_nifti(input_folder, output_folder, output_name):
    """Converts DICOM files in the specified folder to NIfTI using dcm2niix, retaining the original name."""
    try:
        # Command to execute dcm2niix
        command = [
            "/data/golubeka/data2024-mock/dcm2niix",  # Path to dcm2niix executable
            "-z", "y",                    # Enable compression (output .nii.gz)
            "-f", output_name,            # Output filename, based on original DICOM folder name
            "-o", output_folder,          # Output directory
            input_folder                  # Input DICOM directory
        ]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to convert {input_folder} to NIfTI: {e}")

# Process each DICOM folder in the base path
for dicom_folder in tqdm(os.listdir(base_path), desc="Converting DICOM to NIfTI"):
    dicom_path = os.path.join(base_path, dicom_folder)
    if os.path.isdir(dicom_path):
        # Use the folder name as the output NIfTI file name to retain the original naming
        convert_dicom_to_nifti(dicom_path, output_path, dicom_folder)

# Print total processing time
end_time = time.time()
print(f"Total processing time: {end_time - start_time:.2f} seconds")
