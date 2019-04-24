import pygame
import numpy as np

pygame.init()
screen_w = 1024
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

import numpy as np


class Utility_Matrix:
    @staticmethod
    # returns new coordinates after a scale, rotation, and translation (in that order)
    # coordinates parameter = 2 x n array where each column represents an x,y pair to rotated
    def matrix_transformation(angle, delta_x, delta_y, coordinates, scale=1):
        matrix_rotate = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        result_rotate = np.matmul(matrix_rotate, coordinates)
        result_scale = scale * result_rotate
        result_translate = result_scale + np.array([[delta_x] * coordinates.shape[1], [delta_y] * coordinates.shape[1]])
        return result_translate


class Utility_Polygon:
    @staticmethod
    def reg_poly_vertex_radians(n):
        return np.deg2rad(180 - 360 / n)

    @staticmethod
    def reg_poly_inner_radians(n):
        return np.deg2rad(360 / n)


class Fractal_Generation:
    def koch_curve_recursion(order, n, pos, theta, scales, angles, inserts):
        if order == 0:
            return Utility_Matrix.matrix_transformation(theta, pos[0], pos[1], inserts)
        else:
            curve = np.array([pos]).T
            for i in range(n + 1, 0, -1):
                insert_transform = Utility_Matrix.matrix_transformation(angles[i - 1], curve[0, -1], curve[1, -1],
                                                                        inserts, scales[i - 1])
                curve = np.concatenate((curve, np.delete(insert_transform, 0, axis=1)), axis=1)
                ord = order - 1
            return Fractal_Generation.koch_curve_recursion(ord, n, pos, theta, scales, angles, curve)


def draw_loop(order, n, pos, length, ratio, theta):
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break;

        v_rad = Utility_Polygon.reg_poly_vertex_radians(n)
        i_rad = Utility_Polygon.reg_poly_inner_radians(n)
        angles = np.insert([0, v_rad, 0], 2, [v_rad - i_rad] * (n - 2))
        scales = np.insert([(1 - ratio) / 2] * 2, 1, [ratio] * (n - 1))
        inserts = np.array([[0, length], [0, 0]])
        curve = np.transpose(Fractal_Generation.koch_curve_recursion(order, n, pos, theta, scales, angles, inserts))

        pygame.draw.lines(screen, (0, 0, 255), False, curve, 1)
        pygame.display.flip()


draw_loop(2, 3, [100, 700], 1000, 1 / 3, 0)
pygame.quit()