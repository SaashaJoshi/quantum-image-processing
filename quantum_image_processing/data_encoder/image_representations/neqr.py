"""Novel Enhanced Quantum Representation (NEQR) of digital images"""
from __future__ import annotations
import math
import numpy as np
from qiskit.circuit import QuantumCircuit
from quantum_image_processing.data_encoder.image_representations.image_embedding import (
    ImageEmbedding,
)
from quantum_image_processing.mixin.image_embedding_mixin import ImageMixin


class NEQR(ImageEmbedding, ImageMixin):
    """Represents images in NEQR representation format."""

    def __init__(
        self,
        img_dims: tuple[int, int],
        pixel_vals: list,
        max_color_intensity: int = 255,
    ):
        ImageEmbedding.__init__(self, img_dims, pixel_vals)
        self.validate_square_images()

        if max_color_intensity < 0 or max_color_intensity > 255:
            raise ValueError(
                "Maximum color intensity cannot be less than 0 or greater than 255."
            )

        self.feature_dim = int(np.ceil(np.sqrt(math.prod(self.img_dims))))
        self.max_color_intensity = max_color_intensity + 1

        # number of qubits to encode color byte
        self.color_qubits = int(np.ceil(math.log(self.max_color_intensity, 2)))

        # NEQR circuit
        self._circuit = QuantumCircuit(self.feature_dim + self.color_qubits)
        self.qr = self._circuit.qubits

    @property
    def circuit(self):
        """Returns NEQR circuit."""
        return self._circuit

    def pixel_value(self, pixel_pos: int):
        """Embeds pixel (color) values in a circuit"""
        color_byte = f"{int(self.pixel_vals[pixel_pos]):0>8b}"

        control_qubits = list(range(self.feature_dim))
        for index, color in enumerate(color_byte):
            if color == "1":
                self.circuit.mct(
                    control_qubits=control_qubits, target_qubit=self.feature_dim + index
                )

    def build_circuit(self) -> QuantumCircuit:
        # pylint: disable=duplicate-code
        """
        Builds the NEQR image representation on a circuit.

        Returns:
            QuantumCircuit: final circuit with the frqi image
            representation.
        """
        for i in range(self.feature_dim):
            self.circuit.h(i)

        num_theta = math.prod(self.img_dims)
        for pixel in range(num_theta):
            pixel_pos_binary = f"{pixel:0>2b}"

            # Embed pixel position on qubits
            self.pixel_position(pixel_pos_binary)
            # Embed color information on qubits
            self.pixel_value(pixel)
            # Remove pixel position embedding
            self.pixel_position(pixel_pos_binary)

        return self.circuit
