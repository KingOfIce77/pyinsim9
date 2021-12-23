# func.py - helper functions module for pyinsim
#
# Copyright 2008-2020 Alex McBride <xandermcbride@gmail.com>
#
# This software may be used and distributed according to the terms of the
# GNU Lesser General Public License version 3 or any later version.
#

import math
import re
import struct

import pyinsim.strmanip as strmanip

# import numpy as np


_COLOUR_REGEX = re.compile(r'\^[0-9]')
_ENC_REGEX = re.compile(r'\^[LETBJCGHSK]')
_ENC_COL_REGEX = re.compile(r'\^[LETBJCGHSK0-9]')

def stripcols(str_):
    """Strip color codes (^3, ^7 etc..) from a string."""
    return _COLOUR_REGEX.sub('', str_)

def stripenc(str_, cols=True):
    """Strip encoding markers (^L, ^E etc..) from a string. Note: a string 
    stripped of encoding markers cannot be converted to unicode."""
    if cols:
        return _ENC_REGEX.sub('', str_)        
    return _ENC_COL_REGEX.sub('', str_)

def tounicode(str_, cols=True, default='L'):
    """Convert a LFS encoded string to unicode."""
    return strmanip.toUnicode(str_, default, cols)

def fromunicode(ustr, default='L'):
    """Convert a uncode string to a LFS encoded string."""
    return strmanip.fromUnicode(ustr, default)

def time(ms):
    """Convert milliseconds into hours, minutes, seconds and thousanths.   """
    h = ms // 3600000
    m = ms // 60000 % 60
    s = ms // 1000 % 60
    t = ms % 1000
    return [h, m, s, t]

def timestr(ms, hours=False):
    """Convert milliseconds into a formatted time string (e.g. h:mm:ss.ttt)."""
    h, m, s, t = time(ms)
    if h or hours:
        #return '%d.%.2d:%.2d.%.3d' % (h, m, s, t)
        return '{0:}.{1:02d}:{2:02d}.{3:03d}'.format(h, m, s, t)
    #return '%d:%.2d.%.3d' % (m, s, t)
    return '{0:2d}:{1:02d}.{2:03d}'.format(m, s, t)

def mps(speed):
    """Convert speed to meters per second."""
    return speed / 327.68

def mph(speed=0, mps=0):
    """Convert speed to miles per hour."""
    if mps:
        return mps * 2.23
    return speed / 146.486067

def kph(speed=0, mps=0):
    """Convert speed to kilometers per hour."""
    if mps:
        return mps * 3.6
    return speed / 91.0222222

def length(length):
    """Convert LFS length into meters."""
    return length / 65536.0

def miles(length):
    """Convert length to miles."""
    return length(length) / 1609.344

def km(length):
    """Convert length to kilometers."""
    return length(length) / 1000.0

def deg(radians):
    """Convert radians to degrees."""
    return radians * 57.295773

def rad(degrees):
    """Convert degrees to radians."""
    return degrees * 0.01745329

def normalize_angle(angle):
    angle = angle % (2 * math.pi)
    if angle > math.pi:
        angle -= 2 * math.pi
    if angle < -math.pi:
        angle += 2 * math.pi
    return angle


def rpm(radians):
    """Convert radians to RPM."""
    return radians * 9.549295

def dist(a=(0,0,0), b=(0,0,0)):
    """Determine the distance between two points."""
    return math.sqrt((b[0] - a[0]) * (b[0] - a[0]) + (b[1] - a[1]) * (b[1] - a[1]) + (b[2] - a[2]) * (b[2] - a[2]))

def intersects(a=(0, 0, 0, 0), b=(0, 0, 0, 0)):
    """Determine if two rectangles are intersecting."""
    x1 = a[0] + a[2]
    y1 = a[1] + a[3]
    x3 = b[0] + b[2]
    y3 = b[1] + b[3]
    return not (x1 < b[0] or x3 < a[0] or y1 < b[1] or y3 < a[1])

#def world_to_local(world_vector: np.ndarray, pitch: float, roll: float, yaw: float):
    """
    Function to transform world_vector to local_vector using the Euler angles
    and 3D affine transformation. Uses the 3x3 matrix form because only rotation is
    required.

    Credit: https://www.lfs.net/forum/post/1961008#post1961008

    Args:
        world_vector (np.ndarray): The world vector to be transformed
        pitch (float): The pitch of the car
        roll (float): The roll of the car
        yaw (float): The yaw of the car (don't forget outsim provides the heading
        pointing to the right, not straight ahead)

    Returns:
        np.ndarray: The local transformed vector
    """

    """
    sin_roll, cos_roll = np.sin(roll), np.cos(roll)
    sin_pitch, cos_pitch = np.sin(pitch), np.cos(pitch)
    sin_yaw, cos_yaw = np.sin(yaw), np.cos(yaw)

    local_vector = np.empty(3)

    # Total rotation matrix row 1 * world_vector
    local_vector[0] = (
        cos_roll * cos_yaw * world_vector[0]
        + (cos_pitch * sin_yaw + sin_pitch * sin_roll * cos_yaw) * world_vector[1]
        + (sin_pitch * sin_yaw - cos_pitch * sin_roll * cos_yaw) * world_vector[2]
    )

    # Total rotation matrix row 2 * world_vector
    local_vector[1] = (
        -cos_roll * sin_yaw * world_vector[0]
        + (cos_pitch * cos_yaw - sin_pitch * sin_roll * sin_yaw) * world_vector[1]
        + (sin_pitch * cos_yaw + cos_pitch * sin_roll * sin_yaw) * world_vector[2]
    )

    # Total rotation matrix row 3 * world_vector
    local_vector[2] = (
        sin_roll * world_vector[0]
        - sin_pitch * cos_roll * world_vector[1]
        + cos_pitch * cos_roll * world_vector[2]
    )

    return local_vector
    """


_PTH_HEADER = b'LFSPTH'
_PTH_VERSION = 0
_PTH_REVISION = 0
_PTH_HEADER_STRUCT = struct.Struct('6s2B2i')
_PTH_NODE_STRUCT = struct.Struct('3i7f')


class PthException(Exception):
    pass


class _Node:
    def __init__(self, file):
        data = _PTH_NODE_STRUCT.unpack(file.read(_PTH_NODE_STRUCT.size))
        self.X = data[0]
        self.Y = data[1]
        self.Z = data[2]
        self.DirX = data[3]
        self.DirY = data[4]
        self.DirZ = data[5]
        self.LimitLeft = data[6]
        self.LimitRight = data[7]
        self.DriveLeft = data[8]
        self.DriveRight = data[9]


class Pth:
    def __init__(self, path):
        with open(path, 'rb') as file:
            data = _PTH_HEADER_STRUCT.unpack(file.read(_PTH_HEADER_STRUCT.size))

            # Read header.
            if data[0] != _PTH_HEADER:
                raise PthException('Invalid header')
            if data[1] != _PTH_VERSION:
                raise PthException('Invalid version')
            if data[2] != _PTH_REVISION:
                raise PthException('Invalid revision')
            self.path = path
            self.numNodes = data[3]
            self.finishLine = data[4]

            # Read nodes.
            self.nodes = []
            for i in range(self.numNodes):
                self.nodes.append(_Node(file))


if __name__ == '__main__':
    #print [d for d in dir() if not d.startswith('_') and d not in ('re', 'math', 'strmanip')]    
    pass

