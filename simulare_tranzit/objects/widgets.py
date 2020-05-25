import pygame
import os

class Screen:

    def __init__(self, settings, world):
        self.real_view = ViewPort(world, view='real')
        self.tele_view = ViewPort(world, view='tele')
        self.graph_view = GraphPort(self.real_view, self.tele_view, settings)
        self.settings = settings
        self.save = Button('Save', settings, (900,320))
        self.start = Button('Start', settings, (900,420))
        self.exit = Button('Exit', settings, (900,520))
        self.main_display = self.init_display()

    def update(self, world):

        real_view = self.real_view.draw()
        tele_view = self.tele_view.draw()
        graph_view = self.graph_view.draw()
        start_button = self.start.draw()

        if self.start.text == 'Pause':
            self.real_view.update(world)
            self.tele_view.update(world)
            self.graph_view.update(real_view,tele_view)

        self.save.update()
        self.exit.update()
        self.start.update()

        self.draw(real_view, tele_view, graph_view, start_button, self.settings)

        pygame.display.update()

    def init_display(self):
        pygame.init()
        modes = pygame.HWSURFACE | pygame.HWACCEL
        return pygame.display.set_mode((self.settings['mode']['width'],self.settings['mode']['height']), modes)

    def draw(self, real_view, tele_view, graph_view, start_button, settings):
        self.main_display.fill((20,20,20))
        real_view = pygame.transform.smoothscale(real_view,(int(self.settings['mode']['width']*0.66),int(self.settings['mode']['height']*0.66)))
        self.main_display.blit(real_view, (10, 10))
        tele_view = pygame.transform.smoothscale(tele_view,(int(self.settings['mode']['width']*0.32),int(self.settings['mode']['height']*0.32)))
        self.main_display.blit(tele_view, (810, 10))
        self.main_display.blit(graph_view, (10, 610))
        self.main_display.blit(self.save.draw(), self.save.coords)
        self.main_display.blit(self.start.draw(), self.start.coords)
        self.main_display.blit(self.exit.draw(), self.exit.coords)


class ViewPort:

    def __init__(self, world, view):
        self.world = world
        self.view = view
        self.surface = pygame.Surface((int(world.star.radius*2.5),int(world.star.radius*2.1)))
        self.luminosity_value = 0

    def draw(self):
        self.surface.fill((0,0,0))
        self.world.star.draw(self.surface)
        planet_relative_position = self.surface.get_width()//2+self.world.planet.location
        if planet_relative_position > 0 and planet_relative_position < self.surface.get_width():
            self.world.planet.draw(self.surface, (self.surface.get_width()//2+self.world.planet.location, self.surface.get_height()//2))

        if self.view == 'real':
            return self.surface

        if self.view == 'tele':
            small = pygame.transform.smoothscale(self.surface,(self.surface.get_width()//80, self.surface.get_height()//80))
            return small


    def update(self, world):
        self.world = world


class GraphPort:

    def __init__(self, view1, view2,settings):
        self.real_view = view1
        self.real_view_pixel_count = self.real_view.surface.get_width()*self.real_view.surface.get_height()
        self.tele_view = view2
        self.tele_view_pixel_count = self.tele_view.surface.get_width()*self.tele_view.surface.get_height()
        self.real_data = []
        self.tele_data = []
        self.plot_color = (settings['star']['color']['r'],settings['star']['color']['g'],settings['star']['color']['b'])
        self.surface = pygame.Surface((int(settings['mode']['width']*0.98),int(settings['mode']['height']*0.31)))


    def draw(self):
        self.surface.fill((0,0,0))
        pygame.draw.line(self.surface, (200,200,200), (0,self.surface.get_height()//2), (self.surface.get_width(),self.surface.get_height()//2), 1)
        points = self.plot(self.real_data)
        pygame.draw.lines(self.surface, self.plot_color, False, points, 2)

        return self.surface

    def plot(self, series):
        median = self.get_median_pixel_value(series)
        if len(series) == 0:
            _range = 1
        else:
            _range = max(series) - min(series)
        if _range == 0:
            _range = 1
        points=[]
        if len(series) > self.surface.get_width() - 10:
            series = series[-self.surface.get_width() - 10:]
        for i in range(len(series)-1):
            item = series[i]
            y_offset = self.surface.get_height()-int((item-min(series))*self.surface.get_height()/_range)
            points.append((i, y_offset))
        if len(points) < 2:
            points = [(0,self.surface.get_height()//2), (self.surface.get_width(),self.surface.get_height()//2)]
        return points

    def update(self, real_view, tele_view):
        real_view_luminosity = sum([pygame.transform.average_color(real_view)[0],
                                    pygame.transform.average_color(real_view)[1],
                                    pygame.transform.average_color(real_view)[2]])

        self.real_data.append(real_view_luminosity)

        tele_view_luminosity = sum([pygame.transform.average_color(tele_view)[0],
                                    pygame.transform.average_color(tele_view)[1],
                                    pygame.transform.average_color(tele_view)[2]])

        self.tele_data.append(tele_view_luminosity)

    def save_to_csv(self):
        with open(os.path.join(os.getcwd(),'output_series','data.csv'),'w') as ef:
            ef.write('Time,REAL_DATA,TELE_DATA\n')
            for i in range(len(self.real_data)-1):
                ef.write(','.join([str(i),str(self.real_data[i]),str(self.tele_data[i])+'\n']))

    def get_median_pixel_value(self, values):
        if len(values) == 0:
            values = [0]
        return (max(values)+min(values))//2

class Button:

    def __init__(self, text, settings, coords):
        self.surface = pygame.Surface((int(settings['mode']['width']*0.15),int(settings['mode']['height']*0.07)))
        self.text = text
        self.settings = settings
        self.bg_color = (25,25,25)
        self.fg_color = (30,30,30)
        self.text_color = (0,0,0)
        self.coords = coords
        self.col_update = False

    def draw(self):
        self.surface.fill(self.bg_color)
        pygame.draw.rect(self.surface, self.fg_color,(self.surface.get_width()*5//100,self.surface.get_height()*5//100,
                                                      self.surface.get_width()*90//100, self.surface.get_height()*90//100))

        fsize = int(self.surface.get_height()*0.5)
        button_font=pygame.font.SysFont('Courier',fsize)
        button_text=button_font.render(self.text,False,(255,255,255))
        self.surface.blit(button_text,((self.surface.get_width()-button_text.get_width())//2,(self.surface.get_height()-button_text.get_height())//2))

        return self.surface

    def update(self):
        if self.clicked():
            self.click()
            return True
        elif self.mouseover():
            self.mouse_over()
            return True
        else:
            self.reset()

    def click(self):
        self.bg_color = ((255-self.bg_color[0])//2,(255-self.bg_color[1])//2,(255-self.bg_color[2])//2)
        self.fg_color = (255-self.fg_color[0],255-self.fg_color[1],255-self.fg_color[2])
        self.text_color = (255-self.text_color[0],255-self.text_color[1],255-self.text_color[2])

    def mouse_over(self):
        if not self.col_update:
            self.bg_color = ((255-self.bg_color[0])//2,(255-self.bg_color[1])//2,(255-self.bg_color[2])//2)
            self.fg_color = (255-self.fg_color[0],255-self.fg_color[1],255-self.fg_color[2])
            self.text_color = (255-self.text_color[0],255-self.text_color[1],255-self.text_color[2])
            self.col_update = True

    def mouseover(self):
        return (pygame.mouse.get_pos()[0]>=self.coords[0]) and (pygame.mouse.get_pos()[1]>=self.coords[1]) and \
                (pygame.mouse.get_pos()[0]<=self.coords[0]+self.surface.get_width()) and (pygame.mouse.get_pos()[1]<=self.coords[1]+self.surface.get_height())

    def clicked(self):
        return self.mouseover() and pygame.mouse.get_pressed()==(1,0,0)

    def reset(self):
        self.bg_color = (25,25,25)
        self.fg_color = (30,30,30)
        self.text_color = (0,0,0)
        self.col_update = False
