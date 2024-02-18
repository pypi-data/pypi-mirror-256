# DIRESA

This package contains the following modules:
1. diresa.models
    - for creating (V)AE and DIRESA models out of encoder and decoder model
	- for creating AE and DIRESA models from hyperparameters
2. diresa.loss
    - contains Covariance loss function, different Distance loss functions and KL loss function
3. diresa.layers
    - contains Sampling, Distance and Mask layer
4. diresa.callback
    - contains LossWeightAnnealing callback
5. diresa.toolbox
    - function to cut submodels out of a keras model