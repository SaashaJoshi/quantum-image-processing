# (C) Copyright SaashaJoshi 2024.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Unit test for FRQI class"""

from __future__ import annotations

import math
import re
from unittest import mock

import numpy as np
import pytest
from pytest import raises
from qiskit.circuit import ParameterVector, QuantumCircuit

from piqture.embeddings.image_embeddings.frqi import FRQI

PIXEL_POS_BINARY2 = ["00", "01", "10", "11"]


@pytest.fixture(name="circuit_pixel_value")
def circuit_pixel_value_fixture():
    """Fixture for embedding pixel values."""

    def _circuit(img_dims, pixel_vals, pixel):
        feature_dim = int(np.sqrt(math.prod(img_dims)))
        test_circuit = QuantumCircuit(int(math.prod(img_dims)))

        if pixel_vals is None:
            pixel_vals = ParameterVector("Angle", math.prod(img_dims))
        else:
            pixel_vals = [pixel for pixel_list in pixel_vals for pixel in pixel_list]

        # Add gates to test_circuit
        test_circuit.cry(pixel_vals[pixel], feature_dim - 2, feature_dim)
        test_circuit.cx(0, 1)
        test_circuit.cry(-pixel_vals[pixel], feature_dim - 1, feature_dim)
        test_circuit.cx(0, 1)
        test_circuit.cry(pixel_vals[pixel], feature_dim - 1, feature_dim)
        return test_circuit

    return _circuit


class TestFRQI:
    """Tests for FRQI image representation class"""

    @pytest.mark.parametrize(
        "img_dims, pixel_vals",
        [((2.5, 2.5), [list(range(6))]), ({"abc", "def"}, [list(range(6))])],
    )
    def test_abc_type_image_dims(self, img_dims, pixel_vals):
        """Tests the type of img_dims input."""
        pattern = re.escape("Input img_dims must be of the type tuple[int, ...].")
        with raises(TypeError, match=pattern):
            _ = FRQI(img_dims, pixel_vals)

    @pytest.mark.parametrize(
        "img_dims, pixel_vals",
        [
            ((2, 2), [tuple(range(4))]),
            ((2, 2), [{1.0, 2.35, 4.5, 8.9}]),
            ((2, 2), {tuple(range(4))}),
        ],
    )
    def test_abc_type_pixel_vals(self, img_dims, pixel_vals):
        """Tests the type of pixel_vals input."""
        with raises(
            TypeError,
            match=re.escape("Input pixel_vals must be of the type list[list]."),
        ):
            _ = FRQI(img_dims, pixel_vals)

    @pytest.mark.parametrize("img_dims, pixel_vals", [((2, 3), [list(range(6))])])
    def test_init_square_images(self, img_dims, pixel_vals):
        """Tests if the input img_dims represents a square image."""
        with raises(
            ValueError,
            match=r".* supports square images only. "
            r"Input img_dims must have same dimensions.",
        ):
            _ = FRQI(img_dims, pixel_vals)

    @pytest.mark.parametrize("img_dims, pixel_vals", [((2, 2), [[1, 2, 3]])])
    def test_init_len_pixel_values(self, img_dims, pixel_vals):
        # pylint: disable=duplicate-code
        """Tests if the length of pixel_vals input is the same as the image dimension."""
        with raises(
            ValueError,
            match=r"No. of pixels \(\[\d+\]\) "
            r"in each pixel_lists in pixel_vals must be equal to the "
            r"product of image dimensions \d.",
        ):
            _ = FRQI(img_dims, pixel_vals)

    @pytest.mark.parametrize(
        "img_dims, pixel_vals",
        [((2, 2), [[100, -23, 505, 256]]), ((2, 2), [[-100, -23, 230, 256]])],
    )
    def test_pixel_values(self, img_dims, pixel_vals):
        """Tests the range of pixel values."""
        with raises(
            ValueError,
            match=r"Pixel values cannot be less than \d or greater than \d.",
        ):
            _ = FRQI(img_dims, pixel_vals)

    @pytest.mark.parametrize("img_dims, pixel_vals", [((2, 2), [list(range(4))])])
    def test_circuit_property(self, img_dims, pixel_vals):
        """Tests the FRQI circuits initialization."""
        test_circuit = QuantumCircuit(int(np.sqrt(math.prod(img_dims))) + 1)
        assert test_circuit == FRQI(img_dims, pixel_vals).circuit

    @pytest.mark.parametrize(
        "img_dims, pixel_vals, pixel_pos_binary_list",
        [((2, 2), [list(range(4))], PIXEL_POS_BINARY2)],
    )
    def test_pixel_position(
        self,
        img_dims,
        pixel_vals,
        pixel_pos_binary_list,
        circuit_pixel_position,
    ):
        """Tests the circuit received after pixel position embedding."""
        frqi_object = FRQI(img_dims, pixel_vals)
        mock_circuit = QuantumCircuit(int(math.prod(img_dims)))

        for pixel_pos_binary in pixel_pos_binary_list:
            mock_circuit.clear()
            test_circuit = circuit_pixel_position(img_dims, pixel_pos_binary)

            with mock.patch(
                "piqture.embeddings.image_embeddings.frqi.FRQI.circuit",
                new_callable=lambda: mock_circuit,
            ):
                frqi_object.pixel_position(pixel_pos_binary)
                assert mock_circuit == test_circuit

    @pytest.mark.parametrize(
        "img_dims, pixel_vals",
        [((2, 2), [list(range(4))])],
    )
    def test_pixel_value(self, img_dims, pixel_vals, circuit_pixel_value):
        """Tests the circuit received after pixel value embedding."""
        frqi_object = FRQI(img_dims, pixel_vals)
        mock_circuit = QuantumCircuit(int(math.prod(img_dims)))

        for pixel in range(int(math.prod(img_dims))):
            mock_circuit.clear()
            test_circuit = circuit_pixel_value(img_dims, pixel_vals, pixel)

            with mock.patch(
                "piqture.embeddings.image_embeddings.frqi.FRQI.circuit",
                new_callable=lambda: mock_circuit,
            ):
                frqi_object.pixel_value(pixel_pos=pixel)
                assert mock_circuit == test_circuit

    # pylint: disable=too-many-arguments
    @pytest.mark.parametrize(
        "img_dims, pixel_vals, pixel_pos_binary_list",
        [
            ((2, 2), [list(range(4))], PIXEL_POS_BINARY2),
            ((2, 2), None, PIXEL_POS_BINARY2),
        ],
    )

    # pylint: disable=R0917
    def test_frqi(
        self,
        img_dims,
        pixel_vals,
        pixel_pos_binary_list,
        circuit_pixel_position,
        circuit_pixel_value,
    ):
        """Tests the final FRQI circuit."""
        frqi_object = FRQI(img_dims, pixel_vals)
        mock_circuit = QuantumCircuit(int(math.prod(img_dims)))

        test_circuit = QuantumCircuit(int(math.prod(img_dims)))
        test_circuit.h(list(range(int(np.sqrt(math.prod(img_dims))))))
        for pixel, pixel_pos_binary in enumerate(pixel_pos_binary_list):
            test_circuit.compose(
                circuit_pixel_position(img_dims, pixel_pos_binary),
                inplace=True,  # pylint: disable=too-many-arguments
            )
            test_circuit.compose(
                circuit_pixel_value(img_dims, pixel_vals, pixel), inplace=True
            )
            test_circuit.compose(
                circuit_pixel_position(img_dims, pixel_pos_binary), inplace=True
            )

        with mock.patch(
            "piqture.embeddings.image_embeddings.frqi.FRQI.circuit",
            new_callable=lambda: mock_circuit,
        ):
            frqi_object.frqi()

            if pixel_vals is None:
                pixel_vals = np.random.random(math.prod(img_dims))
                test_circuit.assign_parameters(pixel_vals, inplace=True)
                mock_circuit.assign_parameters(pixel_vals, inplace=True)
            assert mock_circuit == test_circuit
