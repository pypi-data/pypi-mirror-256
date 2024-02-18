"""
Implements the class Position2D.
"""
from __future__ import annotations

import dataclasses
from numbers import Real

from spatial_transformation.definitions import PositionDefinition2d, Unit
from spatial_transformation.utils import MathUtilsPosition, MathUtilsPosition2d

import numpy as np


class Position2D:
    """
    Class for calculation with 2D-positions.

    Attributes
    ----------
        val1, val2(float):
            -> parameter for system
        definition coordinate system type (SystemDefinition):
            -> cartesian [x, y],
            -> cylindrical [r, phi]
        units (UnitDef) :
            -> mm and deg
            -> mm and rad

    """

    _vector_position: np.ndarray[float]

    def __init__(
        self,
        val1: float,
        val2: float,
        definition: PositionDefinition2d = PositionDefinition2d.CARTESIAN,
        units: Unit = Unit.MM_DEG,
    ):
        """
        Generates a position...
        - from given position parameters, if specified
        - or with default values (no translation, no rotation)
        """
        self._vector_position = MathUtilsPosition2d.get_posvec_from_uservals([val1, val2], definition, units)

    @staticmethod
    def from_cartesian(x: float, y: float, units: Unit = Unit.MM_DEG) -> Position2D:
        """
        Cartesian coordinates system with...
        -> x, y
        """
        position = Position2D(x, y, definition=PositionDefinition2d.CARTESIAN, units=units)
        return position

    @staticmethod
    def from_cylindrical(r: float, phi: float, units: Unit = Unit.MM_DEG) -> Position2D:
        """
        Cylindrical coordinates system with...
        -> r as radius in the xy-plane,
        -> phi reference is x-axis and
        """
        position = Position2D(r, phi, definition=PositionDefinition2d.CYLINDRICAL, units=units)
        return position

    def __repr__(self) -> str:
        """
        Generate the 2D- position.
        """
        return self.to_string()

    def __add__(self, other: Position2D) -> Position2D:
        """
        Vector addition V3 = V1 + V2.
        """
        pos_result = self._vector_position + other._vector_position

        return Position2D.from_cartesian(*pos_result)

    def __sub__(self, other: Position2D) -> Position2D:
        """
        Vector subtraction V3 = V1 - V2.
        """
        pos_result = self._vector_position - other._vector_position

        return Position2D.from_cartesian(*pos_result)

    def __mul__(self, other: float) -> Position2D:
        """
        Scalar multiplication, keeping the current units.

        returns: New Position2D instance, keeping definition and units
        """
        # type hint float; instance check Real: https://peps.python.org/pep-0484/#the-numeric-tower

        if isinstance(other, Real):  # Real is parent of float and int
            pos_result = self._vector_position * other

            return Position2D.from_cartesian(*pos_result)
        else:
            raise TypeError("multiplication not float")

    def __truediv__(self, other: float) -> Position2D:
        """
        Scalar division.
        """
        pos_result = self._vector_position / other

        return Position2D.from_cartesian(*pos_result)

    def __eq__(self, other: object) -> bool:
        """
        Test for equality with given object.
        """
        is_equal = False
        if isinstance(other, Position2D):
            is_equal = np.allclose(self.get_vector_2x1(), other.get_vector_2x1())
        return is_equal

    def __hash__(self) -> int:
        """
        Return hash values based on id.
        """
        return hash(id(self))

    def is_close(self, other: Position2D, rtol: float = 1e-05, atol: float = 1e-08) -> bool:
        """
        Check if given position is close to self with relative tolerance :param rtol: and absolute tolerance :param atol:.
        """
        is_close = False
        if isinstance(other, Position2D):
            is_close = np.allclose(self.get_vector_2x1(), other.get_vector_2x1(), rtol=rtol, atol=atol)
        else:
            raise TypeError(f"Target definition is not of type {type(self)}!")

        return is_close

    def get_vector_2x1(self) -> np.ndarray[np.float64]:
        """
        Returns the cartesian column vector in mm: [[x], [y], [z]].
        """
        return self.get_vector_1x2().reshape(-1, 1)  # use reshape because transpose does not work with 1D array

    def get_vector_1x2(self) -> np.ndarray[np.float64]:
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

    def get_distance_to(self, other: Position2D, units: Unit = Unit.MM_DEG) -> float:
        """
        Get distance between given this and given position in specified units.
        """
        distance: float = (
            np.linalg.norm(self._vector_position - other._vector_position) / units.get_translation_factor()
        )
        return distance

    def copy(self) -> Position2D:
        """
        Returns copy of this instance.
        """
        return Position2D.from_cartesian(*self._vector_position)

    def update(
        self,
        definition: PositionDefinition2d,
        val1: float | None = None,
        val2: float | None = None,
        units: Unit = Unit.MM_DEG,
    ) -> None:
        """
        Updates specified values in specified format.
        """
        # convert internal tvec to value format, in which user wants to update:
        vals_inUpdateFormat = MathUtilsPosition2d.get_uservals_from_posvec(self._vector_position, definition, units)

        # write every value that has been specified; leave unspecified values as-is
        if val1 is not None:
            vals_inUpdateFormat[0] = val1
        if val2 is not None:
            vals_inUpdateFormat[1] = val2

        self._vector_position[0:2] = MathUtilsPosition2d.get_posvec_from_uservals(
            vals_inUpdateFormat, definition, units
        )  # generate tvec from updated values

    def update_cartesian(self, x: float | None = None, y: float | None = None, units: Unit = Unit.MM_DEG) -> None:
        """
        Updates specified values in cartesian format.
        """
        self.update(PositionDefinition2d.CARTESIAN, x, y, units)

    def update_cylindrical(self, r: float | None = None, phi: float | None = None, units: Unit = Unit.MM_DEG) -> None:
        """Updates specified values in cylindrical format and applies changes to this object."""
        self.update(PositionDefinition2d.CYLINDRICAL, r, phi, units)

    def export(self, definition: PositionDefinition2d, units: Unit = Unit.MM_DEG) -> tuple[float, float]:
        """
        Calculate position's coordinates using the given representation.
        """
        if isinstance(definition, PositionDefinition2d):
            result: list[float] = MathUtilsPosition2d.get_uservals_from_posvec(
                self._vector_position, definition=definition, units=units
            )
            return (result[0], result[1])
        else:
            raise TypeError(f"Target definition {definition} is not supported!")

    def export_as_cartesian(self, units: Unit = Unit.MM_DEG) -> tuple[float, float]:
        """
        Computes cartesian x, y.
        """
        result: list[float] = MathUtilsPosition2d.get_uservals_from_posvec(
            self._vector_position, definition=PositionDefinition2d.CARTESIAN, units=units
        )

        return (result[0], result[1])

    def export_as_cylindrical(self, units: Unit = Unit.MM_DEG) -> tuple[float, float]:
        """
        Computes cartesian x,y to cylindrical r, phi.
        """
        result: list[float] = MathUtilsPosition2d.get_uservals_from_posvec(
            self._vector_position, definition=PositionDefinition2d.CYLINDRICAL, units=units
        )
        return (result[0], result[1])

    def to_string(
        self, definition: PositionDefinition2d = PositionDefinition2d.CARTESIAN, units: Unit = Unit.MM_DEG
    ) -> str:
        """
        Generate the 2D-position.
        """
        rep = "Position2D: \t"

        vals = MathUtilsPosition2d.get_uservals_from_posvec(self._vector_position, definition, units)

        if definition == PositionDefinition2d.CARTESIAN:
            rep += (
                f"\t cartesian (x, y, z):   \t{vals[0]:9.3f} {units.get_translation_unit()}, "
                f"{vals[1]:9.3f} {units.get_translation_unit()}"
            )
        elif definition == PositionDefinition2d.CYLINDRICAL:
            rep += (
                f"\t cylindrical (r, phi, h):\t{vals[0]:9.3f} {units.get_translation_unit()},"
                f"{vals[1]:9.3f} {units.get_rotation_unit()}"
            )

        else:
            raise ValueError(f"Target definition {definition} is not supported!")

        return rep

    def _set_position_vector_ref(self, tvec: np.ndarray[float], keep_own_values: bool = False) -> None:
        """
        Sets internal vector's memory address to the given vector's address. Modifications to this position instance will be seen at the given addresss.
        """
        # should we include this?

        if keep_own_values:
            # write the instance's values to the memory location before using it

            tvec[0:2] = self._vector_position[:]  # write current values to external memory location
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


if __name__ == "__main__":
    # ---------------------------------------------------------------------------------------- position in 3D
    print("Position, cart, mm: x= 10, y= 10")
    p0 = Position2D(10, 10, definition=PositionDefinition2d.CARTESIAN, units=Unit.MM_DEG)
    print("P0: cartesian:   \t", p0.export_as_cartesian(units=Unit.MM_DEG))
    print("P0: cartesian:   \t", p0.export_as_cartesian(units=Unit.MM_RAD))
    print("P1: cartesian:   \t", p0.export_as_cartesian(units=Unit.M_DEG))
    print("P2: cartesian:   \t", p0.export_as_cartesian(units=Unit.M_RAD))
    print()
    # -----------------------------------------------------
    print("Position, cart, mm: x= 10, y= 10")
    p1 = Position2D(10, 45, definition=PositionDefinition2d.CYLINDRICAL, units=Unit.MM_DEG)
    print("p1: cylindrical:   \t", p1.export_as_cylindrical(units=Unit.MM_DEG))
    print("p1: cylindrical:   \t", p1.export_as_cylindrical(units=Unit.MM_RAD))
    print("P1: cylindrical:   \t", p1.export_as_cylindrical(units=Unit.M_DEG))
    print("P2: cylindrical:   \t", p1.export_as_cylindrical(units=Unit.M_RAD))
    print("-----------------------------------------------------")
    d1 = p0 - p1
    print(d1)
    d2 = p0 - p1
    print(d2)
    d3 = p0 - p1
    print(d3)
    d4 = p0 - p1
    print(d4)
    print("-----------------------------------------------------")

    p5 = Position2D.from_cartesian(0, 0, Unit.M_DEG)
