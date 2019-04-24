import pygame
import numpy as np

pygame.init()
screen_w = 1024
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

import numpy as np


class Utility_Matrix:
    @staticmethod
    # returns new coordinates after a counter-clockwise rotation about the origin of angle (in radians)
    # coordinates parameter = 2 x n array where each column represents an x,y pair to rotated
    def rot_cc_origin(angle, coordinates):
        matrix_rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        return np.matmul(matrix_rot, coordinates)

    @staticmethod
    # returns new coordinates after a scale, rotation, and translation (in that order)
    # coordinates parameter = 2 x n array where each column represents an x,y pair to rotated
    def full_transformation(angle, delta_x, delta_y, coordinates, scale=1):
        result_rotate = Utility_Matrix.rot_cc_origin(angle, coordinates)
        result_scale = scale * result_rotate
        result_translate = result_scale + np.array([[delta_x] * coordinates.shape[1], [delta_y] * coordinates.shape[1]])
        return result_translate


class Utility_Polygon:
    @staticmethod
    # identifies all coordinates of a regular polygon of side length, with the lower left vertex on the start_x, start_y position
    def reg_poly_coordinates(n, side_length=1, start_x=0, start_y=0):
        poly_angle = np.deg2rad(360 / n)
        poly_vertices = np.array(
            [[-0.5 * side_length], [-0.5 * side_length * np.cos(0.5 * poly_angle) / np.sin(0.5 * poly_angle)]])
        for i in range(n - 1):
            new_vertices = Utility_Matrix.rot_cc_origin(-poly_angle, poly_vertices[:, [i]])
            poly_vertices = np.concatenate((poly_vertices, new_vertices), axis=1)
        poly_vertices += np.array([[-poly_vertices[0, 0] + start_x] * n, [-poly_vertices[1, 0] + start_y] * n])
        return poly_vertices


class Fractal_Generation:
    def koch_curve_recursion(order, n, poly_ratio, coord_list, identity_poly):
        while order >= 0:
            for i in range(coord_list.shape[1] - 1, 0, -1):
                theta = np.math.atan2((coord_list[1, i] - coord_list[1, i - 1]),
                                      (coord_list[0, i] - coord_list[0, i - 1]))
                pt_delta = coord_list[:, [i]] - coord_list[:, [i - 1]]
                side_length = np.linalg.norm(np.transpose(poly_ratio * pt_delta))
                start_poly = coord_list[:, [i - 1]] + 0.5 * (1 - poly_ratio) * pt_delta
                order_poly = Utility_Matrix.full_transformation(theta, start_poly[0, 0], start_poly[1, 0],
                                                                identity_poly, side_length)
                coord_list = np.insert(coord_list, [i], order_poly, axis=1)
            order = order - 1
            Fractal_Generation.koch_curve_recursion(order, n, poly_ratio, coord_list, identity_poly)
        return coord_list


def draw_loop(order, n, poly_ratio, coord_list):
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break;

        identity_poly = Utility_Polygon.reg_poly_coordinates(n)
        curve = np.transpose(Fractal_Generation.koch_curve_recursion(order, n, poly_ratio, coord_list, identity_poly))
        pygame.draw.lines(screen, (0, 0, 255), False, curve, 1)
        pygame.display.flip()


draw_loop(4, 5, 1 / 3, np.array([[0, 1000], [100, 100]]))
pygame.quit()