"""
Define the units for spatial transformation.

    -> rotation with the base:     rad       and additional:      deg, gon
    -> translation with the base:   mm       and additional:      m,
"""
import dataclasses
from enum import Enum, IntEnum

import numpy as np


class PositionDefinition2d(IntEnum):
    """
    Definition of coordinate system for a position.
        1 = cartesian   -> x,   y
        2 = cylindrical -> r, phi
    """

    # definition in 2D space:
    CARTESIAN = 1  # x,   y  ->  position x, y    #
    CYLINDRICAL = 2  # r, phi  ->  radius, phi = angle to the x-axis (in xy-plane)


class PositionDefinition3d(IntEnum):
    """
    Definition of coordinate system for a position.
        1 = cartesian   -> x,   y,     z
        2 = cylindrical -> r, phi,     h
        3 = spherical   -> r, theta, phi
    """

    # definition in 3D space:
    CARTESIAN = 1  # x,   y,     z  ->  position x, y, z
    #                                                                                        https://en.wikipedia.org/wiki/Cartesian_coordinate_system
    CYLINDRICAL = 2  # r, phi,     h  ->  radius, phi = angle to the x-axis (in xy-plane), h= height over xy-plane (z)
    #                                                                                            https://en.wikipedia.org/wiki/Polar_coordinate_system
    SPHERICAL = 3  # r, theta, phi  ->  radius, theta = angle to z-axis, phi = angle to the x-axis (in xy-plane)
    #                                                                                        https://en.wikipedia.org/wiki/Spherical_coordinate_system


class RotationDefinition2d(IntEnum):
    """
    Definition of coordinate system for rotations.
        1 = cartesian   -> alpha,
    """

    # definition in 2 space:
    Cartesian = 1  # alpha -> rotation around the z-axis
    #                                                                       - https://en.wikipedia.org/wiki/Cartesian_coordinate_system#Two_dimensions


class RotationDefinition3d(IntEnum):
    """
    Type of rotation representations.
        0 = Rotation Matrix  -> M[3x3]
        1 = Rodrigues  -> axis [x, y, z], rotation angle theta is the vector's norm
        2 = Quaternion -> [a, b, c, d]
        3 = Axis-Angle -> define rot axis [x, y, z] and rotation angle [theta]
        4 = antenna ->
        5 = Euler's angles   -> alpha, beta, gamma with rotation sequence
        ...
    """

    # RotationMatrix = 0
    Rodrigues = 1
    Quaternion = 2  # a, b, c, d      ->
    #                                           -> https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    Axis_Angle = 3  # rot axis [x, y, z] and rotation angle [theta]
    #                                           -> https://danceswithcode.net/engineeringnotes/quaternions/quaternions.html
    Antenna = 4  # ->
    #                                     -> https://de.wikipedia.org/wiki/Eulersche_Winkel#Beschreibung_durch_intrinsische_Drehungen -> zy'x'' = XYZ
    EULER_INTRINSIC_XYZ = 5  # intrinsic rotations Euler's angles   -> alpha, beta, gamma with rotation sequence
    EULER_INTRINSIC_ZYX = 6  # intrinsic rotations Euler's angles   -> alpha, beta, gamma with rotation sequence
    # -> https://docs.scipy.org/doc/scipy/reference/spatial.transform.html
    # -> https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html
    # Scipy -> 'XYZ' = intrinsisch, 'xyz' = extrinsisch


class _TranslationUnit(Enum):
    """
    Unit of translation with multiplier to calculation standard mm.
     -> mm =  m * multiplier to mm .value
    """

    MM = 1
    M = 1000


class _RotationUnit(Enum):
    """
    Unit of rotation with multiplier to calculation standard rad.
        -> angle_in_RAD =  DEG * angle_in_DEG.value
    """

    RAD = 1
    DEG = np.pi / 180
    GON = np.pi / 200


@dataclasses.dataclass()
class _TransformationUnits:
    """
    Combined units for translation and rotation with the representation standard.
        -> mm and rad
    """

    trans: _TranslationUnit = _TranslationUnit.MM
    rot: _RotationUnit = _RotationUnit.DEG


class Unit(Enum):
    """
    Defined set of translation and rotation units.
        - mm with rad and deg
        - m  with rad and deg
    """

    MM_RAD = _TransformationUnits(trans=_TranslationUnit.MM, rot=_RotationUnit.RAD)
    MM_DEG = _TransformationUnits(trans=_TranslationUnit.MM, rot=_RotationUnit.DEG)
    M_RAD = _TransformationUnits(trans=_TranslationUnit.M, rot=_RotationUnit.RAD)
    M_DEG = _TransformationUnits(trans=_TranslationUnit.M, rot=_RotationUnit.DEG)

    def __str__(self) -> str:
        """
        Returns this unit's string representation.
        """
        if self.name == "MM_RAD":
            return "units: mm and rad"
        elif self.name == "MM_DEG":
            return "units: mm and deg"
        elif self.name == "M_RAD":
            return "units: m and rad"
        else:
            return "units: m and deg"

    def get_rotation_factor(self) -> float:
        """
        Returns the multiplier to the base unit (rad).
        -> current value * rotation_factor = rad
        """
        st = self.value.rot.value
        return st

    def get_translation_factor(self) -> float:
        """
        Returns the multiplier to the base unit (mm).
        -> current value * rotation_factor = mm
        """
        st = self.value.trans.value
        return st

    def get_rotation_unit(self) -> str:
        """
        Returns the current rotation unit as string.
        """
        name = self.value.rot.name
        if name == "DEG":
            return "deg"
        elif name == "RAD":
            return "rad"
        else:
            return "gon"

    def get_translation_unit(self) -> str:
        """
        Returns the current translation unit as string.
        """
        name = self.value.trans.name
        if name == "MM":
            return "mm"
        else:
            return "m"


if __name__ == "__main__":
    unit = Unit.M_DEG

    print(
        "rotation: \t unit:",
        unit.get_rotation_unit(),
        "\tfactor to rad ",
        unit.get_rotation_factor(),
        "\n",
        "translation: \t unit:",
        unit.get_translation_unit(),
        "\tfactor to mm: ",
        unit.get_translation_factor(),
    )

    print(unit)
