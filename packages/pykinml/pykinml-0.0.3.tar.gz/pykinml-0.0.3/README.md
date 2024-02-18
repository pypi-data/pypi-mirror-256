# pyKinML: Package for training Neural Net Potential Energy Surfaces



## Description
This repository contains the code to train NNPESs and use those models with an ASE calculator.

### How to install

This package can be installed with pip or by cloning this repo and installing it locally.

## Install with pip:

    pip install pykinml

### Clone from repo:
    git clone git@github.com:sandialab/pykinml.git


This package relies on PyTorch_scatter to sum the atomic contributions to energy. Ensure you have the proper version. Instructions for installation can be found at:
https://github.com/rusty1s/pytorch_scatter
