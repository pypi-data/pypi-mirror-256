from spatial_transformation.definitions import PositionDefinition3d, Unit
from spatial_transformation.position_3d import Position3D

import numpy as np
import pytest
import testutils


def test_generation() -> None:
    p1 = Position3D.from_spherical(1, -45, 45, units=Unit.M_DEG)
    p2 = Position3D.from_spherical(1, np.pi / 4, -(np.pi - np.pi / 4), units=Unit.M_RAD)
    assert np.allclose(p1.get_vector_3x1(), p2.get_vector_3x1())


@pytest.mark.randomized
def test_conversion() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        vals = (rng.uniform(-1000, 1000), rng.uniform(-1000, 1000), rng.uniform(-1000, 1000))

        unit = rng.choice(list(Unit))

        p = Position3D.from_spherical(*vals, unit)
        assert Position3D.from_spherical(*p.export_as_spherical(unit), unit) == p

        p = Position3D.from_cylindrical(*vals, unit)
        assert Position3D.from_cylindrical(*p.export_as_cylindrical(unit), unit) == p

        p = Position3D.from_cartesian(*vals, unit)
        assert Position3D.from_cartesian(*p.export_as_cartesian(unit), unit) == p


@pytest.mark.randomized
def test_angle_wrap() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        vals = testutils.random_3_tuple(rng)

        p_0: Position3D = Position3D.from_cylindrical(*vals, Unit.M_RAD)
        p_1: Position3D = Position3D.from_cylindrical(*vals, Unit.M_DEG)

        # test angle wrap cylindrical ---------------------------------------------------------

        vals_p_0 = p_0.export_as_cylindrical(Unit.M_RAD)
        vals_p_1 = p_1.export_as_cylindrical(Unit.M_DEG)

        assert vals_p_0[0] >= 0  # r > 0
        assert vals_p_1[0] >= 0  # r > 0

        assert -np.pi <= vals_p_0[1] < np.pi  # -pi < phi < pi
        assert -180 <= vals_p_1[1] < 180  # -180 < phi < 180

        # test angle wrap spherical ---------------------------------------------------------

        p_0 = Position3D.from_spherical(*vals, Unit.M_RAD)
        p_1 = Position3D.from_spherical(*vals, Unit.M_DEG)

        vals_p_0 = p_0.export_as_spherical(Unit.M_RAD)
        vals_p_1 = p_1.export_as_spherical(Unit.M_DEG)

        assert vals_p_0[0] >= 0  # r > 0
        assert vals_p_1[0] >= 0  # r > 0

        assert 0 <= vals_p_0[1] < np.pi  # theta
        assert -np.pi <= vals_p_0[2] < 2 * np.pi  # phi

        assert 0 <= vals_p_1[1] < 180  # theta
        assert -180 <= vals_p_1[2] < 180  # phi


@pytest.mark.randomized
def test_mul() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        p_0: Position3D = Position3D(
            *testutils.random_3_tuple(rng), definition=testutils.random_definition_position3d(rng), units=Unit.MM_DEG
        )
        p_1: Position3D = Position3D(
            *testutils.random_3_tuple(rng), definition=testutils.random_definition_position3d(rng), units=Unit.MM_DEG
        )

        randfloat = rng.uniform(-1000, 1000)

        # Check if scalar multiplication can be inversed ---------------------
        p_0_mul = p_0 * randfloat
        assert p_0 == p_0_mul / randfloat

        # Check if cross product is perpendiclar to input vectors ------------
        p_cross = p_0 * p_1
        assert np.isclose(np.dot(p_cross.get_vector_1x3(), p_0.get_vector_1x3()), 0, rtol=0, atol=1e-6)
        assert np.isclose(np.dot(p_cross.get_vector_1x3(), p_1.get_vector_1x3()), 0, rtol=0, atol=1e-6)


@pytest.mark.randomized
def test_add() -> None:
    p0 = Position3D.from_cartesian(1, 0, 0, units=Unit.M_DEG)
    p1 = Position3D.from_cylindrical(1, 45, 1, units=Unit.M_DEG)
    p2 = Position3D.from_spherical(1, -45, 45, units=Unit.M_DEG)

    print(p2)

    assert (p0 + p1).is_close(Position3D.from_cartesian(1707.107, 707.107, 1000.0, Unit.MM_DEG), atol=0.1)

    assert p0 == p1 * (-1) + p0 + p1
    assert p0 == p0 - p1 + p1


@pytest.mark.randomized
def test_distance() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        p_0: Position3D = Position3D(
            *testutils.random_3_tuple(rng),
            definition=testutils.random_definition_position3d(rng),
            units=testutils.random_unit(rng),
        )
        p_1: Position3D = Position3D(
            *testutils.random_3_tuple(rng),
            definition=testutils.random_definition_position3d(rng),
            units=testutils.random_unit(rng),
        )

        assert p_0.get_distance_to(p_1) == (p_1.copy() - p_0).get_absolute_value()


if __name__ == "__main__":
    test_conversion()

    test_angle_wrap()

    # print(Position3D.from_spherical(1, 190, 0, Unit.M_DEG))

    test_mul()
    test_add()
    test_distance()
