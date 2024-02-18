"""
Contains utility functions for testing.
"""

from spatial_transformation.definitions import (
    PositionDefinition2d,
    PositionDefinition3d,
    RotationDefinition2d,
    RotationDefinition3d,
    Unit,
)
from spatial_transformation.position_2d import Position2D
from spatial_transformation.position_3d import Position3D
from spatial_transformation.transform_3d import Transform3D

import numpy as np


def random_definition_position2d(rng: np.random.Generator) -> PositionDefinition2d:
    """
    Generate a random 2d position definition.
    """
    choices = [PositionDefinition2d.CARTESIAN, PositionDefinition2d.CYLINDRICAL]

    idx_chosen = rng.choice(choices)

    return PositionDefinition2d(idx_chosen)


def random_definition_position3d(rng: np.random.Generator) -> PositionDefinition3d:
    """
    Generate a random 3d position definition.
    """
    choices = [PositionDefinition3d.CARTESIAN, PositionDefinition3d.CYLINDRICAL, PositionDefinition3d.SPHERICAL]

    idx_chosen = rng.choice(choices)

    return PositionDefinition3d(idx_chosen)


def random_definition_rotation3d(rng: np.random.Generator) -> RotationDefinition3d:
    """
    Generate a random 3d rotation definition.
    """
    choices = [
        RotationDefinition3d.Axis_Angle,
        RotationDefinition3d.EULER_INTRINSIC_XYZ,
        RotationDefinition3d.EULER_INTRINSIC_ZYX,
        RotationDefinition3d.Quaternion,
        RotationDefinition3d.Rodrigues,
    ]

    idx_chosen = rng.choice(choices)

    return RotationDefinition3d(idx_chosen)


def random_4_tuple(rng: np.random.Generator) -> tuple[float, float, float, float]:
    """
    Use NumPy's RNG to generate a four-tuple.
    """
    return (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000), rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))


def random_3_tuple(rng: np.random.Generator) -> tuple[float, float, float]:
    """
    Use NumPy's RNG to generate a three-tuple.
    """
    return (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))


def random_2_tuple(rng: np.random.Generator) -> tuple[float, float]:
    """
    Use NumPy's RNG to generate a two-tuple.
    """
    return (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))


def random_uniform(rng: np.random.Generator) -> float:
    """
    Use NumPy's RNG to generate a two-tuple.
    """
    random_value: float = rng.uniform(-1000, 1000)

    return random_value


def random_definition_rotation2d(rng: np.random.Generator) -> RotationDefinition2d:
    """
    Generate a random 2d rotation definition.
    """
    choices = [RotationDefinition2d.Cartesian]

    idx_chosen = rng.choice(choices)

    return RotationDefinition2d(idx_chosen)


def random_unit(rng: np.random.Generator) -> Unit:
    """
    Generate a random unit.
    """
    choices = [Unit.M_DEG, Unit.MM_DEG, Unit.M_RAD, Unit.MM_RAD]

    idx_chosen = rng.choice(choices)

    return Unit(idx_chosen)


def assert_allclose(arr1: object, arr2: object) -> None:
    """
    Assert if all are close.
    """
    assert np.allclose(arr1, arr2)
