'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys
import pygame
import math
import numpy
import random
import time
import copy
import operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the path network as a list of lines between all path nodes that are traversable by the agent.


def myBuildPathNetwork(pathnodes, world, agent=None):
    lines = []
    ### YOUR CODE GOES BELOW HERE ###
    maxRadius = agent.getMaxRadius()
    linesCopy = []
    for i in range(len(pathnodes)):
        drawCross(world.debug, pathnodes[i], size=4)

    counter = 0
    # Finding all distinct lines between two pathnodes (assuming not on same line)
    for i, point in enumerate(pathnodes):
        for j in range(i+1, len(pathnodes)):
            counter += 1
            linesCopy.append((point, pathnodes[j]))

    lines = copy.deepcopy(linesCopy)
    for i in range(len(linesCopy)):
        p1 = linesCopy[i][0]
        p2 = linesCopy[i][1]
        for obs in world.getObstacles():
            if (rayTraceWorld(p1, p2, obs.getLines())):
                try:
                    lines.remove((p1, p2))
                except:
                    pass
            for obsPoint in obs.getPoints():
                if(minimumDistance((p1, p2), obsPoint) < maxRadius):
                    try:
                        lines.remove((p1, p2))
                    except:
                        pass
    ### YOUR CODE GOES ABOVE HERE ###
    return lines
