Math Concept
==========================================================


Transform API provides three different core structures for representing spatial objects:

#. **Positions** (:doc:`Position2D</api/spatial_transformation.position_2d>` and :doc:`Position3D</api/spatial_transformation.position_3d>`) represent a position in either cartesian, cylindrical or spherical coordinates (3D representation) or cartesian or polar coordinates (2D representation). Internally, positions are stored in cartesian representation, but can be exported into a chosen system as nd-array.

#. **Rotations** (:doc:`Rotation2D</api/spatial_transformation.rotation_2d>` and :doc:`Rotation3D</api/spatial_transformation.rotation_3d>`) represent an orientation. 3D rotations can be defined in either intrinsic euler xyz coordinates, intrinsic euler zyx coordinates, quaternions, rodrigues representation or in axis-angle representation. 2D rotations are represented as an angle in mathematically positive direction. Internally, positions are stored as a rotation matrix, but can be exported into a chosen representation as nd-array.

#. **Transformations** (:doc:`Transform2D</api/spatial_transformation.transform_2d>` and :doc:`Transform3D</api/spatial_transformation.transform_3d>`) combine position and angle. These are represented and stored as an homogeneous matrix but can be manipulated separately.

2D vs 3D Representations
------------------------------------------------------------------------

The core structures are representable as both, a 2-dimensional form and a 3-dimensional form. 3D and 2D representations are designed to work equivalently, which means functions for creation and modification as well as mathematical operators are supported the same way.

.. note::

  2D structures are planned to be convertible into a 3D form. But as the library is WIP, this feature is to be done.

Units
------------------------------------------------------------------------

Transform API supports millimeters and meters for translation as well as degrees and radiants for rotation. As several rotation and position representations are defined by translation and rotation elements, Transform API only offers combined unit definitions. If a representation requires only translation arguments or only rotation arguments, the not-used unit will be ignored.

1. :code:`Unit.MM_DEG` (this is the default unit)
2. :code:`Unit.M_DEG`
3. :code:`Unit.MM_RAD`
4. :code:`Unit.M_RAD`

Units can be passed on element creation using the following code.

.. code-block:: python

    from spatial_transformation.definitions import Unit
    from spatial_transformation.rotation_3d import Rotation3D

    import math

    Rotation3D.from_AXIS_ANGLE(1, 0, 0, math.pi, units=Unit.M_RAD)  # 180° rotation around x axis


Positions
-----------------------------------------------------------------------------------

Transform API has a position class that represents a mathematical vector. Position2D and Position3D provide a set of vector operations that allow the user to replicate mathematical operations like addition, subtraction and cross-multiplying.

Allowed operations for 3D positions are shown in the following snippet.

.. code-block:: python

  p_0 = Position3D.from_cartesian(1, 0, 0)
  p_1 = Position3D.from_cartesian(0, 1, 0)

  p_result = p_0 + p_1  # vector addition
  p_result = p_0 - p_1  # vector subtraction

  p_result = p_0 * p_1  # cross multiplication
  p_result = p_0 * 2    # scalar multiplication
  p_result = p_0 / 2    # scalar division

2D positions allow the subset of operations shown here:

.. code-block:: python

  p_0 = Position2D.from_cartesian(0, 0)
  p_1 = Position2D.from_cartesian(0, 1)

  p_result = p_0 + p_1  # vector addition
  p_result = p_0 - p_1  # vector subtraction

  p_result = p_0 * 2    # scalar multiplication
  p_result = p_0 / 2    # scalar division

Rotations
-----------------------------------------------------------------------------------

Rotation2D and Rotation3D represent a rotation matrix and allow the user to interface with the stored rotation information by using a set of commonly used rotation representations. Transform API's Rotation2D and Rotation3D classes provide a set of functions that mimic mathematical matrix operations.

Allowed operations for 3D rotations are shown in the following snippet.

.. code-block:: python

  R_X = Rotation3D.from_EULER_INTRINSIC_XYZ(90, 0, 0)
  R_Z = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 90)
  p_0 = Position3D.from_cartesian(1, 0, 0)

  R_result = R_X * R_Z  # matrix-matrix multiplication
  R_result = R_X * p_0  # matrix-vector multiplication

Allowed operations for 2D rotations can be used equivalently, as is shown here:

.. code-block:: python

  R_X = Rotation2D.from_CARTESIAN(90)
  R_Z = Rotation2D.from_CARTESIAN(90)
  p_0 = Position2D.from_cartesian(1, 0)

  R_result = R_X * R_Z  # matrix-matrix multiplication
  R_result = R_X * p_0  # matrix-vector multiplication

In this documentation, rotation matrices are denoted as :math:`^0 _A R`, where :math:`0` is the base system and :math:`A` the target. :math:`^0 _A R` can be read as "orientation of system {A} with respect to system {0}". Rotation matrices can be combined to form a consecutive rotation:

.. math::
  ^0 _B R = ^0_AR \cdot ^A_BR

.. image:: /img/consecutive_rotation.png
    :width: 400
    :alt: Consecutive Rotation
    :align: center

In code, this can be represented equivalently:

.. code-block:: python

  R_0_A = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 45) # first system {0} is base
                                                        # second system {A} is target
  R_A_B = Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 45)

  R_0_B = R_0_A * R_A_B

  print(R_0_B) # [0, 0, 90] (Euler XYZ)


Note how :math:`^0 _B R = ^0_AR \cdot ^A_BR` is represented as :code:`R_0_B = R_0_A * R_A_B` in code.

.. _ref-transformation-notation:
Transformations
-----------------------------------------------------------------------------------

A vector with coordinates with reference to system {A} shall be denoted as :math:`^A V`. The transform matrix representing system {A} with reference to system {0} (called "the base system" from here on) is denoted as :math:`^0_A T`. Transform API uses **homogeneous coordinates** in cartesian form for handling internal operations. A homogeneous transformation matrix is represented as

.. math ::
  ^0_A T = \begin{bmatrix}
            R & V \\
            0 & 1
            \end{bmatrix}

where :math:`R` and :math:`V` represent a rotation and a translation. A homogeneous vector is represented as a homogeneous transformation matrix with a rotation matrix equal to the unit matrix and a translation equal to the respective vector value. The homogeneous vector :math:`^A V` with reference to system {A} can therefor be denoted as

.. math ::
  V = \begin{bmatrix}
            x \\
            y \\
            z \\
            1
            \end{bmatrix}

The transformation of :math:`^A V` to a vector :math:`^0 V` represented with reference to the base system {0} can be done using

.. math::
    ^0 V = ^0_A T \cdot ^A V

The above operations represents a translation and a *consecutive* rotation *after* the translation. A rotation *before* translating can be achieved by doing an additional transformation beforehand.


.. math::
    V_{result} = T_{rot} \cdot T_{trans+rot} \cdot V


.. note::

  For example let :math:`^A V` represent a point :math:`P` with coordinates :math:`(2, -1)`. Then :math:`^0 V` will have the coordinates :math:`(1, 2)`.


  .. image:: /img/spatial_transformation_1.png
    :width: 300
    :alt: Alternative text
    :align: center

  This transformation is done using the transform matrix

  .. math ::
    ^0_A T = \begin{bmatrix}
              -1 & 0 & 0 & 3 \\
              0 & -1 & 0 & 1 \\
              0 & 0 & 1 & 0 \\
              0 & 0 & 0 & 1
              \end{bmatrix}

  where the upper left 3x3 matrix represents a rotation of 180° around the z-axis and the right 3x1 column vector represents a translation of :math:`(3, 1, 0)`.

The mathematical notation of :math:`^0 V = ^0_A T \cdot ^A V` can be expressed as shown in the following snippet using the Transform API.

.. code-block:: python

  from spatial_transformation.rotation_3d import Rotation3D
  from spatial_transformation.position_3d import Position3D
  from spatial_transformation.transform_3d import Transform3D

  # create T matrix; in code it may easier to read
  # "transformation of system {A} with base system {0}"
  # BUT mathematically speaking, this should be read as
  # "matrix that represents {0} with respect to {A}"
  T_0_A = Transform3D(Position3D.from_cartesian(3, 1, 0),           # translation
                  Rotation3D.from_EULER_INTRINSIC_XYZ(0, 0, 180))   # rotation around Z-Axis

  # create point with cartesian coordinates with respect to {A}
  p_A = Position3D.from_cartesian(2, -1, 0)

  # transform point to coordinates with respect to {0}
  p_0 = T_0_A * p_A     # will print as (1, 2)

Note how :math:`^0 p = ^0_A T \cdot ^A V` is represented as :code:`V_0 = T_0_A * V_A` in code.
