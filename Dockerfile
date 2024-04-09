# Creates docker container

#############################################
# Select the OS
FROM python:3.9.7-slim-buster AS base

#############################################
# install PyTorch
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# install nnUNet
RUN pip3 install nnunet==1.7.1

# install other Python packages
RUN pip3 install numpy==1.24.0
RUN pip3 install nibabel==3.2.2

#############################################
# Configure entrypoint
FROM base AS release
# COPY input/ /input
COPY nnUNet_preprocessed /nnUNet_preprocessed
COPY nnUNet_raw_data_base /nnUNet_raw_data_base
COPY nnUNet_trained_models /nnUNet_trained_models
COPY *.py .
CMD [ "python3", "run.py" ]
