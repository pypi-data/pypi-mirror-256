Transform Manager
======================================================

The TransformManager class provides a way to manage transformation chains by stacking coordinate systems on top of each other. Users can also add points to coordinate systems which allows easy manipulation of point groups.

A complete code example can be found in :code:`example_docs_transform_manager.py`

Naming Conventions and Element Access
------------------------------------------------------

TransformManager stores **Point**\ s and **CoordinateSystem**\ s using a string identifier. Once an element is registered, all operations access an element using the identifier. **Position**\ s define a position in space. **Point**\ s are positions that carry an additional string identifier and are children of a parent **CoordinateSystem**\ . **CoordinateSystem**\ s can have child **CoordinateSystem**\ s and child **Point**\ s. They also carry a string identifier and a **Transform** which defines the system's position and orientation with reference to a parent **CoordinateSystem**\ .

Objects of type **CoordinateSystem** and **Point** are only used internally by the TransformManager. Return values for the users are of type **Transform** and **Position**, respectively. Modifications can only be done using string identifiers.

These naming conventions are also reflected in the API calls:

* :code:`get_point_pos_in_system(id_point: str, id_system: str)` refers to an already registered point that can be accessed by string identifier
* :code:`get_position_transformed(position: Position3D, id_from: str, id_to: str)` refers to an arbitrary position

Building Chains and Adding Points
------------------------------------------------------

For example, take the following configuration of systems {0}, {A}, {B} and {C}. Point P is to be added to system {C} at position (2, 1). We want to replicate the pictured system structure and use TransformManager to transform point P's coordinates from system {C} to system {B}. The used notation is explained on the :ref:`Math Concept page <ref-transformation-notation>`

.. image:: /img/transform_manager.png
  :width: 300
  :alt: Alternative text
  :align: center

The transform manager class allows recreating this structure as a hierarchical tree. All added coordinate systems are required to have a parent system. TransformManager is initialized with a default root system, which must be used as parent of the very first added system and can be accessed using the identifier returned by :code:`TransformManager#get_root_id()`.

.. code-block:: python

  from spatial_transformation.position_3d import Position3D
  from spatial_transformation.transform_3d import Transform3D
  from spatial_transformation.transform_manager import TransformManager

  tm = TransformManager()

  # add right transformation chain
  tm.add_system(Transform3D(Position3D.from_cartesian(0, 0, 0)), "0",
                          TransformManager.get_root_id())
  tm.add_system(Transform3D(Position3D.from_cartesian(1, 2, 0)), "A", "0")
  tm.add_system(Transform3D(Position3D.from_cartesian(2, 1, 0)), "B", "A")

  # add left transformation chain
  tm.add_system(Transform3D(Position3D.from_cartesian(-2, 3, 0)), "C", "0")

We add point P to system {C} at position :math:`^C V` with reference to system {C}.

.. code-block:: python

  tm.add_point(Position3D.from_cartesian(2, 1, 0), "p", "C")

This will allow us to find the position of the point :math:`^B V` with reference to system {B}.

.. code-block:: python

  p_B = tm.get_point_pos_in_system("p", "B")

  print(p_B)  # (-3, 1, 0)

Reading Positions and Transformations
---------------------------------------------------

Positions and transformations can be accessed either *locally*, *globally* or *relatively*. *Local* transformations are always with reference to the object's immediate parent, *global* transformations are with reference to the tree's root and *relative* transformations are always with reference to another specified coordinate system.

.. image:: /img/transform_manager_local_global_relative.png
  :width: 400
  :alt: Alternative text
  :align: center

For the shown configuration, system {B} positions can be accessed in the following ways:

.. code-block:: python

  tm = TransformManager()

  tm.add_system(Transform3D(Position3D.from_cartesian(1, 2, 0)), "A", tm.get_root_id())
  tm.add_system(Transform3D(Position3D.from_cartesian(1, 2, 0)), "B", "A")
  tm.add_point(Position3D.from_cartesian(2, 1, 0), "P", "B")

  tm.add_system(Transform3D(Position3D.from_cartesian(3, 1, 0)), "C", tm.get_root_id())

  print("{B} local:           " + str(tm.get_system_transform_local("B")
                                      .get_position().export_as_cartesian()))     # [1, 2, 0]
  print("{B} global:          " + str(tm.get_system_transform_global("B")
                                      .get_position().export_as_cartesian()))     # [2, 4, 0]
  print("{B} relative to {C}: " + str(tm.get_system_transform_relative("B", "C")
                                      .get_position().export_as_cartesian()))     # [-1, 3, 0]

Moving Coordinate Systems
---------------------------------------------------

Registered coordinate systems can be moved, this will cause their child systems and points to move as well. Again, take the shown systems that have been registered in the above paragraph as the initial configuration.

.. image:: /img/transform_manager.png
  :width: 300
  :alt: Alternative text
  :align: center

We want to move system {C} from :math:`(-2, 3, 0)` to :math:`(-2, 4, 0)` along with all its registered child points and we want to move system {A} from :math:`(1, 2, 0)` to :math:`(2, 2, 0)` along with all its registered child systems. System {C}'s position is specified with reference to its parent system {0} and that system {A}'s position is specified with reference to system {0}.

.. code-block:: python

  # get system poses
  pose_C = tm.get_system_transform_local("C")
  pose_A = tm.get_system_transform_local("A")

  # move system poses
  pose_C.update_pos_cartesian(-2, 4, 0)   # move from (-2, 3, 0) to (-2, 4, 0)
  pose_A.update_pos_cartesian(2, 2, 0)    # move from (1, 2, 0) to (2, 1, 0)

  # update systems
  tm.update_system_transform_local("C", transform=pose_C)
  tm.update_system_transform_local("A", transform=pose_A)

TransformManager internally caches each registered system's transformation with reference to the root node, which has to be updated too, when a system position or orientation is updated. This is why it is required to

1. read the current coordinate system pose,

2. to then modify the read pose and then

3. to finally write the modified pose to the transform manager, so that the internal cache can be updated.

This results in a new configuration as follows.

.. image:: /img/transform_manager_C_moved.png
  :width: 300
  :alt: Alternative text
  :align: center

Note that point P has been moved along with its parent system {C} and that system {B} has been moved along with its parent system {A}. The position of point P can again be found using the method :code:`get_point_transformed_to(id_point, id_system)`.


.. code-block:: python

  V_0 = tm.get_point_pos_in_system("p", "0")
  V_C = tm.get_point_pos_in_system("p", "C")
  V_B = tm.get_point_pos_in_system("p", "B")

  print("{0}: " + str(V_0)) # (0, 5, 0)
  print("{C}: " + str(V_C)) # (2, 1, 0)
  print("{B}: " + str(V_B)) # (-4, 2, 0)

.. image:: /img/transform_manager_moved_VB_shown.png
  :width: 300
  :alt: Alternative text
  :align: center

Moving Points
-------------------------------------------------------------

Registered points, as all registered elements, can be modified using their string identifier. It is required to first read the current position, then to update the returned position and then to write back the resulting position.

.. code-block:: python

  tm = TransformManager()

  tm.add_system(Transform3D(Position3D.from_cartesian(0, 0, 0)), "0",
                          TransformManager.get_root_id())
  tm.add_point(Position3D.from_cartesian(2, 1, 0), "p", "0")

  pos_P = tm.get_point_pos_local("p")
  pos_P.update_cartesian(x=1)
  tm.update_point_pos_local("p", pos_P)

  print(tm.get_point_pos_local("p"))  # [1, 1, 0]

Changing Parents
------------------------------------------------------------

TransformManager allows points and coordinate systems to change their parent system. This is done using :code:`update_system_parent()` or :code:`update_point_parent()`. The update function will recalculate an object's transform with respect to its new parent and change the parent system reference. This means, only the local transformation will actually be effected by this operation.

.. image:: /img/transform_manager_update_parent_0.drawio.png
  :width: 300
  :alt: Alternative text
  :align: center

.. code-block:: python

  tm = TransformManager()

  # Create the following configuration:
  # 0 -> A -> C ==> pC
  # |--> B
  tm.add_system(Transform3D(), "0", tm.get_root_id())
  tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "A", "0")
  tm.add_system(Transform3D(Position3D.from_cartesian(1, 0, 0)), "C", "A")
  tm.add_system(Transform3D(Position3D.from_cartesian(1, 1, 0),
                            Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)), "B", "0")

  tm.add_point(Position3D.from_cartesian(1, 1, 0), "pC", "C")

  # move entire chain to new parent ----------------------------------------------------------------------
  # move A and all children to B
  # 0 -> B -> A -> C ==> pC
  print(tm.get_system_transform_local("A"))   # Pos: [1, 0, 0]    Rot: [0, 0, 0]
  print(tm.get_system_transform_global("A"))  # Pos: [1, 0, 0]    Rot: [0, 0, 0]
  tm.update_system_parent("A", "B")
  print(tm.get_system_transform_local("A"))   # Pos: [-1, 0, 0]   Rot: [0, 0, -90]
  print(tm.get_system_transform_global("A"))  # Pos: [1, 0, 0]    Rot: [0, 0, 0]

  # move point to new parent
  # 0 -> B -> A -> C
  #      |==> pC
  tm.update_point_parent("pC", "B")

.. image:: /img/transform_manager_update_parent_B.drawio.png
  :width: 300
  :alt: Alternative text
  :align: center

Removing Systems
-----------------------------------------------------------------------

Registered objects can be removed with either :code:`remove_point()` or :code:`remove_system()`. Removing a coordinate system will result in all its child points and all systems along the transformation chain to be removed.
