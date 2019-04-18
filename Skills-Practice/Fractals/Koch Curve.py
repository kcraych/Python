import pygame
import numpy as np

pygame.init()
screen_w = 1024
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

class Matrix_Utility:
    @Staticmethod
    # returns points of a non-origin coordinate after a counter-clockwise rotation about the origin of angle (in radians)
    def rot_cc_origin(angle, start_x = 1, start_y = 0):
        matrix_rot = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        matrix_pos = np.array([[start_x],[start_y]])
        return np.matmul(matrix_rot, matrix_pos)

    @Staticmethod
    # returns points of a coordinate after a horizontal and/or vertical translation
    def translation(delta_x, delta_y, start_x = 0, start_y = 0):
        return np.array([[start_x], [start_y]]) + np.array([[delta_x], [delta_y]])

    @Staticmethod
    def full_transformation(angle, delta_x, delta_y, start_x = 1, start_y = 0, scale = 1):
        result_rotate = Matrix_Utility.rot_cc_origin(angle, start_x, start_y)
        result_scale = scale * result_rotate
        result_translate = Matrix_Utility.translation(delta_x, delta_y, result_scale[0,0], result_scale[0,1])
        return result_translate

class Polygon_Utility:
    @Staticmethod
    def reg_poly_angles_radians(n):
        return [np.deg2rad(360/n), np.deg2rad(180-(360/n))]  # [inner angle, vertex angle]

    @Staticmethod
    def reg_poly_identity_coordinates_origin(n):
        poly_angles = Polygon_Utility.reg_poly_angles_radians(n)
        poly_vertices_x = [-np.cos(poly_angles[1] / 2)]
        poly_vertices_y = [-np.sin(poly_angles[1] / 2)]
        for i in range (1, n-1):
            poly_vertices_new = Matrix_Utility.rot_cc_origin(poly_angles[0], poly_vertices_x[i-1], poly_vertices_y[i-1])
            poly_vertices_x.append(poly_vertices_new[0,0])
            poly_vertices_y.append(poly_vertices_new[1,0])

    @Staticmethod
    def reg_poly_coordinates(n, radius, x, y):
        poly_angles = Polygon_Utility.reg_poly_angles_radians(n)






class Fractals_Koch_Curve
    def __init__(self, order, ratio, size, n, pos):
        ang = Fractals_Utility.reg_poly_vertex_angle_radians(n)


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