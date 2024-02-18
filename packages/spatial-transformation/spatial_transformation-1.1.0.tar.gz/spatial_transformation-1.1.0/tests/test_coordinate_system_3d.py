from enum import IntEnum

from spatial_transformation.definitions import PositionDefinition3d, RotationDefinition2d, RotationDefinition3d, Unit
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


def random_definition_position3d(rng: np.random.Generator) -> PositionDefinition3d:
    choices = [PositionDefinition3d.CARTESIAN, PositionDefinition3d.CYLINDRICAL, PositionDefinition3d.SPHERICAL]

    idx_chosen = rng.choice(choices)

    return PositionDefinition3d(idx_chosen)


def random_definition_rotation3d(rng: np.random.Generator) -> RotationDefinition3d:
    choices = [
        RotationDefinition3d.Axis_Angle,
        RotationDefinition3d.EULER_INTRINSIC_XYZ,
        RotationDefinition3d.EULER_INTRINSIC_ZYX,
        RotationDefinition3d.Quaternion,
        RotationDefinition3d.Rodrigues,
    ]

    idx_chosen = rng.choice(choices)

    return RotationDefinition3d(idx_chosen)


def random_unit(rng: np.random.Generator) -> Unit:
    choices = [Unit.M_DEG, Unit.MM_DEG, Unit.M_RAD, Unit.MM_RAD]

    idx_chosen = rng.choice(choices)

    return Unit(idx_chosen)


@pytest.mark.randomized
def test_from_rotmat_random() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        # -------------------------------------------------------------------------------------------------------------------
        # Use Transform3D to create a random tmat and check if Transform3D.from_tmat() returns the same object.

        csys = Transform3D(
            Position3D(
                *testutils.random_3_tuple(rng), definition=random_definition_position3d(rng), units=random_unit(rng)
            ),
            Rotation3D(
                *testutils.random_4_tuple(rng), definition=random_definition_rotation3d(rng), units=random_unit(rng)
            ),
        )

        assert csys == Transform3D.from_tmat(csys._tmat)  # system created from tmat should match original system

        # -------------------------------------------------------------------------------------------------------------------
        # Check if tmat is correctly converted back to rotation definition

        # Create system in random definition and unit from tmat
        csys1 = Transform3D.from_tmat(csys._tmat)

        assert_allclose(
            csys.get_rotation_reference().export_as_AXIS_ANGLE(), csys1.get_rotation_reference().export_as_AXIS_ANGLE()
        )
        assert_allclose(
            csys.get_rotation_reference().export_as_EULER_INTRINSIC_XYZ(),
            csys1.get_rotation_reference().export_as_EULER_INTRINSIC_XYZ(),
        )
        assert_allclose(
            csys.get_rotation_reference().export_as_EULER_INTRINSIC_ZYX(),
            csys1.get_rotation_reference().export_as_EULER_INTRINSIC_ZYX(),
        )
        assert_allclose(
            csys.get_rotation_reference().export_as_QUATERNION(), csys1.get_rotation_reference().export_as_QUATERNION()
        )
        assert_allclose(
            csys.get_rotation_reference().export_as_RODRIGUES(), csys1.get_rotation_reference().export_as_RODRIGUES()
        )

        assert_allclose(
            csys.get_position_reference().export_as_cartesian(), csys1.get_position_reference().export_as_cartesian()
        )
        assert_allclose(
            csys.get_position_reference().export_as_cylindrical(),
            csys1.get_position_reference().export_as_cylindrical(),
        )
        assert_allclose(
            csys.get_position_reference().export_as_spherical(), csys1.get_position_reference().export_as_spherical()
        )


@pytest.mark.randomized
def test_update() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        csys = Transform3D()

        randunit = random_unit(rng)

        randpos = testutils.random_3_tuple(rng)
        randrot = testutils.random_4_tuple(rng)

        # -------------------------------------------------------------------------------------------------------------------
        # Test if updated system equals a system, that has been created with the same values

        # --------- Translations
        csys.update_pos_cartesian(*randpos, units=randunit)
        assert csys == Transform3D(Position3D.from_cartesian(*randpos, units=randunit))

        csys.update_pos_cylindrical(*randpos, units=randunit)
        assert csys == Transform3D(Position3D.from_cylindrical(*randpos, units=randunit))

        csys.update_pos_spherical(*randpos, units=randunit)
        assert csys == Transform3D(Position3D.from_spherical(*randpos, units=randunit))

        csys = Transform3D()

        # ----------- Rotations

        csys.update_rot_as_EULER_REP_XYZ(*randpos, units=randunit)
        assert csys == Transform3D(rotation=Rotation3D.from_EULER_INTRINSIC_XYZ(*randpos, units=randunit))
        csys.update_rot_as_EULER_REP_ZYX(*randpos, units=randunit)
        assert csys == Transform3D(rotation=Rotation3D.from_EULER_INTRINSIC_ZYX(*randpos, units=randunit))
        csys.update_rot_as_AXIS_ANGLE(*randrot, units=randunit)
        assert csys == Transform3D(rotation=Rotation3D.from_AXIS_ANGLE(*randrot, units=randunit))
        csys.update_rot_as_QUATERNION(*randrot)
        assert csys == Transform3D(rotation=Rotation3D.from_QUATERNION(*randrot))
        csys.update_rot_as_RODRIGUES(*randpos, units=randunit)
        assert csys == Transform3D(rotation=Rotation3D.from_RODRIGUES(*randpos, units=randunit))


@pytest.mark.randomized
def test_arithmethic_random() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        csys1 = Transform3D(
            Position3D(
                *testutils.random_3_tuple(rng), definition=random_definition_position3d(rng), units=random_unit(rng)
            ),
            Rotation3D(
                *testutils.random_4_tuple(rng), definition=random_definition_rotation3d(rng), units=random_unit(rng)
            ),
        )
        csys2 = Transform3D(
            Position3D(
                *testutils.random_3_tuple(rng), definition=random_definition_position3d(rng), units=random_unit(rng)
            ),
            Rotation3D(
                *testutils.random_4_tuple(rng), definition=random_definition_rotation3d(rng), units=random_unit(rng)
            ),
        )

        csys3 = csys1 * csys2

        assert isinstance(csys3, Transform3D)

        p0 = Position3D(
            *testutils.random_3_tuple(rng), definition=random_definition_position3d(rng), units=random_unit(rng)
        )

        p1_1 = csys1 * csys2 * p0
        p1_2 = csys3 * p0

        assert isinstance(p1_1, Position3D)

        assert p1_1 == p1_2
        assert csys1 == csys1.invert().invert()
        assert csys1 * csys1.invert() * p0 == p0
        assert csys2.invert() * csys1.invert() * p1_1 == p0
        assert csys3.invert() * p1_2 == p0


@pytest.mark.randomized
def test_input_checks() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        sys_2d = Transform2D(
            Position2D(
                *testutils.random_2_tuple(rng),
                definition=testutils.random_definition_position2d(rng),
                units=random_unit(rng),
            ),
            Rotation2D(rng.uniform(-1000, 1000), definition=RotationDefinition2d.Cartesian, units=random_unit(rng)),
        )

        # test if tmat shape is checked -------------------------------------------
        with pytest.raises(ValueError):
            Transform3D.from_tmat(sys_2d._tmat)


@pytest.mark.hardcoded
def test_arithmetic() -> None:
    sys = Transform3D(Position3D(0, 0, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90))
    p0 = Position3D(1, 0, 0)

    assert sys * p0 == Position3D(0, 1, 0)

    sys.update_pos_cartesian(1, 0, 0)
    assert sys * p0 == Position3D(1, 1, 0)
    sys.get_position_reference().update_cartesian(1, 0, 0)
    assert sys * p0 == Position3D(1, 1, 0)

    sys.update_rot_as_EULER_REP_XYZ(rz=-90)
    assert sys * p0 == Position3D(1, -1, 0)
    sys.get_rotation_reference().update_as_EULER_INTRINSIC_XYZ(rz=-90)
    assert sys * p0 == Position3D(1, -1, 0)

    sys.update_pos_cylindrical(2, 0)
    sys.update_rot_as_EULER_REP_XYZ(rz=0)
    assert sys * p0 == Position3D(3, 0, 0)
    sys.get_position_reference().update_cylindrical(2, 0)
    sys.get_rotation_reference().update_as_EULER_INTRINSIC_XYZ(rz=0)
    assert sys * p0 == Position3D(3, 0, 0)

    sys = Transform3D(Position3D(1, 0, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 0))
    p0 = Position3D(1, 0, 0)

    assert sys.invert() * p0 == Position3D(0, 0, 0)

    sys.get_rotation_reference().update_as_EULER_INTRINSIC_XYZ(rz=90)
    sys.update_pos_cartesian(0, 0, 0)
    assert sys.invert() * p0 == Position3D(0, -1, 0)

    sys.get_rotation_reference().update_as_EULER_INTRINSIC_XYZ(rz=90)
    sys.update_pos_cartesian(1, 1)
    assert sys * Position3D.from_cartesian(1, 0, 0) == Position3D(1, 2, 0)  # T_0_A * p_A
    assert sys.invert() * Position3D.from_cartesian(1, 0, 0) == Position3D(-1, 0, 0)  # T_A_0 * p_0


if __name__ == "__main__":
    # test_from_rotmat_random()
    test_arithmetic()
    # test_from_rotmat_random()
    # test_input_checks()
    # test_update()

    # test_in/put_checks()
