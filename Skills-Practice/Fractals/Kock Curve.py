import pygame
import numpy as np

pygame.init()
screen_w = 1024
screen_h = 768
screen = pygame.display.set_mode((screen_w, screen_h))

def matrix_manipulation(this, ratio, size, pos_arr, angle, theta):
    this.r = ratio
    this.s = size
    this.a = angle
    this.pos_arr = pos_arr
    this.rot_matrix = np.array([[np.cos(this.a), -np.sin(this.a)], [np.sin(this.a), np.cos(this.a)]])
    this.sld_matrix = np.array([[1], [0]])
    return this.s * this.r * (np.matmul(this.rot_matrix, this.pos_arr)) + this.sld_matrix

def koch_curve(this, order, ratio, size, n, pos):
    this.ratio = ratio
    this.ang = np.deg2rad(360/n)

    rotations = [0, this.ang, -this.ang, 0]
    for rot in rotations:
        this.pos_arr = np.array([[pos.x], [pos.y]])
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