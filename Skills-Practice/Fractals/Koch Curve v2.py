import pygame
import numpy as np

pygame.init()
screen_w = 1024
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

class Utility_Methods:
    @staticmethod
    # returns new coordinates after a scale, rotation, and translation (in that order)
    # coordinates parameter = 2 x n array where each column represents an x,y pair to rotated
    def matrix_transformation(coordinates, angle=0, delta_x=0, delta_y=0, scale=1):
        matrix_rotate = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
        result_rotate = np.matmul(matrix_rotate, coordinates)
        result_scale = scale * result_rotate
        result_translate = result_scale + np.array([[delta_x] * coordinates.shape[1], [delta_y] * coordinates.shape[1]])
        return result_translate

    @staticmethod
    # returns the coordinates from taking a pattern given by a set of coordinates starting at the origin and repeating
    # the pattern after scaling to various lengths and rotating at various angles, always connecting the next scale and
    # rotation at the final point of the previous scaled and rotation.
    def pattern_repeats(a, s, p=np.array([[0, 1], [0, 0]])):
        repeats = np.array([[0, 0]]).T
        for i in range(a.size, 0, -1):
            section = Utility_Methods.matrix_transformation(p, a[i - 1], repeats[0, -1], repeats[1, -1], s[i - 1])
            repeats = np.concatenate((repeats, np.delete(section, 0, axis=1)), axis=1)
        return repeats

    @staticmethod
    # returns the result of recursively calling a pattern repeat
    def pattern_recursion(order, n, angles, scales, pattern=np.array([[0, 1], [0, 0]])):
        if order == 0:
            return pattern
        else:
            new_pattern = Utility_Methods.pattern_repeats(angles, scales, pattern)
            return Utility_Methods.pattern_recursion(order-1, n, angles, scales, new_pattern)

    @staticmethod
    def reg_poly_vertex_radians(n):
        return np.deg2rad(180 - 360 / n)

    @staticmethod
    def reg_poly_inner_radians(n):
        return np.deg2rad(360 / n)


class Fractal_Generation:
    def koch_curve(order, n, ratio):
        v_rad = Utility_Methods.reg_poly_vertex_radians(n)
        i_rad = Utility_Methods.reg_poly_inner_radians(n)
        angles = np.insert([0., 0.], 1, np.array([v_rad] * (n - 1)) - np.array(range(0, n - 1)) * i_rad)
        scales = np.insert([(1 - ratio) / 2] * 2, 1, [ratio] * (n - 1))
        return Utility_Methods.pattern_recursion(order, n, angles, scales)

    def reg_poly_pattern(n):
        v_rad = Utility_Methods.reg_poly_vertex_radians(n)
        i_rad = Utility_Methods.reg_poly_inner_radians(n)
        angles = np.insert([0., 0.], 1, np.array([v_rad] * (n - 1)) - np.array(range(0, n - 1)) * i_rad)
        return Utility_Methods.pattern_recursion(1, n, [1]*n, angles)

def draw_loop(order, n, pos, length, ratio, theta):
    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break;
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                break;

        curve = Fractal_Generation.koch_curve(order, n, ratio)
        curve = Utility_Methods.matrix_transformation(curve, theta, pos[0], pos[1], length)
        print(curve.T)

        pygame.draw.lines(screen, (0, 0, 255), False, curve.T, 1)
        pygame.display.flip()

draw_loop(3, 3, [100,700], 800, 1/3, 0)
pygame.quit()

