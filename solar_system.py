import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT)) # set pop up screen size
pygame.display.set_caption("Solar System") # set title of window

WHITE = (255, 255, 255) # color white
YELLOW = (255, 255, 0) # color yellow
BLUE = (0, 0, 255) # color blue
RED = (255, 0, 0) # color red
GREY = (100, 100, 100) # color grey

FONT = pygame.font.SysFont("garamond", 16)

class Planet:
    AU = 149.6e6 * 1000 # distance from earth to sun
    G = 6.67428e-11 # gravitational constant
    SCALE = 200 / AU # small value to scale down the solar system to fit it on the screen
    TIMESTEP = 60 * 60 * 24 # 1 day

    # Constructor
    def __init__(self, x, y, radius, color, mass):
        self.x = x # x position
        self.y = y # y position
        self.radius = radius # radius
        self.color = color # color
        self.mass = mass # mass
        self.sun = False # if it's the sun
        self.dis_to_sun = 0 # distance from planet to sun
        self.orbit = []
        self.x_speed = 0 # x velocity
        self.y_speed = 0 # y velocity

    # 
    def draw(self, SCREEN):
        # divide by two because pygame (0, 0) is the top left corner
        x = self.x * self.SCALE + WIDTH / 2 # x position on screen
        y = self.y * self.SCALE + HEIGHT / 2 # y position on screen

        if len(self.orbit) > 3:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(SCREEN, self.color, False, updated_points)

        if not self.sun:
            distance_text = FONT.render(f"{self.distance_to_sun / 1000:.2f} km", True, self.color)
            SCREEN.blit(distance_text, (x - distance_text.get_width() / 2, y - distance_text.get_height() / 2 - 20))

        pygame.draw.circle(SCREEN, self.color, (x, y), self.radius) # draw the planet

    def attraction(self, other):
        other_x, other_y = other.x, other.y # other planet's x and y position
        distance_x = other_x - self.x # distance between x positions
        distance_y = other_y - self.y # distance between y positions
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2) # distance between planets
        if other.sun: # if the other "planet" is the sun
            self.distance_to_sun = distance # distance to display on the planet
        force = self.G * self.mass * other.mass / distance ** 2 # force between the planets
        theta = math.atan2(distance_y, distance_x) # angle between the planets x and y positions
        force_x = math.cos(theta) * force # force in the x direction
        force_y = math.sin(theta) * force # force in the y direction
        return force_x, force_y

    def update_pos(self, planets):
        total_fx = total_fy = 0 # initialize x and y force to zero
        for planet in planets:
            if self == planet: # if the planet is itself
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_speed += total_fx / self.mass * self.TIMESTEP
        self.y_speed += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_speed * self.TIMESTEP
        self.y += self.y_speed * self.TIMESTEP
        self.orbit.append((self.x, self.y))

def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10 ** 30)
    sun.sun = True

    mercury = Planet(-0.387 * Planet.AU, 0,  8, GREY, 0.330 * 10 ** 24)
    mercury.y_speed = 47.36 * 10 ** 3

    venus = Planet(-0.723 * Planet.AU, 0,  14, WHITE, 4.8685 * 10 ** 24)
    venus.y_speed = 35.02 * 10 ** 3

    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.972 * 10 ** 24)
    earth.y_speed = 29.78 * 10 ** 3

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 ** 23)
    mars.y_speed = 24.07 * 10 ** 3

    planets = [sun, mercury, venus, earth, mars]

    while run:
        clock.tick(60)
        SCREEN.fill((0, 0, 0)) # fill the screen black every frame, or else the old frames will still be on the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_pos(planets) # update the position of the planets using the forces of attraction
            planet.draw(SCREEN) # draw the planets

        pygame.display.update() # update the display

    pygame.quit()



if __name__ == '__main__':
    main()