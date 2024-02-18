"""
Contains an example for usage of base classes like Position3D, Rotation3D or Transform3D.
"""
from spatial_transformation.definitions import (
    PositionDefinition2d,
    PositionDefinition3d,
    RotationDefinition2d,
    RotationDefinition3d,
    Unit,
)
from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_3d import Transform3D
from spatial_transformation.transform_manager import TransformManager

if __name__ == "__main__":
    """
    Transform library contains 3 base types:
        - Position3D    .. represents a 3D position as a 3D vector
        - Rotation3D    .. represents a 3D rotation as a 3x3 matrix
        - Transform3D   .. combines a position and a rotation as 4x4 matrix
    """
    """
    Positions can be created in various coordinate system definitions with various units.
    """
    p0 = Position3D.from_cartesian(0, 1, 2, Unit.MM_DEG)
    p0 = Position3D.from_cylindrical(0, 1, 2, Unit.M_RAD)
    p0 = Position3D.from_spherical(1, 0, 0, Unit.M_DEG)

    """
    Positions can be added / substracted and multiplied by with a scalar.
    """
    print(p0 + p0)
    print(p0 * p0)  # cross product
    print(p0 * 2)

    """
    Rotations can also be created in different systems.
    """
    R0 = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)
    R0 = Rotation3D.from_EULER_INTRINSIC_ZYX(90, 0, 0)
    R0 = Rotation3D.from_AXIS_ANGLE(0, 0, 1, 90)

    """
    Both can be updated using any definition that can be used for creation.
    """
    p0.update_cartesian(x=90)
    R0.update_as_QUATERNION(0.2, 0.4)

    """
    Transform3D can be updated using equivalent methods.
    """
    trans = Transform3D()

    trans.update_pos_cartesian(x=90)
    trans.update_rot_as_QUATERNION(0.2, 0.4)

    """ Viewing the Base Objects ================================================================================
    Rotation and Position can be exported to a given definition. Transform objects allow access to their internal
    value with get_position() and get_orientation()
    """
    print(p0.export_as_cartesian())
    print(R0.export_as_EULER_INTRINSIC_XYZ())
    print(trans.get_position().export_as_cartesian())

    """ Doing Transformation Operations ========================================================================= """
    """
    Transformation objects can be used for rotating/translating points.
    """
    p0_inA = Position3D.from_cartesian(0, 0, 0)
    trans_0_A = Transform3D(Position3D.from_cartesian(1, 0, 0))  # {A} is transformed with x = 1 mm with respect to {0}

    p0_in0 = trans_0_A * p0_inA  # position of p0_inA when seen from {0}, {0} is moved with x = 1 mm
    print(p0_in0)
