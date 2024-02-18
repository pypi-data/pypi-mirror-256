from spatial_transformation.definitions import PositionDefinition2d, RotationDefinition2d, Unit
from spatial_transformation.position_2d import Position2D
from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_2d import Rotation2D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_2d import Transform2D
from spatial_transformation.transform_3d import Transform3D

import numpy as np
import pytest
import testutils
from testutils import assert_allclose


def random_definition_position2d(rng: np.random.Generator) -> PositionDefinition2d:
    choices = [PositionDefinition2d.CARTESIAN, PositionDefinition2d.CYLINDRICAL]

    idx_chosen = rng.choice(choices)

    return PositionDefinition2d(idx_chosen)


def random_definition_rotation2d(rng: np.random.Generator) -> RotationDefinition2d:
    choices = [RotationDefinition2d.Cartesian]

    idx_chosen = rng.choice(choices)

    return RotationDefinition2d(idx_chosen)


def random_unit(rng: np.random.Generator) -> Unit:
    choices = [Unit.M_DEG, Unit.MM_DEG, Unit.M_RAD, Unit.MM_RAD]

    idx_chosen = rng.choice(choices)

    return Unit(idx_chosen)


@pytest.mark.randomized
def test_from_rotmat_random() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        # --------------------------------------------------------------------------------------------------------
        # Use Transform2D to create a random tmat and check if Transform2D.from_tmat() returns the same object.

        csys = Transform2D(
            Position2D(
                *testutils.random_2_tuple(rng), definition=random_definition_position2d(rng), units=random_unit(rng)
            ),
            Rotation2D(
                testutils.random_uniform(rng), definition=random_definition_rotation2d(rng), units=random_unit(rng)
            ),
        )

        assert csys == Transform2D.from_tmat(csys._tmat)  # system created from tmat should match original system

        # -------------------------------------------------------------------------------------------------------------------
        # Check if tmat is correctly converted back to rotation definition
        csys1 = Transform2D.from_tmat(csys._tmat)

        assert_allclose(csys.get_rotation().export_as_CARTESIAN(), csys1.get_rotation().export_as_CARTESIAN())

        assert_allclose(csys.get_position().export_as_cartesian(), csys1.get_position().export_as_cartesian())
        assert_allclose(csys.get_position().export_as_cylindrical(), csys1.get_position().export_as_cylindrical())


@pytest.mark.randomized
def test_update() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        csys = Transform2D()

        randunit = random_unit(rng)

        randpos = testutils.random_2_tuple(rng)

        # -------------------------------------------------------------------------------------------------------------------
        # Test if updated system equals a system that has been created with the same values

        # --------- Translations
        csys.update_pos_cartesian(*randpos, units=randunit)
        assert csys == Transform2D(Position2D.from_cartesian(*randpos, units=randunit))

        csys.update_pos_cylindrical(*randpos, units=randunit)
        assert csys == Transform2D(Position2D.from_cylindrical(*randpos, units=randunit))

        csys = Transform2D()

        # ----------- Rotations

        csys.update_rot_as_Cartesian(randpos[0], units=randunit)
        assert csys == Transform2D(rotation=Rotation2D.from_CARTESIAN(randpos[0], units=randunit))


@pytest.mark.randomized
def test_arithmethic_random() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        csys1 = Transform2D(
            Position2D(
                *testutils.random_2_tuple(rng), definition=random_definition_position2d(rng), units=random_unit(rng)
            ),
            Rotation2D(
                testutils.random_uniform(rng), definition=random_definition_rotation2d(rng), units=random_unit(rng)
            ),
        )
        csys2 = Transform2D(
            Position2D(
                *testutils.random_2_tuple(rng), definition=random_definition_position2d(rng), units=random_unit(rng)
            ),
            Rotation2D(
                testutils.random_uniform(rng), definition=random_definition_rotation2d(rng), units=random_unit(rng)
            ),
        )

        p0 = Position2D(
            *testutils.random_2_tuple(rng), definition=random_definition_position2d(rng), units=random_unit(rng)
        )

        # test multiplication with inverted systems -----------------------------
        csys3 = csys1 * csys2

        assert isinstance(csys3, Transform2D)

        p1_1 = csys1 * csys2 * p0  # type: ignore[operator]
        p1_2 = csys3 * p0

        assert p1_1 == p1_2
        assert csys3.invert() * p1_1 == p0
        assert csys3.invert() * p1_2 == p0
        assert csys2.invert() * csys1.invert() * p1_1 == p0  # type: ignore[operator]
        assert csys2.invert() * csys1.invert() * p1_2 == p0  # type: ignore[operator]

        p0 = Position2D(
            *testutils.random_2_tuple(rng), definition=random_definition_position2d(rng), units=random_unit(rng)
        )


@pytest.mark.randomized
def test_input_checks() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        sys_3d = Transform3D(
            Position3D(
                *testutils.random_3_tuple(rng),
                definition=testutils.random_definition_position3d(rng),
                units=random_unit(rng),
            ),
            Rotation3D(
                *testutils.random_4_tuple(rng),
                definition=testutils.random_definition_rotation3d(rng),
                units=random_unit(rng),
            ),
        )

        # test if tmat shape is checked -------------------------------------------
        with pytest.raises(ValueError):
            Transform2D.from_tmat(sys_3d._tmat)


@pytest.mark.hardcoded
def test_arithmetic() -> None:
    sys = Transform2D(Position2D(0, 0), Rotation2D(90))
    p0 = Position2D(1, 0)

    assert sys * p0 == Position2D(0, 1)

    sys.update_pos_cartesian(1, 0)
    assert sys * p0 == Position2D(1, 1)
    sys.get_position().update_cartesian(1, 0)
    assert sys * p0 == Position2D(1, 1)

    sys.update_rot_as_Cartesian(-90)
    assert sys * p0 == Position2D(1, -1)
    sys.get_rotation().update_as_CARTESIAN(-90)
    assert sys * p0 == Position2D(1, -1)

    sys.update_pos_cylindrical(2, 0)
    sys.update_rot_as_Cartesian(0)
    assert sys * p0 == Position2D(3, 0)
    sys.get_position().update_cylindrical(2, 0)
    sys.get_rotation().update_as_CARTESIAN(0)
    assert sys * p0 == Position2D(3, 0)

    sys = Transform2D(Position2D(1, 0), Rotation2D(0))
    p0 = Position2D(1, 0)

    assert sys.invert() * p0 == Position2D(0, 0)

    sys.get_rotation().update_as_CARTESIAN(90)
    sys.update_pos_cartesian(0, 0)
    assert sys.invert() * p0 == Position2D(0, -1)

    sys.get_rotation().update_as_CARTESIAN(90)
    sys.update_pos_cartesian(1, 1)
    assert sys * Position2D.from_cartesian(1, 0) == Position2D(1, 2)  # T_0_A * p_A
    assert sys.invert() * Position2D.from_cartesian(1, 0) == Position2D(-1, 0)  # T_A_0 * p_0


# @pytest.mark.hardcoded
# def test_references() -> None:
#     vp = Position2D(0, 0)  # vehicle position
#     vo = Rotation2D.from_CARTESIAN(0)    # vehicle rotation
#     sys = Transform2D(vp, vo)    # vehicle system, reference to vp and vo is kept

#     vx = Position2D(1, 0)

#     assert sys*vx == Position2D(1, 0)

#     # 1. move vehicle position
#     vp.update_cartesian(1, 0)   # updating vp will be seen in sys since reference is kept
#     assert sys*vx == Position2D(2, 0)

#     # 2. rotate vehicle
#     vp.update_cartesian(0, 0)
#     vo.update_as_CARTESIAN(90)
#     assert sys*vx == Position2D(0, 1)

if __name__ == "__main__":
    # test_arithmethic_random()
    # test_from_rotmat_random()
    # test_input_checks()
    # test_update()

    # test_references()
    pass
