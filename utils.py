import pygame
import numpy as np
import random
from colour import *

IMAGE_PATH = "monalisa.png" #Image path for recreation

IMG_WIDTH, IMG_HEIGHT = 40, 40 #Image for recreation width and height
SCREEN_WIDTH, SCREEN_HEIGHT = 1600, 400 #Display width and height

ALPHA_VALUE_RANGE = 255, 255 #Alpha value for new shapes created with mutation
GENOME_COUNT = 8 #Number of shapes in objects of inital population

REPRODUCTION_CHANCE = [0.65, 0.05, 0.3] #Chance of reproduction methods => 
# 0: Reproduce by alpha values, highest chance
# 1: Reproduce with random pixels, very small chance
# 2: Reproduce with bottom and top parts of images, medium chance
MUTATION_CHANCE = 0.05 #Chance of mutation

DRAW_WITH_CIRCLE = False #Draw shapes with circles instead of polygons
MAX_CIRCLE_SIZE = 12 #Max circle size if DRAW_WITH_CIRCLE is True
RANDOM_PIXELS = 10 #Number of random pixels to change in mutation method 2

MAX_POPULATION = 400 #Max population size
TOURNAMENT_SIZE = 4 #Tournament size for selection method
ELITISM_RATE = 0.01 #Elitism rate for selection method



def tournament_selection(population, tournament_size=3, selection_probability=0.8):
    tournament = random.sample(population, tournament_size)
    tournament.sort()
    
    if random.random() < selection_probability:
        return tournament[0]
    else:
        return random.choice(tournament)

def get_pixel_delta_e_difference(img1, img2):
    """Calculate the Delta E difference between two surfaces and return the summed difference."""
    img1_array = pygame.surfarray.array3d(img1)
    img2_array = pygame.surfarray.array3d(img2)

    img1_array = img1_array / 255.0
    img2_array = img2_array / 255.0

    lab_img1 = rgb_to_lab(img1_array)
    lab_img2 = rgb_to_lab(img2_array)

    delta_e_diff = np.linalg.norm(lab_img1 - lab_img2, axis=2)

    return np.sum(delta_e_diff)

def rgb_to_lab(rgb_array):
    """Convert an RGB numpy array to CIE Lab color space."""
    xyz_array = sRGB_to_XYZ(rgb_array)
    lab_array = XYZ_to_Lab(xyz_array)

    return lab_array