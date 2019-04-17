import pygame
import numpy as np

pygame.init()
screen_w = 1024
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

class Fractals_Utility:
    @Staticmethod
    def matrix_manipulation(ratio, size, pos_arr, angle, theta):
        rot_matrix = np.array([[np.cos(this.a), -np.sin(this.a)], [np.sin(this.a), np.cos(this.a)]])
        sld_matrix = np.array([[1], [0]])
        return size * ratio * (np.matmul(rot_matrix, pos_arr)) + sld_matrix

    @Staticmethod
    def regular_polygon_vertex_angle_radians(n):
        return np.deg2rad(180-(360/n))


class Fractals_Koch_Curve
    def __init__(self, order, ratio, size, n, pos):
        ang = Fractals_Utility.regular_polygon_vertex_angle_radians(n)


class Fractals_Koch_Curve_Unit
    def __init__(self, ratio, size, angle, pos, base_angle):
        rotations = [0, angle, -angle, 0]
        for rot in rotations:
            pos_arr = np.array([[pos.x], [pos.y]])
            newpos_arr = matrix_manipulation(this, this.ratio, this.pos_arr, rot, 0)
            newpos = (newpos_arr[0, 0], newpos_arr[1, 0])
            pygame.draw.line(screen, (0, 0, 255), pos, newpos)
            pos = newpos




def draw_loop():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break;

        koch_curve(0, 1/3, 100, 3, (screen_w//2, screen_h//2))
        pygame.display.flip()

draw_loop()
pygame.quit()