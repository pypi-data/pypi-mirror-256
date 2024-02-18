"""
Contains functions for the conversion of angles to frames and vice versa. Moreover, frames can be plotted.
"""
from __future__ import annotations

import dataclasses
from numbers import Real

from spatial_transformation.definitions import PositionDefinition3d, RotationDefinition3d, Unit
from spatial_transformation.position_3d import Position3D
from spatial_transformation.utils import MathUtilsRotation, MathUtilsRotation3d

import numpy as np
from scipy.spatial.transform import Rotation


class Rotation3D:
    """
    3D-rotation.

    Attributes
    ----------
        value1 (float):
            An element containing 3D axis rotation value (angle/value).
        value2 (float):
            An element containing 3D axis rotation value (angle/value).
        value3 (float):
            An element containing 3D axis rotation value (angle/value).
        value4 (float):
            An element containing 3D axis rotation value. value4 is used for quaternion
        rotmat (np.ndarray):
            An element containing 4x4 homogenous rotation matrix.

        definition (RotationRepresentation):
            To convert the angles to rotation matrix rotation representation is required.
            'EULER_INTRINSIC_XYZ' or 'EULER_INTRINSIC_ZYX': To convert to euler angles
            'RODRIGUES':  To convert using rodrigues
            'QUATERNION': To convert from quaternion

        units (UnitDef):
            Defines the unit type for position and rotation.
                unit_trans (UnitTrans):
                    position unit_trans repr,
                    Select the type of position unit_trans such as 'mm' or 'm'. By default, 'mm' is used.
                unit_rot (UnitRot):
                    angle unit_rot repr,
                    Select the type of position unit_trans such as 'deg' or 'rad'. By default, 'deg' is used.

    """

    _rotmat: np.ndarray

    def __init__(
        self,
        val1: float,
        val2: float,
        val3: float,
        val4: float,
        definition: RotationDefinition3d = RotationDefinition3d.EULER_INTRINSIC_XYZ,
        units: Unit = Unit.MM_DEG,
    ):
        """
        Generates a rotation...
        - from "rot_mat", if specified
        - from given rotation parameters, if specified
        - or with default values (no translation, no rotation)
        """
        self._rotmat = MathUtilsRotation3d.get_rotmat_from_vals([val1, val2, val3, val4], definition, units)

    def update(
        self,
        definition: RotationDefinition3d = RotationDefinition3d.EULER_INTRINSIC_XYZ,
        val1: float | None = None,
        val2: float | None = None,
        val3: float | None = None,
        val4: float | None = None,
        units: Unit = Unit.MM_DEG,
    ) -> None:
        # TODO Place definition behind values
        """
        Updates specified values in specified format.
        """
        # convert internal tvec to value format, in which user wants to update:
        vals_inUpdateFormat = MathUtilsRotation3d.get_vals_from_rotmat(self._rotmat, definition, units)

        # write every value that has been specified; leave unspecified values as-is
        if val1 is not None:
            vals_inUpdateFormat[0] = val1
        if val2 is not None:
            vals_inUpdateFormat[1] = val2
        if val3 is not None:
            vals_inUpdateFormat[2] = val3
        if len(vals_inUpdateFormat) > 3 and val4 is not None:
            vals_inUpdateFormat[3] = val4

        self._rotmat[:, :] = MathUtilsRotation3d.get_rotmat_from_vals(
            vals_inUpdateFormat, definition, units
        )  # generate tvec from updated values

    def update_as_EULER_INTRINSIC_XYZ(
        self, rx: float | None = None, ry: float | None = None, rz: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """
        Updates the specified values of EULER_REP_XYZ and applies them to this object.

        returns: None
        """
        self.update(RotationDefinition3d.EULER_INTRINSIC_XYZ, rx, ry, rz, units=units)

    def update_as_EULER_INTRINSIC_ZYX(
        self, rz: float | None = None, ry: float | None = None, rx: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """
        Updates the specified values of EULER_REP_ZYX and applies them to this object.
        """
        self.update(RotationDefinition3d.EULER_INTRINSIC_ZYX, rz, ry, rx, units=units)

    def update_as_QUATERNION(
        self, a: float | None = None, b: float | None = None, c: float | None = None, d: float | None = None
    ) -> None:
        """
        Updates the specified values of QUATERNION and applies them to this object.

        returns: None
        """
        self.update(RotationDefinition3d.Quaternion, a, b, c, d)

    def update_as_RODRIGUES(
        self, rx: float | None = None, ry: float | None = None, rz: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """
        Updates the specified values of RODRIGUES and applies them to this object.

        returns: None
        """
        self.update(RotationDefinition3d.Rodrigues, rx, ry, rz, units=units)

    def update_as_AXIS_ANGLE(
        self,
        rx: float | None = None,
        ry: float | None = None,
        rz: float | None = None,
        angle: float | None = None,
        units: Unit = Unit.MM_DEG,
    ) -> None:
        """
        Updates the specified values of AXIS_ANGLE and applies them to this object.

        returns: None
        """
        self.update(RotationDefinition3d.Axis_Angle, rx, ry, rz, angle, units=units)

    def export(
        self, definition: RotationDefinition3d, units: Unit = Unit.MM_DEG
    ) -> tuple[float, float, float] | tuple[float, float, float, float]:
        """
        Returns rotation in specified definition with specified units.
        """
        if definition == RotationDefinition3d.EULER_INTRINSIC_XYZ:
            return self.export_as_EULER_INTRINSIC_XYZ(units)
        elif definition == RotationDefinition3d.EULER_INTRINSIC_ZYX:
            return self.export_as_EULER_INTRINSIC_ZYX(units)
        elif definition == RotationDefinition3d.Quaternion:
            return self.export_as_QUATERNION()
        elif definition == RotationDefinition3d.Axis_Angle:
            return self.export_as_AXIS_ANGLE(units)
        elif definition == RotationDefinition3d.Rodrigues:
            return self.export_as_RODRIGUES(units)
        else:
            raise ValueError(f"Target definition {definition} is not supported!")

    def export_as_EULER_INTRINSIC_XYZ(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Returns intrinsic Euler angles XYZ.
        """
        result: list[float] = MathUtilsRotation3d.get_vals_from_rotmat(
            self._rotmat, definition=RotationDefinition3d.EULER_INTRINSIC_XYZ, units=units
        )
        return (result[0], result[1], result[2])

    def export_as_EULER_INTRINSIC_ZYX(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Returns intrinsic Euler angles ZYX.
        """
        result: list[float] = MathUtilsRotation3d.get_vals_from_rotmat(
            self._rotmat, definition=RotationDefinition3d.EULER_INTRINSIC_ZYX, units=units
        )
        return (result[0], result[1], result[2])

    def export_as_QUATERNION(self) -> tuple[float, float, float, float]:
        """
        Returns: 4 quaternions: (x, y, z, w) format.
        """
        result: list[float] = MathUtilsRotation3d.get_vals_from_rotmat(
            self._rotmat, definition=RotationDefinition3d.Quaternion
        )
        return (result[0], result[1], result[2], result[3])

    def export_as_RODRIGUES(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Returns: 3-dimensional vector which is co-directional to the axis of rotation and whose norm gives the angle of rotation.
        """
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_rotvec.html

        result: list[float] = MathUtilsRotation3d.get_vals_from_rotmat(
            self._rotmat, definition=RotationDefinition3d.Rodrigues, units=units
        )
        return (result[0], result[1], result[2])

    def export_as_AXIS_ANGLE(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float, float]:
        """
        Returns: rotation, represented by rotation axis (vec[0] ... vev[2]) and rotation angle (vec[3]).
        """
        result: list[float] = MathUtilsRotation3d.get_vals_from_rotmat(
            self._rotmat, definition=RotationDefinition3d.Axis_Angle, units=units
        )
        return (result[0], result[1], result[2], result[3])

    def export_as_matrix(self) -> np.ndarray:
        """
        Exports this rotation's matrix representation. This matrix is a new object, changes to it will not reflect on the original object.
        """
        return self._rotmat.copy()

    @staticmethod
    def from_EULER_INTRINSIC_XYZ(rx: float, ry: float, rz: float, units: Unit = Unit.MM_DEG) -> Rotation3D:
        """
        X angle belongs to [-180, 180] degrees (both inclusive).
        Z angle belongs to [-180, 180] degrees (both inclusive).
        Second angle belongs to [-90, 90] degrees.
        """
        ori = Rotation3D(rx, ry, rz, 0, definition=RotationDefinition3d.EULER_INTRINSIC_XYZ, units=units)
        return ori

    @staticmethod
    def from_EULER_INTRINSIC_ZYX(rz: float, ry: float, rx: float, units: Unit = Unit.MM_DEG) -> Rotation3D:
        """
        X angle belongs to [-180, 180] degrees (both inclusive).
        Z angle belongs to [-180, 180] degrees (both inclusive).
        X angle belongs to [-90, 90] degrees.
        """
        ori = Rotation3D(rz, ry, rx, 0, definition=RotationDefinition3d.EULER_INTRINSIC_ZYX, units=units)
        return ori

    @staticmethod
    def from_QUATERNION(a: float, b: float, c: float, d: float) -> Rotation3D:
        """
        Scipy function -> a, b, c, d without a unit.
        """
        ori = Rotation3D(a, b, c, d, definition=RotationDefinition3d.Quaternion, units=Unit.MM_DEG)
        return ori

    @staticmethod
    def from_RODRIGUES(x: float, y: float, z: float, units: Unit = Unit.MM_DEG) -> Rotation3D:
        """
        Scipy function -> x, y, z without a unit.
        """
        ori = Rotation3D(x, y, z, 0, definition=RotationDefinition3d.Rodrigues, units=units)

        return ori

    @staticmethod
    def from_AXIS_ANGLE(x: float, y: float, z: float, alpha: float, units: Unit = Unit.MM_DEG) -> Rotation3D:
        """
        Scipy function -> x, y, z without unit; alpha [-180, 180] in unit.
        """
        ori = Rotation3D(x, y, z, alpha, definition=RotationDefinition3d.Axis_Angle, units=units)

        return ori

    @staticmethod
    def from_rotmat(rotmat: np.ndarray) -> Rotation3D:
        """
        Returns rotation object calculated from a rotation matrix.
        """
        # generate new instance
        result = Rotation3D(0, 0, 0, 0)

        # appy given rotmat
        result._rotmat[:, :] = rotmat

        return result

    def __repr__(self) -> str:
        """
        Generates string representation in intrinsic euler xyz representation [-180°, 180°].
        """
        return self.to_string(definition=RotationDefinition3d.EULER_INTRINSIC_XYZ, units=Unit.MM_DEG)

    def __mul__(self, other: Rotation3D | Position3D) -> Rotation3D | Position3D:
        """
        Multiplication with either Rotation3D or Position3D. Definition and unit of resulting object will be...
        - if both operands are of type Rotation3d:
            - the same as the one of self and other, if both operands have the same unit and definition
            - the default definition and unit, if operands differ
        - if operand2 is of type Position3d:
            - the definition and unit of the Position3d

        Returns: Resulting position or rotation.
        """
        if isinstance(other, Rotation3D):
            rotmat_result = other._rotmat @ self._rotmat
            return Rotation3D.from_rotmat(rotmat=rotmat_result)
        elif isinstance(other, Position3D):
            rotmat_result = self._rotmat @ other.get_vector_3x1()
            return Position3D.from_cartesian(*rotmat_result.flatten())
        else:
            raise TypeError("multiplication not a Rotation3D (for multiplication) or a Position3D (cross product)")

    def __eq__(self, other: object) -> bool:
        """
        Checks for equality in a defined range.
        See https://numpy.org/doc/stable/reference/generated/numpy.allclose.html
        """
        is_equal = False
        if isinstance(other, Rotation3D):
            is_equal = np.allclose(self._rotmat, other._rotmat)

        return is_equal

    def __hash__(self) -> int:
        """
        Calculates hash based on id.
        """
        return hash(id(self))

    def is_close(self, other: Rotation3D, rtol: float = 1e-05, atol: float = 1e-08) -> bool:
        """
        Checks for equality in a range that can be specified with rtol and atol.
        See https://numpy.org/doc/stable/reference/generated/numpy.allclose.html
        """
        is_equal = False
        if isinstance(other, Rotation3D):
            is_equal = np.allclose(self._rotmat, other._rotmat, rtol=rtol, atol=atol)

        return is_equal

    def invert(self, definition: RotationDefinition3d | None = None, units: Unit = Unit.MM_DEG) -> Rotation3D:
        """
        Returns inverted rotation. Uses default definition and units if not specified in parameters.
        """
        rotmat_inverted = np.matrix.transpose(self._rotmat)
        return Rotation3D.from_rotmat(rotmat_inverted)

    def copy(self) -> Rotation3D:
        """
        Returns copy of this object.
        """
        return Rotation3D.from_rotmat(self._rotmat)

    def to_string(
        self, definition: RotationDefinition3d = RotationDefinition3d.EULER_INTRINSIC_XYZ, units: Unit = Unit.MM_DEG
    ) -> str:
        """
        Generates string representation in given definition and units.
        """
        vals = MathUtilsRotation3d.get_vals_from_rotmat(self._rotmat, definition=definition, units=units)

        rep = "Rotation:"
        # p_cyl = self.cartesian_to_cylindrical()
        # p_sphe = self.cartesian_to_spherical()
        if definition == RotationDefinition3d.EULER_INTRINSIC_XYZ:
            rep += (
                f"\t Euler XYZ (rx, ry, rz):   \t{vals[0]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[1]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[2]:9.3f} {units.get_rotation_unit()}"
            )

        elif definition == RotationDefinition3d.EULER_INTRINSIC_ZYX:
            rep += (
                f"\t Euler ZYX (rz, ry, ry):   \t{vals[0]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[1]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[2]:9.3f} {units.get_rotation_unit()}"
            )

        elif definition == RotationDefinition3d.Quaternion:
            rep += (
                f"\t Quaternion (a, b, c, d):   \t{vals[0]:9.3f} --, "
                f"{vals[1]:9.3f} --, "
                f"{vals[2]:9.3f} --, "
                f"{vals[3]:9.3f} --, "
            )

        elif definition == RotationDefinition3d.Rodrigues:
            rep += (
                f"\t Rodrigues (x, y, z):   \t{vals[0]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[1]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[2]:9.3f} {units.get_rotation_unit()}, "
            )

        elif definition == RotationDefinition3d.Axis_Angle:
            rep += (
                f"\t Axis Angle (x, y, z, alpha):   \t{vals[0]:9.3f} {units.get_translation_unit()}, "
                f"{vals[1]:9.3f} {units.get_translation_unit()}, "
                f"{vals[2]:9.3f} {units.get_translation_unit()}, "
                f"{vals[3]:9.3f} {units.get_rotation_unit()}, "
            )

        else:
            rep += f"\t angle: {vals[0]:9.4f}, {vals[1]:9.4f}, {vals[2]:9.4f}, {vals[3]:9.4f}\t"

        return rep

    def set_rotmat_ref(self, rotmat: np.ndarray[float], write_own_values: bool = False) -> None:
        """
        Sets internal vector's memory address to the given vector's address. Modifications to this position instance will be seen at the given addresss.
        """
        if write_own_values:
            # write the instance's values to the memory location before using it

            rotmat[:, :] = self._rotmat[:, :]  # write current values to external memory location

            self._rotmat = rotmat  # now use external memory location as internal
        else:
            # write the memory location's value to this instance

            self._rotmat = rotmat

    def set_rotmat_ref_and_keep_own_values(self, rotmat: np.ndarray[float]) -> None:
        """
        Use given rotmat to store data but first write this instance's values to the given rotmat.

        Modifications to this position instance then will be seen at the given addresss.
        """
        self.set_rotmat_ref(rotmat=rotmat, write_own_values=True)

    def set_rotmat_ref_and_adopt_values(self, rotmat: np.ndarray[float]) -> None:
        """
        Use given rotmat to store data and update this instances own values from the given rotmat.

        Modifications to this position instance then will be seen at the given addresss.
        """
        self.set_rotmat_ref(rotmat=rotmat, write_own_values=False)
