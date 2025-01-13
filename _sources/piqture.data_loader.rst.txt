Data Loader
============================

`piqture.data_loader.mnist_data_loader` module
-----------------------------------------------

This module provides a `load_mnist_dataset` function that simplifies loading the MNIST dataset for machine learning and deep learning experiments. It supports custom batch sizes, label selection, image resizing, and normalization options.

.. automodule:: piqture.data_loader.mnist_data_loader
   :members:
   :undoc-members:
   :show-inheritance:

Overview
--------

The `load_mnist_dataset` function in this module is designed to streamline the process of loading and preparing the MNIST dataset for image-based machine learning models, especially those involving quantum machine learning or custom image processing workflows.

Features
--------

- Supports custom image resizing to specified dimensions.
- Optionally filters specific labels from the MNIST dataset.
- Integrates custom normalization using `MinMaxNormalization`.
- Provides separate training and testing DataLoaders.

.. note::

   Make sure that the `torch` and `torchvision` libraries are installed, as these are used internally for dataset handling and transformations.

Function Documentation
----------------------

**`load_mnist_dataset`**

.. autofunction:: piqture.data_loader.mnist_data_loader.load_mnist_dataset

Usage Example
-------------

Here's an example of how to use the `load_mnist_dataset` function to load the MNIST dataset and apply custom configurations:

.. code-block:: python

    from piqture.data_loader import mnist_data_loader

    # Load MNIST dataset with custom configurations
    train_loader, test_loader = mnist_data_loader.load_mnist_dataset(
        img_size=(32, 32),          # Resize images to 32x32
        batch_size=64,              # Set batch size to 64
        labels=[0, 1, 2],           # Include only labels 0, 1, and 2
        normalize_min=0.0,          # Normalize minimum value to 0.0
        normalize_max=1.0           # Normalize maximum value to 1.0
    )

    # Print some batch information
    for images, labels in train_loader:
        print(f"Batch image shape: {images.shape}")
        print(f"Batch labels: {labels}")
        break

Parameters
----------

- **`img_size`** (*int* or *tuple[int, int]*, optional):
  - Size to which MNIST images will be resized.
  - If an integer, images will be resized to a square of that size.
  - If a tuple, it should specify `(height, width)` for the images.
  - **Default:** `28` (images are resized to 28x28 pixels).

- **`batch_size`** (*int*, optional):
  - Specifies the number of samples per batch for training and testing DataLoaders.
  - If not specified, the batch size defaults to `1`.

- **`labels`** (*list[int]*, optional):
  - A list of integers representing the labels to include in the dataset.
  - For example, setting `labels=[0, 1]` will include images of digits 0 and 1 only.

- **`normalize_min`** (*float*, optional):
  - Minimum value for pixel normalization.
  - **Default:** `None` (no normalization).

- **`normalize_max`** (*float*, optional):
  - Maximum value for pixel normalization.
  - **Default:** `None` (no normalization).

Returns
-------

- **`Tuple[torch.utils.data.DataLoader, torch.utils.data.DataLoader]`**:
  - A tuple containing:
    - **Training DataLoader**: A PyTorch DataLoader for training data.
    - **Testing DataLoader**: A PyTorch DataLoader for testing data.

Related Functions and Classes
-----------------------------

**`collate_fn`**

The `collate_fn` function is used to filter and organize batches based on the specified `labels`. It only includes images that match the desired labels.

.. autofunction:: piqture.data_loader.mnist_data_loader.collate_fn

Dependencies
------------

- **torch**: Required for creating PyTorch DataLoaders.
- **torchvision**: Required for dataset loading and transformations.
- **piqture.transforms.MinMaxNormalization**: Custom normalization transform available in the `piqture.transforms` module.

Handling Edge Cases
-------------------

The function performs type checking and validation to ensure that the input parameters are valid:

- **`img_size`**: Raises a `TypeError` if the value is not of type `int` or `tuple[int, int]`.
- **`batch_size`**: Raises a `TypeError` if the value is not an integer.
- **`labels`**: Raises a `TypeError` if the value is not a list.

Refer to the `source code <https://github.com/SaashaJoshi/piqture>`_ for additional implementation details and advanced configurations.

.. seealso::

   - `torchvision.datasets.MNIST <https://pytorch.org/vision/stable/datasets.html#mnist>`_
   - `piqture.transforms.MinMaxNormalization <https://piqture.readthedocs.io/en/latest/transforms.html#piqture.transforms.MinMaxNormalization>`_
