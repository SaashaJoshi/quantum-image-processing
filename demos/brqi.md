
# BRQI Demo

This demo showcases the Bitplane Representation of Quantum Images (BRQI) using the piQture library. It demonstrates how to load an image, convert it to a quantum circuit using BRQI encoding, and visualize the results.

## Prerequisites

- Python 3.7+
- piQture library
- Qiskit
- NumPy
- Pillow (PIL)
- Matplotlib

## Installation

1. Install the required libraries:

```
pip install piqture qiskit qiskit-aer numpy pillow matplotlib
```

2. Clone the piQture repository or ensure you have the BRQI module available.

## Usage

1. Place your input image in a known location.

2. Update the `image_path` variable in the `main()` function:


```
def main():
    # Path to your input image
    image_path = '/Users/dylanmoraes/Downloads/image-1.png'
```


3. Run the script:

```
python brqi_demo.py
```

## How it works

The demo follows these steps:

1. **Load and preprocess the image**:
   - Opens the image file
   - Converts it to grayscale
   - Resizes it to a small dimension (default 4x4)
   - Normalizes pixel values to the range [0, 255]

2. **Create BRQI circuit**:
   - Initializes a BRQI object with the image dimensions and pixel values
   - Generates the quantum circuit representation of the image

3. **Visualize results**:
   - Displays the original image
   - Simulates the quantum circuit using Qiskit's QASM simulator
   - Plots a histogram of the measurement results

## Customization

- To change the target size of the image, modify the `target_size` parameter in the `load_and_preprocess_image()` function call:


```67:67:demos/brqi_demo.py
    img_array = load_and_preprocess_image(image_path)
```


- To adjust the number of shots in the quantum simulation, change the `shots` parameter in the `backend.run()` function:


```
    job = backend.run(transpiled_circuit, shots=1000)
```


## Understanding the Output

The script will display two plots:
1. The original grayscale image
2. A histogram of the measurement results from the quantum circuit simulation

The histogram represents the probability distribution of different quantum states, which encodes the information from the original image in the BRQI format.

## Troubleshooting

If you encounter any issues:
- Ensure all required libraries are installed correctly
- Check that the image path is correct and the file exists
- Verify that the piQture library and BRQI module are properly imported

For more information on the BRQI encoding method and the piQture library, refer to the main piQture documentation.
