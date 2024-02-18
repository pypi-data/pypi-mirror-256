import dataclasses
from enum import IntEnum

from spatial_transformation.definitions import PositionDefinition3d, RotationDefinition3d, Unit
from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_3d import Transform3D

import numpy as np
import pytest
import testutils


def random_definition_position3d(rng: np.random.Generator) -> PositionDefinition3d:
    choices = [PositionDefinition3d.CARTESIAN, PositionDefinition3d.CYLINDRICAL, PositionDefinition3d.SPHERICAL]

    idx_chosen = rng.choice(choices)

    return PositionDefinition3d(idx_chosen)


def random_unit(rng: np.random.Generator) -> Unit:
    choices = [Unit.M_DEG, Unit.MM_DEG, Unit.M_RAD, Unit.MM_RAD]

    idx_chosen = rng.choice(choices)

    return Unit(idx_chosen)


@pytest.mark.randomized
def test_angle_wrap_EULER_REP_XYZ() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        ori = Rotation3D(
            *testutils.random_4_tuple(rng), definition=RotationDefinition3d.EULER_INTRINSIC_XYZ, units=Unit.MM_RAD
        )

        uservals = ori.export_as_EULER_INTRINSIC_XYZ(Unit.MM_RAD)

        assert -np.pi <= uservals[0] <= np.pi
        assert -np.pi <= uservals[1] <= np.pi
        assert -np.pi <= uservals[2] <= np.pi


@pytest.mark.randomized
def test_angle_wrap_EULER_REP_ZYX() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        ori = Rotation3D(
            *testutils.random_4_tuple(rng), definition=RotationDefinition3d.EULER_INTRINSIC_ZYX, units=Unit.MM_RAD
        )

        uservals = ori.export_as_EULER_INTRINSIC_ZYX(Unit.MM_RAD)

        assert -np.pi <= uservals[0] <= np.pi
        assert -np.pi <= uservals[1] <= np.pi
        assert -np.pi <= uservals[2] <= np.pi


@pytest.mark.randomized
def test_angle_wrap_QUATERNION() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        ori = Rotation3D(*testutils.random_4_tuple(rng), definition=RotationDefinition3d.Quaternion, units=Unit.MM_RAD)

        uservals = ori.export_as_QUATERNION()

        assert -1 <= uservals[0] <= 1
        assert -1 <= uservals[1] <= 1
        assert -1 <= uservals[2] <= 1
        assert -1 <= uservals[3] <= 1


@pytest.mark.randomized
def test_angle_wrap_RODRIGUES() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        ori = Rotation3D(*testutils.random_4_tuple(rng), definition=RotationDefinition3d.Rodrigues, units=Unit.MM_RAD)

        uservals = ori.export_as_RODRIGUES(Unit.M_RAD)

        assert -np.pi <= uservals[0] <= np.pi
        assert -np.pi <= uservals[1] <= np.pi
        assert -np.pi <= uservals[2] <= np.pi

        # print(str(ori) + " " + str(np.linalg.norm([ori.val1, ori.val2, ori.val3])))


@pytest.mark.randomized
def test_angle_wrap_AXIS_ANGLE() -> None:
    rng = np.random.default_rng(0)

    for i in range(1000):
        ori = Rotation3D(*testutils.random_4_tuple(rng))

        assert -np.pi <= ori.export_as_AXIS_ANGLE(Unit.MM_RAD)[3] <= np.pi

        ori = Rotation3D(*testutils.random_4_tuple(rng), definition=RotationDefinition3d.Axis_Angle, units=Unit.M_DEG)

        assert -180 <= ori.export_as_AXIS_ANGLE(Unit.MM_DEG)[3] <= 180

        # print(ori)


@pytest.mark.randomized
def test_invert_random() -> None:
    choice_def = list(RotationDefinition3d)
    choice_def.remove(RotationDefinition3d.Antenna)  # Not implemented

    rng = np.random.default_rng(0)

    for i in range(1000):
        definition_original = rng.choice(choice_def)
        units_original = rng.choice(list(Unit))
        ori = Rotation3D(*testutils.random_4_tuple(rng), definition=definition_original, units=units_original)

        p_0: Position3D = Position3D(
            *testutils.random_3_tuple(rng), random_definition_position3d(rng), rng.choice(list(Unit))
        )

        definition_random = testutils.random_definition_rotation3d(rng)
        units_random = random_unit(rng)

        p_1 = ori * p_0
        assert ori.invert(definition=definition_random, units=units_random) * p_1 == p_0

        assert ori == ori.invert(definition=definition_random, units=units_random).invert(
            definition=definition_random, units=units_random
        )


@pytest.mark.randomized
def test_from_rotmat_random() -> None:
    choice_def = list(RotationDefinition3d)
    choice_def.remove(RotationDefinition3d.Antenna)  # Not implemented

    rng = np.random.default_rng(0)

    for i in range(1000):
        definition_original = rng.choice(choice_def)
        units_original = rng.choice(list(Unit))

        ori = Rotation3D(*testutils.random_4_tuple(rng), definition=definition_original, units=units_original)

        tmat_random = ori._rotmat
        assert ori == Rotation3D.from_rotmat(tmat_random)


@pytest.mark.randomized
def test_mul() -> None:
    choice_def = list(RotationDefinition3d)
    choice_def.remove(RotationDefinition3d.Antenna)  # Not implemented

    rng = np.random.default_rng(0)

    for i in range(1000):
        o1 = Rotation3D(*testutils.random_4_tuple(rng), testutils.random_definition_rotation3d(rng), random_unit(rng))
        o2 = Rotation3D(*testutils.random_4_tuple(rng), testutils.random_definition_rotation3d(rng), random_unit(rng))
        o3 = Rotation3D(*testutils.random_4_tuple(rng), testutils.random_definition_rotation3d(rng), random_unit(rng))

        assert (o2 * o3).invert() == o3.invert() * o2.invert()  # type: ignore[union-attr]
        assert (o1 * o2 * o3).invert() == o3.invert() * o2.invert() * o1.invert()  # type: ignore[union-attr, operator]
        assert o1.copy() * o2 == o1 * o2.copy()


@pytest.mark.hardcoded
def test_invert() -> None:
    o = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 45, 0, Unit.MM_DEG)
    p0 = Position3D.from_cartesian(1000, 0, 0, Unit.MM_DEG)
    p1 = o * p0

    assert p0 == o.invert() * p1


# @pytest.mark.hardcoded
# def test_arithmetic() -> None:
#     print("")
#     o0 = Rotation3D.from_EULER_INTRINSIC_XYZ(210, 120, 140, Unit.MM_DEG)
#     print(o0)
#     o00 = Rotation3D.from_EULER_INTRINSIC_ZYX(210, 120, 140, Unit.MM_DEG)
#     print(o0.invert().export_as_EULER_INTRINSIC_XYZ(units=Unit.MM_DEG))
#     print(o0.invert().export_as_EULER_INTRINSIC_ZYX(units=Unit.MM_DEG))
#     print(o0.invert().export_as_EULER_INTRINSIC_XYZ(units=Unit.MM_DEG))
#     o3 = o0 * Rotation3D.from_EULER_INTRINSIC_XYZ(0, 90, 0, Unit.MM_DEG)
#     print(o3)


#     o2 = Rotation3D.from_EULER_INTRINSIC_ZYX(210, 120, 140, Unit.MM_DEG)
#     print(o2)
#     o3 = o2.export_as_EULER_INTRINSIC_ZYX()
#     print(o3)

#     print("-----------------------------------")
#     o00 = Rotation3D.from_EULER_INTRINSIC_ZYX(36.059, 18.809, 36.059, Unit.MM_DEG)
#     print(o00)
#     o3 = o00.export_as_RODRIGUES()
#     print(o3)
#     distance = np.linalg.norm(o00.export_as_RODRIGUES())
#     print("angle ", distance)
#     print(o00.export_as_EULER_INTRINSIC_ZYX())
#     print("-----------------------------------")
#     o5 = Rotation3D.from_RODRIGUES(0.5, 0.5, 0.5, Unit.MM_DEG)
#     # o5 = Rotation3D.from_RODRIGUES(0.488, 0.195, 0, Unit.MM_DEG)
#     print(o5)
#     o6 = o5.export_as_EULER_INTRINSIC_XYZ(units=Unit.MM_DEG)
#     print("from Rodrigues to Euler_XYZ: ", o6)
#     print("from Rodrigues to Euler_XYZ: ", o5.export_as_EULER_INTRINSIC_XYZ(units=Unit.MM_DEG))
#     print("from Rodrigues to Euler_XYZ: ", o5.export_as_EULER_INTRINSIC_ZYX(units=Unit.MM_DEG))
#     print("from Rodrigues to Euler_XYZ: ", o5.export_as_RODRIGUES(units=Unit.MM_DEG))
#     print("from Rodrigues to Euler_XYZ: ", o5.export_as_QUATERNION())
#     print("from Rodrigues to Euler_XYZ: ", o5.export_as_EULER_INTRINSIC_XYZ(units=Unit.MM_DEG))
#     print("-----------------------------------")
#     o2 = Rotation3D.from_QUATERNION(0.25, 0.1, 0.5, 0.99)
#     print('02 -> ', o2.export_as_QUATERNION())
#     # o2 = Rotation3D.from_QUATERNION(20.045, 0.53, -10.165, 0.83)

#     vals = o2.export_as_QUATERNION()
#     o2 = Rotation3D.from_QUATERNION(vals[0], vals[1], vals[2], vals[3])
#     print('02 -> ', o2)
#     o3 = o2.export_as_EULER_INTRINSIC_ZYX(units=Unit.MM_DEG)
#     print('O3 -> ', o3)
#     o7 = o2.invert().export_as_QUATERNION()
#     print('O3 -> ', o3)
#     o4 = o2.export_as_QUATERNION()
#     print('O4 -> ', o4)
#     print("-----------------------------------")
#     o2 = Rotation3D.from_AXIS_ANGLE(0.5, 0.89, 0.72, 83, Unit.MM_DEG)
#     print(o2)
#     o3 = o2.export_as_QUATERNION()
#     print(o3)
#     o4 = o2.export_as_AXIS_ANGLE(units=Unit.MM_DEG)
#     print(o4)
#     o4 = o2.from_QUATERNION(0.045, 0.53, -0.165, 0.83)
#     print(o4)

#     print("-----------------------------------")
#     print("-----------------------------------")
#     o2 = Rotation3D.from_EULER_INTRINSIC_XYZ(210, 120, 140, Unit.MM_DEG)

#     print(o2)
#     o3 = o2.export_as_QUATERNION()
#     print(o3)
#     o4 = Rotation3D.from_QUATERNION(0.045, 0.53, -0.165, 0.83)
#     print(o4)

#     o2 = Rotation3D.from_EULER_INTRINSIC_XYZ(90, 0, 0, Unit.MM_DEG)
#     p1 = Position3D.from_cartesian(0, 90, 0, Unit.MM_DEG)
#     p = o2 * p1
#     print(p)

#     o = Rotation3D.from_EULER_INTRINSIC_XYZ(90, 45, 0, Unit.MM_DEG)
#     print(o._rotmat)
#     print(o.invert(definition=RotationDefinition3d.Axis_Angle).invert()._rotmat - o._rotmat)

#     o = Rotation3D.from_EULER_INTRINSIC_XYZ(90, 0, 0, Unit.MM_DEG)
#     print(Rotation3D.from_rotmat(o._rotmat))

if __name__ == "__main__":
    test_angle_wrap_EULER_REP_XYZ()
    test_angle_wrap_EULER_REP_ZYX()
    test_angle_wrap_QUATERNION()
    test_angle_wrap_RODRIGUES()
    test_angle_wrap_AXIS_ANGLE()

    test_invert_random()
    test_invert()
    test_from_rotmat_random()

    test_mul()
