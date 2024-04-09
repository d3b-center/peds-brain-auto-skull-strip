# Pediatric automated defacing

Dependencies:
- Python 3.9
- PyTorch
- nnUNet v1

The package will run nnUNet testing/inference with the pre-trained auto-segmentation model on the input files.

Required inputs:
- image

Configured to run on CPU.

### Push to Docker Hub

Build the image locally:

```
docker build -t afam00/peds-brain-auto-skull-strip:0.0.0 .
```

Push the image to the Docker Hub:

```
docker image push afam00/peds-brain-auto-skull-strip:0.0.0
```

### Testing

From within the directory:

```
docker build -t peds-brain-auto-skull-strip .
```

```
docker run --rm peds-brain-auto-skull-strip
```

## Available models:

- 

## References

- Isensee, F., Jaeger, P.F., Kohl, S.A.A. et al. "nnU-Net: a self-configuring method for deep learning-based biomedical image segmentation." Nat Methods (2020). https://doi.org/10.1038/s41592-020-01008-z
