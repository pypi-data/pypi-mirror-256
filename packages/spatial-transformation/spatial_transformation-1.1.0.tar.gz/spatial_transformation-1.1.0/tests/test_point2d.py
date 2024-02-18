from spatial_transformation.definitions import PositionDefinition2d, Unit
from spatial_transformation.position_2d import Position2D

import numpy as np
import pytest
import testutils


@pytest.mark.randomized
def test_angle_wrap_cylindrical() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        vals = testutils.random_2_tuple(rng)

        p_0: Position2D = Position2D.from_cylindrical(*vals, Unit.M_RAD)
        p_1: Position2D = Position2D.from_cylindrical(*vals, Unit.M_DEG)

        p_add = p_0 + p_1

        vals_p_0 = p_0.export_as_cylindrical(Unit.MM_RAD)
        vals_p_1 = p_1.export_as_cylindrical(Unit.MM_DEG)
        vals_p_add = p_add.export_as_cylindrical(Unit.MM_DEG)

        assert vals_p_0[0] >= 0  # r > 0
        assert vals_p_1[0] >= 0  # r > 0
        assert vals_p_add[0] >= 0  # r > 0

        assert -np.pi <= vals_p_0[1] < np.pi  # -pi < phi < pi
        assert -180 <= vals_p_1[1] < 180  # -180 < phi < 180
        assert -180 <= vals_p_add[1] < 180  # -180 < phi < 180


@pytest.mark.randomized
def test_mul() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        p_0: Position2D = Position2D(
            *testutils.random_2_tuple(rng), definition=testutils.random_definition_position2d(rng), units=Unit.MM_DEG
        )

        randfloat = rng.uniform(-1000, 1000)

        # Check if scalar multiplication can be inversed ---------------------
        p_0_mul = p_0 * randfloat
        assert p_0 == p_0_mul / randfloat


@pytest.mark.randomized
def test_distance() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        p_0: Position2D = Position2D(
            *testutils.random_2_tuple(rng),
            definition=testutils.random_definition_position2d(rng),
            units=testutils.random_unit(rng),
        )
        p_1: Position2D = Position2D(
            *testutils.random_2_tuple(rng),
            definition=testutils.random_definition_position2d(rng),
            units=testutils.random_unit(rng),
        )

        assert p_0.get_distance_to(p_1) == (p_1.copy() - p_0).get_absolute_value()


# def test_add() -> None:
#     p1 = Position2D.from_cylindrical(1, 45, 1, units=Unit.M_DEG)
#     p2 = Position2D.from_spherical(1, -45, 45, units=Unit.M_DEG)

#     print(p2)

#     assert (p0 + p1).is_close(Position2D.from_cartesian(1707.107, 707.107, 1000.0, Unit.MM_DEG), atol=0.1)


if __name__ == "__main__":
    test_angle_wrap_cylindrical()

    # print(Position2D.from_spherical(1, 190, 0, Unit.M_DEG))

    test_mul()
    test_distance()
