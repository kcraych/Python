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
    def full_transformation(angle, delta_x, delta_y, coordinates, scale = 1):
        result_rotate = Utility_Matrix.rot_cc_origin(angle, coordinates)
        result_scale = scale * result_rotate
        result_translate = result_scale + np.array([[delta_x]*coordinates.shape[1],[delta_y]*coordinates.shape[1]])
        return result_translate

class Utility_Polygon:
    @staticmethod
    def reg_poly_inner_angle_radians(n):
        return np.deg2rad(360/n)

    @staticmethod
    # identifies all coordinates of a regular polygon of side length, with the lower left vertex on the start_x, start_y position
    def reg_poly_coordinates_identity_origin(n, side_length = 1, start_x = 0, start_y = 0):
        poly_angle = Utility_Polygon.reg_poly_inner_angle_radians(n)
        poly_vertices = np.array([[-0.5*side_length], [-0.5*side_length*np.cos(0.5*poly_angle)/np.sin(0.5*poly_angle)]])
        for i in range (n-1):
            new_vertices = Utility_Matrix.rot_cc_origin(-poly_angle, poly_vertices[:,[i]])
            poly_vertices = np.concatenate((poly_vertices, new_vertices), axis=1)
        poly_vertices += np.array([[-poly_vertices[0,0] + start_x]*n, [-poly_vertices[1,0] + start_y]*n])
        return poly_vertices

class Utility_Fractals:
    def unit_koch_curve(n = 3, start_x = 0, start_y = 0, theta = 0, unit_length = 1, poly_ratio = 1/3):
        unit_poly_coordinates = Utility_Polygon.reg_poly_coordinates_identity_origin(n, poly_ratio, 0.5*(1-poly_ratio), 0)
        unit_koch_coordinates = np.concatenate((np.array([[0],[0]]), unit_poly_coordinates, np.array([[1],[0]])), axis=1)
        koch_coordinates = Utility_Matrix.full_transformation(theta, start_x, start_y, unit_koch_coordinates, unit_length)
        return koch_coordinates

class Fractal_Generation:
    def koch_curve(n, start_x, start_y, theta, unit_length, poly_ratio):
        unit_coordinates = Utility_Fractals.unit_koch_curve(n, start_x, start_y, theta, unit_length, poly_ratio)
        koch_coordinates = unit_coordinates[:,[0]]
        for j in range(1,unit_coordinates.shape[1]-2):
            start_x = unit_coordinates[0,j]
            start_y = unit_coordinates[1,j]
            coordinates_delta = unit_coordinates[:,[j+1]] - unit_coordinates[:,[j]]
            theta = np.arctan(coordinates_delta[1,0]/coordinates_delta[0,0])
            unit_new = Utility_Fractals.unit_koch_curve(n, start_x, start_y, theta, unit_length, poly_ratio)
            koch_coordinates = np.concatenate((koch_coordinates, unit_new[:,:(n+1)]), axis=1)
        koch_coordinates = np.concatenate((koch_coordinates, unit_coordinates[:,[n+1]]), axis=1)
        return koch_coordinates

def draw_loop():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break;

        curve = Fractal_Generation.koch_curve(3,0,0,0,1,1/3)
        pygame.draw.lines(screen, (0, 0, 255), False, curve, 1)
        pygame.display.flip()


draw_loop()
pygame.quit()