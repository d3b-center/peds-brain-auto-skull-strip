
import os
import shutil
import sys
from glob import glob

from apply_face_mask import apply_mask

CONTAINER="[d3b-ped-auto-deface]"
print(f"{CONTAINER}  Initiated")

###############################################################################
out_path="output/"

print(f"{CONTAINER}  STEP 1/3 Preparing files and directories for nnUNet inference")
test_data_dir="nnUNet_raw_data_base/nnUNet_raw_data/Task070_autosegm/imageTs/"
result_data_dir="nnUNet_trained_models/nnUNet_prediction/"

# set required nnUnet environment variables
os.environ["nnUNet_raw_data_base"] = "nnUNet_raw_data_base"
os.environ["nnUNet_preprocessed"] = "nnUNet_preprocessed"
os.environ["RESULTS_FOLDER"] = "nnUNet_trained_models"


## Find the input files
for im_file in glob("input/*.nii*"):

    # define the output file name
    orig_im_fn = os.path.basename(im_file)
    if orig_im_fn.endswith('.nii.gz'):
        out_file_name = orig_im_fn.rstrip('.nii.gz') + '_defaced.nii.gz'
        out_mask_name = orig_im_fn.rstrip('.nii.gz') + '_face_mask.nii.gz'
    elif orig_im_fn.endswith('.nii'):
        out_file_name = orig_im_fn.rstrip('.nii') + '_defaced.nii.gz'
        out_mask_name = orig_im_fn.rstrip('.nii') + '_face_mask.nii.gz'

    shutil.copy(im_file, f'{test_data_dir}/chop_000_0000.nii.gz')
    # nnUNet_plan_and_preprocess -t 070

    print(f"{CONTAINER}  STEP 2/3 Running nnUNet automated face mask inference on file: {im_file}")
    ## usage: nnUNet_predict -i INPUT_FOLDER -o OUTPUT_FOLDER -t TASK_NAME_OR_ID -m CONFIGURATION
    os.system(f'nnUNet_predict -i {test_data_dir} -o {result_data_dir} -t Task070_autosegm -m 3d_fullres')

    # rename the output files
    if not os.path.exists('output'):
        os.makedirs('output')

    shutil.move(f'{result_data_dir}/chop_000.nii.gz', f'output/{out_mask_name}')
    print(f"           face mask saved to: output/{out_mask_name}")

    # apply the predicted face mask to the original image, output defaced image called "[orig_im_name]_defaced.nii.gz"
    print(f"{CONTAINER}  STEP 3/3 Applying predicted face mask to input image")
    apply_mask(f'{test_data_dir}/chop_000_0000.nii.gz', f'output/{out_mask_name}', f'output/{out_file_name}')
    print(f"           defaced image saved to: output/{out_file_name}")

    ################# Finish up #################

    print(f"{CONTAINER}  Done!")
