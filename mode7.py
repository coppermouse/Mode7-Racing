import pygame as pg
from math import sin, cos, pi

vec = pg.math.Vector2


class Camera:
    pos = vec(999.904, 1000.38)
    angle = -1.54


class Mode7:
    def __init__(self, size=(1024, 1024)):
        self.px_game_screen = pg.PixelArray(pg.Surface((200, 150)))
        self.image = pg.Surface(size)
        self.image.fill(pg.Color('black'))

        tilesize = 32
        for x in range(0, size[0], tilesize):
            pg.draw.line(self.image, pg.Color('darkturquoise'),
                         (x, 0), (x, size[1]), 4)
        for y in range(0, size[1], tilesize):
            pg.draw.line(self.image, pg.Color('blueviolet'),
                         (0, y), (size[0], y), 4)

        # settings for the near and far plane
        self.near = 0.005
        self.far = 0.01215
        # field of view
        self.fov_half = pi / 4

    def draw(self, camera):

        ps = self.px_game_screen

        # references to the "fake" screen (the one that gets rendered onto the screen)
        sw = 200
        sh = 150
        _, _, iw, ih = self.image.get_rect()
        player = camera
        horizon = 0.2

        # create the frustum corner points
        self.far_x1 = player.pos.x + \
            cos(player.angle - self.fov_half) * self.far
        self.far_y1 = player.pos.y + \
            sin(player.angle - self.fov_half) * self.far

        self.near_x1 = player.pos.x + \
            cos(player.angle - self.fov_half) * self.near
        self.near_y1 = player.pos.y + \
            sin(player.angle - self.fov_half) * self.near

        self.far_x2 = player.pos.x + \
            cos(player.angle + self.fov_half) * self.far
        self.far_y2 = player.pos.y + \
            sin(player.angle + self.fov_half) * self.far

        self.near_x2 = player.pos.x + \
            cos(player.angle + self.fov_half) * self.near
        self.near_y2 = player.pos.y + \
            sin(player.angle + self.fov_half) * self.near

        # loop over every pixel on the image, beginning furthest away towards the
        # camera point
        for y in range(sh):
            # take a sample point for depth linearly related to rows on the screen
            sample_depth = y / sh + 0.0000001  # this prevents div by 0 errors
            # not sure how this is handled in the c++ code

            # Use sample point in non-linear (1/x) way to enable perspective
            # and grab start and end points for lines across the screen
            start_x = (self.far_x1 - self.near_x1) / \
                sample_depth + self.near_x1
            start_y = (self.far_y1 - self.near_y1) / \
                sample_depth + self.near_y1
            end_x = (self.far_x2 - self.near_x2) / sample_depth + self.near_x2
            end_y = (self.far_y2 - self.near_y2) / sample_depth + self.near_y2

            ps[0:sw, y] = [
                self.image.get_at((int((((end_x - start_x) * (x / sw) + start_x) % 1) * iw),
                                   int((((end_y - start_y) * (x / sw) + start_y) % 1) * ih)))
                for x in range(sw)
            ]

    def get_surface(self):
        return self.px_game_screen.surface


if __name__ == "__main__":

    m = Mode7()

    import pygame

    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    clock = pygame.time.Clock()
    running = True

    camera = Camera()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                running = False

        camera.angle += 0.1

        screen.fill("#152830")
        m.draw(camera)
        screen.blit(pygame.transform.scale(
            m.get_surface(), (600, 450)), (0, 150))

        pygame.display.flip()

        clock.tick(500)
        print(clock.get_fps())

    pygame.quit()
