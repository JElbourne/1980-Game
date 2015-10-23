
"""
utils.py

Created by Jason Elbourne on 2014-09-17.
Copyright (c) 2014 Jason Elbourne. All rights reserved.
"""

import math

from core.config import CONFIG


def compare_coords(fromCoord, targetCoord):
    """ Use the Pythagorean Theorem to determine distance """
    dx = targetCoord[0] - fromCoord[0]
    dy = targetCoord[1] - fromCoord[1]
    distance = int(round(math.sqrt(dx**2 + dy**2)))
    return dx, dy, distance


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
        for i in range(1, rh): # return Home
            y += ss
            ringCoords.append((int(x),int(y),int(z)))

    return ringCoords


"""
Recursive shadowcasting - Björn Bergström

In octant 1 and 6 the scans are performed row by row, going from the leftmost cell to the rightmost cell in each row.
In octant 2 and 5 the scans are performed row by row, going from the rightmost cell to the leftmost cell in each row.
In octant 3 and 8 the scans are performed column by column, going from the topmost cell to the bottom most cell in each column.
In octant 4 and 7 the scans are performed column by column, going from the bottom most cell to the topmost cell in each column.

Fig.1 Area of coverage by each octant
======================
             Shared
             edge by
  Shared     1 & 2      Shared
  edge by\      |      /edge by
  1 & 8   \     |     / 2 & 3
           \1111|2222/
           8\111|222/3
           88\11|22/33
           888\1|2/333
  Shared   8888\|/3333  Shared
  edge by-------@-------edge by
  7 & 8    7777/|\4444  3 & 4
           777/6|5\444
           77/66|55\44
           7/666|555\4
           /6666|5555\
  Shared  /     |     \ Shared
  edge by/      |      \edge by
  6 & 7      Shared     4 & 5
             edge by
             5 & 6


Fig.2 Field of view
======================
 ................. 16  @ = starting cell
  ......###....... 15  # = blocking cell
   .....###....... 14  . = non-blocking cell
    ....###..#..## 13
     ...##........ 12
      ............ 11
       ........... 10
        .......... 9
         ......... 8
          ........ 7
           ....... 6
            ...... 5
             ..... 4
              .... 3
               ... 2
                .. 1
                 @


Fig.3 The first blocking cell
======================
 ................. 16  # = blocking cell
  ......###....... 15  . = non-blocking cell
   .....###....... 14
    ....###..#..## 13
     ...x#........ 12  x = first blocking cell


Fig.4 Current scans
======================
 2222............. 16  # = blocking cell
  2222..###....... 15  . = non-blocking cell
   222..###....... 14
    222.###..#..## 13  1 = original scan
     111##11111111 12  2 = new scan


Fig.5 First non-blocking cell after a blocker
======================
 ................. 16  # = blocking cell
  ......###....... 15  . = non-blocking cell
   .....###....... 14
    ....###..#..## 13
     ...##o....... 12  o = first non-blocking cell after a section of blockers


Fig.6 Starting with a blocking cell
======================
 ................. 16  # = blocking cell
  ......###....... 15  . = non-blocking cell
   .....###....... 14
    ....##x..#..## 13  x = blocking cell in original scan


Fig.7 Another blocking cell
======================
 ................. 16  # = blocking cell
  ......###....... 15  . = non-blocking cell
   .....###....... 14
    ....##...x..## 13  x = blocking cell in original scan


Fig.8 Active scans
======================
 2222......33..... 16
  2222..##333..... 15
   222..##333..... 14
    222.###11#11## 13


Fig.9 Active scans
======================
 2222......33444.. 16
  2222..##333.44.. 15
   222..##333.44.. 14
    222.##111#11## 13


======================
 ....ssssss.....ss 16  @ = starting cell
  ....ssss#..s..ss 15  # = blocking cell
   ...ssss#..s..ss 14  . = non-blocking cell
    ...ss##..#..## 13  s = shadowed cells
     ...##........ 12
      ............ 11
       ........... 10
        .......... 9
         ......... 8
          ........ 7
           ....... 6
            ...... 5
             ..... 4
              .... 3
               ... 2
                .. 1
                 @

"""



























