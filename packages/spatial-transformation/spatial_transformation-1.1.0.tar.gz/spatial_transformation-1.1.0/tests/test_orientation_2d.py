import dataclasses
from enum import IntEnum

from spatial_transformation.definitions import PositionDefinition2d, RotationDefinition2d, Unit
from spatial_transformation.position_2d import Position2D
from spatial_transformation.rotation_2d import Rotation2D
from spatial_transformation.transform_2d import Transform2D

import numpy as np
import pytest
import testutils


def random_definition_position2d(rng: np.random.Generator) -> PositionDefinition2d:
    choices = [PositionDefinition2d.CARTESIAN, PositionDefinition2d.CYLINDRICAL]

    idx_chosen = rng.choice(choices)

    return PositionDefinition2d(idx_chosen)


def random_unit(rng: np.random.Generator) -> Unit:
    choices = [Unit.M_DEG, Unit.MM_DEG, Unit.M_RAD, Unit.MM_RAD]

    idx_chosen = rng.choice(choices)

    return Unit(idx_chosen)


@pytest.mark.randomized
def test_angle_wrap() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        ori = Rotation2D.from_CARTESIAN(rng.uniform(-1000, 1000), Unit.M_DEG)
        assert -180 <= ori.export_as_CARTESIAN(Unit.M_DEG) <= 180

        ori = Rotation2D.from_CARTESIAN(rng.uniform(-1000, 1000), Unit.M_RAD)
        assert -np.pi <= ori.export_as_CARTESIAN(Unit.M_RAD) <= np.pi


@pytest.mark.randomized
def test_invert_random() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        units_original = rng.choice(list(Unit))
        ori = Rotation2D(rng.uniform(-1000, 1000), definition=RotationDefinition2d.Cartesian, units=units_original)

        p_0: Position2D = Position2D(
            *testutils.random_2_tuple(rng), random_definition_position2d(rng), rng.choice(list(Unit))
        )

        # test forward and backward transformation with inverted rotation and position ----------------------
        p_1 = ori * p_0
        assert ori.invert() * p_1 == p_0

        # test forward and backward transformation with double inversion ------------------------------------
        assert ori == ori.invert().invert()

        # test multiplication with rotation
        o1 = Rotation2D(rng.uniform(-1000, 1000), definition=RotationDefinition2d.Cartesian, units=random_unit(rng))
        o2 = Rotation2D(rng.uniform(-1000, 1000), definition=RotationDefinition2d.Cartesian, units=random_unit(rng))

        o1_mul_o2 = o1 * o2

        assert isinstance(o1_mul_o2, Rotation2D)  # make sure result is Rotation2D
        assert o1_mul_o2.invert() == o2.invert() * o1.invert()
        # else:
        #     assert False


@pytest.mark.randomized
def test_from_rotmat_random() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        definition_original = RotationDefinition2d.Cartesian
        units_original = rng.choice(list(Unit))

        ori = Rotation2D(rng.uniform(-1000, 1000), definition=definition_original, units=units_original)

        tmat_random = ori._rotmat
        assert ori == Rotation2D.from_rotmat(tmat_random)


if __name__ == "__main__":
    test_angle_wrap()

    test_invert_random()
    test_from_rotmat_random()

    # p0 = Position2D.from_cartesian(1, 0, Unit.M_DEG)
    # o = Rotation2D.from_Cartesian(45, Unit.M_DEG)

    # p1 = o * p0

    # print(p0)
    # print(p1)
    # print(o.invert() * p1)
