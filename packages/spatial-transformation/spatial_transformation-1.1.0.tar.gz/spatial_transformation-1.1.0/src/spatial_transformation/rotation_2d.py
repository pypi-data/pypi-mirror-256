"""
Contains functions for the conversion of angles to frames and vice versa. Moreover, frames can be plotted.
"""
from __future__ import annotations

import dataclasses

from spatial_transformation.definitions import RotationDefinition2d, Unit
from spatial_transformation.position_2d import Position2D
from spatial_transformation.utils import MathUtilsRotation, MathUtilsRotation2d

import numpy as np
from scipy.spatial.transform import Rotation


class Rotation2D:
    """
    2D-rotation.

    Attributes
    ----------
        angle1 (float):
            An element containing 3D axis rotation value
        rotmat (np.ndarray):
            An element containing 2x2 homogenous rotation matrix.
        definition (RotationRepresentation):
            ...
        units (UnitDef):
            Defines the unit type for position and rotation.
                unit_trans (UnitTrans):
                    position unit_trans repr,
                    Select the type of position unit_trans such as 'mm', 'cm' or 'm'. By default, 'mm' is used.
                unit_rot (UnitRot):
                    angle unit_rot repr,
                    Select the type of position unit_trans such as 'deg' or 'rad'. By default, 'deg' is used.

    """

    _rotmat: np.ndarray[float]

    def __init__(
        self, val1: float, definition: RotationDefinition2d = RotationDefinition2d.Cartesian, units: Unit = Unit.MM_DEG
    ):
        """
        Generates a rotation...
        - from "rot_mat", if specified
        - from given rotation parameters, if specified
        - or with default values (no translation, no rotation)
        """
        self._rotmat = MathUtilsRotation2d.get_rotmat_from_uservals([val1], definition, units)

    def update_as_CARTESIAN(self, angle: float, units: Unit = Unit.MM_DEG) -> None:
        """
        Updates specified values in specified format.
        """
        # convert internal tvec to value format, in which user wants to update:
        vals_inUpdateFormat = MathUtilsRotation2d.get_uservals_from_rotmat(
            self._rotmat, RotationDefinition2d.Cartesian, units
        )

        vals_inUpdateFormat[0] = angle

        self._rotmat[:, :] = MathUtilsRotation2d.get_rotmat_from_uservals(
            vals_inUpdateFormat, RotationDefinition2d.Cartesian, units
        )  # generate tvec from updated values

    def export_as_CARTESIAN(self, units: Unit = Unit.MM_DEG) -> float:
        """
        Scipy ->  https://math.stackexchange.com/questions/301319/derive-a-rotation-from-a-2d-rotation-matrix.
        """
        vals: list[float] = MathUtilsRotation2d.get_uservals_from_rotmat(
            self._rotmat, RotationDefinition2d.Cartesian, units
        )

        return vals[0]

    def export_as_matrix(self) -> np.ndarray:
        """
        Exports this rotation's matrix representation. This matrix is a new object, changes to it will not reflect on the original object.
        """
        return self._rotmat.copy()

    @staticmethod
    def from_CARTESIAN(rx: float, units: Unit = Unit.MM_DEG) -> Rotation2D:
        """
        Generate a 2D rotation from an input angle rx. A positive angle will move in mathematically positive direction (counter clockwise).

        returns: generated 2D rotation
        """
        ori = Rotation2D(rx, definition=RotationDefinition2d.Cartesian, units=units)
        return ori

    @staticmethod
    def from_rotmat(rotmat: np.ndarray) -> Rotation2D:
        """
        Generates 2D rotation from a 2D rotation matrix. Matrix must be in shape (2x2).

        returns: generated 2D rotation
        """
        if rotmat.shape != (2, 2):
            raise ValueError(f"Invalid rotation matrix shape {rotmat.shape}. Shape must be (4x4)")

        # generate new instance
        result = Rotation2D(0)

        # appy given rotmat
        result._rotmat[:, :] = rotmat

        return result

    def __repr__(self) -> str:
        """
        Generate the string representation of this rotation.
        """
        return self.to_string()

    def __mul__(self, other: Rotation2D | Position2D) -> Rotation2D | Position2D:
        """
        Multiply either with an rotation, resulting in a position; Or multiply with a position, resulting in a scalar.
        """
        if isinstance(other, Rotation2D):
            rotmat = other._rotmat @ self._rotmat
            return Rotation2D.from_rotmat(rotmat)
        elif isinstance(other, Position2D):
            rotmat_result = self._rotmat @ other.get_vector_2x1()
            return Position2D.from_cartesian(*rotmat_result.flatten())
        else:
            raise TypeError("multiplication not a Rotation2D (for multiplication) or a Position2D (cross product)")

    def __eq__(self, other: object) -> bool:
        """
        Check if the given object is equal.
        """
        is_equal = False
        if isinstance(other, Rotation2D):
            is_equal = np.allclose(self._rotmat, other._rotmat)

        return is_equal

    def __hash__(self) -> int:
        """
        Calculate the hash based on the id.
        """
        return hash(id(self))

    def is_close(self, other: Rotation2D, rtol: float = 1e-05, atol: float = 1e-08) -> bool:
        """
        Checks for equality in a range that can be specified with rtol and atol.
        See https://numpy.org/doc/stable/reference/generated/numpy.allclose.html
        """
        is_close = False
        if isinstance(other, Rotation2D):
            is_close = np.allclose(self._rotmat, other._rotmat, rtol=rtol, atol=atol)
        else:
            raise ValueError(f"Comparison target is not in type {type(self)}!")
        return is_close

    def invert(self) -> Rotation2D:
        """
        Returns inverted rotation in given units.
        """
        rotmat_inverted = np.matrix.transpose(self._rotmat)
        return Rotation2D.from_rotmat(rotmat_inverted)

    def copy(self) -> Rotation2D:
        """
        Returns copy of this instance.
        """
        return Rotation2D.from_rotmat(self._rotmat)

    def to_string(
        self, definition: RotationDefinition2d = RotationDefinition2d.Cartesian, units: Unit = Unit.MM_DEG
    ) -> str:
        """
        Generates string representation in given definition and units.
        """
        vals = MathUtilsRotation2d.get_uservals_from_rotmat(self._rotmat, definition=definition, units=units)

        rep = "Rotation: \t"
        if definition == RotationDefinition2d.Cartesian:
            rep += f"\t _Cartesian (rz):   \t{vals[0]:9.3f} {units.get_rotation_unit()} "
        else:
            raise ValueError(f"Target definition {definition} is not supported!")

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


if __name__ == "__main__":
    print("")
    o0 = Rotation2D.from_CARTESIAN(370, Unit.MM_DEG)
    print("o0", o0)
    print("o0 inverted", o0.invert())
    print("export as cylindrical definition (modify all units):")
    print("\tP1:\t", o0.export_as_CARTESIAN(units=Unit.MM_RAD))
    print("\tP2:\t", o0.export_as_CARTESIAN(units=Unit.MM_DEG))
    print("\tP3:\t", o0.export_as_CARTESIAN(units=Unit.M_RAD))
    print("\tP4:\t", o0.export_as_CARTESIAN(units=Unit.M_DEG))

    # o3 = o0 - o1
    # print(o3)

    # Test rotmat
    o = Rotation2D.from_CARTESIAN(50, Unit.MM_DEG)
    print(o._rotmat)
    print(Rotation2D.from_rotmat(o._rotmat)._rotmat)
    assert np.allclose(o._rotmat, Rotation2D.from_rotmat(o._rotmat)._rotmat)
