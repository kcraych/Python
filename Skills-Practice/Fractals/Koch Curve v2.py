import numpy as np
import pygame

class Utility_Math:
    @staticmethod
    # returns new coordinates after a scale, rotation, and translation (in that order)
    # coordinates parameter = n x 2 array where each row represents an x,y pair to rotated, scales, and translated
    def matrix_transformation(coordinates, angle=0, delta_x=0, delta_y=0, scale=1, x_flip=1, y_flip=1):
        matrix_rotate = np.array([[np.cos(angle), np.sin(angle)], [-np.sin(angle), np.cos(angle)]])
        matrix_flip = np.array([[x_flip,0],[0,y_flip]])
        result_rotate = np.matmul(coordinates, matrix_rotate)
        result_scale = scale * result_rotate
        result_flip = np.matmul(result_scale, matrix_flip)
        coord_count = coordinates.shape[0]
        result_translate = result_flip + np.array([[delta_x] * coord_count, [delta_y] * coord_count]).T
        return result_translate

    @staticmethod
    # returns the coordinates from taking a pattern given by a set of coordinates starting at the origin and repeating
    # the pattern after scaling to various lengths and rotating at various angles, always connecting the next scale and
    # rotation at the final point of the previous scaled and rotation.
    def pattern_repeats(angles, scales, pattern = np.array([[0, 0], [1, 0]])):
        repeats = np.array([[0, 0]])
        for i in range(1, len(angles) + 1):
            section = Utility_Math.matrix_transformation(pattern, angles[i - 1], repeats[-1, 0], repeats[-1, 1], scales[i - 1])
            repeats = np.concatenate((repeats, np.delete(section, 0, axis=0)), axis=0)
        return repeats

    @staticmethod
    # returns the result of recursively calling a pattern repeat
    def pattern_recursion(order, n, angles, scales, pattern = np.array([[0, 0], [1, 0]])):
        if order == 0:
            return pattern
        else:
            new_pattern = Utility_Math.pattern_repeats(angles, scales, pattern)
            return Utility_Math.pattern_recursion(order-1, n, angles, scales, new_pattern)

    @staticmethod
    # returns the angle in radians at each vertex of a regular polygon with n sides
    def reg_poly_vertex_radians(n):
        return np.deg2rad(180 - 360 / n)

    @staticmethod
    # returns the angle at the center of the "pie slice" created by drawing lines from each vertex the center of a
    # regular polygon
    def reg_poly_inner_radians(n):
        return np.deg2rad(360 / n)

class Utility_Draw:
    # returns coordinates after a scale and shift which maximizes the given screen space using screen dimensions
    # final coordinates are centered on the screen and takes up 95% of it's tightest fitting dimension (h or w)
    @staticmethod
    def image_screen_fit(screen_w, screen_h, coordinates):
        coordinates_combined = np.empty([0,2])
        for i in range(len(coordinates)):
            coordinates_combined = np.concatenate((coordinates_combined, coordinates[i]), axis=0)
        img_w = max(coordinates_combined[:, 0]) - min(coordinates_combined[:, 0])
        img_h = max(coordinates_combined[:, 1]) - min(coordinates_combined[:, 1])
        scale = .95 * min(screen_w / img_w, screen_h / img_h)
        x_delta = screen_w / 2 - scale * (min(coordinates_combined[:, 0]) + img_w / 2)
        y_delta = screen_h / 2 - scale * (min(coordinates_combined[:, 1]) + img_h / 2)
        coordinates_transformed = []
        for i in range(len(coordinates)):
            coordinate_set = Utility_Math.matrix_transformation(coordinates[i], 0, x_delta, y_delta, scale, 1, 1)
            coordinates_transformed.append(coordinate_set)
        return coordinates_transformed

    @staticmethod
    # returns image for a set of given coordinates in a window of given pixel width and height,
    # connecting the coordinates in consecutive order in the given color line (on a white background)
    def draw_image(screen_w, screen_h, coordinates, color=(0,0,0)):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                break;
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    break;

            screen = pygame.display.set_mode((screen_w, screen_h))
            screen.fill((255, 255, 255))
            for i in range(len(coordinates)):
                curve = coordinates[i]
                pygame.draw.lines(screen, color, False, curve, 1)
            pygame.display.flip()

class Fractal_Generation:
    # returns coordinates for a koch curve of depth n and given ratio, starting at the origin and is 1 unit in length
    # any transformations (stretch/shrink, rotate, shift, reflect) needed will be done in the koch_curve method
    def koch_curve_line(order, n, ratio):
        v_rad = Utility_Math.reg_poly_vertex_radians(n)
        i_rad = Utility_Math.reg_poly_inner_radians(n)
        angles = np.insert([0., 0.], 1, np.array([v_rad] * (n - 1)) - np.array(range(0, n - 1)) * i_rad)
        scales = np.insert([(1 - ratio) / 2] * 2, 1, [ratio] * (n - 1))
        curve = Utility_Math.pattern_recursion(order, n, angles, scales)
        return Utility_Math.matrix_transformation(curve, y_flip=-1)

    # returns coordinates for a regular polygon with the lower left coordinate at origin.
    # each edge is replaced with the given pattern (default is a normal straight line edge)
    # the pattern will face out as a default, but can face in if invert=True
    def reg_poly_pattern(n, pattern=np.array([[0,0],[1,0]]), invert=False):
        if not invert:
            pattern = Utility_Math.matrix_transformation(pattern, y_flip=-1)
        v_rad = Utility_Math.reg_poly_vertex_radians(n)
        i_rad = Utility_Math.reg_poly_inner_radians(n)
        angles = np.array([v_rad] * n) - np.array(range(0, n)) * i_rad
        return [Utility_Math.pattern_repeats(angles, [1]*n, pattern)]

    def cyclic_symmetry_pattern(n, pattern=np.array([[0,0],[1,0]])):
        i_rad = Utility_Math.reg_poly_inner_radians(n)
        angles = np.array(range(0, n)) * i_rad
        cycles = []
        for i in range(n):
            cycles.append(Utility_Math.pattern_repeats([angles[i]], [1], pattern))
        return cycles

    # returns coordinates of a koch_curve being used with a regular polygon base shape
    # utilizes the koch_curve_line to get the pattern coordinates to use in the reg_poly_pattern to generate final
    # coordinate set for desired koch curve
    def koch_curve(order, n, ratio, base, m, invert):
        koch_curve = Fractal_Generation.koch_curve_line(order, n, ratio)
        if base == "reg-poly":
            curve = Fractal_Generation.reg_poly_pattern(m, koch_curve, invert)
        elif base == "cyclic":
            curve = Fractal_Generation.cyclic_symmetry_pattern(m, koch_curve)
        return curve

class Image_Draw:
    # returns image of a koch curve in a given screen, with a depth of n and given ratio
    # can be drawn in/out of a regular polygon base shape
    def draw_koch_fractal(order=5, n=3, ratio=1/3, base="reg-poly", m=1, invert=False, screen_w=1024, screen_h=768, color=(0,0,0)):
        pygame.init()
        curve = Fractal_Generation.koch_curve(order, n, ratio, base, m, invert)
        curve = Utility_Draw.image_screen_fit(screen_w, screen_h, curve)
        Utility_Draw.draw_image(screen_w, screen_h, curve, color)
        pygame.quit()

Image_Draw.draw_koch_fractal(n=3, ratio=1/3, base="cyclic", m=3)
