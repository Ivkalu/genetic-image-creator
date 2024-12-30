import pygame
import numpy as np
from utils import *
import random

def randomPointColor(size = 5):
    points = [(random.randint(0, IMG_WIDTH), random.randint(0, IMG_HEIGHT)) for _ in range(size)]
    c = pygame.color.Color(random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(0, 255),
                            random.randint(*ALPHA_VALUE_RANGE))
    return points, c

class Obj:
    img: pygame.Surface
    loss: float

    def __init__(self, rand=False):
        if not rand:
            return
        
        self.img = pygame.Surface((IMG_WIDTH, IMG_HEIGHT))
        _, c = randomPointColor()
        self.img.fill(c)
        self._create_shapes(GENOME_COUNT, self.img)

    def _create_shapes(self, shape_count, surface):
        for _ in range(shape_count):
            if DRAW_WITH_CIRCLE:
                points, c = randomPointColor(1)
                pygame.draw.circle(surface, c, points[0], random.randint(0, MAX_CIRCLE_SIZE))
            else:
                points, c = randomPointColor()
                pygame.draw.polygon(surface, c, points, 0)

    def calc_loss(self, img):
        self.loss = get_pixel_delta_e_difference(self.img, img)
        return self

    def fuck(self, other):
        img1 = self.img.copy().convert_alpha()
        img2 = other.img.copy().convert_alpha()
        o = Obj()
        chance = np.random.uniform(0, 1)

        # Reproduce by alpha values, highest chance
        if chance < REPRODUCTION_CHANCE[0]:
            blended_surface = pygame.Surface((IMG_WIDTH, IMG_HEIGHT)).convert_alpha()
            alpha = np.random.uniform(0, 1)

            img1_array = pygame.surfarray.pixels3d(img1)
            img2_array = pygame.surfarray.pixels3d(img2)
            img1_alpha = pygame.surfarray.pixels_alpha(img1)
            img2_alpha = pygame.surfarray.pixels_alpha(img2)

            blended_rgb = alpha * img1_array + (1 - alpha) * img2_array
            blended_alpha = alpha * img1_alpha + (1 - alpha) * img2_alpha

            pygame.surfarray.blit_array(blended_surface, blended_rgb)
            pygame.surfarray.pixels_alpha(blended_surface)[:] = blended_alpha

            o.img = blended_surface

        # Reproduce with random pixels, very small chance 
        elif chance < sum(REPRODUCTION_CHANCE[:1]):
            child_img = pygame.Surface((img1.get_width(), img1.get_height()), pygame.SRCALPHA)

            # Use numpy arrays for faster pixel manipulation
            img1_array = pygame.surfarray.pixels3d(img1)
            img2_array = pygame.surfarray.pixels3d(img2)
            child_array = pygame.surfarray.pixels3d(child_img)

            mask = np.random.rand(img1.get_width(), img1.get_height(), 1) < 0.5
            child_array[mask] = img1_array[mask]
            child_array[~mask] = img2_array[~mask]

            pygame.surfarray.blit_array(child_img, child_array)
            o.img = child_img

        # Reproduce by taking upper part of one img and lower part of other img
        else:
            cut_value = np.random.uniform(0, 1)

            combined_surface = pygame.Surface((IMG_WIDTH, IMG_HEIGHT))
            upper_rect = pygame.Rect(0, 0, IMG_WIDTH, IMG_HEIGHT * cut_value)  # Upper half
            combined_surface.blit(img1, (0, 0), upper_rect)

            lower_rect = pygame.Rect(0, IMG_HEIGHT * cut_value, IMG_WIDTH, IMG_HEIGHT * (1-cut_value)+1)  # Lower half
            combined_surface.blit(img2, (0, IMG_HEIGHT * cut_value), lower_rect)

            o.img = combined_surface
            
        return o
    
    def mutate(self):
        chance = np.random.uniform(0, 1)
        # Chance for any mutation
        if chance > MUTATION_CHANCE:
            return
    
        chance = np.random.uniform(0, 1)
        # Chance to mutate by creating new polygon
        if chance < 0.5:            
            tmp_surface = pygame.Surface((IMG_WIDTH, IMG_HEIGHT), pygame.SRCALPHA)
            self._create_shapes(1, tmp_surface)
            self.img.blit(tmp_surface, (0, 0))

        # Chance to mutate by adding some random pixels
        else:
            for _ in range(RANDOM_PIXELS):
                points, c = randomPointColor(1)
                self.img.fill(c, (points[0], (1, 1)))
            
    def __lt__(self, other):
        return self.loss < other.loss