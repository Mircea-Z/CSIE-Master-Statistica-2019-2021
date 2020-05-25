import pygame
from .widgets import Screen
from .entities import World


class App:

    def __init__(self, settings):
        self.settings = settings
        self.world = World(self.settings)
        self.screen = Screen(self.settings, self.world)

    def run(self):
        egzit = False
        while not egzit:

            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    egzit = True

                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_s:
                        self.screen.graph_view.save_to_csv()

            if self.screen.exit.clicked():
                break
            if self.screen.save.clicked():
                self.screen.graph_view.save_to_csv()
            if self.screen.start.clicked():
                if self.screen.start.text == 'Pause':
                    self.screen.start.text = 'Start'
                else:
                    self.screen.start.text = 'Pause'
            if self.screen.start.text == 'Pause':
                self.world.update()
            self.screen.update(self.world)
            self.settings = self.screen.settings


        pygame.quit()
