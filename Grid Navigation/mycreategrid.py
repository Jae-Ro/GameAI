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
from pygame.locals import *

from constants import *
from utils import *
from core import *

import csv
import pandas as pd


# Creates a grid as a 2D array of True/False values (True = traversable). Also returns the dimensions of the grid as a (columns, rows) list.


def myCreateGrid(world, cellsize):
    grid = None
    dimensions = (0, 0)
    ### YOUR CODE GOES BELOW HERE ###
    # print (world.getDimensions())
    # print (cellsize)

    worldWidth = world.getDimensions()[0]
    worldHeight = world.getDimensions()[1]
    gridWidth = worldWidth/cellsize
    gridHeight = worldHeight/cellsize

    # print (gridWidth, gridHeight)
    dimensions = (int(math.floor(gridWidth)), int(math.floor(gridHeight)))
    # print(dimensions)
    grid = [[True for x in range(dimensions[1])] for y in range(dimensions[0])]

    for i in range(dimensions[1]):
        for j in range(dimensions[0]):
            topLeft = (j*cellsize, i*cellsize)
            topRight = ((j+1)*cellsize, i*cellsize)
            bottomLeft = (j*cellsize, (i+1)*cellsize)
            bottomRight = ((j+1)*cellsize, (i+1)*cellsize)

            # print (topLeft, topRight, bottomLeft, bottomRight)
            for obs in world.getObstacles():

                # CHECKING IF CELL VERTICES IN OBSTACLE
                if (obs.pointInside(topLeft) == True or obs.pointInside(topRight) == True or obs.pointInside(bottomLeft) == True or obs.pointInside(bottomRight) == True):
                    grid[j][i] = False

                obstacleLines = obs.getLines()
                intersectPointTop = rayTraceWorldNoEndPoints(
                    topLeft, topRight, obstacleLines)
                intersectPointRight = rayTraceWorldNoEndPoints(
                    topRight, bottomRight, obstacleLines)
                intersectPointBottom = rayTraceWorldNoEndPoints(
                    bottomRight, bottomLeft, obstacleLines)
                intersectPointLeft = rayTraceWorldNoEndPoints(
                    bottomLeft, topLeft, obstacleLines)

                # CHECKING IF CELL SIDES INTERSECT OBSTACLE SIDES
                if (intersectPointTop or intersectPointRight or intersectPointBottom or intersectPointLeft):
                    grid[j][i] = False

                obstaclePoints = obs.getPoints()
                for obsPoint in obstaclePoints:
                    # CHECKING IF OBSTACLE IN CELL
                    if (pointInsidePolygonPoints(obsPoint, [topLeft, topRight, bottomLeft, bottomRight])):
                        grid[j][i] = False
    markBox(world, grid, dimensions, cellsize)

    ### YOUR CODE GOES ABOVE HERE ###
    # with open("runrandom1_Jae.csv", "w+") as my_csv:
    #     csvWriter = csv.writer(my_csv, delimiter=',')
    #     csvWriter.writerows(grid)

    return grid, dimensions


def markBox(world, grid, dimensions, cellsize):
    countF = 0
    for i in range(dimensions[1]):
        for j in range(dimensions[0]):
            if (grid[j][i] == False):
                countF += 1
                topLeftMark = (j*cellsize, i*cellsize)
                topRightMark = ((j+1)*cellsize, i*cellsize)
                bottomLeftMark = (j*cellsize, (i+1)*cellsize)
                bottomRightMark = ((j+1)*cellsize, (i+1)*cellsize)
                midWidthMark = (topRightMark[0] + topLeftMark[0])/2
                midHeightMark = (bottomRightMark[1]+topRightMark[1])/2
                midPointMark = (int(midWidthMark), int(midHeightMark))

                # print (midPointMark, grid[j][i])
                drawCross(world.debug, midPointMark)
    # print countF
