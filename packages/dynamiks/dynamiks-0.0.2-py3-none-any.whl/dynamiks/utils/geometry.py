import numpy as np


def get_xyz(east_north_height, wind_direction, center_offset):
    if wind_direction == 270:
        return np.asarray(east_north_height)
    theta = np.deg2rad(wind_direction - 270)
    c, s = np.cos(theta), np.sin(theta)
    center_offset = center_offset.reshape((3,) + (1,) * len(np.shape(east_north_height)[1:]))
    e, n, h = east_north_height - center_offset
    return np.array([c * e - s * n, c * n + s * e, h]) + center_offset


def get_east_north_height(xyz, wind_direction, center_offset):
    if wind_direction == 270:
        return np.asarray(xyz)
    return get_xyz(xyz, -wind_direction + 180, center_offset)
