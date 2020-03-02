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
from moba import *


class MyMinion(Minion):

    def __init__(self, position, orientation, world, image=NPC, speed=SPEED, viewangle=360, hitpoints=HITPOINTS, firerate=FIRERATE, bulletclass=SmallBullet):
        Minion.__init__(self, position, orientation, world, image,
                        speed, viewangle, hitpoints, firerate, bulletclass)
        self.states = [Idle, Taunt, Move,
                       Attack_Structure, Attack_Enemy]

        # Add your states to self.states (but don't remove Idle)
        ### YOUR CODE GOES BELOW HERE ###

        ### YOUR CODE GOES ABOVE HERE ###

    def start(self):
        Minion.start(self)
        self.changeState(Idle)


############################
# Idle
###
# This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):

    def enter(self, oldstate):
        State.enter(self, oldstate)
        # stop moving
        self.agent.stopMoving()

    def execute(self, delta=0):
        State.execute(self, delta)
        self.agent.changeState(Move, 0)

    def exit(self):
        # print("moving from Idle")
        pass
        ##############################
        # Taunt
        ###
        # This is a state given as an example of how to pass arbitrary parameters into a State.
        # To taunt someome, Agent.changeState(Taunt, enemyagent)


class Taunt(State):

    def parseArgs(self, args):
        self.victim = args[0]
        # print(self.victim)

    def execute(self, delta=0):
        if self.victim is not None:
            print("Hey " + str(self.victim) + ", I don't like you!")
        self.agent.changeState(Move)

##############################
# YOUR STATES GO HERE:


class Move(State):

    def parseArgs(self, args):

        self.myTeamFlag = self.agent.getTeam()

        self.bases = self.agent.world.getEnemyBases(self.myTeamFlag)
        self.towers = self.agent.world.getEnemyTowers(self.myTeamFlag)

        self.enemy_buildings = []
        if(len(self.enemy_buildings) <= 1):
            for base in self.bases:
                self.enemy_buildings.append(base)

            for tower in self.towers:
                self.enemy_buildings.append(tower)

        if args[0] < 0:
            self.target = self.bases[0].position
        elif args[0] == 0:
            self.target = random.choice(self.enemy_buildings).position
        else:
            self.target = args[0]

    def enter(self, oldstate):
        self.prevPosition = (0, 0)
        self.prevPosition2 = (0, 0)
        self.prevPosition3 = (0, 0)

        self.myTeam = self.agent.world.getNPCsForTeam(self.myTeamFlag)

        if self.target is not None:

            self.agent.navigateTo(self.target)

    def execute(self, delta=0):
        State.execute(self, delta)
        pos = self.agent.position

        # REPLANNING PATH IN CASE OF OBSTACLES OR GETTING STUCK
        if (pos == self.prevPosition and pos == self.prevPosition2 and pos == self.prevPosition3):
            # self.agent.changeState(Idle)
            self.agent.changeState(Move, 0)
        else:
            self.prevPosition3 = self.prevPosition2
            self.prevPosition2 = self.prevPosition
            self.prevPosition = pos

        # CHANGING STATE TO ATTACK ENEMY
        for npc in self.agent.world.npcs:
            if npc.getTeam() == None or npc.getTeam() != self.agent.getTeam() and distance(self.agent.getLocation(), npc.getLocation()) < SMALLBULLETRANGE:
                self.agent.changeState(Attack_Enemy)

        # CHANGING STATE TO ATTACK STRUCTURE
        closest_building = sorted(self.enemy_buildings, key=lambda x: distance(
            self.agent.getLocation(), x.position))
        if distance(self.agent.getLocation(), closest_building[0].position) < SMALLBULLETRANGE:
            self.agent.changeState(Attack_Structure)

    def exit(self):
        pass


class Attack_Enemy(State):

    def enter(self, oldstate):
        self.myTeamFlag = self.agent.getTeam()
        self.myTeam = self.agent.world.getNPCsForTeam(self.myTeamFlag)

    def execute(self, delta=0):
        State.execute(self, delta)
        enemyTargets = []

        for npc in self.agent.world.npcs:
            if npc.getTeam() == None or npc.getTeam() != self.agent.getTeam() and distance(self.agent.getLocation(), npc.getLocation()) < SMALLBULLETRANGE:
                hit = rayTraceWorld(self.agent.getLocation(
                ), npc.getLocation(), self.agent.world.getLines())

                if hit == None:
                    enemyTargets.append(npc)

        minions = sorted(enemyTargets, key=lambda x: distance(
            self.agent.getLocation(), x.getLocation()))

        if len(minions) > 0:
            self.agent.turnToFace(minions[0].getLocation())
            self.agent.shoot()
            self.agent.changeState(Move, -1)
        else:
            self.agent.changeState(Move, -1)

    def exit(self):
        pass


class Attack_Structure(State):

    def enter(self, oldstate):
        self.myTeamFlag = self.agent.getTeam()

        self.bases = self.agent.world.getEnemyBases(self.myTeamFlag)
        self.towers = self.agent.world.getEnemyTowers(self.myTeamFlag)

        self.enemy_buildings = []
        if(len(self.enemy_buildings) <= 1):
            for base in self.bases:
                self.enemy_buildings.append(base)
            for tower in self.towers:
                self.enemy_buildings.append(tower)

    def execute(self, delta=0):
        State.execute(self, delta)

        building_targets = []
        for structure in self.enemy_buildings:
            if distance(self.agent.getLocation(), structure.position) < SMALLBULLETRANGE:
                hit = rayTraceWorld(self.agent.getLocation(
                ), structure.position, self.agent.world.getLines())
                if hit == None:
                    building_targets.append(structure)

        targets = sorted(building_targets, key=lambda x: distance(
            self.agent.getLocation(), x.position))

        if len(targets) > 0:
            self.agent.turnToFace(targets[0].position)
            dist = distance(self.agent.getLocation(), targets[0].position)
            self.agent.shoot()

            self.agent.changeState(Move, -1)

    def exit(self):
        pass
