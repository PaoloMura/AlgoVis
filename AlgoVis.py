# algorithm visualisation simulation

from Array import *
from Mediator import *
from LinearSearch import *
from BinarySearch import *
from AlgorithmFactory import AlgoFactory
from States import *
import pygame
from pygame import time
import random
from enum import Enum

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    MOUSEBUTTONDOWN,
    QUIT,
)


# CONSTANTS:
WHITE = (255,255,255)
ARRAY_LENGTH_BOUNDS = (5,10)
ARRAY_VALUE_BOUNDS = (0,99)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500

LIN_SEAR = 0
BIN_SEAR = 1
BUB_SORT = 2
INS_SORT = 3
MER_SORT = 4
QUI_SORT = 5

ALGO_NAMES = ["Linear Search", "Binary Search", "Bubble Sort",
              "Insertion Sort", "Merge Sort", "Quick Sort"]


# randomly generate an array
def generate_array(algo):
    if algo == BIN_SEAR:
        return generate_sorted_array()
    else:
        array = []
        length = random.randint(ARRAY_LENGTH_BOUNDS[0], ARRAY_LENGTH_BOUNDS[1])
        for i in range(length):
            value = random.randint(ARRAY_VALUE_BOUNDS[0], ARRAY_VALUE_BOUNDS[1])
            array.append(value)
        return array


# randomly generate a sorted array
def generate_sorted_array():
    length = random.randint(ARRAY_LENGTH_BOUNDS[0], ARRAY_LENGTH_BOUNDS[1])
    array = [random.randint(ARRAY_VALUE_BOUNDS[0], int(ARRAY_VALUE_BOUNDS[1]/length))]
    for i in range(1, length):
        # the following tries to ensure a mostly balanced distrubtion of numbers
        value = 0
        low = array[i-1]
        high = int(ARRAY_VALUE_BOUNDS[0] + (i+1) * (ARRAY_VALUE_BOUNDS[1] - ARRAY_VALUE_BOUNDS[0]) / length)
        value = random.randint(low, high)
        array.append(value)
    return array


# main procedure for AlgoVis
def run_algorithm(algo):
    # setup the screen
    screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
    screen.fill(WHITE)
    pygame.display.set_caption(ALGO_NAMES[algo])

    # SPRITE GROUPS: create the sprites groups
    all_sprites = pygame.sprite.Group()
    buttons = pygame.sprite.Group()

    # SPRITE: create the array
    values = generate_array(algo)
    array = Array(values, all_sprites, SCREEN_WIDTH, SCREEN_HEIGHT * 0.2)

    # SPRITE: create the subarrays for merge sort
    left_array = Array([], all_sprites, SCREEN_WIDTH * 0.5, SCREEN_HEIGHT * 0.4)
    right_array = Array([], all_sprites, SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 0.4)

    # SPRITE: create the navigation/control buttons
    i = SCREEN_WIDTH * 0.9
    j = SCREEN_HEIGHT * 0.9
    btn_next = Button("Next", (i,j))
    buttons.add(btn_next)

    i = SCREEN_WIDTH * 0.1
    j = SCREEN_HEIGHT * 0.9
    btn_prev = Button("Prev", (i,j))
    buttons.add(btn_prev)

    i = SCREEN_WIDTH * 0.1
    j = SCREEN_HEIGHT * 0.1
    btn_exit = Button("Exit", (i,j))
    buttons.add(btn_exit)

    i = SCREEN_WIDTH * 0.9
    j = SCREEN_HEIGHT * 0.1
    btn_new = Button("New", (i,j))
    buttons.add(btn_new)

    for button in buttons:
        all_sprites.add(button)

    # SPRITE: create a box to contain descriptive messages
    i = SCREEN_WIDTH * 0.5
    j = SCREEN_HEIGHT * 0.6
    box_description = MessageBox("", (i,j))
    all_sprites.add(box_description)

    # SPRITE: create a box to contain the result
    i = SCREEN_WIDTH * 0.5
    j = SCREEN_HEIGHT * 0.7
    box_result = MessageBox("Result = ", (i,j))
    all_sprites.add(box_result)


    # create a Mediator to coordinate calls to the sprites
    mediator = None
    if algo == MER_SORT:
        mediator = MergeMediator(array, left_array, right_array, box_description, box_result)
    else:
        mediator = Mediator(array, box_description, box_result)

    # instantiate the algorithm
    search_item = None
    factory = AlgoFactory()
    algorithm = None
    if algo == LIN_SEAR:
        algorithm = factory.create_lin_sear(values, mediator)
        search_item = algorithm.get_item()
    elif algo == BIN_SEAR:
        algorithm = factory.create_bin_sear(values, mediator)
        search_item = algorithm.get_item()
    elif algo == BUB_SORT:
        algorithm = factory.create_bub_sort(values, mediator)
    elif algo == INS_SORT:
        algorithm = factory.create_ins_sort(values, mediator)
    elif algo == MER_SORT:
        algorithm = factory.create_mer_sort(values, mediator)


    # SPRITE: create a box to contain the item being searched for
    if algo == LIN_SEAR or algo == BIN_SEAR:
        i = SCREEN_WIDTH * 0.5
        j = SCREEN_HEIGHT * 0.5
        box_item = MessageBox("Looking for: "+ str(search_item), (i,j))
        all_sprites.add(box_item)

    # initialise the memento stack
    stack = MementoStack()
    stack.push_memento(Memento(array.get_state(), box_description.get_state(), box_result.get_state(), algorithm.get_state()))


    # Event loop
    running = True
    while running:
        for button in buttons:
            button.deselect()
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_RIGHT:
                    btn_next.select()
                elif event.key == K_LEFT:
                    btn_prev.select()
            elif event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(mouse_pos):
                        button.select()
                        if button == btn_next and not algorithm.is_finished():
                            memento = None
                            if algo == MER_SORT:
                                memento = MergeMemento(array.get_state(), left_array.get_state(), right_array.get_state(),
                                                        box_description.get_state(), box_result.get_state(), algorithm.get_state())
                            else:
                                memento = Memento(array.get_state(), box_description.get_state(), box_result.get_state(), algorithm.get_state())
                            stack.push_memento(memento)
                            algorithm.next()
                        elif button == btn_prev and algorithm.is_started():
                            memento = stack.pop_memento()
                            if memento != None:
                                array.set_state(memento.array_state)
                                box_description.set_state(memento.description_state)
                                box_result.set_state(memento.result_state)
                                algorithm.set_state(memento.algo_state)
                                if type(memento) == MergeMemento:
                                    left_array.set_state(memento.child1_state)
                                    right_array.set_state(memento.child2_state)
                        elif button == btn_new:
                            return True
                        elif button == btn_exit:
                            return False

        all_sprites.update()
        screen.fill(WHITE)
        all_sprites.draw(screen)
        pygame.display.flip()


def run(algo):
    pygame.init()
    again = run_algorithm(algo)
    pygame.quit()
    return again
