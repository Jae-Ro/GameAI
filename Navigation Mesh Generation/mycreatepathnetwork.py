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

import numpy as np

# Creates a path node network that connects the midpoints of each nav mesh together


def myCreatePathNetwork(world, agent=None):
    nodes = []
    edges = []
    polys = []
    ### YOUR CODE GOES BELOW HERE ###

    worldPoints = world.getPoints()

    obstaclePoints = []
    for obs in world.getObstacles():
        for point in obs.getPoints():
            # print(point)
            obstaclePoints.append(point)

    worldCorners = list(set(worldPoints) - set(obstaclePoints))
    obstacleLines = world.getLinesWithoutBorders()

    testPolys = []
    polyLines = []
    lineArr = []

    # Drawing all possible lines that don't cross any obstacles
    for p1 in worldPoints:
        for p2 in worldPoints:
            validLine = True
            if (len(set({p1, p2})) < 2):
                validLine = False
            else:
                line = (p1, p2)
                # drawLine(p1, p2, world.debug)

                if (rayTraceWorldNoEndPoints(p1, p2, world.getLinesWithoutBorders())):
                    validLine = False
                else:
                    for obs in world.getObstacles():
                        if(pointInsidePolygonLines(midPoint(p1, p2), obs.getLines())):
                            validLine = False

                if(validLine):
                    if ((distance(p1, p2), line) in lineArr):
                        pass
                    else:
                        lineArr.append((distance(p1, p2), line))

    # Sorting all the lines by distance in ASC order
    lineArr.sort()
    # print(len(lineArr))
    distinctLineArr = []

    # Getting rid of duplicate backwards lines (ex. (p1,p2) == (p2,p1))
    for i in range(len(lineArr)):
        line1 = lineArr[i]
        # print(lineArr[i])
        for j in range(i+1, len(lineArr)):
            line2 = lineArr[j]
            # print(lineArr[i], lineArr[j])
            if(set(line1[1]) == set(line2[1])):
                if(line2 not in distinctLineArr):
                    distinctLineArr.append(line2)
    # print(len(distinctLineArr))

    justLinesTest = []
    uniqueLines = []

    # Getting rid of line intersections
    for i in range(len(distinctLineArr)):
        line = distinctLineArr[i]
        # drawLine(line[1][0], line[1][1], world.debug, color=(255, 0, 0))
        if(rayTraceWorldNoEndPoints(line[1][0], line[1][1], justLinesTest)):
            pass
        else:
            # print(line)
            uniqueLines.append(line)
            justLinesTest.append(line[1])
            # drawLine(line[1][0], line[1][1], world.debug, color=(255, 0, 0))

    # Adding obstacle lines to our list of lines
    justLines = justLinesTest
    for line in world.getLines():
        justLines.append(line)

    # print(len(uniqueLines))

    # Iterating through our unique lines list that does not include obstacle lines
    # Making Triangles out of Lines
    for i in range(len(uniqueLines)):
        line = uniqueLines[i]
        # print("LINE 1: ", line)
        # drawLine(line[1][0], line[1][1], world.debug, color=(255, 0, 0))
        for j in range(i+1, len(uniqueLines)):
            nextLine = uniqueLines[j]
            # print("NextLINE: ", nextLine)

            p1L1 = line[1][0]
            p2L1 = line[1][1]
            p1L2 = nextLine[1][0]
            p2L2 = nextLine[1][1]

            p1L1 = (int(p1L1[0]), int(p1L1[1]))
            p2L1 = (int(p2L1[0]), int(p2L1[1]))
            p1L2 = (int(p1L2[0]), int(p1L2[1]))
            p2L2 = (int(p2L2[0]), int(p2L2[1]))

            # Finding Intersection point between line and nextLine
            intersectPoint = calculateIntersectPoint(p1L1, p2L1, p1L2, p2L2)
            if (intersectPoint):
                intersectPoint = (
                    round(intersectPoint[0]), round(intersectPoint[1]))
            # print("IntersectPoint: ", intersectPoint)

            # If the intersection point is an endpoint of line, lets look for third line to complete triangle
            if (intersectPoint == line[1][0] or intersectPoint == line[1][1]):
                if (intersectPoint == line[1][0]):
                    interL1 = line[1][0]
                    nonInterL1 = line[1][1]
                elif(intersectPoint == line[1][1]):
                    interL1 = line[1][1]
                    nonInterL1 = line[1][0]
                validL2 = nextLine
                # print("Line 1: ", line[1], "Line 2: ", validL2[1])
                if (validL2[1][0] == intersectPoint):
                    nonIntersectPoint = validL2[1][1]
                elif (validL2[1][1] == intersectPoint):
                    nonIntersectPoint = validL2[1][0]

                # print ("NonIntersectPoint: ", nonIntersectPoint)
                potentialThirdLine = list(
                    set([nonIntersectPoint, nonInterL1]))
                # print("PotentialThirdLine: ", potentialThirdLine)

                if (len(potentialThirdLine) != 2):
                    pass
                else:
                    # print("length is good")
                    l3v1 = (potentialThirdLine[0], potentialThirdLine[1])
                    l3v2 = (potentialThirdLine[1], potentialThirdLine[0])
                    if (l3v1 in justLines and l3v1 != line[1] and l3v1 != validL2[1]):

                        validL3 = (
                            potentialThirdLine[0], potentialThirdLine[1])
                        # print("l3v1 is good:", l3v1)
                    elif (l3v2 in justLines and l3v2 != line[1] and l3v2 != validL2[1]):
                        validL3 = (
                            potentialThirdLine[1], potentialThirdLine[0])
                        # print("l3v1 is good:", l3v1)
                    else:
                        validL3 = None

                    if (line and validL2 and validL3):
                        # print(line[1], validL2[1], validL3)
                        triangle = tuple(
                            set([line[1][0], line[1][1], validL2[1][0], validL2[1][1], validL3[0], validL3[1]]))
                        # print ("TRIANGLE: ", triangle)
                        triangle = list(set(triangle))
                        triangle.sort()
                        triangle = tuple(triangle)
                        if (triangle not in polys):

                            polys.append(triangle)

                            if(line[1] in world.getLines()):
                                firstLines = line[1]
                            else:
                                firstLine = list(line[1])
                                firstLine.sort()
                                firstLine = tuple(firstLine)
                            if(validL2[1] in world.getLines()):
                                secondLine = validL2[1]
                            else:
                                secondLine = list(validL2[1])
                                secondLine.sort()
                                secondLine = tuple(secondLine)
                            if(validL3 in world.getLines()):
                                thirdLine = validL3
                            else:
                                thirdLine = list(validL3)
                                thirdLine.sort()
                                thirdLine = tuple(thirdLine)

                            if (firstLine not in polyLines and firstLine not in world.getLines()):
                                polyLines.append(firstLine)
                            if(secondLine not in polyLines and secondLine not in world.getLines()):
                                polyLines.append(secondLine)
                            if(thirdLine not in polyLines and thirdLine not in world.getLines()):
                                polyLines.append(thirdLine)

    # Finding the center of each polygon
    for poly in polys:
        node = centerOfPolygon(poly)
        # drawCross(world.debug, node, color=(255, 0, 0))
        nodes.append(node)

    # Finding the portals between each polygon
    for line in polyLines:
        # print(line)
        if (line not in world.getLines()):
            portalMark = midPoint(line[0], line[1])
            # drawCross(world.debug, portalMark, color=(255, 0, 0))
            nodes.append(portalMark)

    print(len(polys))
    print(len(polyLines))

    testPolys = polys
    testPolys.sort()
    # for poly in polys:
    #     if (poly not in testPolys):
    #         poly = list(set(poly))
    #         poly.sort()
    #         poly = tuple(poly)
    #         testPolys.append(poly)

    # testPolys = list(set(testPolys))
    # testPolys.sort()

    print(len(testPolys))

    # Merging Triangles to form 4-sided polygons
    quadPolys = copy.deepcopy(testPolys)
    finalLines = []
    for i in range(len(testPolys)):
        p1 = testPolys[i]
        for j in range(i+1, len(testPolys)):
            p2 = testPolys[j]
            if (polygonsAdjacent(p1, p2)):
                # print(p1, p2)
                p1s1 = [p1[0], p1[1]]
                p1s2 = [p1[1], p1[2]]
                p1s3 = [p1[2], p1[0]]

                p2s1 = [p2[0], p2[1]]
                p2s2 = [p2[1], p2[2]]
                p2s3 = [p2[2], p2[0]]

                p1s1.sort()
                p1s2.sort()
                p1s3.sort()

                p2s1.sort()
                p2s2.sort()
                p2s3.sort()

                p1s1 = tuple(p1s1)
                p1s2 = tuple(p1s2)
                p1s3 = tuple(p1s3)

                p2s1 = tuple(p2s1)
                p2s2 = tuple(p2s2)
                p2s3 = tuple(p2s3)

                uneditedLines = [p1s1, p1s2, p1s3, p2s1, p2s2, p2s3]

                # What could be a valid quadrilateral
                setPoints = list(
                    set([p1[0], p1[1], p1[2], p2[0], p2[1], p2[2]]))
                setPoints.sort()

                if (rayTraceWorldNoEndPoints(setPoints[0], setPoints[1], world.getLinesWithoutBorders()) or rayTraceWorldNoEndPoints(setPoints[1], setPoints[2], world.getLinesWithoutBorders()) or rayTraceWorldNoEndPoints(setPoints[0], setPoints[2], world.getLinesWithoutBorders())):
                    pass
                else:
                    if(isConvex(setPoints)):
                        try:
                            # remove the two original triangles
                            quadPolys.remove(p1)
                            quadPolys.remove(p2)

                            # append the new quad polygon
                            quadPolys.append(setPoints)
                        except:
                            pass

    finalPolys = []
    for poly in quadPolys:
        if (poly not in finalPolys):
            poly = list(set(poly))
            poly.sort()
            poly = tuple(poly)
            finalPolys.append(poly)

    finalPolys = list(set(finalPolys))
    finalPolys.sort()
    print(len(finalPolys))

    nodes = []
    polys = finalPolys
    for poly in finalPolys:
        node = centerOfPolygon(poly)
        # drawCross(world.debug, node, color=(255, 0, 0))
        nodes.append(node)

    realFinalLines = []
    for poly in finalPolys:
        # print(poly)
        n = len(poly)
        sides = []

        if (n == 3):
            s1 = (poly[0], poly[1])
            s2 = (poly[1], poly[2])
            s3 = (poly[2], poly[0])
            sides = [s1, s2, s3]

        elif(n == 4):
            s1 = (poly[0], poly[1])
            s2 = (poly[1], poly[2])
            s3 = (poly[2], poly[3])
            s4 = (poly[3], poly[0])
            sides = [s1, s2, s3, s4]

        for line in sides:
            lineAlt = (line[1], line[0])
            if (line not in world.getLines() and lineAlt not in world.getLines()):

                if(line not in realFinalLines and lineAlt not in realFinalLines):
                    realFinalLines.append(line)

    portals = []

    for line in realFinalLines:
        drawLine(line[0], line[1], world.debug, color=(255, 0, 0))
        portalMark = midPoint(line[0], line[1])
        drawCross(world.debug, portalMark, color=(255, 0, 0))
        portals.append(portalMark)
        nodes.append(portalMark)

    print("final Lines", len(realFinalLines))

    print(len(nodes))

    edgesPre = []
    for i in range(len(portals)):
        node1 = portals[i]
        print(node1)
        # drawCross(world.debug, node1, color=(255, 0, 0))
        for j in range(i+1, len(portals)):
            node2 = portals[j]
            if (rayTraceWorldNoEndPoints(node1, node2, world.getLinesWithoutBorders())):
                pass
            else:
                edge = (node1, node2)
                edgeAlt = (node2, node1)

                if(edge not in edgesPre and edgeAlt not in edgesPre):
                    edgesPre.append(edge)
                # drawLine(node1, node2, world.debug, color=(255, 0, 0))

    edgesPost = []
    edgesPost = copy.deepcopy(edgesPre)

    for edge in edgesPre:
        for obs in world.getObstacles():
            maxRadius = agent.getMaxRadius()
            if (rayTraceWorld(edge[0], edge[1], obs.getLines())):
                try:
                    edgesPost.remove(edge)
                except:
                    pass
            for obsPoint in obs.getPoints():
                if(minimumDistance(edge, obsPoint) < maxRadius):
                    try:
                        edgesPost.remove(edge)
                    except:
                        pass

    completeEdges = []
    edgesPost = list(set(edgesPost))

    for edge in edgesPost:
        if (rayTraceWorldNoEndPoints(edge[0], edge[1], completeEdges)):
            pass
        else:
            intersectPoint = rayTraceWorldNoEndPoints(
                edge[0], edge[1], realFinalLines)
            if(intersectPoint):
                intersectPoint = (
                    int(round(intersectPoint[0])), int(round(intersectPoint[1])))

                if(intersectPoint in portals):
                    print(edge, intersectPoint, "GOOD EDGE")
                    completeEdges.append(edge)
                else:
                    print(edge, intersectPoint, "BAD EDGE")

    edges = completeEdges
    # print(nodes)
    polys = []
    return nodes, edges, polys


def drawLine(p1, p2, screen, color=(0, 255, 0), width=1, center=False):
    pygame.draw.line(screen, color, p1, p2, width)


def midPoint(p1, p2):
    return ((p1[0] + p2[0])/2, (p1[1] + p2[1])/2)


def calcLegLength(hyp):
    leg = hyp/math.sqrt(2)


def calcSlope(p1, p2):
    numerator = float(-p2[1]) - float(-p1[1])
    denominator = float(p2[0]) - float(p1[0])

    if (denominator == 0):
        slope = float("inf")
    else:
        slope = numerator/denominator

    return slope


def findPointOnLine(center, point, m, d):
    errorMargin = 0.000001

    px = point[0]
    py = point[1]

    if (m == 0):  # horizontal line
        if (point[0] > center[0]):  # lies to the right
            px = point[0] - d
            py = point[1]
        else:  # lies to the left
            px = point[0] + d
            py = point[1]
    elif(m == float("inf")):  # vertical line
        if (point[1] > center[1]):  # lies above
            py = point[1] - d
            px = point[0]
        else:  # lies below
            py = point[1] + d
            px = point[0]
    else:  # all other cases

        m2PlusOne = 1 + m**2
        dx = d / math.sqrt(m2PlusOne)
        dy = dx*abs(m)
        # print(m, dx, dy)
        if (point[0] < center[0]):  # lies left
            px = point[0] + dx
        else:  # lies right
            px = point[0] - dx
        if (point[1] > center[1]):
            py = point[1] - dy
        else:
            py = point[1] + dy

    return (px, py)


def cornersPolygon(polygon, agent):
    agentRadius = agent.getMaxRadius()
    d = agentRadius + 0.1

    points = []
    for corner in polygon:
        polyCenter = centerOfPolygon(polygon)
        m = calcSlope(corner, polyCenter)
        bufferPoint = findPointOnLine(polyCenter, corner, m, d)
        # print(polyCenter, corner, m, bufferPoint)
        points.append(bufferPoint)
    return points


def centerOfPolygon(polygon):
    distanceArr = []
    midPointsArr = []
    xSum = 0
    ySum = 0
    for point in polygon:
        x = point[0]
        y = point[1]
        xSum += x
        ySum += y

    xCenter = xSum/len(polygon)
    yCenter = ySum/len(polygon)

    return (xCenter, yCenter)
