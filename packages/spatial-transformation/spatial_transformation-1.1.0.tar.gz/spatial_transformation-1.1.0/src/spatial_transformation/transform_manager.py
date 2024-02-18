"""
The transform_manager module implements the TransformManager class.

See :doc:`/usage/transform_manager`.
"""
from __future__ import annotations

from spatial_transformation.definitions import PositionDefinition2d, PositionDefinition3d, Unit
from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_3d import Transform3D
from spatial_transformation.transform_utils import CoordinateSystem3D, Point3D


class TransformManager:
    """
    The TransformManager stores a network of coordinate systems and can calculate homogenous transformation matrices between them. The TransformManager also supports storing points in a coordinate system which can also be transformed homogeneously.

    CoordinateSystems and Points are stored and accessed by an unique string id. Modifications can only be done using the TransformationManager class directly.


    Add coordinate systems with
        add_system(transform: Transform3D, new_system: str, parent: str)
    Modify coordinate systems with
        update_system_parent(id_system: str, id_parent_new: str)
        update_system_transform_local(id_system: str, position: Position3D | None = None, rotation: Rotation3D | None = None, transform: Transform3D | None = None)

    Add points with:
        add_point(position: Position3D, id_point: str, id_parent: str)
    Modify points with
        update_point_parent(id_point: str, id_parent_new: str)
        update_point_pos_local(id_point: str, position: Position3D)

    Get transformation with
        get_transform(id_base: str, id_target: str)

        get_system_transform_global(id_system: str)
        get_system_transform_local(id_system: str)
        get_system_transform_relative(id_system: str, sys_base: str)
    """

    # Storage ---------------------------------------------------------------------
    _system_for_id: dict[str, CoordinateSystem3D]  # coordinate systems additionalyl store list of added points
    _point_for_id: dict[str, Point3D]

    # Constants -------------------------------------------------------------------
    _ROOT_NODE: CoordinateSystem3D = CoordinateSystem3D("__root__", None, None)

    def __init__(self) -> None:
        """
        Initialize internal structures.
        """
        # self._system_for_point = BiMappedStorage(Point3D, str)

        self._system_for_id = dict()
        self._point_for_id = dict()

        self._system_for_id[self.get_root_id()] = TransformManager._ROOT_NODE

    # Point Management ----------------------------------------------------------------------------------------------

    def add_point(self, position: Position3D, id_point: str, id_parent: str) -> None:
        """
        Binds the given position to the specified system. The specified system must have been defined.

        :param position: The point's position.
        :param id_point: The point's id. The point's id must not have
            been defined.
        :param id_parent: The parent system's id. The parent system must
            have already been defined. If None, then the root system is
            used.
        :return: A reference to the given point.
        """
        position_to_add = position.copy()
        point_to_add = Point3D(id_system_base=id_parent, id=id_point, position=position_to_add)

        self._point_for_id[id_point] = point_to_add
        self.__get_system(id_parent).add_point(point_to_add)

    def remove_point(self, id_point: str) -> None:
        """
        Removes given point.
        """
        point = self.__get_point(id_point)
        system_base = self.__get_system(point.id_system_base)

        system_base.remove_point(id_point)  # remove from system
        del self._point_for_id[id_point]  # remove from global storage

    def __get_point(self, id_point: str) -> Point3D:
        """
        Returns point by id using the internal type representation.
        """
        if id_point not in self._point_for_id:
            raise KeyError(f"Point id {id_point} is not known.")

        return self._point_for_id[id_point]

    def get_point_pos_local(self, id_point: str) -> Position3D:
        """
        Returns the given point's position with reference to its parent system.
        """
        return self.__get_point_position_ref(id_point).copy()

    def get_point_pos_global(self, id_point: str) -> Position3D:
        """
        Returns the given point's position with reference to the root system.
        """
        return self.get_point_pos_in_system(id_point, self.get_root_id())

    def get_point_pos_in_system(self, id_point: str, id_sys: str) -> Position3D:
        """
        Calculates given point's point in the given system. The point's initial system must be known.

        :return: The point's position in the given system.

        Raises: KeyError if id_sys is not known.
        """
        id_base = self.get_point_parent(id_point)
        transformation = self.get_transform(id_sys, id_base)

        pos_result = transformation * self.get_point_pos_local(id_point)

        if isinstance(pos_result, Position3D):
            return pos_result
        else:
            raise RuntimeError("Multiplication Transform3D * Position3D did not result in Position3D")

    def __get_point_position_ref(self, id_point: str) -> Position3D:
        """
        Returns the given point's position as reference.

        Changes to this reference will reflect on the original point.
        """
        return self.__get_point(id_point).position

    def update_point_pos_local(self, id_point: str, position: Position3D) -> None:
        """
        Sets the given point's position to the given value with reference to the parent.

        The given position will be copied, the reference will be lost.
        """
        values_cartesian: list[float] = list(position.export_as_cartesian(Unit.MM_DEG))

        self.__get_point(id_point).position.update_cartesian(
            values_cartesian[0], values_cartesian[1], values_cartesian[2], units=Unit.MM_DEG
        )

    def update_point_parent(self, id_point: str, id_parent_new: str) -> None:
        """
        Changes the given point's basis. The given point's coordinates will then be with reference to the new system and the point will behave as child of {id_new_parent}.

        :param id_point: The id of the target point
        :param id_new_system: The id of the new parent system
        """
        id_parent_old = self.get_point_parent(id_point)

        pos_point_new = self.get_point_pos_in_system(id_point, id_parent_new)  # calc point position in new system

        self.__get_system(id_parent_old).remove_point(id_point)  # remove point from old system
        self.add_point(pos_point_new, id_point, id_parent_new)  # add point to new system

    def get_point_parent(self, id_point: str) -> str:
        """
        Returns: System that has been registered for the given point.

        Raises: KeyError if id_sys is not known.
        """
        return self.__get_point(id_point).id_system_base

    def __get_points_in_system(self, id_system: str) -> list[Point3D]:
        """
        Returns: List of points in given system.
        """
        return self.__get_system(id_system).get_points()

    def get_points_with_parent(self, id_system: str) -> list[str]:
        """
        Returns list of point ids in the given system.
        """
        return self.__get_system(id_system).get_point_ids()

    def get_points_all(self) -> list[str]:
        """
        Returns list of all registered points.

        :return: list of all registered point ids
        """
        return [point.id for point in self._point_for_id.values()]

    # Point Utilities ----------------------------------------------------------------------------------------------

    def get_point_distance(self, id_point_1: str, id_point_2: str, units: Unit = Unit.MM_DEG) -> float:
        """
        Transforms given points into the same system and calculates their distance.

        Returns: Distance between given points.
        """
        # find transform between 2 points so we can put them into the same base
        T_12 = self.get_transform(self.get_point_parent(id_point_1), self.get_point_parent(id_point_2))

        # convert to same base
        p_1_in_sys1 = self.__get_point(id_point_1).position
        p_2_in_sys1 = T_12 * self.__get_point(id_point_2).position

        if isinstance(p_2_in_sys1, Position3D):
            return p_1_in_sys1.get_distance_to(p_2_in_sys1, units)
        else:
            raise RuntimeError("Position of point 2 is not of type Position3D")

    def get_position_transformed(self, position: Position3D, sys_from: str, sys_to: str) -> Position3D:
        """
        Transforms the given point from the given base system in to the given target system.

        This assumes that point's coordinates are given with reference to {sys_from} and that the transformed point's
        coordinates should be given with reference to {sys_to}.

        Returns: Copy of given point after being transformed from base to target system.
        """
        transformation = self.get_transform(sys_to, sys_from)

        if not isinstance(position, Position3D):
            raise TypeError("Argument 'position' must be of type Position3D")

        result = transformation * position

        if isinstance(result, Position3D):
            return result
        else:
            raise RuntimeError("Result is not of type Position3D")

    # coordinate system management --------------------------------------------------------------------------

    def has_transformation(self, id_from: str, id_to: str) -> bool:
        """
        Checks if a transformation between id_from and id_to has been registered.
        """
        return (id_from in self._system_for_id) and (id_to in self._system_for_id)

    def __get_system(self, id_system: str) -> CoordinateSystem3D:
        """
        Returns coordinate system by given system id.

        :param system: A registered system identifier.
        """
        if id_system not in self._system_for_id:
            raise KeyError(f"System for id {id_system} is not known!")

        return self._system_for_id[id_system]

    def get_system_transform_local(self, id_system: str) -> Transform3D:
        """
        Returns the given coordinate system's pose with reference to its parent as copy.

        :param system: A registered system identifier.
        """
        return self.__get_system(id_system).get_transform_from_parent().copy()

    def get_system_transform_global(self, id_system: str) -> Transform3D:
        """
        Returns the given coordinate system's pose with reference to the root node as copy.

        :param system: A registered system identifier.
        """
        return self.__get_system(id_system).get_transform_from_root().copy()

    def get_transform(self, id_base: str, id_target: str) -> Transform3D:
        """
        Calculates and returns transformation chain for transforming a point from 'id_base' into 'id_target'. The resulting transform T from system 'base' to system 'target' can be used as follows.

        p_base = T_base_target * p_target

        :returns: Resulting transformation or None if no transformation
            has been found
        """
        return self.get_system_transform_relative(id_target, id_base)

    def get_system_transform_relative(self, id_system: str, sys_base: str) -> Transform3D:
        """
        Calculates and returns transformation of {sys_target} with reference to {sys_base}.

        The resulting transform T from system 'base' to system 'target' can be used as follows.

        p_base = T_base_to * p_target

        :returns: Resulting transformation or None if no transformation
            has been found
        """
        # calculate transform from transform to root ------------------------------------------------------------
        # base = A; target = B; root = 0;
        # first id is superscripted, second id is subscripted: T_A_B
        sys_root_base = self.__get_system(sys_base).get_transform_from_root()  # T_0_A
        sys_root_target = self.__get_system(id_system).get_transform_from_root()  # T_0_B

        result = sys_root_base.invert() * sys_root_target  # T_0_A.inv() * T_0_B = T_A_0 * T_0_B = T_A_B

        if isinstance(result, Transform3D):
            return result
        else:
            raise RuntimeError("Result is not of type Transform3D.")

    def get_system_parent(self, id_system: str) -> str:
        """
        Returns the given system's parent id.
        """
        return self.__get_system(id_system).get_parent_id()

    def update_system_parent(self, id_system: str, id_parent_new: str) -> None:
        """
        Changes the given point's basis. The given point's coordinates will then be with reference to the new system and the point will behave as child of {id_new_parent}.

        :param id_system: The id of the target point
        :param id_new_system: The id of the new parent system
        """
        # calculate system pose in new system ---------------------------------------------------------------------------
        id_parent_old = self.get_system_parent(id_system)  # 1. get old parent

        T_new_old = self.get_transform(id_parent_new, id_parent_old)  # 2. get transformation to new parent

        pose_system_new = T_new_old * self.get_system_transform_local(id_system)  # 3. calc system pose in new system

        if not isinstance(pose_system_new, Transform3D):
            raise RuntimeError("Multiplication of Transform3D and Transform3D did not result in Transform3D.")

        # update system references in memory ----------------------------------------------------------------------------

        # 1. update target system references
        system_to_move = self.__get_system(id_system)
        system_to_move.set_transform(pose_system_new)
        system_to_move.set_parent(self.__get_system(id_parent_new))

        # 2. update references in global storage
        self.__get_system(id_parent_old).remove_child(id_system)  # remove system from old system
        self.__get_system(id_parent_new).add_child(system_to_move)

    def add_system(self, transform: Transform3D, new_system: str, parent: str) -> None:
        """
        Add new coordinate system and choose an existing system as parent.

        :param transform: The system's pose with reference to its parent
            system (T_parent_newsystem)
        :param new_system: The id of the new coordinate system.
        :param parent: The parent coordinate system's id. If left None,
            the root system will be used.
        :return: A copy of the created system's transform from parent.
        """
        # check if systems exist -------------------------------------------------------------------
        if new_system in self._system_for_id:
            raise ValueError(f"Coordinate system id {new_system} has already been registered!")

        # build new system and add to manager ------------------------------------------------------
        sys_parent = self.__get_system(parent)

        sys_new = CoordinateSystem3D(new_system, sys_parent, transform.copy())
        self._system_for_id[sys_new.id] = sys_new

        # add system to its parent
        sys_parent.add_child(sys_new)

    def remove_system(self, id_system: str) -> None:
        """
        Removes the given system, all its child systems and all its child points.
        """
        list_child_systems = self.get_systems_with_parent(id_system)

        # remove all child systems and their points ---------------------------------------------
        for child_system in list_child_systems:
            self.remove_system(child_system)

        # remove target system and its points ---------------------------------------------------
        # remove target system's points (shallow)
        for child_point in self.__get_system(id_system).get_points():
            del self._point_for_id[child_point.id]  # remove from global storage

        # remove target system
        del self._system_for_id[id_system]

    def get_systems_all(self) -> list[str]:
        """
        Returns a list of all defined coordinate systems.

        :return: list of all coordinate system ids
        """
        return [point.id for point in self._system_for_id.values()]

    def get_systems_with_parent(self, id_parent: str) -> list[str]:
        """
        Returns a list of all coordinate systems with parent :param id_parent:.

        :return: list of all coordinate system ids
        """
        return [system.id for system in self.__get_system(id_parent).get_child_systems()]

    def update_system_transform_local(
        self,
        id_system: str,
        position: Position3D | None = None,
        rotation: Rotation3D | None = None,
        transform: Transform3D | None = None,
    ) -> None:
        """
        Update position and/or rotation of the given coordinate system with reference to its parent system.

        If parameter transform is set, then parameters rotation and position will be ignored. The given parameters will be used as copy.

        :param id_system: The target system.
        :param transform: Both, rotation and position of the system will be updated. If rotation and/or position are set additionally, they will be ignored.
        :param rotation: Sets the system's rotation.
        :param position: Sets the system's position.
        """
        sys_to_update = self.__get_system(id_system)

        if transform is not None:
            sys_to_update.set_transform(transform)
            pass
        else:
            if position is not None:
                sys_to_update.set_position(position)

            if rotation is not None:
                sys_to_update.set_orientation(rotation)

    @staticmethod
    def get_root_id() -> str:
        """
        Returns the tree's root id.

        This must be used for adding systems to the tree's root.
        """
        return TransformManager._ROOT_NODE.id


if __name__ == "__main__":
    """
    Funktionsweise:
    - CoordinateSystem und Point sind extern nur als str-id ansprechbar
        - Veränderung nur durch update_system() bzw. update_point()
    - Hinzufügen mit
        - add_point_to_system(id_parent: str, id_point: str, position: Position3D) -> Position3D
        - add_coordinate_system_to(id_parent: str, id_new_system: str, pose_in_parent_system: Transform3D) -> Transform3D#

        - das zuerst hinzugefügte System muss auf dem ROOT system aufbauen, das mit TransformManager.root_id() abgerufen
          werden kann
        - hinzugefügte Systeme müssen auf bereits bekannten Systemen aufbauen
    - Abrufen nur mit:
        - get_point_position(id: str) -> Position3D
        - get_coordinate_system_pose(id: str) -> Transform3D

    Grund: Beim Hinzufügen von Systemen wird der Parameter CoordinateSystem3D.transform_from_root berechnet, der bei
    Veränderung der Position eines Systems entsprechend neu berechnet werden muss. Das direkte Verändern eines Systems
    wird daher unterbunden.
    """
    # == Manage Coordinate Systems ===============================================================================
    tm = TransformManager()

    # -- Create Coordinate Systems -------------------------------------------------------------------------------
    # first added system must have root node as parent
    tm.add_system(Transform3D(), "0", tm.get_root_id())

    # all systems must have already registered systems as parent, this could also be the root node
    tm.add_system(Transform3D(position=Position3D.from_cartesian(0, 0, 2)), "C", "0")

    # the add_coordinate_system() function returns a reference to the coordinate system position
    tm.add_system(Transform3D(position=Position3D.from_cartesian(2, 0, 0)), "A", "0")
    tm.add_system(
        Transform3D(
            position=Position3D.from_cartesian(0, -2, 0), rotation=Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, -90)
        ),
        "B",
        "0",
    )

    # -- Modify Transformations ----------------------------------------------------------------------------------
    # systems can be modified with tm.update_system()
    print(tm.get_transform(tm.get_root_id(), "A"))
    assert tm.get_transform(tm.get_root_id(), "A") == Transform3D(position=Position3D.from_cartesian(2, 0, 0))

    sys_0 = tm.get_system_transform_local("0")

    sys_0.update_pos_cartesian(1, 0, 0)
    tm.update_system_transform_local("0", transform=sys_0)
    print(tm.get_system_transform_global("0"))
    assert tm.get_transform(tm.get_root_id(), "A") == Transform3D(position=Position3D.from_cartesian(3, 0, 0))

    # == Manage positions ========================================================================================

    # -- Adding points -------------------------------------------------------------------------------------------
    # points can be added to a registered system, returning a reference to the position
    tm.add_point(Position3D(1, 2, 3), "p0", "A")
    tm.add_point(Position3D.from_cartesian(0, 0, 0), "p1", "B")

    # -- Modifying points ----------------------------------------------------------------------------------------
    # or by setting a new position directly
    tm.update_point_pos_local("p0", Position3D.from_cartesian(0, 0, 0))

    # -- Transforming Points -------------------------------------------------------------------------------------
    # Note that already registered points can not switch systems on-the-fly. But it is possible to use these known
    # definitions to get the position of a point in a different system.

    assert tm.get_point_pos_in_system("p0", "B") == Position3D.from_cartesian(-2, 2, 0)

    # But, positions can be transformed even though they have not been registered.
    p0 = Position3D.from_cartesian(0, 0, 0)  # this point is not registered in a system
    pos_p0_in_B = tm.get_position_transformed(position=p0, sys_from="A", sys_to="B")
    assert pos_p0_in_B == Position3D.from_cartesian(-2, 2, 0)

    # Or

    # == Using Transformations ===================================================================================

    # transformation matrices between systems can be calculated using get_transform()
    assert tm.get_transform("A", "B") * Position3D.from_cartesian(0, 2, 0) == Position3D.from_cartesian(0, -2, 0)
