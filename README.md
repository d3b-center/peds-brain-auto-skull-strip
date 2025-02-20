# Pediatric automated single- or multi-parametric skull stripping with nnUNet

This pipeline can be used to generate AI-predicted brain masks and skull-stripped images for pediatric patients with single- or multi-parametric MRIs. It was trained using the nnU-Net framework on a multi-institutional, heterogeneous dataset.

Dependencies include:
1. Python 3.9
2. PyTorch
3. nnUNet v1

The package will run nnUNet testing/inference with the pre-trained auto-skull-stripping model on the input files.

### Acknowledgement 
Ariana Familiar, PhD, Center for Data-Driven Discovery in Biomedicine (D3b), Children's Hospital of Philadelphia

## STEP 1: Prepare the input files

Required inputs:
All of the following pre-processed pediatric brain MRI scans for the multi-parametric model OR just one of the scans for the single-parametric model: 
1. T1-weighted pre-contrast (T1w)
2. T1-weighted post-contrast (T1w post-contrast)
3. T2-weighted (T2w)
4. T2-weighted FLAIR (T2w-FLAIR)

Input files (raw data) must be located in an directory folder and named with the following format: `[subID]_[imageID]...[.nii/.nii.gz]` where the imageID for each image type is:

| Image type      | imageID | nnUNet naming |
| ----------- | ----------- | ----------- |
| T2w-FLAIR      | FL       | 0000        |
| T1w   | T1        | 0001        |
| T1w post-contrast   | T1CE        | 0002        |
| T2w   | T2        | 0003        |


NOTE: the exact file format is required with an underscore: [subID]_[imageID]

For example:
```
input/
    sub001_FL.nii.gz
    sub001_T1.nii.gz
    sub001_T1CE.nii.gz
    sub001_T2.nii.gz
    sub002_FL.nii.gz
    ...
```

Configured to run on CPU.

## STEP 2: Usage

### [Install Docker](https://docs.docker.com/engine/install/)
### Copy all files into a single directory

1. copy the appropriate `.yml` file from this repository into the directory that contains your `input/` folder:
   docker-compose_single-parametric.yml for Single-parametric input
   docker-compose_multi-parametric.yml for Multi-parametric inputs

    Single-parametric model example: 
    ```
    docker-compose_single-parametric.yml
    input/
        sub001_FL.nii.gz
        sub002_T2.nii.gz
        ...
    ```

    Multi-parametric model example: 
    ```
    docker-compose_multi-parametric.yml
    input/
        sub001_FL.nii.gz
        sub002_T2.nii.gz
        ...
    ```
    
3. from within that folder, run the command:
    ```
    docker compose -f docker-compose_single-parametric.yml up

    or

    docker compose -f docker-compose_multi-parametric.yml up
    ```

## Available models:

- nnUNet-based skull-stripping using single-parametric brain MRI scans as input: Version 1
- nnUNet-based skull-stripping using multi-parametric brain MRI scans as input: Version 1

## References

- Isensee, F., Jaeger, P.F., Kohl, S.A.A. et al. "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation." Nat Methods (2020). https://doi.org/10.1038/s41592-020-01008-z


## Licenses

This software includes third party open source software components with their own licenses: 

- nnUnet: Apache-2.0 license : https://github.com/MIC-DKFZ/nnUNet?tab=Apache-2.0-1-ov-file
