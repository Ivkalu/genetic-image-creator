import pygame
import sys
from obj import Obj
from utils import *

if __name__ == "__main__":
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Image and Shape Drawer")

    image = pygame.image.load(IMAGE_PATH)
    image = pygame.transform.scale(image, (IMG_WIDTH, IMG_HEIGHT))

    population = [Obj(rand=True).calc_loss(image) for _ in range(MAX_POPULATION)]

    it = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        population.sort()
        new_population = population[:int(MAX_POPULATION*ELITISM_RATE)]
        while len(new_population) < MAX_POPULATION:
            parent1 = tournament_selection(population, tournament_size=TOURNAMENT_SIZE)
            parent2 = tournament_selection(population, tournament_size=TOURNAMENT_SIZE)

            child = parent1.fuck(parent2)
            child.mutate()
            child.calc_loss(image)

            new_population.append(child)

        population = new_population
        
        total_loss= sum([i.loss for i in population])
        print(f"{it}: {total_loss/IMG_WIDTH/IMG_HEIGHT/MAX_POPULATION}")

        for ind, img in enumerate([image, population[0].img, population[MAX_POPULATION//2].img, population[-1].img]):
            resized_img1 = pygame.transform.scale(img, (400, 400))
            screen.blit(resized_img1, (ind*400, 0))  

        pygame.display.flip()
        it += 1
