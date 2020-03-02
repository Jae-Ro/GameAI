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
from moba2 import *
from btnode import *

###########################
# SET UP BEHAVIOR TREE


def treeSpec(agent):
    myid = str(agent.getTeam())
    spec = None
    ### YOUR CODE GOES BELOW HERE ###

    ### YOUR CODE GOES ABOVE HERE ###
    return spec


def myBuildTree(agent):
    myid = str(agent.getTeam())
    root = None
    ### YOUR CODE GOES BELOW HERE ###

    retreat = makeNode(Retreat, agent, 0.5, "retreat")
    hitpoint_daemon = makeNode(HitpointDaemon, agent, 0.5, "hitpoint_daemon")
    buff_daemon = makeNode(BuffDaemon, agent, 1, "buff_daemon")
    chase_hero = makeNode(FindHero, agent, "chase_hero")
    chase_minion = makeNode(FindMinion, agent, "chase_minion")
    kill_hero = makeNode(AttackHero, agent, "kill_hero")
    kill_minion = makeNode(AttackMinion, agent, "kill_minion")

    root = makeNode(BoosterAgent, agent, "booster_agent")
    retreat_selector = makeNode(Selector, agent, "retreat_selector")
    enemy_selector = makeNode(Selector, agent, "enemy_selector")
    hero_sequence = makeNode(Sequence, agent, "hero_sequence")
    minion_sequence = makeNode(Sequence, agent, "minon_sequence")

    root.addChild(enemy_selector)

    # retreat_selector.addChild(retreat)
    # retreat_selector.addChild(hitpoint_daemon)
    # hitpoint_daemon.addChild(enemy_selector)
    enemy_selector.addChild(buff_daemon)
    buff_daemon.addChild(hero_sequence)

    hero_sequence.addChild(chase_hero)
    hero_sequence.addChild(kill_hero)
    enemy_selector.addChild(minion_sequence)
    minion_sequence.addChild(chase_minion)
    minion_sequence.addChild(kill_minion)

    ### YOUR CODE GOES ABOVE HERE ###
    return root

# Helper function for making BTNodes (and sub-classes of BTNodes).
# type: class type (BTNode or a sub-class)
# agent: reference to the agent to be controlled
# This function takes any number of additional arguments that will be passed to the BTNode and parsed using BTNode.parseArgs()


def makeNode(type, agent, *args):
    node = type(agent, args)
    return node

###############################
# BEHAVIOR CLASSES:


class Taunt(BTNode):

    # target: the enemy agent to taunt

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the target
        if len(args) > 0:
            self.target = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target is not None:
            print "Hey", self.target, "I don't like you!"
        return ret

##################
# MoveToTarget
###
# Move the agent to a given (x, y)
# Parameters:
# 0: a point (x, y)
# 1: node ID string (optional)


class MoveToTarget(BTNode):

    # target: a point (x, y)

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the target
        if len(args) > 0:
            self.target = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def enter(self):
        BTNode.enter(self)
        self.agent.navigateTo(self.target)

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None:
            # failed executability conditions
            print "exec", self.id, "false"
            return False
        elif distance(self.agent.getLocation(), self.target) < self.agent.getRadius():
            # Execution succeeds
            print "exec", self.id, "true"
            return True
        else:
            # executing
            return None
        return ret

##################
# Retreat
###
# Move the agent back to the base to be healed
# Parameters:
# 0: percentage of hitpoints that must have been lost to retreat
# 1: node ID string (optional)


class Retreat(BTNode):

    # percentage: Percentage of hitpoints that must have been lost

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.percentage = 0.5
        # First argument is the factor
        if len(args) > 0:
            self.percentage = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def enter(self):
        BTNode.enter(self)
        base = self.agent.world.getBaseForTeam(self.agent.getTeam())
        if base:
            self.agent.navigateTo(base.getLocation())

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.agent.getHitpoints() > self.agent.getMaxHitpoints() * self.percentage:
            # fail executability conditions
            print "exec", self.id, "false"
            return False
        elif self.agent.getHitpoints() == self.agent.getMaxHitpoints():
            # Exection succeeds
            print "exec", self.id, "true"
            return True
        else:
            # executing
            return None
        return ret

##################
# ChaseMinion
###
# Find the closest minion and move to intercept it.
# Parameters:
# 0: node ID string (optional)


class ChaseMinion(BTNode):

    # target: the minion to chase
    # timer: how often to replan

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        if len(enemies) > 0:
            best = None
            dist = 0
            for e in enemies:
                if isinstance(e, Minion):
                    d = distance(self.agent.getLocation(), e.getLocation())
                    if best == None or d < dist:
                        best = e
                        dist = d
            self.target = best
        if self.target is not None:
            navTarget = self.chooseNavigationTarget()
            if navTarget is not None:
                self.agent.navigateTo(navTarget)

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or self.target.isAlive() == False:
            # failed execution conditions
            print "exec", self.id, "false"
            return False
        elif self.target is not None and distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.timer = self.timer - 1
            if self.timer <= 0:
                self.timer = 50
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
            return None
        return ret

    def chooseNavigationTarget(self):
        if self.target is not None:
            return self.target.getLocation()
        else:
            return None

##################
# KillMinion
###
# Kill the closest minion. Assumes it is already in range.
# Parameters:
# 0: node ID string (optional)


class KillMinion(BTNode):

    # target: the minion to shoot

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.agent.stopMoving()
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        if len(enemies) > 0:
            best = None
            dist = 0
            for e in enemies:
                if isinstance(e, Minion):
                    d = distance(self.agent.getLocation(), e.getLocation())
                    if best == None or d < dist:
                        best = e
                        dist = d
            self.target = best

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
            # failed executability conditions
            print "exec", self.id, "false"
            return False
        elif self.target.isAlive() == False:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.shootAtTarget()
            return None
        return ret

    def shootAtTarget(self):
        if self.agent is not None and self.target is not None:
            self.agent.turnToFace(self.target.getLocation())
            self.agent.shoot()


##################
# ChaseHero
###
# Move to intercept the enemy Hero.
# Parameters:
# 0: node ID string (optional)

class ChaseHero(BTNode):

    # target: the hero to chase
    # timer: how often to replan

    def ParseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                self.target = e
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
                return None

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or self.target.isAlive() == False:
            # fails executability conditions
            print "exec", self.id, "false"
            return False
        elif distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.timer = self.timer - 1
            if self.timer <= 0:
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
            return None
        return ret

    def chooseNavigationTarget(self):
        if self.target is not None:
            return self.target.getLocation()
        else:
            return None

##################
# KillHero
###
# Kill the enemy hero. Assumes it is already in range.
# Parameters:
# 0: node ID string (optional)


class KillHero(BTNode):

    # target: the minion to shoot

    def ParseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.agent.stopMoving()
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                self.target = e
                return None

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
            # failed executability conditions
            if self.target == None:
                print "foo none"
            else:
                print "foo dist", distance(self.agent.getLocation(), self.target.getLocation())
            print "exec", self.id, "false"
            return False
        elif self.target.isAlive() == False:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing
            self.shootAtTarget()
            return None
        return ret

    def shootAtTarget(self):
        if self.agent is not None and self.target is not None:
            self.agent.turnToFace(self.target.getLocation())
            self.agent.shoot()


##################
# HitpointDaemon
###
# Only execute children if hitpoints are above a certain threshold.
# Parameters:
# 0: percentage of hitpoints that must be remaining to pass the daemon check
# 1: node ID string (optional)


class HitpointDaemon(BTNode):

    # percentage: percentage of hitpoints that must be remaining to pass the daemon check

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.percentage = 0.5
        # First argument is the factor
        if len(args) > 0:
            self.percentage = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.agent.getHitpoints() < self.agent.getMaxHitpoints() * self.percentage:
            # Check failed
            print "exec", self.id, "fail"
            return False
        else:
            # Check didn't fail, return child's status
            return self.getChild(0).execute(delta)
        return ret

##################
# BuffDaemon
###
# Only execute children if agent's level is significantly above enemy hero's level.
# Parameters:
# 0: Number of levels above enemy level necessary to not fail the check
# 1: node ID string (optional)


class BuffDaemon(BTNode):

    # advantage: Number of levels above enemy level necessary to not fail the check

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.advantage = 0
        # First argument is the advantage
        if len(args) > 0:
            self.advantage = args[0]
        # Second argument is the node ID
        if len(args) > 1:
            self.id = args[1]

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        hero = None
        # Get a reference to the enemy hero
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                hero = e
                break
        if hero == None or self.agent.level <= hero.level + self.advantage:
            # fail check
            print "exec", self.id, "fail"
            return False
        else:
            # Check didn't fail, return child's status
            return self.getChild(0).execute(delta)
        return ret


#################################
# MY CUSTOM BEHAVIOR CLASSES
class BoosterAgent(BTNode):

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        # self.target = None

        if len(args) > 0:
            self.id = args[0]

    def execute(self, delta):
        BTNode.execute(self, delta)
        success = self.children[0].execute()

        agent = self.agent

        enemies = agent.world.getEnemyNPCs(agent.getTeam())
        sorted_enemies = []

        # ATTACK SHOOT
        if agent.canFire and len(enemies) > 0:

            for enemy in enemies:
                dist = distance(agent.getLocation(), enemy.getLocation())
                sorted_enemies.append((dist, enemy))

            closest_enemy = min(sorted_enemies)[1]

            myscore = self.agent.world.getScore(self.agent.getTeam())
            enemyscore = self.agent.world.getScore(closest_enemy.getTeam())

            # print("SCORE CHECK: ", "ME: ", myscore, " ENEMY: ", enemyscore)

            if distance(agent.getLocation(), closest_enemy.getLocation()) < BIGBULLETRANGE:
                agent.turnToFace(closest_enemy.getLocation())
                agent.shoot()

        # DODGE
        if agent.getVisibleType(Bullet):
            # print("DODGING")
            enemy_bullets = []
            for bullet in agent.getVisibleType(Bullet):
                if bullet.getOwner().getTeam() != agent.getTeam():
                    enemy_bullets.append(bullet)
            if len(enemy_bullets) > 0:
                sorted_bullets = []
                for bullet in enemy_bullets:
                    b_dist = distance(agent.getLocation(), bullet.getLocation())
                    sorted_bullets.append((b_dist, bullet))

                sorted_bullets = sorted(sorted_bullets)
                # print(sorted_bullets)
                for bullet_pack in sorted_bullets:
                    bullet = bullet_pack[1]
                    agent_radius = agent.getMaxRadius()
                    b_loc = bullet.getLocation()
                    x_scale = 1000 * math.cos(math.radians(bullet.orientation))
                    y_scale = -1000 * math.sin(math.radians(bullet.orientation))

                    if agent_radius > minimumDistance([b_loc, (b_loc[0] + x_scale, b_loc[1] + y_scale)], agent.getLocation()):
                        rad_angle = math.radians(bullet.orientation)
                        vector = (math.cos(math.radians(math.pi / 2 + rad_angle)), -math.sin(math.radians(math.pi / 2 + rad_angle)))
                        offset = vector[0]*agent.getMaxRadius(), vector[1]*agent.getMaxRadius()
                        pred_loc = tuple(map(lambda x, y: x + y, agent.getLocation(), offset))
                        if not insideObstacle(pred_loc, agent.world.getObstacles()):
                            agent.dodge(math.pi / 2 + rad_angle)
        # ATTACK AREA EFFECT
        if agent.canAreaEffect() and len(enemies) > 0:
            for enemy in enemies:
                agent.areaEffect()

        return success


class FindMinion(BTNode):

    # target: the minion to chase
    # timer: how often to replan

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        if len(enemies) > 0:
            best = None
            dist = 0
            for e in enemies:
                if isinstance(e, Minion):
                    d = distance(self.agent.getLocation(), e.getLocation())
                    if best == None or d < dist:
                        best = e
                        dist = d
            self.target = best
        if self.target is not None:
            navTarget = self.chooseNavigationTarget()
            if navTarget is not None:
                self.agent.navigateTo(navTarget)

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or self.target.isAlive() == False:
            # failed execution conditions
            print "exec", self.id, "false"
            return False
        elif self.target is not None and distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
            # succeeded
            print "exec", self.id, "true"
            return True
        else:
            # executing

            agent = self.agent
            if (agent.getVisibleType(Bullet)):
                # print("DODGING")
                enemy_bullets = []
                for bullet in agent.getVisibleType(Bullet):
                    if bullet.getOwner().getTeam() != agent.getTeam():
                        enemy_bullets.append(bullet)
                if len(enemy_bullets) > 0:
                    sorted_bullets = []
                    for bullet in enemy_bullets:
                        b_dist = distance(agent.getLocation(), bullet.getLocation())
                        sorted_bullets.append((b_dist, bullet))

                    sorted_bullets = sorted(sorted_bullets)
                    # print(sorted_bullets)
                    for bullet_pack in sorted_bullets:
                        bullet = bullet_pack[1]
                        agent_radius = agent.getMaxRadius()
                        b_loc = bullet.getLocation()
                        x_scale = 1000 * math.cos(math.radians(bullet.orientation))
                        y_scale = -1000 * math.sin(math.radians(bullet.orientation))

                        if agent_radius > minimumDistance([b_loc, (b_loc[0] + x_scale, b_loc[1] + y_scale)], agent.getLocation()):
                            rad_angle = math.radians(bullet.orientation)
                            agent.dodge(math.pi / 2 + rad_angle)
            self.timer = self.timer - 1
            if self.timer <= 0:
                self.timer = 50
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
            return None
        return ret

    def chooseNavigationTarget(self):
        if self.target is not None:
            return self.target.getLocation()
        else:
            return None

##################
# KillMinion
###
# Kill the closest minion. Assumes it is already in range.
# Parameters:
# 0: node ID string (optional)


class AttackMinion(BTNode):

    # target: the minion to shoot

    def parseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.agent.stopMoving()
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        if len(enemies) > 0:
            best = None
            dist = 0
            for e in enemies:
                if isinstance(e, Minion):
                    d = distance(self.agent.getLocation(), e.getLocation())
                    if best == None or d < dist:
                        best = e
                        dist = d
            self.target = best

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
            # failed executability conditions
            # print "exec", self.id, "false"
            return False
        elif self.target.isAlive() == False:
            # succeeded
            # print "exec", self.id, "true"
            return True
        else:
            # executing

            agent = self.agent

            enemies = agent.world.getEnemyNPCs(agent.getTeam())
            sorted_enemies = []
            if enemies and agent.canFire:
                for enemy in enemies:
                    dist = distance(agent.getLocation(), enemy.getLocation())
                    sorted_enemies.append((dist, enemy))

                closest_enemy = min(sorted_enemies)[1]
                borders = list(set(agent.world.getLines()) - set(agent.world.getLinesWithoutBorders()))
                sorted_borders = []
                for line in borders:
                    dist = minimumDistance(line, agent.getLocation())
                    sorted_borders.append((dist, line))

                closest_border = min(sorted_borders)[1]

                if distance(agent.getLocation(), closest_enemy.getLocation()) <= BIGBULLETRANGE:
                    midpoint = ((closest_border[0][0] + closest_border[1][0])/2, (closest_border[0][1] + closest_border[1][1])/2)
                    agent.navigateTo(midpoint)
                    agent.move((1, 1))
                    agent.turnToFace(closest_enemy.getLocation())
                    agent.shoot()
                    agent.stopMoving()
            return None
        return ret

    def shootAtTarget(self):
        if self.agent is not None and self.target is not None:
            self.agent.turnToFace(self.target.getLocation())
            self.agent.shoot()


##################
# ChaseHero
###
# Move to intercept the enemy Hero.
# Parameters:
# 0: node ID string (optional)

class FindHero(BTNode):

    # target: the hero to chase
    # timer: how often to replan

    def ParseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        self.timer = 50
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.timer = 50
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                self.target = e
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
                return None

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or self.target.isAlive() == False:
            # fails executability conditions
            # print "exec", self.id, "false"
            return False
        elif distance(self.agent.getLocation(), self.target.getLocation()) < BIGBULLETRANGE:
            # succeeded
            # print "exec", self.id, "true"
            return True
        else:
            # executing

            agent = self.agent

            if (agent.getVisibleType(Bullet)):
                # print("DODGING")
                enemy_bullets = []
                for bullet in agent.getVisibleType(Bullet):
                    if bullet.getOwner().getTeam() != agent.getTeam():
                        enemy_bullets.append(bullet)
                if len(enemy_bullets) > 0:
                    sorted_bullets = []
                    for bullet in enemy_bullets:
                        b_dist = distance(agent.getLocation(), bullet.getLocation())
                        sorted_bullets.append((b_dist, bullet))

                    sorted_bullets = sorted(sorted_bullets)
                    # print(sorted_bullets)
                    for bullet_pack in sorted_bullets:
                        bullet = bullet_pack[1]
                        agent_radius = agent.getMaxRadius()
                        b_loc = bullet.getLocation()
                        x_scale = 1000 * math.cos(math.radians(bullet.orientation))
                        y_scale = -1000 * math.sin(math.radians(bullet.orientation))

                        if agent_radius > minimumDistance([b_loc, (b_loc[0] + x_scale, b_loc[1] + y_scale)], agent.getLocation()):
                            rad_angle = math.radians(bullet.orientation)
                            agent.dodge(math.pi / 2 + rad_angle)

            self.timer = self.timer - 1
            if self.timer <= 0:
                navTarget = self.chooseNavigationTarget()
                if navTarget is not None:
                    self.agent.navigateTo(navTarget)
            return None
        return ret

    def chooseNavigationTarget(self):
        if self.target is not None:
            return self.target.getLocation()
        else:
            return None

##################
# KillHero
###
# Kill the enemy hero. Assumes it is already in range.
# Parameters:
# 0: node ID string (optional)


class AttackHero(BTNode):

    # target: the minion to shoot

    def ParseArgs(self, args):
        BTNode.parseArgs(self, args)
        self.target = None
        # First argument is the node ID
        if len(args) > 0:
            self.id = args[0]

    def enter(self):
        BTNode.enter(self)
        self.agent.stopMoving()
        enemies = self.agent.world.getEnemyNPCs(self.agent.getTeam())
        for e in enemies:
            if isinstance(e, Hero):
                self.target = e
                return None

    def execute(self, delta=0):
        ret = BTNode.execute(self, delta)
        if self.target == None or distance(self.agent.getLocation(), self.target.getLocation()) > BIGBULLETRANGE:
            # failed executability conditions
            if self.target == None:
                # print "foo none"
                pass
            else:
                # print "foo dist", distance(self.agent.getLocation(), self.target.getLocation())
                # print "exec", self.id, "false"
                pass
            return False
        elif self.target.isAlive() == False:
            # succeeded
            # print "exec", self.id, "true"
            return True
        else:

            agent = self.agent

            enemies = agent.world.getEnemyNPCs(agent.getTeam())
            sorted_enemies = []
            if enemies and agent.canFire:
                for enemy in enemies:
                    dist = distance(agent.getLocation(), enemy.getLocation())
                    sorted_enemies.append((dist, enemy))

                closest_enemy = min(sorted_enemies)[1]
                borders = list(set(agent.world.getLines()) - set(agent.world.getLinesWithoutBorders()))
                sorted_borders = []
                for line in borders:
                    dist = minimumDistance(line, agent.getLocation())
                    sorted_borders.append((dist, line))

                closest_border = min(sorted_borders)[1]

                if distance(agent.getLocation(), closest_enemy.getLocation()) <= BIGBULLETRANGE:
                    midpoint = ((closest_border[0][0] + closest_border[1][0])/2, (closest_border[0][1] + closest_border[1][1])/2)
                    agent.navigateTo(midpoint)
                    # agent.move((1, 1))
                    agent.turnToFace(closest_enemy.getLocation())
                    agent.shoot()

            return None

        return ret

    def shootAtTarget(self):
        if self.agent is not None and self.target is not None:
            self.agent.turnToFace(self.target.getLocation())
            self.agent.shoot()
