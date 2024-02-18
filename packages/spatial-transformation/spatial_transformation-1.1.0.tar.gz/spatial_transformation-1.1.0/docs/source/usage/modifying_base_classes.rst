Modifying Base Classes
==============================================================

Modifying Points
---------------------------------------------------------------

Already created points can be modified in all supported coordinate system definitions (Cartesian, Polar or Spherical). The corresponding functions are called similarly to

:code:`update_cartesian(x=None, y=None, z=None, units=Unit.MM_DEG)`

Note that all three coordinate parameters are optional. This allows modifying only one coordinate and keeping the others constant. TransformAPI also allows modifying positions in a different system than that in which they were initially created in, so that the following code is entirely valid:


.. code-block:: python

  p = Position3D.from_cartesian(1, 0, 0)
  p.update_cylindrical(phi=45)
  print(p)    # (0.71, 0.71, 0)

Modifying Rotations
---------------------------------------------------------------

Already created rotations can be modified in all rotation representations that are available for creation. The representation used for updating does not have to be equal to that used for creation. Modifying functions are called similarly to

:code:`update_as_EULER_INTRINSIC_XYZ(rx=None, ry=None, rz=None, units: Unit=Unit.MM_DEG)`

All coordinate parameters are optional.

.. code-block:: python

  r = Rotation3D.from_EULER_INTRINSIC_XYZ(90, 0, 0)
  r.update_as_EULER_INTRINSIC_XYZ(95, 0, 0)
  print(r)  # [95, 0, 0]

Modifying Transformations
---------------------------------------------------------------

Transformations can be modified by independently updating their position or their rotation.

.. code-block:: python

  t = Transform3D(Position3D.from_cartesian(1, 1, 0),
                  Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90))

  print(t)  # Position: [1, 1, 0]
            # Rotation: [0, 0, 90]  (Euler XYZ)

  t.update_pos_cylindrical(phi=90)
  t.update_rot_as_RODRIGUES(z=45)

  print(t)  # Position: [0, 1.414, 0]
            # Rotation: [0, 0, 45]  (Euler XYZ)
