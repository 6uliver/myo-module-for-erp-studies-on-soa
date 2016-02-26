import math
from collections import namedtuple

Quaternion = namedtuple('Quaternion', 'w x y z')
Euler = namedtuple('Euler', 'x y z')

def quaternion_to_euler(q):
    sqw = q.w * q.w
    sqx = q.x * q.x
    sqy = q.y * q.y
    sqz = q.z * q.z

    normal = math.sqrt(sqw + sqx + sqy + sqz)
    pole_result = (q.x * q.z) + (q.y * q.w)

    if (pole_result > (0.5 * normal)): # singularity at north pole
        ry = math.pi/2 #heading/yaw?
        rz = 0 #attitude/roll?
        rx = 2 * math.atan2(q.x, q.w) #bank/pitch?
        return Euler(rx, ry, rz)
    if (pole_result < (-0.5 * normal)): # singularity at south pole
        ry = -math.pi/2
        rz = 0
        rx = -2 * math.atan2(q.x, q.w)
        return Euler(rx, ry, rz)

    r11 = 2*(q.x*q.y + q.w*q.z)
    r12 = sqw + sqx - sqy - sqz
    r21 = -2*(q.x*q.z - q.w*q.y)
    r31 = 2*(q.y*q.z + q.w*q.x)
    r32 = sqw - sqx - sqy + sqz

    rx = math.atan2( r31, r32 )
    ry = math.asin ( r21 )
    rz = math.atan2( r11, r12 )

    return Euler(rx, ry, rz)

class MyoMouse:
    def __init__(self, scale=[1,1]):
        self.scale = scale
        self._onPosition = None
        self.lastX = None
        self.lastY = None
        self.x = 0.5
        self.y = 0.5

    def reset(self):
        self.lastX = None
        self.lastY = None
        self.x = 0.5
        self.y = 0.5

    def onPosition(self, callback):
        self._onPosition = callback

    def onOrientation(self, coords):
        angles = quaternion_to_euler(Quaternion(coords['w'], coords['x'], coords['y'], coords['z']))
        x = angles.z
        y = angles.y

        if self.lastY == None:
            self.lastY = y
        diff = (y - self.lastY) * self.scale[0]
        self.y = min(1, max(self.y + diff, 0))
        self.lastY = y

        if self.lastX == None:
            self.lastX = x
        diff = (x - self.lastX) * self.scale[1]
        self.x = min(1, max(self.x + diff, 0))
        self.lastX = x

        pos = [-(self.x-0.5), (self.y-0.5)]
        if self._onPosition:
            self._onPosition(pos)
