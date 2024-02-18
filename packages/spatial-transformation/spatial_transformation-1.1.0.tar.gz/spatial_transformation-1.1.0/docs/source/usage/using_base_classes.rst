Using the Base Classes
=======================================================================

Transform API's base classes can be created and exported using several commonly used **definitions**. While all base classes are internally represented in homogenous coordinates, they can be created using a number of different representation formats that are described in this document.

Rotation and Position classes provide static functions named similarly to

:code:`<Rotation/Position>.from_<definition>(..., units=<units>)`

Using the constructor is discouraged. A created rotation or position can be converted back into an array of values that represent the class in a given definition. This is done using a function named similarly to

:code:`<Rotation/Position>.export_as_<definition>(..., units=<units>)`

This document includes detailed explanations of all supported representation types.

Positions
-----------------------------------------------------------------------

Positions3D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Allowed definitions for 3D positions are:

1. **Cartesian Coordinates** that represent the position in a x-y-z system. Points can be created in cartesian coordinates using

.. code-block:: python

    p = Position3D.from_cartesian(x=3, y=1, z=0)  # creates a point at (3 mm, 1 mm, 0 mm)
    p.export_as_cartesian() # [3, 1, 0]

2. **Cylindrical Coordinates** that represent a position in r-phi-z coordinates. `See Wikipedia <https://en.wikipedia.org/wiki/Cylindrical_coordinate_system>`_

.. image:: /img/cylindrical_coords.png
  :width: 200
  :align: center

Points in cylindrical coordinates can be created using

.. code-block:: python

    p = Position3D.from_cylindrical(r=2, phi=90, z=0)   # creates a point at (0 mm, 2 mm, 0 mm)
    p.export_as_cylindrical() # [2, 90, 0]

3. **Spherical Coordinates**  that represent a position in r-theta-phi coordinates. `See Wikipedia <https://en.wikipedia.org/wiki/Spherical_coordinate_system>`_

.. image:: /img/spherical_coords.png
  :width: 200
  :align: center

Points in spherical coordinates can be created using

.. code-block:: python

    p = Position3D.from_spherical(r=2, theta=90, phi=180)   # creates a point at (-2 mm, 0 mm, 0 mm)
    p.export_as_spherical() # [2, 90, 180]


Positions2D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Allowed definitions for 2D positions are:

1. **Cartesian Coordinates** in the x-y-plane

.. code-block:: python

    p = Position2D.from_cartesian(0, 1) # point at (0 mm, 1 mm)
    p.export_as_cartesian() # [0, 1]



2. **Polar Coordinates** that represent a position in a r-phi system.

.. code-block:: python

    p = Position2D.from_cylindrical(1, 45)  # point at (0.707 mm, 0.707 mm)
    p.export_as_cartesian() # [1, 45]

Rotations
-----------------------------------------------------------------------

Rotations are internally stored as rotation matrices. They can be created using one of the representations described in this document. Note that Transform API uses `SciPy's Rotation class <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.html>`_ internally. All angle values provided to Transform API's base classes will be wrapped into a range as specified here.

.. note::

    Some representations are ambiguous. For example, creating a Rotation object using **Euler Angles** with a z-rotation of 190° results in information loss due to angle wrapping.

    .. code-block:: python

        r = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 180 + 10)   # 190° rotation around z
        print(r.export_as_EULER_INTRINSIC_XYZ()) # [0, 0, -170]

Rotation3D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

3D rotations can be represented as one of the following:



1. **Intrinsic Euler XYZ** rotation (consecutive rotation around x, y and z axis; the axes rotate with the system; `See Wikipedia <https://en.wikipedia.org/wiki/Euler_angles#Conventions_by_intrinsic_rotations>`_). This function uses `SciPy's from_euler function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.from_euler.html>`_ internally.

 .. code-block:: python

    r = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)   # 90° rotation around z
    r.export_as_EULER_INTRINSIC_XYZ() # [0, 0, 90]

 The exported x- and z-angle belong to a range of [-180°, 180°]. The y-angle belongs to a range of [-90°, 90°]. During creation, all angles outside of the respective range will be wrapped into it.


2. **Intrinsic Euler ZYX** rotation (consecutive rotation around z, y and x axis; the axes rotate with the system; `See Wikipedia <https://en.wikipedia.org/wiki/Euler_angles#Conventions_by_intrinsic_rotations>`_). This function uses `SciPy's from_euler function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.from_euler.html>`_ internally.

 .. code-block:: python

    r = Rotation3D.from_EULER_INTRINSIC_ZYX(90, 0, 0)   # 90° rotation around z
    r.export_as_EULER_INTRINSIC_ZYX() # [90, 0, 0]

 The exported x- and z-angle belong to a range of [-180°, 180°]. The y-angle belongs to a range of [-90°, 90°]. During creation, all angles outside of the respective range will be wrapped into it.

3. **Axis Angle** representation (rotation around an axis that is represented in cartesian coordinates; rotation angle is specified as a 4th parameter; `See Wikipedia <https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation>`_). This function uses `SciPy's from_rotvec function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.from_rotvec.html>`_ internally.

 .. code-block:: python

    r = Rotation3D.from_AXIS_ANGLE(1, 0, 0, 45) # 45 degree rotation around x
    r.export_as_AXIS_ANGLE() # [1, 0, 0, 45]

 The exported angle value will be in range [0°, 180°].

4. **Rodrigues** representation (rotation around an axis in cartesian coordinates; rotation angle is encoded as the vector's norm; `See Wikipedia <https://en.wikipedia.org/wiki/Rodrigues%27_rotation_formula>`_). This function uses `SciPy's from_rotvec function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.from_rotvec.html>`_ internally.

 .. code-block:: python

    r = Rotation3D.from_RODRIGUES(0, 3, 4)  # 5 degree rotation around (0, 3, 4)
    r.export_as_RODRIGUES() # [0, 3, 4]

5. **Quaternions** (unique but over-determined representation; `See Wikipedia <https://en.wikipedia.org/wiki/Quaternion>`_). This function uses `SciPy's from_quat function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.from_quat.html>`_ internally.


 .. code-block:: python

    r = Rotation3D.from_QUATERNION(0.7071068, 0, 0, 0.7071068)  # 90° rotation around x
    r.export_as_QUATERNION() # [0.7071068, 0, 0, 0.7071068]


Rotation2D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

2D rotations can be represented as an angle :math:`\phi` in mathematically positive direction. This function uses `SciPy's from_euler function <https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.spatial_transformation.Rotation.from_euler.html>`_ internally.

 .. code-block:: python

    r = Rotation2D.from_CARTESIAN(45)   # 45° rotation
    r.export_as_CARTESIAN() # [45]

Transformations
-----------------------------------------------------------------------

Transformations are represented as a homogenous transformation matrix internally. They can be created by combining a Rotation and Position object into a Transform object using any possible combination of definitions.

Transformation3D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 .. code-block:: python

    t = Transform3D(Position3D.from_cartesian(1, 1, 0),
                Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90))
    t.get_position().export_as_CARTESIAN() # (1, 1, 0)
    t.get_rotation().export_as_EULER_INTRINSIC_XYZ() # (0, 0, 90)

Transformation2D
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 .. code-block:: python

    t = Transform2D(Position2D.from_cartesian(1, 1),
                Rotation2D.from_CARTESIAN(90))
    t.get_position().export_as_CARTESIAN() # (1, 1)
    t.get_rotation().export_as_EULER_INTRINSIC_XYZ() # (90)

Converting Between Systems
------------------------------------------------------------------------

All base classes can be exported to any other supported representation type. As all positions are handled in cartesian coordinates and all rotations are internally represented as rotation matrices, a direct conversion is not possible and not needed.

.. code-block:: python

    # cartesian point converted to cylindrical coordinates
    p = Position3D.from_cartesian(1, 1, 0)
    p.export_as_cylindrical()   # [1.414, 45, 0]

    # rotation created in axis angle representation converted to intrinsic Euler XYZ angles
    r = Rotation3D.from_AXIS_ANGLE(0, 0, 1, 10)
    r.export_as_EULER_INTRINSIC_XYZ()   # [0, 0, 10]
