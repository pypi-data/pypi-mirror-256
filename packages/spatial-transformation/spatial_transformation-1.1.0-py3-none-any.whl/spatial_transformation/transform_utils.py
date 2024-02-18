"""
Contains utility functions for the TransformManager class.
"""
from __future__ import annotations

import dataclasses

from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_3d import Transform3D


@dataclasses.dataclass
class Point3D:
    """
    Point3D represents a position that has an id string and a parent coordinate system.
    """

    id: str
    id_system_base: str

    position: Position3D  # position in base system

    def __hash__(self) -> int:
        """
        Calculate hash based on id.
        """
        return id(self)

    def __repr__(self) -> str:
        """
        Represent the point as string.
        """
        return (
            f'Point3D(id="{self.id}", parent="{self.id_system_base}", position={self.position.export_as_cartesian()})'
        )


class CoordinateSystem3D:
    """
    CoordinateSystem3D represents a coordinate system that has an id string, a parent coordinate system and a transform with reference to its parent.
    """

    id: str
    system_parent: CoordinateSystem3D | None
    transform_from_parent: Transform3D | None

    # protected variables -----------------------------------------------------
    _point_for_id: dict[str, Point3D]  # child points
    _child_systems: dict[str, CoordinateSystem3D]  # child systems, used for calculating cache

    # cached for speedup -------------------------------------------------------
    _transform_from_root: Transform3D

    def __init__(self, id: str, system_parent: CoordinateSystem3D | None, transform_from_parent: Transform3D | None):
        """
        Create a coordinate system with id :param id:, parent system :param system_parent: and a pose :param transform_from_parent:.
        """
        self.id = id
        self.system_parent = system_parent
        self.transform_from_parent = transform_from_parent

        self._point_for_id = dict()
        self._child_systems = dict()

        self._calculate_cache()

    def get_transform_from_root(self) -> Transform3D:
        """
        Get cached transform from root system.
        """
        if self._transform_from_root is not None:
            return self._transform_from_root
        else:
            return Transform3D()

    def get_transform_from_parent(self) -> Transform3D:
        """
        Get cached transform from parent system.
        """
        if self.transform_from_parent is not None:
            return self.transform_from_parent
        else:
            return Transform3D()

    def __hash__(self) -> int:
        """
        Calculate has based on id.
        """
        return id(self)

    def __repr__(self) -> str:
        """
        Represent this coordinate system as string.
        """
        if self.get_parent() is not None:
            transform_from_parent: Transform3D = self.get_transform_from_parent()

            return (
                f'CoordinateSystem3D(id="{self.id}", id_parent="{self.get_parent_id()}"'
                f" position={transform_from_parent.get_position().export_as_cartesian()})"
                f" rotation={transform_from_parent.get_rotation().export_as_EULER_INTRINSIC_XYZ()})"
            )
        else:
            return f'CoordinateSystem3D(id="{self.id}")'

    def add_point(self, point: Point3D) -> None:
        """
        Add point to internal point dict.
        """
        self._point_for_id[point.id] = point

    def remove_point(self, id_point: str) -> None:
        """
        Remove point from internal point dict.
        """
        del self._point_for_id[id_point]

    def has_point(self, id_point: str) -> bool:
        """
        Check if point has been registered.
        """
        return id_point in self._point_for_id

    def get_points(self) -> list[Point3D]:
        """
        Get all registered points.
        """
        return list(self._point_for_id.values())

    def get_point_ids(self) -> list[str]:
        """
        Get all registered point ids.
        """
        return list(self._point_for_id.keys())

    def add_child(self, system: CoordinateSystem3D) -> None:
        """
        Add child system. Child systems will be updated on recalculation.
        """
        self._child_systems[system.id] = system

    def remove_child(self, id_system: str) -> None:
        """
        Remove child system.
        """
        del self._child_systems[id_system]

    def get_child_systems(self) -> list[CoordinateSystem3D]:
        """
        Get list of all immediate child systems. This does not include children of child systems.
        """
        return list(self._child_systems.values())

    def get_child_systems_recursively(self) -> list[CoordinateSystem3D]:
        """
        Get list of all child systems. This includes children of child systems.
        """
        list_children = []

        for child in self.get_child_systems():
            list_children.extend(child.get_child_systems_recursively())

        return list_children

    def get_parent(self) -> CoordinateSystem3D | None:
        """
        Returns this system's parent or None if there is no parent.
        """
        return self.system_parent

    def get_parent_id(self) -> str:
        """
        Returns this system's parent's id.
        """
        if self.system_parent is not None:
            return self.system_parent.id
        else:
            raise AttributeError(f'System "{self.id}" does not have a parent')

    def set_parent(self, parent: CoordinateSystem3D) -> None:
        """
        Set this system's parent.
        """
        self.system_parent = parent

        self._calculate_cache_recursively()

    def set_orientation(self, orientation: Rotation3D) -> None:
        """
        Set the system's orientation.
        """
        self.get_transform_from_parent().update_rot_as_EULER_REP_XYZ(*orientation.export_as_EULER_INTRINSIC_XYZ())

        # recalculate cached values
        self._calculate_cache_recursively()

    def set_position(self, position: Position3D) -> None:
        """
        Set the system's position.
        """
        self.get_transform_from_parent().update_pos_cartesian(*position.export_as_cartesian())

        # recalculate cached values
        self._calculate_cache_recursively()

    def set_transform(self, transform: Transform3D) -> None:
        """
        Set the system's transform.
        """
        self.get_transform_from_parent().update_pos_cartesian(*transform.get_position_reference().export_as_cartesian())
        self.get_transform_from_parent().update_rot_as_EULER_REP_XYZ(
            *transform.get_rotation_reference().export_as_EULER_INTRINSIC_XYZ()
        )

        # recalculate cached values
        self._calculate_cache_recursively()

    def _calculate_cache(self) -> None:
        """
        Calculate transform to root.
        """
        self._transform_from_root = CoordinateSystem3D._calculate_transform_from_root(
            self.system_parent, self.transform_from_parent
        )

    def _calculate_cache_recursively(self) -> None:
        """
        Calculate transform to root and update all child systems.
        """
        self._calculate_cache()

        for child_system in self._child_systems.values():
            child_system._calculate_cache_recursively()

    @staticmethod
    def _calculate_transform_from_root(
        system_parent: CoordinateSystem3D | None, transform_from_parent: Transform3D | None
    ) -> Transform3D:
        """
        Calculate transform from root node.
        """
        if system_parent is not None and transform_from_parent is not None:
            # ROOT_NODE has no parent

            transform_from_root = system_parent.get_transform_from_root() * transform_from_parent

            if isinstance(transform_from_root, Transform3D):
                return transform_from_root
            else:
                raise RuntimeError("Multiplication Transform3D * Transform3D did not result in Transform3D")
        else:
            return Transform3D()

    @staticmethod
    def get_none_system() -> CoordinateSystem3D:
        """
        Returns system that represents a None object.
        """
        return CoordinateSystem3D("__None_System__", None, None)
