
import os
import shutil
import sys
from glob import glob

from apply_nifti_mask import apply_mask

CONTAINER="[d3b-ped-skull-strip]"
print(f"{CONTAINER}  Initiated")

###############################################################################
input_folder='input/'
out_path="output/"

## RENAME INPUT FILES (if needed)
# | Image type      | imageID |
# | ----------- | ----------- |
# | T2w-FLAIR      | 0000       |
# | T1w   | 0001        |
# | T1w post-contrast   | 0002        |
# | T2w   | 0003        |
print(f"{CONTAINER}  STEP 1/3 Preparing files and directories for nnUNet inference")
for file_path in glob(f'{input_folder}/*.nii*'):
    file_name = file_path.split('/')[-1]
    if len(file_name.split('.gz')) > 1:
        file_ending = '.nii.gz'
    else:
        file_ending = '.nii'
    if '_T1CE' in file_name:
        sub_id = file_name.split('_T1CE')[0]
        new_fn = f'{sub_id}_0002{file_ending}'
        shutil.move(file_path, f'{input_folder}/{new_fn}')
    elif '_T2' in file_name:
        sub_id = file_name.split('_T2')[0]
        new_fn = f'{sub_id}_0003{file_ending}'
        shutil.move(file_path, f'{input_folder}/{new_fn}')
    elif '_FL' in file_name:
        sub_id = file_name.split('_FL')[0]
        new_fn = f'{sub_id}_0000{file_ending}'
        shutil.move(file_path, f'{input_folder}/{new_fn}')
    elif '_T1' in file_name:
        sub_id = file_name.split('_T1')[0]
        new_fn = f'{sub_id}_0001{file_ending}'
        shutil.move(file_path, f'{input_folder}/{new_fn}')

# set required nnUnet environment variables
os.environ["nnUNet_raw_data_base"] = "nnUNet_raw_data_base"
os.environ["nnUNet_preprocessed"] = "nnUNet_preprocessed"
test_data_dir=f"{input_folder}"
os.environ["RESULTS_FOLDER"] = "nnUNet_trained_models"
result_data_dir="nnUNet_trained_models/nnUNet_prediction/"

print(f"{CONTAINER}  STEP 2/3 Running nnUNet automated brain mask inference with 4 input files:")
## usage: nnUNet_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -t TASK_NAME_OR_ID -m CONFIGURATION
os.system(f'nnUNet_predict -i {test_data_dir} -o {result_data_dir} -t Task070_autosegm -m 3d_fullres')

# rename the output files
if not os.path.exists(out_path):
    os.makedirs(out_path)

print(f"{CONTAINER}  STEP 3/3 Applying predicted face masks to input images")
for pred_mask_path in glob(f'{result_data_dir}/*.nii*'):
    sub_id = pred_mask_path.split('/')[-1].split('.nii.gz')[0]
    # rename the mask file
    out_mask_name = f'{sub_id}_pred_brainMask.nii.gz'
    shutil.move(f'{pred_mask_path}', f'{out_path}/{out_mask_name}')
    # shutil.move(f'{result_data_dir}/chop_000.nii.gz', f'{out_path}/{out_mask_name}')
    print(f"           face mask saved to: {out_path}/{out_mask_name}")
    # apply the predicted mask to the original image
    for in_file in glob(f'{input_folder}/{sub_id}*'):
        orig_im_fn = os.path.basename(in_file)
        out_file_name = orig_im_fn.replace('.nii.gz','') + '_ss.nii.gz'
        apply_mask(f'{in_file}', f'{out_path}/{out_mask_name}', f'{out_path}/{out_file_name}')
        print(f"           skull stripped image saved to: {out_path}/{out_file_name}")

################# Finish up #################
# for in_file in glob(test_data_dir):
#     os.remove(in_file)

print(f"{CONTAINER}  Done subject: {sub_id}")