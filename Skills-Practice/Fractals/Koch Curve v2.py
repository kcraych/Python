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
    # returns sets of coordinates from taking a pattern given by a set of coordinates
    # starting at the origin and repeating the pattern after scaling to various lengths and rotating at various angles.
    def pattern_repeats_disjoint(angles, scales, pattern = [np.array([[0, 0], [1, 0]])]):
        repeats = np.empty(shape=(len(angles),len(pattern)), dtype=object)
        for i in range(len(angles)):
            delta_x = 0 if i == 0 else repeats[i-1, 0][-1, 0]
            delta_y = 0 if i == 0 else repeats[i-1, 0][-1, 1]
            for j in range(len(pattern)):
                test = Utility_Math.matrix_transformation(pattern[j], angles[i], delta_x, delta_y, scales[i])
                repeats[i, j] = Utility_Math.matrix_transformation(pattern[j], angles[i], delta_x, delta_y, scales[i])
        return repeats.flatten()

    @staticmethod
    # returns one set of coordinates, given multiple sets of coordinates where the last coordinate and the first
    # coordinate of consecutive sets match, to form a continuous set of coordinates (rather than disjoint).
    def pattern_repeats_continuous(disjoint):
        continuous = disjoint[0]
        for i in range(len(disjoint)-1):
            continuous = np.concatenate((continuous, np.delete(disjoint[i+1], 0, axis=0)), axis=0)
        return [continuous]

    @staticmethod
    # returns the result of recursively calling a pattern repeat
    def pattern_recursion(order, angles, scales, pattern = [np.array([[0, 0], [1, 0]])]):
        if order == 0:
            return pattern
        else:
            new_pattern = Utility_Math.pattern_repeats_disjoint(angles, scales, pattern)
            new_pattern = Utility_Math.pattern_repeats_continuous(new_pattern) if len(new_pattern) > 1 else new_pattern
            return Utility_Math.pattern_recursion(order-1, angles, scales, new_pattern)

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
        coordinates_combined = coordinates[0]
        for i in range(len(coordinates)-1):
            coordinates_combined = np.concatenate((coordinates_combined, coordinates[i+1]), axis=0)
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
        curve = Utility_Math.pattern_recursion(order, angles, scales)
        return Utility_Math.matrix_transformation(curve[0], y_flip=-1)

    # returns coordinates for a regular polygon with the lower left coordinate at origin.
    # each edge is replaced with the given pattern (default is a normal straight line edge)
    # the pattern will face out as a default, but can face in if invert=True
    def reg_poly_pattern(n, pattern=np.array([[0,0],[1,0]]), invert=False):
        if not invert:
            pattern = Utility_Math.matrix_transformation(pattern, y_flip=-1)
        v_rad = Utility_Math.reg_poly_vertex_radians(n)
        i_rad = Utility_Math.reg_poly_inner_radians(n)
        angles = np.array([v_rad] * n) - np.array(range(0, n)) * i_rad
        poly_disjoint = Utility_Math.pattern_repeats_disjoint(angles, [1]*n, [pattern])
        return Utility_Math.pattern_repeats_continuous(poly_disjoint)

    def cyclic_symmetry_pattern(z, pattern=np.array([[0,0],[1,0]])):
        i_rad = Utility_Math.reg_poly_inner_radians(z)
        angles = np.array(range(0, z)) * i_rad
        cycles = []
        for i in range(z):
            cycle_disjoint = Utility_Math.pattern_repeats_disjoint([angles[i]], [1], pattern)
            cycles.extend(Utility_Math.pattern_repeats_continuous(cycle_disjoint))
        return cycles

    # returns coordinates of a koch_curve being used with a regular polygon base shape
    # utilizes the koch_curve_line to get the pattern coordinates to use in the reg_poly_pattern to generate final
    # coordinate set for desired koch curve
    def koch_curve_reg_poly(order, n, ratio, m, invert):
        koch_curve = Fractal_Generation.koch_curve_line(order, n, ratio)
        curve = Fractal_Generation.reg_poly_pattern(m, koch_curve, invert)
        return curve

    def koch_curve_z_group(order, n, ratio, z):
        v_rad = Utility_Math.reg_poly_vertex_radians(n)
        i_rad = Utility_Math.reg_poly_inner_radians(n)
        angles = np.insert([0., 0.], 1, np.array([v_rad] * (n - 1)) - np.array(range(0, n - 1)) * i_rad)
        scales = np.insert([(1 - ratio) / 2] * 2, 1, [ratio] * (n - 1))
        koch_curve = Fractal_Generation.koch_curve_line(1, n, ratio)
        z_curve = Fractal_Generation.cyclic_symmetry_pattern(z, [koch_curve])
        curve = Utility_Math.pattern_recursion(order, angles, scales, z_curve)
        return curve

class Image_Draw:
    # returns image of a koch curve in a given screen, with a depth of n and given ratio
    # can be drawn in/out of a regular polygon base shape
    def draw_koch_fractal(order=5, n=3, ratio=1/3, base="reg-poly", mzd=3, invert=False, screen_w=1024, screen_h=768, color=(0,0,0)):
        pygame.init()
        if base == "reg-poly":
            curve = Fractal_Generation.koch_curve_reg_poly(order, n, ratio, mzd, invert)
        elif base == "z-group":
            curve = Fractal_Generation.koch_curve_z_group(order, n, ratio, mzd)
        curve = Utility_Draw.image_screen_fit(screen_w, screen_h, curve)
        Utility_Draw.draw_image(screen_w, screen_h, curve, color)
        pygame.quit()

Image_Draw.draw_koch_fractal(base="z-group")
