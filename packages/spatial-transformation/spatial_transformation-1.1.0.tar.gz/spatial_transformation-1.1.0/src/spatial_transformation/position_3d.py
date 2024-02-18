"""
Contains functions for the conversion of angles to frames and vice versa. Moreover, frames can be plotted.
"""
from __future__ import annotations

from numbers import Real

from spatial_transformation.definitions import PositionDefinition3d, Unit
from spatial_transformation.utils import MathUtilsPosition, MathUtilsPosition3d

import numpy as np


class Position3D:
    """
    3D-position class for spatial transformation.

    Attributes
    ----------
        _position_vector for internal calculation:
            -> cartesian [x, y, z] in [mm]

    Usage
    -----
    create by a specific definition of the coordinate system type (SystemDefinition):
        from_cartesian    -> cartesian [x, y, z],
        from_cylindrical  -> cylindrical [r, phi, h],
        from_spherical    -> spherical [r, theta, phi]

    and units (UnitDef) :
            -> mm and deg     -> STANDARD
            -> mm and rad
            -> m and deg
            -> m and rad

    """

    _vector_position: np.ndarray[float]  # x, y, z values in cartesian mm representation

    def __init__(
        self,
        val1: float,
        val2: float,
        val3: float,
        definition: PositionDefinition3d = PositionDefinition3d.CARTESIAN,
        units: Unit = Unit.MM_DEG,
    ):
        """
        Generates a cartesian position in standard units (mm) from...
        - from given position parameters (definition)
        - in given units (units)
        """
        vals = np.array([val1, val2, val3], dtype=np.float64)

        self._vector_position = np.array([0, 0, 0], dtype=np.float64)
        self._vector_position[0:3] = MathUtilsPosition3d.get_posvec_from_uservals(vals, definition, units)

    @staticmethod
    def from_cartesian(x: float, y: float, z: float, units: Unit = Unit.MM_DEG) -> Position3D:
        """
        Cartesian coordinates system with...
            -> x, y, z
        """
        position = Position3D(x, y, z, definition=PositionDefinition3d.CARTESIAN, units=units)
        return position

    @staticmethod
    def from_cylindrical(r: float, phi: float, h: float, units: Unit = Unit.MM_DEG) -> Position3D:
        """
        Cylindrical coordinates system with...
            -> r as radius in the xy-plane,
            -> phi reference is x-axis  [-180°,180°] and
            -> h as height from xy-plane
        """
        position = Position3D(r, phi, h, definition=PositionDefinition3d.CYLINDRICAL, units=units)
        return position

    @staticmethod
    def from_spherical(r: float, theta: float, phi: float, units: Unit = Unit.MM_DEG) -> Position3D:
        """
        Spherical coordinates system with...
            -> r as radius
            -> theta reference is z-axis from [0,180°] and
            -> phi reference is x-axis from [-180°,180°]
        """
        position = Position3D(r, theta, phi, definition=PositionDefinition3d.SPHERICAL, units=units)
        return position

    @staticmethod
    def from_opencv_tvec(tvec: np.ndarray[np.float64]) -> Position3D:
        """
        Return new Position3D instance that has been generated from a opencv tvec (tvec -> cartesian, mm).
        """
        # TODO Are these actually compatible? Does tvec from opencv equal a cartesian vector in MM?

        # generate new instance
        result = Position3D.from_cartesian(*tvec)

        return result

    def __repr__(self) -> str:
        """
        Represent in cartesian form x, y, z and [mm].
        """
        return self.to_string()

    def __add__(self, other: Position3D) -> Position3D:
        """
        Vector addition V3 = V1 + V2.
        """
        position_vec = self._vector_position + other._vector_position
        return Position3D.from_cartesian(*position_vec)

    def __sub__(self, other: Position3D) -> Position3D:
        """
        Vector subtraction V3 = V1 - V2.
        """
        position_vec = self._vector_position - other._vector_position

        return Position3D.from_cartesian(*position_vec)

    def __mul__(self, other: float | Position3D) -> Position3D:
        """
        Multiplication...
         -> scalar (keeps definition)
         -> cross product (returns same units/definition in case units/definition of operands match, else returns default definition)
        """
        # type hint float; instance check Real: https://peps.python.org/pep-0484/#the-numeric-tower

        if isinstance(other, Real):  # Real is parent of float and int; type hint float for mypy
            position_vec = self._vector_position * other
            return Position3D.from_cartesian(*position_vec)
        elif isinstance(other, Position3D):
            position_vec = np.cross(self._vector_position, other._vector_position)
            return Position3D.from_cartesian(*position_vec)
        else:
            raise TypeError("multiplication factor not a scalar (for multiplication) or a Position3D (cross product)")

    def __truediv__(self, other: Real) -> Position3D:
        """
        Scalar division.
        """
        position_vec = self._vector_position / other

        return Position3D.from_cartesian(*position_vec)

    def __eq__(self, other: object) -> bool:
        """
        Check if given object is equal to self.
        """
        equal = False
        if isinstance(other, Position3D):
            equal = np.allclose(self.get_vector_3x1(), other.get_vector_3x1())
        return equal

    def __hash__(self) -> int:
        """
        Calculate hash from id.
        """
        return hash(id(self))

    def is_close(self, other: Position3D, rtol: float = 1e-05, atol: float = 1e-08) -> bool:
        """
        Check if given position is close to self with relative tolerance :param rtol: and absolute tolerance :param atol:.
        """
        is_close = False
        if isinstance(other, Position3D):
            is_close = np.allclose(self.get_vector_3x1(), other.get_vector_3x1(), rtol=rtol, atol=atol)
        return is_close

    def get_vector_3x1(self) -> np.ndarray[np.float64]:
        """
        Returns the cartesian column vector in mm: [[x], [y], [z]].
        """
        return self.get_vector_1x3().reshape(-1, 1)  # use reshape because transpose does not work with 1D array

    def get_vector_1x3(self) -> np.ndarray[np.float64]:
        """
        Returns the cartesian row vector in mm: [x, y, z].
        """
        return self._vector_position.copy()

    def get_absolute_value(self, units: Unit = Unit.MM_DEG) -> float:
        """
        Returns the absolute_value of the cartesian vector in mm: [x, y, z].
        """
        absolute_value: float = np.linalg.norm(self._vector_position) / units.get_translation_factor()
        return absolute_value

    def get_distance_to(self, other: Position3D, units: Unit = Unit.MM_DEG) -> float:
        """
        Get distance between given this and given position in specified units.
        """
        distance_to: float = (
            np.linalg.norm(self._vector_position - other._vector_position) / units.get_translation_factor()
        )
        return distance_to

    def copy(self) -> Position3D:
        """
        Returns copy of this instance.
        """
        return Position3D.from_cartesian(*self._vector_position)

    def update(
        self,
        definition: PositionDefinition3d,
        val1: float | None = None,
        val2: float | None = None,
        val3: float | None = None,
        units: Unit = Unit.MM_DEG,
    ) -> None:
        """
        Updates specified values in specified format.
        """
        # convert internal tvec to value format in which user wants to update:
        vals_inUpdateFormat = MathUtilsPosition3d.get_uservals_from_posvec(self._vector_position, definition, units)

        # write every value that has been specified; leave unspecified values as-is
        if val1 is not None:
            vals_inUpdateFormat[0] = val1
        if val2 is not None:
            vals_inUpdateFormat[1] = val2
        if val3 is not None:
            vals_inUpdateFormat[2] = val3

        # write back new values
        self._vector_position[0:3] = MathUtilsPosition3d.get_posvec_from_uservals(
            vals_inUpdateFormat, definition, units
        )  # generate tvec from updated values

    def update_cartesian(
        self, x: float | None = None, y: float | None = None, z: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """
        Updates specified values in cartesian format.
        """
        self.update(PositionDefinition3d.CARTESIAN, x, y, z, units)

    def update_cylindrical(
        self, r: float | None = None, phi: float | None = None, z: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """
        Updates specified values in cylindrical format and applies changes to this object.
        """
        self.update(PositionDefinition3d.CYLINDRICAL, r, phi, z, units)

    def update_spherical(
        self, r: float | None = None, theta: float | None = None, phi: float | None = None, units: Unit = Unit.MM_DEG
    ) -> None:
        """
        Updates specified values in spherical format and applies changes to this object.
        """
        self.update(PositionDefinition3d.SPHERICAL, r, theta, phi, units)

    # export routines -----------------------------------------------------------------------------------------------------

    def export(self, target_definition: PositionDefinition3d, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Calculate position's coordinates using the given representation.
        """
        if target_definition == PositionDefinition3d.CARTESIAN:
            return self.export_as_cartesian(units=units)
        elif target_definition == PositionDefinition3d.CYLINDRICAL:
            return self.export_as_cylindrical(units=units)
        elif target_definition == PositionDefinition3d.SPHERICAL:
            return self.export_as_spherical(units=units)
        else:
            raise ValueError(f"Target definition {target_definition} is not supported!")

    def export_as_cartesian(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Computes cartesian x, y, z.
        """
        result: list[float] = MathUtilsPosition.get_uservals_from_posvec_CARTESIAN(self._vector_position, units=units)

        return (result[0], result[1], result[2])  # guarantees correct types

    def export_as_cylindrical(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Computes cartesian x,y,z to cylindrical r, phi, h.
        """
        result = MathUtilsPosition.get_uservals_from_posvec_CYLINDRICAL(self._vector_position, units=units)
        return (result[0], result[1], result[2])  # guarantees correct types

    def export_as_spherical(self, units: Unit = Unit.MM_DEG) -> tuple[float, float, float]:
        """
        Computes cartesian x, y, z to cylindrical r, theta, phi.
        """
        result = MathUtilsPosition.get_uservals_from_posvec_SPHERICAL(self._vector_position, units=units)
        return (result[0], result[1], result[2])  # guarantees correct types

    def to_string(
        self, definition: PositionDefinition3d = PositionDefinition3d.CARTESIAN, units: Unit = Unit.MM_DEG
    ) -> str:
        """
        Generate the 3D-position.
        """
        rep = "Position3D: \t"

        vals = MathUtilsPosition3d.get_uservals_from_posvec(self._vector_position, definition=definition, units=units)

        if definition == PositionDefinition3d.CARTESIAN:
            rep += (
                f"\t cartesian (x, y, z):   \t{vals[0]:9.3f} {units.get_translation_unit()}, "
                f"{vals[1]:9.3f} {units.get_translation_unit()}, "
                f"{vals[2]:9.3f} {units.get_translation_unit()}"
            )
        elif definition == PositionDefinition3d.CYLINDRICAL:
            rep += (
                f"\t cylindrical (r, phi, h):\t{vals[0]:9.3f} {units.get_translation_unit()},"
                f"{vals[1]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[2]:9.3f} {units.get_translation_unit()}"
            )
        elif definition == PositionDefinition3d.SPHERICAL:
            rep += (
                f"\t spherical (r, theta, phi):\t{vals[0]:9.3f} {units.get_translation_unit()},"
                f"{vals[1]:9.3f} {units.get_rotation_unit()}, "
                f"{vals[2]:9.3f} {units.get_rotation_unit()}"
            )

        return rep

    def _set_position_vector_ref(self, tvec: np.ndarray[float], keep_own_values: bool = False) -> None:
        """
        Sets internal vector's memory address to the given vector's address. Modifications to this position instance will be seen at the given addresss.
        """
        # should we include this?

        if keep_own_values:
            # write the instance's values to the memory location before using it

            tvec[:] = self._vector_position[0:3]  # write current values to external memory location
            self._vector_position = tvec  # now use external memory location as internal
        else:
            # write the memory location's value to this instance

            self._vector_position = tvec

    def set_position_vector_ref_and_keep_own_values(self, tvec: np.ndarray[float]) -> None:
        """
        Use given vector to store data but first write this instance's values to the given vector.

        Modifications to this position instance then will be seen at the given addresss.
        """
        self._set_position_vector_ref(tvec=tvec, keep_own_values=True)

    def set_position_vector_ref_and_adopt_values(self, tvec: np.ndarray[float]) -> None:
        """
        Use given vector to store data and update this instances own values from the given vector.

        Modifications to this position instance then will be seen at the given addresss.
        """
        self._set_position_vector_ref(tvec=tvec, keep_own_values=False)
