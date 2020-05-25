import pygame
from random import randint
import math
import numpy as np

from .utils import generate_sprite

class World:

    def __init__(self, settings):
        self.settings = settings
        self.star = Star(self.settings)
        self.planet = Planet(self.settings)

    def update(self):
        self.star.update()
        self.planet.update()

class Planet:

    def __init__(self, settings):
        self.radius = int(settings['planet']['radius'])
        self.vel = int(settings['planet']['velocity'])
        self.orbit_length = int(settings['planet']['period'])*self.vel
        self.location = -self.orbit_length//2

    def draw(self, surface, center):
        pygame.draw.circle(surface, (0,0,0), center, self.radius)

    def update(self):
        self.location = self.location+self.vel
        if self.location > self.orbit_length//2:
            self.location = -self.orbit_length + self.location

        if self.location < -self.orbit_length//2:
            self.location = self.orbit_length - self.location

class Star:

    def __init__(self, settings):
        self.radius = int(settings['star']['radius'])
        self.variability = settings['star']['variability']
        self.base_luminosity = int(settings['star']['base_luminosity'])
        self.luminosity = self.base_luminosity
        self.color = (settings['star']['color']['r']*self.luminosity,settings['star']['color']['g']*self.luminosity,settings['star']['color']['b']*self.luminosity)
        self.timer = 0
        self.frames = []

    def build_animation(self):
        sp=np.zeros((int(round(self.radius*2)),int(round(self.radius*2)),3))
        srf = pygame.surfarray.make_surface(generate_sprite(self.radius,self.radius*0.5,sp,self.compute_color(self.color)))
        srf.set_colorkey((0,0,0))
        return srf

    def draw(self, surface):
        srf = self.build_animation()
        # if len(self.frames) < self.variability['period']:
        #     srf = self.build_animation()
        #     self.frames.append(srf)
        # else:
        #     srf = self.frames[self.timer%self.variability['period']]
        surface.blit(srf, ((surface.get_width()-srf.get_width())//2, (surface.get_height()-srf.get_height())//2))

    def compute_color(self,color):
        return (int(min(255,color[0]*self.luminosity)),
                int(min(255,color[1]*self.luminosity)),
                int(min(255,color[2]*self.luminosity)))

    def update(self):
        self.timer+=1
        print(math.sin(self.timer), self.luminosity, self.color, sep='|')
        # self.luminosity = self.variability['amplitude']+(math.cos(self.timer)/self.variability['period'])*self.variability['amplitude']**2
        # self.luminosity = self.luminosity*randint(10000*(1-self.variability['noise']),10000*(1+self.variability['noise']))/10000

        self.luminosity = 1-self.variability['amplitude']+(math.cos(self.timer/self.variability['period']))*self.variability['amplitude']
        self.luminosity = self.luminosity*randint(10000*(1-self.variability['noise']),10000*(1+self.variability['noise']))/10000
