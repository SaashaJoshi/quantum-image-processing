Getting Started
================

Setup
-----

Begin by creating a new Python environment or activating an existing one for working with the `piQture` library. You set up a Python virtual environment `venv` or a Conda environment and use `pip` or `conda` to install the `piQture` package.

Here's how you can create a conda environment and manage a Python environment:

.. code:: sh

    # Create a new conda environment
    conda create -n piqture_env python=3.x

    # Activate the conda environment
    conda activate piqture_env

Installation
------------

Once the Python environment is activated, the required `piQture` package can be installed using `pip`. You can install the latest version directly from PyPI.

.. code:: sh

    pip install piqture

To create a development environment, and install `piQture` from source, you can refer to section :ref:`Install from Source <installation_from_source>`.

.. _installation_from_source:

Installation from Source
------------------------

To set up a development environment and install `piQture` from source, follow these steps:

1. Start by cloning the `piQture` repository from GitHub.

.. code:: sh

    # Clone the GitHub repository.
    git clone https://github.com/SaashaJoshi/piQture.git


2. Activate the Python environment and navigate to the `piQture` repository directory. Then, inside the Python environment, install the required dependencies from the `requirements.txt` configuration file.

.. code:: sh

    # Install the required dependencies
    pip install -r requirements.txt


3. Install `piQture` in editable mode to make changes to the source code.

.. code:: sh

    # Install from source in editable mode
    pip install -e .

Your development environment is set up, and `piQture` is installed from source. You can now start making changes to the code, running tests, and contributing to the project as a developer.
