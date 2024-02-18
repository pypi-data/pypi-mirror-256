"""
A collection of functions that operate on python lists as if
they were vectors.  A basic implementation to forgo the need
to use numpy.
"""
import math
import sys
from math import sqrt, cos, sin, fabs, atan2


def magnitude(v):
    return sqrt(sum(v[i] * v[i] for i in range(len(v))))


def add(u, v):
    return [u[i] + v[i] for i in range(len(u))]


def sub(u, v):
    return [u[i] - v[i] for i in range(len(u))]


def dot(u, v):
    return sum(u[i] * v[i] for i in range(len(u)))


def eldiv(u, v):
    return [u[i] / v[i] for i in range(len(u))]


def elmult(u, v):
    return [u[i] * v[i] for i in range(len(u))]


def normalize(v):
    vmag = magnitude(v)
    return [v[i] / vmag for i in range(len(v))]


def cross(u, v):
    c = [u[1] * v[2] - u[2] * v[1],
         u[2] * v[0] - u[0] * v[2],
         u[0] * v[1] - u[1] * v[0]]

    return c


def mult(u, c):
    return [u[i] * c for i in range(len(u))]


def div(u, c):
    return [u[i] / c for i in range(len(u))]


def quaternion_to_rotation_matrix(quaternion):
    """
    This method takes a quaternion representing a rotation
    and turns it into a rotation matrix.
    :return: 3x3 rotation matrix suitable for pre-multiplying vector v:
    i.e. v' = Mv
    """
    mag_q = magnitude(quaternion)
    norm_q = div(quaternion, mag_q)
    qw, qx, qy, qz = norm_q
    ww, xx, yy, zz = qw * qw, qx * qx, qy * qy, qz * qz
    wx, wy, wz, xy, xz, yz = qw * qx, qw * qy, qw * qz, qx * qy, qx * qz, qy * qz
    # mx = [[qw * qw + qx * qx - qy * qy - qz * qz, 2 * qx * qy - 2 * qw * qz, 2 * qx * qz + 2 * qw * qy],
    #       [2 * qx * qy + 2 * qw * qz, qw * qw - qx * qx + qy * qy - qz * qz, 2 * qy * qz - 2 * qw * qx],
    #       [2 * qx * qz - 2 * qw * qy, 2 * qy * qz + 2 * qw * qx, qw * qw - qx * qx - qy * qy + qz * qz]]
    # aa, bb, cc, dd = a * a, b * b, c * c, d * d
    # bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d

    mx = [[ww + xx - yy - zz, 2 * (xy + wz), 2 * (xz - wy)],
          [2 * (xy - wz), ww + yy - xx - zz, 2 * (yz + wx)],
          [2 * (xz + wy), 2 * (yz - wx), ww + zz - xx - yy]]
    return mx


def matrix_constant_mult(m, c):
    """
    Multiply components of matrix m by constant c
    """
    return [mult(row_m, c) for row_m in m]


def matrix_vector_mult(m, v):
    """
    Post multiply matrix m by vector v
    """
    return [dot(row_m, v) for row_m in m]


def vector_matrix_mult(v, m):
    """
    Premultiply matrix m by vector v
    """
    rows = len(m)
    if len(v) != rows:
        raise ValueError('vector_matrix_mult mismatched rows')
    columns = len(m[0])
    result = []
    for c in range(0, columns):
        result.append(sum(v[r] * m[r][c] for r in range(rows)))
    return result


def matrix_mult(a, b):
    """
    Multiply 2 matrices: first index is down row, second is across column.
    Assumes sizes are compatible (number of columns of a == number of rows of b).
    """
    return [vector_matrix_mult(row_a, b) for row_a in a]


def matrix_minor(a, i, j):
    return [row[:j] + row[j + 1:] for row in (a[:i] + a[i + 1:])]


def matrix_det(a):
    if len(a) == 2:
        return a[0][0] * a[1][1] - a[0][1] * a[1][0]

    det = 0.0
    for c in range(len(a)):
        det += ((-1) ** c) * a[0][c] * matrix_det(matrix_minor(a, 0, c))

    return det


def matrix_inv(a):
    """
    Invert a square matrix by compouting the determinant and cofactor matrix.
    """
    det = matrix_det(a)

    if len(a) == 2:
        return matrix_constant_mult([[a[1][1], -1 * a[0][1]], [-1 * a[1][0], a[0][0]]], 1 / det)

    cofactor = []
    for r in range(len(a)):
        row = []
        for c in range(len(a)):
            minor = matrix_minor(a, r, c)
            row.append(((-1) ** (r + c)) * matrix_det(minor))
        cofactor.append(row)

    cofactor_t = transpose(cofactor)
    return matrix_constant_mult(cofactor_t, 1 / det)


def identity_matrix(size):
    """
    Create an identity matrix of size size.
    """
    identity = []
    for r in range(size):
        row = []
        for c in range(size):
            row.append(1.0 if r == c else 0.0)

        identity.append(row)

    return identity


def transpose(a):
    if sys.version_info < (3, 0):
        return map(list, zip(*a))
    return list(map(list, zip(*a)))


def angle(u, v):
    """
    Calculate the angle between two non-zero vectors.
    :return: The angle between them in radians.
    """
    d = magnitude(u) * magnitude(v)
    return math.acos(dot(u, v) / d)


def euler_to_rotation_matrix(euler_angles):
    """
    From Zinc graphics_library.cpp, with matrix transposed to row major.
    Matrix is product RzRyRx, giving rotation about x, then y, then z with
    positive angles rotating by right hand rule about axis.
    :param euler_angles: 3 angles in radians, components:
    0 = azimuth (about z)
    1 = elevation (about y)
    2 = roll (about x)
    :return: 3x3 rotation matrix suitable for pre-multiplying vector v:
    i.e. v' = Mv
    """
    cos_azimuth = cos(euler_angles[0])
    sin_azimuth = sin(euler_angles[0])
    cos_elevation = cos(euler_angles[1])
    sin_elevation = sin(euler_angles[1])
    cos_roll = cos(euler_angles[2])
    sin_roll = sin(euler_angles[2])
    mat3x3 = [
        [cos_azimuth * cos_elevation, cos_azimuth * sin_elevation * sin_roll - sin_azimuth * cos_roll, cos_azimuth * sin_elevation * cos_roll + sin_azimuth * sin_roll],
        [sin_azimuth * cos_elevation, sin_azimuth * sin_elevation * sin_roll + cos_azimuth * cos_roll, sin_azimuth * sin_elevation * cos_roll - cos_azimuth * sin_roll],
        [-sin_elevation, cos_elevation * sin_roll, cos_elevation * cos_roll]]
    return mat3x3


def rotation_matrix_to_euler(matrix):
    """
    From Zinc graphics_library.cpp, with matrix transposed to row major.
    Inverse function to euler_to_rotation_matrix.
    """
    MATRIX_TO_EULER_TOLERANCE = 1.0E-12
    euler_angles = [0.0, 0.0, 0.0]
    if fabs(matrix[0][0]) > MATRIX_TO_EULER_TOLERANCE:
        euler_angles[0] = atan2(matrix[1][0], matrix[0][0])
        euler_angles[2] = atan2(matrix[2][1], matrix[2][2])
        euler_angles[1] = atan2(-matrix[2][0], matrix[0][0] / cos(euler_angles[0]))
    elif fabs(matrix[0][1]) > MATRIX_TO_EULER_TOLERANCE:
        euler_angles[0] = atan2(matrix[1][0], matrix[0][0])
        euler_angles[2] = atan2(matrix[2][1], matrix[2][2])
        euler_angles[1] = atan2(-matrix[2][0], matrix[1][0] / sin(euler_angles[0]))
    else:
        euler_angles[1] = atan2(-matrix[2][0], 0)  # get +/-1
        euler_angles[0] = 0
        euler_angles[2] = atan2(-matrix[1][2], -matrix[0][2] * matrix[2][0])
    return euler_angles


def axis_angle_to_quaternion(axis, theta):
    """
    :param axis: Unit vector axis of rotation.
    :param theta: Angle of rotation in right hand sense around axis, in radians.
    :return: Quaternion representing rotation.
    """
    sin_half_angle = sin(theta / 2)
    return [cos(theta / 2), axis[0] * sin_half_angle, axis[1] * sin_half_angle, axis[2] * sin_half_angle]


def axis_angle_to_rotation_matrix(axis, theta):
    """
    Convert axis angle to a rotation matrix.

    :param axis: Unit vector axis of rotation.
    :param theta: Angle of rotation in right hand sense around axis, in radians.
    :return: 3x3 rotation matrix suitable for pre-multiplying vector v: i.e. v' = Mv
    """
    axis = div(axis, sqrt(dot(axis, axis)))
    a = cos(theta / 2.0)
    b, c, d = mult(axis, -sin(theta / 2.0))
    aa, bb, cc, dd = a * a, b * b, c * c, d * d
    bc, ad, ac, ab, bd, cd = b * c, a * d, a * c, a * b, b * d, c * d
    return [[aa + bb - cc - dd, 2 * (bc + ad), 2 * (bd - ac)],
            [2 * (bc - ad), aa + cc - bb - dd, 2 * (cd + ab)],
            [2 * (bd + ac), 2 * (cd - ab), aa + dd - bb - cc]]


def reshape(a, new_shape):
    b = []
    if isinstance(new_shape, tuple):
        index = 0
        for x in range(new_shape[0]):
            row = []
            for y in range(new_shape[1]):
                row.append(a[index])
                index += 1
            b.append(row)
    elif isinstance(new_shape, int):
        flat_list = [item for sublist in a for item in sublist]
        if 0 <= new_shape < len(flat_list):
            b = flat_list[:new_shape]
        else:
            b = flat_list

    return b


# legacy function names
rotmx = quaternion_to_rotation_matrix
mxconstantmult = matrix_constant_mult
mxvectormult = matrix_vector_mult
vectormxmult = vectormatrixmult = vector_matrix_mult
mxmult = matrixmult = matrix_mult
eulerToRotationMatrix3 = euler_to_rotation_matrix
rotationMatrix3ToEuler = rotation_matrix_to_euler
axisAngleToQuaternion = axis_angle_to_quaternion
axisAngleToRotationMatrix = axis_angle_to_rotation_matrix
