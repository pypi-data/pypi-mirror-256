"""
Contains an example for using the transform manager.
"""
from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_3d import Transform3D
from spatial_transformation.transform_manager import TransformManager


def example_main() -> None:
    """
    Method shows the basic usage.
    """
    # == Manage Coordinate Systems ===============================================================================
    tm = TransformManager()

    # -- Create Coordinate Systems -------------------------------------------------------------------------------
    # first added system must have root node as parent
    tm.add_system(Transform3D(), "0", tm.get_root_id())

    # the add_coordinate_system() function returns a reference to the coordinate system position
    tm.add_system(Transform3D(position=Position3D.from_cartesian(1, 2, 0)), "A", "0")
    tm.add_system(Transform3D(position=Position3D.from_cartesian(2, 1, 0)), "B", "A")

    # all systems must have already registered systems as parent, this could also be the root node
    tm.add_system(Transform3D(position=Position3D.from_cartesian(-2, 3, 0)), "C", "0")

    # == Manage Positions ========================================================================================

    # -- Adding points -------------------------------------------------------------------------------------------
    # points can be added to a registered system, returning a reference to the position
    tm.add_point(Position3D(2, 1, 0), "p", "C")

    # -- Transforming Points -------------------------------------------------------------------------------------
    print("Transforming points --------------------------------")
    print("p in C: " + str(tm.get_point_pos_in_system("p", "C")))
    print("p in B: " + str(tm.get_point_pos_in_system("p", "B")))

    # coordinate transformations can also be done using the get_position_transformed() method
    p0 = Position3D.from_cartesian(0, 0, 0)  # this point is not registered in a system
    pos_p0_in_B = tm.get_position_transformed(position=p0, sys_from="A", sys_to="B")
    assert pos_p0_in_B == Position3D.from_cartesian(-2, -1, 0)

    # == Moving Coordinate Systems ==============================================================================

    # get system poses
    pose_C = tm.get_system_transform_local("C")
    pose_A = tm.get_system_transform_local("A")

    # move system poses
    pose_C.update_pos_cartesian(-2, 4, 0)  # move from (-2, 3, 0) to (-2, 4, 0)
    pose_A.update_pos_cartesian(2, 2, 0)  # move from (1, 2, 0) to (2, 1, 0)

    # update systems
    # this will move the system, all its child systems and all points
    tm.update_system_transform_local("C", transform=pose_C)
    tm.update_system_transform_local("A", transform=pose_A)

    print("Transforming Systems --------------------------------")
    p_0 = tm.get_point_pos_in_system("p", "0")
    p_C = tm.get_point_pos_in_system("p", "C")
    p_B = tm.get_point_pos_in_system("p", "B")

    print("{0}: " + str(p_0))  # (0, 5, 0)
    print("{C}: " + str(p_C))  # (2, 1, 0)
    print("{B}: " + str(p_B))  # (-4, 2, 0)

    # == Moving Points ============================================================================================

    p = tm.get_point_pos_local("p")

    p.update_cartesian(0, 1, 0)

    tm.update_point_pos_local("p", p)

    print("Modifying Points ------------------------------------")
    print(tm.get_point_pos_local("p"))


def example_change_parent() -> None:
    """
    Method shows how to change the parent of already registered systems/points.
    """
    # == Changing the Parent of a Coordinate System or Point ======================================================

    # TransformManager allows already created branches to be moved to a new branch

    tm = TransformManager()

    # Create the following transformation chain:
    # 0 -> A -> C ==> pC
    # |--> B
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "C", "A")
    tm.add_system(
        Transform3D(Position3D.from_cartesian(1, 1, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)), "B", "0"
    )

    # Add these points
    tm.add_point(Position3D.from_cartesian(1, 1, 0), "pC", "C")

    # move entire chain to new parent ----------------------------------------------------------------------
    # move A and all children to B
    # 0 -> B -> A -> C ==> pC
    tm.update_system_parent("A", "B")

    # move point to new parent
    # 0 -> B -> A -> C
    #      |==> pC
    tm.update_point_parent("pC", "B")


if __name__ == "__main__":
    example_main()
    example_change_parent()
