
"""
utils.py
"""

from core.config import CONFIG

def build_ring_coords(x, y, z, rw, rh):
    """

    x = x position of the center of the ring
    y = y position of the center of the ring

    rw = radiusWidth
    rh = radiusHeight

    ss = spriteSize

    """
    ss = CONFIG["spriteSize"]

    ringCoords = []

    x += (rw*ss)
    ringCoords.append((int(x),int(y),int(z)))
    for i in range(1,rh+1): # step up
        y += ss
        ringCoords.append((int(x),int(y),int(z)))
    for i in range(1,(rw*2)+1): # step left
        x -= ss
        ringCoords.append((int(x),int(y),int(z)))
    for i in range(1,(rh*2)+1): # step down
        y -= ss
        ringCoords.append((int(x),int(y),int(z)))
    for i in range(1,(rw*2)+1): # step right
        x += ss
        ringCoords.append((int(x),int(y),int(z)))
    if rh > 1:
        for i in range(1,rw): # return Home
            y += ss
            ringCoords.append((int(x),int(y),int(z)))

    return ringCoords

