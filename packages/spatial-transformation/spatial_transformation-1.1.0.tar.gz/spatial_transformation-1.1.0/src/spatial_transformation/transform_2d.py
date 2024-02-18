"""
Contains functions for the conversion of angles to frames and vice versa. Moreover, frames can be plotted.
"""
from __future__ import annotations

from spatial_transformation.definitions import PositionDefinition2d, Unit
from spatial_transformation.position_2d import Position2D
from spatial_transformation.rotation_2d import Rotation2D

import numpy as np
from scipy.spatial.transform import Rotation


class Transform2D:
    """
    Transform2D represents a homogeneous 3x3 transformation matrix.

    Attributes
    ----------
    position : Position2D,
        An element containing 2D axis position value in terms of cartesian cs
    rotation : Rotation,
        An element containing 2D axis rotation value
    tmat : np.ndarray,
        An element containing 3x3 homogenous matrix.

    """

    _position: Position2D
    _rotation: Rotation2D

    _tmat: np.ndarray  # tmat for calculations; note that position and rotation will access this data using numpy views

    def __init__(
        self, position: Position2D | None = None, rotation: Rotation2D | None = None, tmat: np.ndarray | None = None
    ) -> None:
        """
        Generates a coordinate system...
        - from "tmat", if specified
        - from "position" and "rotation", if specified
        - or with default values (no translation, no rotation)
        """
        # tmat can be stored at known memory location
        if tmat is None:
            self._tmat = np.eye(3)
        else:
            self._tmat = tmat

        if position is None:
            # no position argument, so generate new one but specifically use this instance's tmat to store data
            self._position = Position2D(0, 0)
            self._position.set_position_vector_ref_and_adopt_values(self._tmat[0:2, 2])
        else:
            # use given position data and write to own tmat
            self._position = position.copy()  # copy so changes wont reflect on input position
            self._position.set_position_vector_ref_and_keep_own_values(self._tmat[0:2, 2])

        if rotation is None:
            # no rotation argument, so generate new one but specifically use this instance's tmat to store data
            self._rotation = Rotation2D.from_CARTESIAN(0)
            self._rotation.set_rotmat_ref_and_adopt_values(self._tmat[0:2, 0:2])
        else:
            # use given rotation data and write to own tmat
            self._rotation = rotation.copy()  # copy so changes wont reflect on input rotation
            self._rotation.set_rotmat_ref_and_keep_own_values(self._tmat[0:2, 0:2])  # use self._tmat as data storage

    @staticmethod
    def from_tmat(tmat: np.ndarray) -> Transform2D:
        """
        Generates 2D coordinate system from tmat.
        tmat must have shape (3x3) and must define a 2D transformation in the xy-plane!
        """
        # Test if tmat is 3x3
        if tmat.shape != (3, 3):
            raise ValueError("tmat is in shape " + str(tmat.shape) + " but is expected in shape (3, 3)")

        # Test if tmat is valid
        if not (np.all(np.concatenate([tmat[2, 0:2]]) == 0) and tmat[2, 2] == 1):
            raise ValueError("tmat includes scale and/or perspective change, which are not supported yet!")

        sys_result = Transform2D(Position2D.from_cartesian(*tmat[0:2, 2]), Rotation2D.from_rotmat(tmat[0:2, 0:2]))

        return sys_result

    def __mul__(self, other: Transform2D | Position2D) -> Transform2D | Position2D:
        """
        Multiplication with either Transform2D or Position2D. Definition and unit of resulting object will be...
        - the default if both operands are of type Transform2D
        - the definition and unit of the other operand, if it is of type Position2d

        Returns: Resulting position or coordinate system
        """
        if isinstance(other, Transform2D):  # return wrapped 3x3 tmat
            return Transform2D(tmat=(self._tmat @ other._tmat))

        elif isinstance(other, Position2D):  # return wrapped 3x1 tvec
            vector_pos_homogenous = np.array([0, 0, 1], dtype=np.float64).reshape(-1, 1)
            vector_pos_homogenous[0:2] = other.get_vector_2x1()

            vec_pos_homogenous_resulting = self._tmat @ vector_pos_homogenous
            vec_pos_resulting = vec_pos_homogenous_resulting[0:2]

            return Position2D.from_cartesian(*vec_pos_resulting.flatten())
        else:
            msg = f"unsupported operand types for __mul__: '{type(self)}' and '{type(other)}'"
            print(msg)
            raise TypeError(msg)

    def __eq__(self, other: object) -> bool:
        """
        Check if the given object is equal.
        """
        is_equal = False
        if isinstance(other, Transform2D):
            is_equal = np.allclose(self._tmat, other._tmat)
        return is_equal

    def __repr__(self) -> str:
        """
        Generate string representation of coordinate system.
        """
        return self.to_string()

    def invert(self) -> Transform2D:
        """
        Returns inversed coordinate system in new instance.
        """
        rotation_inverted: Rotation2D = self._rotation.invert()
        position_inverted = rotation_inverted * (self._position * (-1))

        if not isinstance(position_inverted, Position2D):
            raise RuntimeError("Multiplication Rotation2D * Position2D did not result in Position2D")

        return Transform2D(position=position_inverted, rotation=rotation_inverted)

    def get_rotation(self) -> Rotation2D:
        """
        Returns the system's rotation. Changes to the rotation will reflect on the system.
        """
        return self._rotation

    def get_position(self) -> Position2D:
        """
        Returns the system's position. Changes to the position will reflect on the system.
        """
        return self._position

    def export_as_matrix(self) -> np.ndarray:
        """
        Returns this transformation as homogenous 3x3 matrix. This matrix is a new object, changes to it will not reflect on the original object.
        """
        tmat_result = np.eye(3)

        tmat_result[0:2, 0:2] = self.get_rotation().export_as_matrix()
        tmat_result[0:2, 2] = self.get_position().export_as_cartesian()

        return tmat_result

    def to_string(self) -> str:
        """
        Generate string representation of coordinate system.
        """
        rep = "Transform2d:\n"
        rep += f"  - {self._position}\n"
        rep += f"  - {self._rotation}\n"

        return rep

    def get_copy(self) -> Transform2D:
        """
        Returns new instance with same properties.
        """
        return Transform2D(position=self.get_position().copy(), rotation=self.get_rotation().copy())

    # Update functions for position ---------------------

    def update_pos_cylindrical(
        self, r: float | None = None, phi: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """Set position values, overwriting existing values."""
        self.get_position().update_cylindrical(r, phi, units)

    def update_pos_cartesian(self, x: float | None = None, y: float | None = None, units: Unit = Unit.MM_DEG) -> None:
        """Set position values, overwriting existing values."""
        self.get_position().update_cartesian(x, y, units)

    # Update functions for rotation

    def update_rot_as_Cartesian(self, angle: float, units: Unit = Unit.MM_DEG) -> None:
        """Set rotation values, overwriting existing values."""
        self.get_rotation().update_as_CARTESIAN(angle, units)


# example
if __name__ == "__main__":
    sys_R = Transform2D(
        Position2D.from_cartesian(0, 1000, Unit.MM_DEG), Rotation2D.from_CARTESIAN(0, units=Unit.MM_DEG)
    )

    sys_R.update_pos_cylindrical(phi=-90, units=Unit.M_DEG)

    print(sys_R)
    print(sys_R._tmat)
    sys_new = Transform2D.from_tmat(sys_R._tmat)
    print(sys_new)
    print(sys_new._tmat)

    sys_R = Transform2D(Position2D.from_cartesian(0, 0, Unit.MM_RAD), Rotation2D.from_CARTESIAN(90, units=Unit.MM_DEG))
    p = Position2D.from_cartesian(1, 0, units=Unit.M_DEG)

    pass
