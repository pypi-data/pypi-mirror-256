"""
Contains functions for the conversion of angles to frames and vice versa. Moreover, frames can be plotted.
"""
from __future__ import annotations

from spatial_transformation.definitions import PositionDefinition3d, RotationDefinition3d, Unit
from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D

import numpy as np
from scipy.spatial.transform import Rotation


class Transform3D:
    """
    Transform3D implements a transformation as a homogeneous 4x4 matrix.

    Attributes
    ----------
        position : Position3D,
            An element containing 3D axis position value in terms of cartesian cs
        rotation : Rotation,
            An element containing 3D axis rotation value
        tmat : np.ndarray,
            An element containing 4x4 homogenous matrix.

    """

    _tmat: np.ndarray  # tmat for calculations; note that position and rotation will access this data using numpy views

    _position: Position3D
    _rotation: Rotation3D

    def __init__(
        self,
        position: Position3D | None = None,
        rotation: Rotation3D | None = None,
        tmat: np.ndarray[float] | None = None,
    ) -> None:
        """
        Generates a coordinate system...
        - from "tmat", if specified
        - from "position" and "rotation", if specified
        - or with default values (no translation, no rotation)
        """
        # tmat can be stored at known memory location
        if tmat is None:
            self._tmat = np.eye(4)
        else:
            self._tmat = tmat

        if position is None:
            # no position argument, so generate new one but specifically use this instance's tmat to store data
            self._position = Position3D(0, 0, 0)
            self._position.set_position_vector_ref_and_adopt_values(self._tmat[0:3, 3])
        else:
            # use given position data and write to own tmat
            self._position = position.copy()  # copy so changes wont reflect on input position
            self._position.set_position_vector_ref_and_keep_own_values(self._tmat[0:3, 3])

        if rotation is None:
            # no rotation argument, so generate new one but specifically use this instance's tmat to store data
            self._rotation = Rotation3D(0, 0, 0, 0)
            self._rotation.set_rotmat_ref_and_adopt_values(self._tmat[0:3, 0:3])
        else:
            # use given rotation data and write to own tmat
            self._rotation = rotation.copy()  # copy so changes wont reflect on input position
            self._rotation.set_rotmat_ref_and_keep_own_values(self._tmat[0:3, 0:3])  # use self._tmat as data storage

    @staticmethod
    def from_tmat(tmat: np.ndarray) -> Transform3D:
        """
        Generate coordinate system using the given format from a given tmat. The tmat must be in shape (4x4).

        Raises: ValueError if tmat is not in correct shape or includes scale/perspective values.
        """
        # Test if shape is valid
        if tmat.shape != (4, 4):
            raise ValueError("tmat is in shape " + str(tmat.shape) + " but is expected in shape (4, 4)")

        # Test if scale/perspective changes are included
        if not (np.all(np.concatenate([tmat[3, 0:3]]) == 0) and tmat[3, 3] == 1):
            raise ValueError("tmat includes scale and/or perspective change, which are not supported yet!")

        sys_result = Transform3D(Position3D.from_cartesian(*tmat[0:3, 3]), Rotation3D.from_rotmat(tmat[0:3, 0:3]))

        return sys_result

    def __mul__(self, other: Transform3D | Position3D) -> Transform3D | Position3D:
        """
        Multiplication with either Transform3D or Position3D. Definition and unit of resulting object will be...
        - the default if both operands are of type Transform3D
        - the definition and unit of the other operand, if it is of type Position3d

        returns: Resulting position or coordinate system
        """
        if isinstance(other, Transform3D):  # return wrapped 4x4 tmat
            return Transform3D(tmat=(self._tmat @ other._tmat))

        elif isinstance(other, Position3D):  # return wrapped 4x1 tvec
            vector_pos_homogenous = np.array([0, 0, 0, 1], dtype=np.float64)
            vector_pos_homogenous[0:3] = other.get_vector_3x1().flatten()

            vec_pos_homogenous_resulting = self._tmat @ vector_pos_homogenous
            vec_pos_resulting = vec_pos_homogenous_resulting[0:3]

            return Position3D.from_cartesian(*vec_pos_resulting)
        else:
            msg = f"unsupported operand types for __mul__: '{type(self)}' and '{type(other)}'"
            print(msg)
            raise TypeError(msg)

    def __eq__(self, other: object) -> bool:
        """
        Check if given object is equal.
        """
        is_equal = False
        if isinstance(other, Transform3D):
            is_equal = np.allclose(self._tmat, other._tmat)
        return is_equal

    def __repr__(self) -> str:
        """
        Generate string representation of coordinate system.
        """
        return self.to_string()

    def invert(self) -> Transform3D:
        """
        Returns inversed coordinate system in new instance.
        """
        # calculate inverse function -------------------------------------------------------------------------

        # TODO: mypy does not like "position_inverted: Position3D rotation_inverted * self._position * (-1.0)", should we do this instead:

        rotation_inverted: Rotation3D = self._rotation.invert()
        position_inverted = rotation_inverted * (self._position * (-1.0))  # parentheses because mypy wants them

        if not isinstance(position_inverted, Position3D):
            raise RuntimeError("Multiplication Rotation3D * Position3D did not result in Position3D")

        return Transform3D(position=position_inverted, rotation=rotation_inverted)

    def get_rotation_reference(self) -> Rotation3D:
        """
        Returns the system's rotation. Changes to the rotation will reflect on the system.
        """
        return self._rotation

    def get_position_reference(self) -> Position3D:
        """
        Returns the system's position. Changes to the position will reflect on the system.
        """
        return self._position

    def get_rotation(self) -> Rotation3D:
        """
        Returns the system's rotation. Changes to the rotation will reflect on the system.
        """
        return self.get_rotation_reference().copy()

    def get_position(self) -> Position3D:
        """
        Returns the system's position. Changes to the position will reflect on the system.
        """
        return self.get_position_reference().copy()

    def copy(self) -> Transform3D:
        """
        Returns new instance with same properties.
        """
        return Transform3D(position=self.get_position_reference().copy(), rotation=self.get_rotation_reference().copy())

    def export_as_matrix(self) -> np.ndarray:
        """
        Returns this transformation as homogenous 4x4 transformation matrix. This matrix is a new object, changes to it will not reflect on the original object.
        """
        tmat_result = np.eye(4)

        tmat_result[0:3, 0:3] = self.get_rotation_reference().export_as_matrix()
        tmat_result[0:3, 3] = self.get_position_reference().export_as_cartesian()

        return tmat_result

    def to_string(
        self,
        definition_position: PositionDefinition3d = PositionDefinition3d.CARTESIAN,
        units_position: Unit = Unit.MM_DEG,
        definition_rotation: RotationDefinition3d = RotationDefinition3d.EULER_INTRINSIC_XYZ,
        units_rotation: Unit = Unit.MM_DEG,
    ) -> str:
        """
        Represent the transformation in the given representation types.
        """
        rep = "Transform3d:\n"
        rep += f"  - {self._position.to_string(definition_position, units_position)}\n"
        rep += f"  - {self._rotation.to_string(definition_rotation, units_rotation)}\n"

        return rep

    # Update functions for position ---------------------

    def update_pos_spherical(
        self, r: float | None = None, theta: float | None = None, phi: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set position values, overwriting existing values."""
        self._position.update_spherical(
            r, theta, phi, units
        )  # _position shares a slice of tmat; changes will be seen there

    def update_pos_cylindrical(
        self, r: float | None = None, phi: float | None = None, z: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set position values, overwriting existing values."""
        self._position.update_cylindrical(
            r, phi, z, units
        )  # _position shares a slice of tmat; changes will be seen there

    def update_pos_cartesian(
        self, x: float | None = None, y: float | None = None, z: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set position values, overwriting existing values."""
        self._position.update_cartesian(x, y, z, units)  # _position shares a slice of tmat; changes will be seen there

    def update_rot_as_EULER_REP_XYZ(
        self, rx: float | None = None, ry: float | None = None, rz: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set rotation values, overwriting existing values."""
        self._rotation.update_as_EULER_INTRINSIC_XYZ(
            rx, ry, rz, units
        )  # _rotation shares a slice of tmat; changes will be seen there

    def update_rot_as_EULER_REP_ZYX(
        self, rz: float | None = None, ry: float | None = None, rx: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set rotation values, overwriting existing values."""
        self._rotation.update_as_EULER_INTRINSIC_ZYX(
            rz, ry, rx, units
        )  # _rotation shares a slice of tmat; changes will be seen there

    def update_rot_as_QUATERNION(
        self, a: float | None = None, b: float | None = None, c: float | None = None, d: float | None = None
    ) -> None:
        """Set rotation values, overwriting existing values."""
        self._rotation.update_as_QUATERNION(a, b, c, d)  # _rotation shares a slice of tmat; changes will be seen there

    def update_rot_as_RODRIGUES(
        self, x: float | None = None, y: float | None = None, z: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set rotation values, overwriting existing values."""
        self._rotation.update_as_RODRIGUES(
            x, y, z, units
        )  # _rotation shares a slice of tmat; changes will be seen there

    def update_rot_as_AXIS_ANGLE(
        self,
        x: float | None = None,
        y: float | None = None,
        z: float | None = None,
        angle: float | None = None,
        units: Unit = Unit.MM_DEG,
    ) -> None:
        """Set rotation values, overwriting existing values."""
        self._rotation.update_as_AXIS_ANGLE(
            x, y, z, angle, units
        )  # _rotation shares a slice of tmat; changes will be seen there


# example
if __name__ == "__main__":
    t_0_1 = Transform3D(
        Position3D.from_cartesian(0, 0, 0, Unit.MM_DEG),
        Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90, units=Unit.MM_DEG),
    )

    print(t_0_1.invert() * Position3D(1, 0, 0))

    t_0_1 = Transform3D(
        Position3D.from_cartesian(0, 0, 0, Unit.MM_DEG), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 0, units=Unit.MM_DEG)
    )

    t_1_2 = Transform3D(
        Position3D.from_cartesian(0, 1000, 0, Unit.MM_DEG),
        Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 0, units=Unit.MM_DEG),
    )

    p = Position3D.from_cartesian(1, 0, 0, units=Unit.M_DEG)
    t_0_1.get_rotation_reference().update_as_EULER_INTRINSIC_XYZ(rz=90, units=Unit.MM_DEG)
    print(t_0_1 * p)
    assert t_0_1 * p == Position3D.from_cartesian(0, 1, 0, units=Unit.M_DEG)
    print(t_0_1 * p)

    t_0_1 = Transform3D()  # T_0_1
    t_1_2 = Transform3D()  # T_1_2

    t_0_1.update_pos_cartesian(x=1, units=Unit.M_DEG)
    t_1_2.update_pos_cartesian(y=1, units=Unit.M_DEG)
    t_1_2.get_rotation_reference().update_as_EULER_INTRINSIC_XYZ(rz=90, units=Unit.MM_DEG)
    print(t_0_1)
    sys_3 = t_0_1 * t_1_2
    print(t_0_1 * p)
    print(sys_3 * p)
    # assert sys_3 * p == Position3D.from_cartesian(1, 2, 0, units=Unit.M_DEG)
    print(t_0_1.invert() * p)
    assert t_0_1.invert() * p == Position3D.from_cartesian(0, 0, 0)
