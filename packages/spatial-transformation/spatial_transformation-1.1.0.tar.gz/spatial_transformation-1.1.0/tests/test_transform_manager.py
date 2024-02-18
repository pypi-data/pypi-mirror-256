from spatial_transformation.position_3d import Position3D
from spatial_transformation.rotation_3d import Rotation3D
from spatial_transformation.transform_3d import Transform3D
from spatial_transformation.transform_manager import TransformManager

import numpy as np
import pytest
import testutils


@pytest.mark.hardcoded
def test_transform() -> None:
    tm = TransformManager()

    # build system tree
    # root -> 0 -> A
    #         |--> B
    tm.add_system(Transform3D(), "0", tm.get_root_id())

    tm.add_system(Transform3D(position=Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(
        Transform3D(
            position=Position3D.from_cartesian(0, 1, 0), rotation=Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)
        ),
        "B",
        "0",
    )

    assert tm.has_transformation("A", "0")

    # add points to A and B
    tm.add_point(Position3D.from_cartesian(0, 0, 0), "pA", "A")
    tm.add_point(Position3D.from_cartesian(1, 1, 0), "pB", "B")

    # transform point in system A to system 0; system A is translated
    # read as "get_transform(system_to, system_from)"
    assert tm.get_transform("0", "A") * Position3D.from_cartesian(0, 0, 0) == Position3D(
        1, 0, 0
    )  # use calculated transform
    # read as "get_point_pos_in_system(id_of_point, system_from_base_coords)"
    assert tm.get_point_pos_in_system("pA", "0") == Position3D(1, 0, 0)  # use registered point
    # transform point in system 0 to system A
    assert tm.get_transform("A", "0") * Position3D.from_cartesian(0, 0, 0) == Position3D(-1, 0, 0)
    assert tm.get_position_transformed(Position3D.from_cartesian(0, 0, 0), "0", "A") == Position3D(-1, 0, 0)

    # transform point in system B to system 0; system B is rotated and translated
    assert tm.get_transform("0", "B") * Position3D.from_cartesian(1, 1, 0) == Position3D(-1, 2, 0)
    assert tm.get_point_pos_in_system("pB", "0") == Position3D(-1, 2, 0)
    assert tm.get_transform("B", "0") * Position3D.from_cartesian(1, 1, 0) == Position3D(0, -1, 0)
    assert tm.get_position_transformed(Position3D.from_cartesian(1, 1, 0), "0", "B") == Position3D(0, -1, 0)


@pytest.mark.hardcoded
def test_update_point_parent() -> None:
    tm = TransformManager()

    # 0 -> A -> C
    # |--> B
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")

    tm.add_point(Position3D.from_cartesian(0, 0, 0), "p", "A")

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(0, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(1, 0, 0)

    # set parent of p to 0
    tm.update_point_parent("p", "0")

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(1, 0, 0)


@pytest.mark.hardcoded
def test_update_point_position() -> None:
    tm = TransformManager()

    # 0 -> A -> C
    # |--> B
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(Transform3D(Position3D.from_cartesian(0, 1, 0)), "B", "0")

    tm.add_point(Position3D.from_cartesian(0, 0, 0), "p", "A")

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(0, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_in_system("p", "B") == Position3D.from_cartesian(1, -1, 0)

    # update point position

    tm.update_point_pos_local("p", Position3D.from_cartesian(1, 0, 0))
    assert tm.get_point_pos_in_system("p", "B") == Position3D.from_cartesian(2, -1, 0)


@pytest.mark.hardcoded
def test_update_system_transform() -> None:
    tm = TransformManager()

    # 0 -> A -> B -> p
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "B", "A")

    tm.add_point(Position3D.from_cartesian(1, 0, 0), "p", "B")

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(3, 0, 0)
    assert tm.get_point_pos_in_system("p", "A") == Position3D.from_cartesian(2, 0, 0)

    # update system position

    tm.update_system_transform_local("A", Position3D.from_cartesian(2, 0, 0))

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(4, 0, 0)
    assert tm.get_point_pos_in_system("p", "A") == Position3D.from_cartesian(2, 0, 0)

    # update second layer

    tm.update_system_transform_local("B", Position3D.from_cartesian(2, 0, 0))

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(5, 0, 0)
    assert tm.get_point_pos_in_system("p", "A") == Position3D.from_cartesian(3, 0, 0)


@pytest.mark.hardcoded
def test_update_system_rotation() -> None:
    # update system rotation

    tm = TransformManager()

    # 0 -> A -> B -> p
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "B", "A")

    tm.add_point(Position3D.from_cartesian(1, 0, 0), "p", "B")

    # use transform keyword argument, but only change rotation
    tm.update_system_transform_local(
        "A", transform=Transform3D(Position3D.from_cartesian(1, 0, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90))
    )

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(1, 2, 0)

    # use rotation keyword argument
    tm.update_system_transform_local("A", rotation=Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90))

    assert tm.get_point_pos_local("p") == Position3D.from_cartesian(1, 0, 0)
    assert tm.get_point_pos_global("p") == Position3D.from_cartesian(1, 2, 0)


@pytest.mark.hardcoded
def test_add_remove_list() -> None:
    tm = TransformManager()

    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(), "A", "0")
    tm.add_system(Transform3D(), "B", "A")

    tm.add_point(Position3D(1, 0, 0), "p1", "0")
    tm.add_point(Position3D(0, 1, 0), "p2", "A")
    tm.add_point(Position3D(0, 3, 0), "p3", "A")
    tm.add_point(Position3D(0, 3, 0), "p4", "B")

    assert tm.get_points_all() == ["p1", "p2", "p3", "p4"]
    assert tm.get_points_with_parent("A") == ["p2", "p3"]
    assert tm.get_systems_all() == ["__root__", "0", "A", "B"]

    # remove a point

    tm.remove_point("p3")
    assert tm.get_points_all() == ["p1", "p2", "p4"]

    # remove a system

    tm.remove_system("A")
    assert tm.get_systems_all() == ["__root__", "0"]
    assert tm.get_points_all() == ["p1"]


@pytest.mark.hardcoded
def test_update_system_parent() -> None:
    tm = TransformManager()

    # 0 -> A -> C
    # |--> B
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "C", "A")
    tm.add_system(
        Transform3D(Position3D.from_cartesian(1, 1, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)), "B", "0"
    )

    tm.add_point(Position3D.from_cartesian(1, 1, 0), "pA", "A")
    tm.add_point(Position3D.from_cartesian(1, 1, 0), "pC", "C")

    assert tm.get_point_pos_in_system("pA", "B") == Position3D.from_cartesian(0, -1, 0)
    assert tm.get_transform("B", "A") * Position3D.from_cartesian(1, 1, 0) == Position3D.from_cartesian(0, -1, 0)

    # move entire chain to new parent ----------------------------------------------------------------------

    assert tm.get_system_transform_local("A") == Transform3D(Position3D.from_cartesian(1, 0, 0))

    assert tm.get_system_transform_relative("A", "0") == Transform3D(Position3D.from_cartesian(1, 0, 0))
    assert tm.get_system_transform_global("C") == Transform3D(Position3D.from_cartesian(2, 0, 0))

    assert tm.get_system_transform_relative("A", "B") == Transform3D(
        Position3D.from_cartesian(-1, 0, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, -90)
    )

    pos_pA_inC = tm.get_point_pos_in_system("pA", "C")
    pos_pA_global = tm.get_point_pos_global("pA")
    pos_pA_local = tm.get_point_pos_local("pA")

    # move A and all children to B
    # 0
    # |--> B -> A -> C
    tm.update_system_parent("A", "B")

    # local transformation of system (= transform with reference to parent) should change
    assert tm.get_system_transform_local("A") == Transform3D(
        Position3D.from_cartesian(-1, 0, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, -90)
    )

    # point transformation should stay the same
    assert pos_pA_inC == tm.get_point_pos_in_system("pA", "C")
    assert pos_pA_global == tm.get_point_pos_global("pA")
    assert pos_pA_local == tm.get_point_pos_local("pA")

    assert tm.get_point_pos_in_system("pA", "B") == Position3D.from_cartesian(0, -1, 0)
    assert tm.get_system_parent("A") == "B"


@pytest.mark.randomized
def test_point_distance() -> None:
    tm = TransformManager()

    # 0 -> A -> C
    # |--> B
    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
    tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "C", "A")
    tm.add_system(
        Transform3D(Position3D.from_cartesian(1, 1, 0), Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)), "B", "0"
    )

    tm.add_point(Position3D.from_cartesian(1, 1, 0), "pA", "A")
    tm.add_point(Position3D.from_cartesian(0, 1, 0), "pB", "B")
    tm.add_point(Position3D.from_cartesian(1, 1, 0), "pC", "C")

    assert tm.get_point_distance("pB", "pC") == 3


@pytest.mark.randomized
def test_transform_loop() -> None:
    rng = np.random.default_rng(0)

    tm = TransformManager()

    tm.add_system(Transform3D(), "0", tm.get_root_id())
    tm.add_system(Transform3D(), "1", "0")
    tm.add_system(Transform3D(), "2", "1")

    for i in range(1000):
        vals = testutils.random_3_tuple(rng)

        tm.update_system_transform_local("1", Position3D.from_cartesian(*vals))

        trans = tm.get_transform("0", "2")

        sys_1 = tm.get_system_transform_local("1")
        sys_2 = tm.get_system_transform_local("2")

        assert trans == sys_1 * sys_2


if __name__ == "__main__":
    test_transform()
    test_update_system_parent()
    test_transform_loop()
    test_update_point_parent()
    test_update_point_position()
    test_update_system_transform()
    test_add_remove_list()
    test_point_distance()
    test_update_system_rotation()
