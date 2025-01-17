# pylint: disable=R0801
"""Demo script for BRQI (Binary Representation of Quantum Images) encoding.

This script demonstrates how to load an image, convert it to BRQI representation,
and visualize the results using quantum circuit simulation.
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from qiskit import transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import Aer

from piqture.embeddings.image_embeddings.brqi import BRQI


def load_and_preprocess_image(image_path, target_size=(4, 4)):
    """Load and preprocess an image for BRQI encoding.

    Args:
        image_path (str): Path to the input image file
        target_size (tuple): Desired dimensions for the resized image (default: (4, 4))

    Returns:
        numpy.ndarray: Preprocessed image array with normalized pixel values
    """
    # Load the image
    img = Image.open(image_path)

    # Convert to grayscale
    img = img.convert("L")

    # Resize the image
    img = img.resize(target_size)

    # Convert to numpy array
    img_array = np.array(img)

    # Normalize pixel values to range [0, 255]
    img_array = (img_array / img_array.max() * 255).astype(int)

    return img_array


def create_brqi_circuit(img_array):
    """Create a quantum circuit using BRQI encoding for the input image.

    Args:
        img_array (numpy.ndarray): Input image array with pixel values

    Returns:
        QuantumCircuit: BRQI encoded quantum circuit
    """
    img_dims = img_array.shape
    pixel_vals = [img_array.flatten().tolist()]

    # Create BRQI object
    brqi_object = BRQI(img_dims, pixel_vals)

    # Generate BRQI circuit
    brqi_circuit = brqi_object.brqi()

    return brqi_circuit


def visualize_results(original_image, brqi_circuit):
    """Visualize the original image and quantum circuit simulation results.

    Args:
        original_image (numpy.ndarray): The original input image array
        brqi_circuit (QuantumCircuit): The BRQI encoded quantum circuit

    Returns:
        None: Displays plots of the original image and measurement results
    """
    # Display original image
    plt.figure(figsize=(10, 5))
    plt.subplot(1, 2, 1)
    plt.imshow(original_image, cmap="gray")
    plt.title("Original Image")

    # Simulate the quantum circuit
    backend = Aer.get_backend("qasm_simulator")
    transpiled_circuit = transpile(brqi_circuit, backend)
    job = backend.run(transpiled_circuit, shots=1000)
    result = job.result()
    counts = result.get_counts()

    # Plot the histogram of measurement results
    plt.subplot(1, 2, 2)
    plot_histogram(counts)
    plt.title("BRQI Measurement Results")

    plt.tight_layout()
    plt.show()


def main():
    """Main function to demonstrate BRQI encoding on an image.

    This function serves as the entry point for the demo script.
    It loads an image, creates a BRQI circuit, and visualizes the results.
    """
    # Path to your input image
    image_path = "/path/to/image.jpg"

    # Load and preprocess the image
    img_array = load_and_preprocess_image(image_path)

    # Create BRQI circuit
    brqi_circuit = create_brqi_circuit(img_array)

    # Visualize results
    visualize_results(img_array, brqi_circuit)


if __name__ == "__main__":
    main()
