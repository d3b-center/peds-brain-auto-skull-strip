import os

import nibabel as nib
import numpy as np

def apply_mask(nifti_fn, mask_fn, out_file_path):
    # nifti_fn = input image
    # mask_fn = face mask
    # out_file_path = output image

    # Get the data arrays from the images
    nifti_image = nib.load(nifti_fn)
    mask_image = nib.load(mask_fn)
    nifti_data = nifti_image.get_fdata()
    mask_data = mask_image.get_fdata()

    # Apply the binary mask to the NIfTI data
    inv_mask_data = 1 - mask_data
    masked_data = nifti_data * inv_mask_data

    # Create a new NIfTI image with the masked data
    masked_image = nib.Nifti1Image(masked_data, nifti_image.affine)

    # Save the masked image to a new file
    nib.save(masked_image, f'{out_file_path}')
