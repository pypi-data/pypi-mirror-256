"""
Contains utility functions for converting between positional/rotational representations.
"""
from spatial_transformation.definitions import (
    PositionDefinition2d,
    PositionDefinition3d,
    RotationDefinition2d,
    RotationDefinition3d,
    Unit,
)

import numpy as np
from scipy.spatial.transform import Rotation


class MathUtilsRotation2d:
    """
    Math utilities that only accept 2D operations.

    Internally, 3d operations are used, but on a 2D plane.
    """

    @staticmethod
    def get_rotmat_from_uservals(
        vals: np.ndarray[float], definition: RotationDefinition2d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates rotation matrix from the given user values.
        """
        # TODO definition should not be required as arg
        rotmat = np.eye(2, dtype=np.float64)

        if definition == RotationDefinition2d.Cartesian:
            rotmat[:, :] = MathUtilsRotation.get_rotmat_from_EULER_INTRINSIC_XYZ([0, 0, vals[0]], units)[0:2, 0:2]
        else:
            raise ValueError(f"Unknown definition {definition}")

        return rotmat

    @staticmethod
    def get_uservals_from_rotmat(
        rotmat: np.ndarray[float], definition: RotationDefinition2d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates user values from the given rotation matrix.
        """
        # TODO definition should not be required as arg
        vals = np.array([0], dtype=np.float64)

        rotmat_in = np.eye(3)
        rotmat_in[0:2, 0:2] = rotmat

        if definition == RotationDefinition2d.Cartesian:
            vals[0] = MathUtilsRotation.get_vals_EULER_INTRINSIC_XYZ(rotmat_in, units)[2]
        else:
            raise ValueError(f"Unknown definition {definition}")

        return vals


class MathUtilsRotation3d:
    """
    Math utilities that only accept 3D operations.
    """

    @staticmethod
    def get_rotmat_from_vals(
        vals: np.ndarray[float], definition: RotationDefinition3d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates rotation matrix from the given user values.
        """
        # TODO definition should not be required as arg
        rotmat = np.eye(3, dtype=np.float64)

        if definition == RotationDefinition3d.EULER_INTRINSIC_XYZ:
            rotmat[:, :] = MathUtilsRotation.get_rotmat_from_EULER_INTRINSIC_XYZ(vals, units)
        elif definition == RotationDefinition3d.EULER_INTRINSIC_ZYX:
            rotmat[:, :] = MathUtilsRotation.get_rotmat_from_EULER_INTRINSIC_ZYX(vals, units)
        elif definition == RotationDefinition3d.Axis_Angle:
            rotmat[:, :] = MathUtilsRotation.get_rotmat_from_AXIS_ANGLE(vals, units)
        elif definition == RotationDefinition3d.Quaternion:
            rotmat[:, :] = MathUtilsRotation.get_rotmat_from_QUATERNION(vals, units)
        elif definition == RotationDefinition3d.Rodrigues:
            rotmat[:, :] = MathUtilsRotation.get_rotmat_from_RODRIGUES(vals, units)
        else:
            raise ValueError(f"Unknown definition {definition}")

        return rotmat

    @staticmethod
    def get_vals_from_rotmat(
        rotmat: np.ndarray[float], definition: RotationDefinition3d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates user values from the given rotation matrix.
        """
        # TODO definition should not be required as arg
        vals = np.array([0, 0, 0, 0], dtype=np.float64)

        if definition == RotationDefinition3d.EULER_INTRINSIC_XYZ:
            vals = MathUtilsRotation.get_vals_EULER_INTRINSIC_XYZ(rotmat, units)
        elif definition == RotationDefinition3d.EULER_INTRINSIC_ZYX:
            vals = MathUtilsRotation.get_vals_EULER_INTRINSIC_ZYX(rotmat, units)
        elif definition == RotationDefinition3d.Axis_Angle:
            vals = MathUtilsRotation.get_vals_AXIS_ANGLE(rotmat, units)
        elif definition == RotationDefinition3d.Quaternion:
            vals = MathUtilsRotation.get_vals_QUATERNION(rotmat)
        elif definition == RotationDefinition3d.Rodrigues:
            vals = MathUtilsRotation.get_vals_RODRIGUES(rotmat, units)
        else:
            raise ValueError(f"Unknown definition {definition}")

        return vals


class MathUtilsRotation:
    """
    Utilities for converting between rotation matrix and user values.

    By user values we mean the different definitions which can be used to input data into the Rotation3d object.
    """

    @staticmethod
    def get_rotmat_from_EULER_INTRINSIC_XYZ(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Generates rotation matrix from 3 Euler angles in [self.val1 .. self.val3].
        intrinsic rotations: 1. rotation around z axis, 2. rotation around x' axis, 3. rotation around z" axis for co-rotating axes : x y'z" or
        """
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html
        # https://en.wikipedia.org/wiki/Euler_angles#Definition_by_intrinsic_rotations

        v = [
            vals[0] * units.get_rotation_factor(),
            vals[1] * units.get_rotation_factor(),
            vals[2] * units.get_rotation_factor(),
        ]

        r = Rotation.from_euler("XYZ", v)
        rotmat = r.as_matrix()
        rot_mat = rotmat

        return rot_mat

    @staticmethod
    def get_rotmat_from_EULER_INTRINSIC_ZYX(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Generates rotation matrix from 3 Euler angles in [self.val1 .. self.val3].
        intrinsic rotations: 1. rotation around z-axis, 2. rotation around y'-axis, 3. rotation around x"-axis for co-rotating axes : z y'x" or
        """
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_euler.html
        # https://en.wikipedia.org/wiki/Euler_angles#Definition_by_intrinsic_rotations
        v = [
            vals[0] * units.get_rotation_factor(),
            vals[1] * units.get_rotation_factor(),
            vals[2] * units.get_rotation_factor(),
        ]

        r = Rotation.from_euler("ZYX", v)
        rotmat = r.as_matrix()
        rot_mat = rotmat

        return rot_mat

    @staticmethod
    def get_rotmat_from_QUATERNION(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Generates rotation matrix from 4 quaternions ((x, y, z, w) format)  in [self.val1 .. self.val4].
        """
        # https: // docs.scipy.org / doc / scipy / reference / generated / scipy.spatial.transform.Rotation.from_quat.html
        # https: // en.wikipedia.org / wiki / Quaternions_and_spatial_rotation
        # with internal normalization of the vector

        v = [
            vals[0] * units.get_rotation_factor(),
            vals[1] * units.get_rotation_factor(),
            vals[2] * units.get_rotation_factor(),
            vals[3] * units.get_rotation_factor(),
        ]

        # rotation might have been intialized with empty values and only quaternion definition, so treat as "no-rotation"
        if np.linalg.norm(v) != 0:
            r = Rotation.from_quat(v)
            rotmat = r.as_matrix()
        else:
            rotmat = np.eye(3)

        return rotmat

    @staticmethod
    def get_rotmat_from_RODRIGUES(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Generates rotation matrix from Rodrigues (axis)  in [self.val1 .. self.val3].
        """
        # https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation#Rotation_vector
        # https: // docs.scipy.org / doc / scipy / reference / generated / scipy.spatial.transform.Rotation.from_rotvec.html

        v = [
            vals[0] * units.get_rotation_factor(),
            vals[1] * units.get_rotation_factor(),
            vals[2] * units.get_rotation_factor(),
        ]

        r = Rotation.from_rotvec(v)
        rotmat = r.as_matrix()

        return rotmat

    @staticmethod
    def get_rotmat_from_AXIS_ANGLE(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Generates rotation matrix from Axis and Angle  in [self.val1 .. self.val4].
        """
        v = [vals[0], vals[1], vals[2]]

        norm = np.linalg.norm(v)

        if norm != 0:
            v = v / norm  # normalize vector
            v = v * vals[3] * units.get_rotation_factor()  # scale vector according to angle

            r = Rotation.from_rotvec(v)
            rotmat = r.as_matrix()
            rot_mat = rotmat
        else:
            rot_mat = np.eye(3)

        return rot_mat

    @staticmethod
    def get_vals_EULER_INTRINSIC_XYZ(rot_mat: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Returns: Euler angles.
        """
        # https: // docs.scipy.org / doc / scipy / reference / generated / scipy.spatial.transform.Rotation.from_matrix.html
        # scipy -> https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.html
        r = Rotation.from_matrix(rot_mat)
        vec = r.as_euler("XYZ")

        rx = vec[0] / units.get_rotation_factor()
        ry = vec[1] / units.get_rotation_factor()
        rz = vec[2] / units.get_rotation_factor()

        return [rx, ry, rz]

    @staticmethod
    def get_vals_EULER_INTRINSIC_ZYX(rot_mat: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Returns: Euler angles.
        """
        # https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_euler.html
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.from_matrix.html
        r = Rotation.from_matrix(rot_mat)
        vec = r.as_euler("ZYX")

        rz = vec[0] / units.get_rotation_factor()
        ry = vec[1] / units.get_rotation_factor()
        rx = vec[2] / units.get_rotation_factor()

        return [rz, ry, rx]

    @staticmethod
    def get_vals_QUATERNION(rot_mat: np.ndarray[float]) -> np.ndarray[float]:
        """
        Returns: 4 quaternions: (x, y, z, w) format.
        """
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_quat.html
        r = Rotation.from_matrix(rot_mat)
        vec = r.as_quat(canonical=True)
        return vec

    @staticmethod
    def get_vals_RODRIGUES(rot_mat: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Returns: 3-dimensional vector which is co-directional to the axis of rotation and whose norm gives the angle of rotation.
        """
        # https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.transform.Rotation.as_rorot_mat.html
        r = Rotation.from_matrix(rot_mat)
        vec = r.as_rotvec()

        rx = vec[0] / units.get_rotation_factor()
        ry = vec[1] / units.get_rotation_factor()
        rz = vec[2] / units.get_rotation_factor()

        return [rx, ry, rz]

    @staticmethod
    def get_vals_AXIS_ANGLE(rot_mat: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Returns: vector representing rotation axis (vec[0] ... vev[2]) and rotation angle (vec[3]).
        """
        r = Rotation.from_matrix(rot_mat)
        vec = r.as_rotvec()
        angle = np.linalg.norm(vec) / units.get_rotation_factor()
        norm = np.linalg.norm(vec)

        if norm != 0:
            # raise ValueError("Axis vector can not be zero-vector!")
            vec = vec / norm

        return np.append(vec, angle)


class MathUtilsPosition2d:
    """
    Math utilities that only accept 2D operations.

    Internally, 3d operations are used, but on a 2D plane.
    """

    @staticmethod
    def get_posvec_from_uservals(
        vals: np.ndarray[float], definition: PositionDefinition2d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates position vector from the given user values.
        """
        tvec = np.array([0, 0], dtype=np.float64)

        vals_3d = np.concatenate([vals, [0]])  # transform to 3d

        if definition == PositionDefinition2d.CARTESIAN:
            tvec[0:2] = MathUtilsPosition.get_posvec_from_uservals_cartesian(vals_3d, units)[0:2]
        elif definition == PositionDefinition2d.CYLINDRICAL:
            tvec[0:2] = MathUtilsPosition.get_posvec_from_uservals_cylindrical(vals_3d, units)[0:2]
        else:
            raise ValueError(f"Unknown definition {definition}")

        return tvec

    @staticmethod
    def get_uservals_from_posvec(
        tvec: np.ndarray[float], definition: PositionDefinition2d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates user values from given position vector.
        """
        vals = np.array([0, 0], dtype=np.float64)

        tvec_3d = np.concatenate([tvec, [0]])  # transform to 3d

        if definition == PositionDefinition2d.CARTESIAN:
            vals[0:2] = MathUtilsPosition.get_uservals_from_posvec_CARTESIAN(tvec_3d + [0], units)[0:2]
        elif definition == PositionDefinition2d.CYLINDRICAL:
            vals[0:2] = MathUtilsPosition.get_uservals_from_posvec_CYLINDRICAL(tvec_3d + [0], units)[0:2]
        else:
            raise ValueError(f"Unknown definition {definition}")

        return vals


class MathUtilsPosition3d:
    """
    Math utilities that only accept 2D operations.
    """

    pass

    @staticmethod
    def get_posvec_from_uservals(
        vals: np.ndarray[float], definition: PositionDefinition3d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates position vector from the given user values.
        """
        # TODO definition should not be required as arg
        tvec = np.array([0, 0, 0], dtype=np.float64)

        if definition == PositionDefinition3d.CARTESIAN:
            tvec[0:3] = MathUtilsPosition.get_posvec_from_uservals_cartesian(vals, units)
        elif definition == PositionDefinition3d.CYLINDRICAL:
            tvec[0:3] = MathUtilsPosition.get_posvec_from_uservals_cylindrical(vals, units)
        elif definition == PositionDefinition3d.SPHERICAL:
            tvec[0:3] = MathUtilsPosition.get_posvec_from_uservals_spherical(vals, units)
        else:
            raise ValueError(f"Unknown definition {definition}")

        return tvec

    @staticmethod
    def get_uservals_from_posvec(
        tvec: np.ndarray[float], definition: PositionDefinition3d, units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Generates user values from given position vector.
        """
        # TODO definition should not be required as arg
        vals = np.array([0, 0, 0], dtype=np.float64)

        if definition == PositionDefinition3d.CARTESIAN:
            vals[0:3] = MathUtilsPosition.get_uservals_from_posvec_CARTESIAN(tvec, units)
        elif definition == PositionDefinition3d.CYLINDRICAL:
            vals[0:3] = MathUtilsPosition.get_uservals_from_posvec_CYLINDRICAL(tvec, units)
        elif definition == PositionDefinition3d.SPHERICAL:
            vals[0:3] = MathUtilsPosition.get_uservals_from_posvec_SPHERICAL(tvec, units)
        else:
            raise ValueError(f"Unknown definition {definition}")

        return vals


class MathUtilsPosition:
    """
    Utilities for converting between rotation matrix and user values.

    By user values we mean the different definitions which can be used to input data into the Rotation3d object.
    """

    @staticmethod
    def get_posvec_from_uservals_cartesian(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Computes cartesian unit conversion.
        """
        return vals * units.get_translation_factor()

    @staticmethod
    def get_posvec_from_uservals_cylindrical(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Computes cylindrical r, phi, h to cartesian x, y, z.
        """
        # -> https://www.maths2mind.com/schluesselwoerter/umrechnung-zylinderkoordinaten-auf-kartesische-koordinaten
        r = vals[0] * units.get_translation_factor()
        phi = vals[1] * units.get_rotation_factor()
        h = vals[2] * units.get_translation_factor()

        tvec = np.array([0, 0, 0], dtype=np.float64)
        tvec[0] = r * np.cos(phi)
        tvec[1] = r * np.sin(phi)
        tvec[2] = h

        return tvec

    @staticmethod
    def get_posvec_from_uservals_spherical(vals: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Computes spherical r, theta, phi  to cartesian x, y, z.
        """
        # https://en.wikipedia.org/wiki/Spherical_coordinate_system
        # ------------------------------------------------------ convert to mm and rad
        r = vals[0] * units.get_translation_factor()
        theta = vals[1] * units.get_rotation_factor()
        phi = vals[2] * units.get_rotation_factor()

        # ------------------------------------------------------- convert to cartesian
        tvec = np.array([0, 0, 0], dtype=np.float64)
        tvec[0] = r * np.sin(theta) * np.cos(phi)
        tvec[1] = r * np.sin(theta) * np.sin(phi)
        tvec[2] = r * np.cos(theta)

        return tvec

    # ------------------------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def get_uservals_from_posvec_CARTESIAN(tvec: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Computes raw cartesian x,y,z to cartesian x, y, z and returns as vector.

        Internal use only!
        """
        return tvec / units.get_translation_factor()

    @staticmethod
    def get_uservals_from_posvec_CYLINDRICAL(tvec: np.ndarray[float], units: Unit = Unit.MM_DEG) -> np.ndarray[float]:
        """
        Computes raw cartesian x,y,z to cylindrical r, phi, h and returns as vector.

        Internal use only!
        """
        # https://www.maths2mind.com/schluesselwoerter/umrechnung-zylinderkoordinaten-auf-kartesische-koordinaten
        # ----------------------------------------------------------------------------------------------------------- calculate in mm and rad
        r = np.sqrt(np.square(tvec[0]) + np.square(tvec[1]))
        phi = np.arctan2(tvec[1], tvec[0])
        h = tvec[2]
        # -------------------------------------------------------------------------------------------------------------- scale to target unit
        r = r / units.get_translation_factor()
        phi = phi / units.get_rotation_factor()
        h = h / units.get_translation_factor()

        return np.array([r, phi, h], dtype=np.float64)

    @staticmethod
    def get_uservals_from_posvec_SPHERICAL(
        tvec: np.ndarray[float], units: Unit = Unit.MM_DEG
    ) -> np.ndarray[np.float64]:
        """
        Computes cartesian x, y, z to cylindrical r, theta, phi and returns as vector.

        Internal use only!
        """
        # https://en.wikipedia.org/wiki/Spherical_coordinate_system
        # ---------------------------------------------------------- calculate in mm and rad
        r = np.sqrt(np.square(tvec[0]) + np.square(tvec[1]) + np.square(tvec[2]))
        if r != 0:
            theta = np.arccos(tvec[2] / r)
        else:
            theta = 0
        phi = np.arctan2(tvec[1], tvec[0])

        # ------------------------------------------------ scale to target unit
        r = r / units.get_translation_factor()
        theta = theta / units.get_rotation_factor()
        phi = phi / units.get_rotation_factor()

        return np.array([r, theta, phi], dtype=np.float64)


if __name__ == "__main__":
    pass
