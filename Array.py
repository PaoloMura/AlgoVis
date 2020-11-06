# sprites for array objects, buttons and text boxes

import pygame

# constants
FONT_SIZE = 50
CELL_WIDTH = 80
LINE_WIDTH = 3
MESSAGE_WIDTH = 600

BLACK = (0,0,0)
WHITE = (255,255,255)
BG_COLOUR = (200,200,200)
HIGHLIGHT_COLOUR = (0,200,0)
SHADOW_COLOUR = (100,100,100)
BTN_COLOUR = (0,100,250)
SELECTED_COLOUR = (0,0,100)


# class for cell sprites used to contain a single value onscreen
class Cell(pygame.sprite.Sprite):
    width = CELL_WIDTH
    def __init__(self, value, coordinate):
        super(Cell, self).__init__()
        self.value = value
        self.coordinate = coordinate    # top left corner of the cell within the screen
        self.height = 0
        self.rect = None
        self.image = self.generate_image(BG_COLOUR)

    # returns a surface for the cell with the given background colour
    def generate_image(self, colour):
        # create the text
        font = pygame.font.Font(None, FONT_SIZE)
        text_image = None
        text_image = font.render(str(self.value), True, BLACK, colour)
        text_width = text_image.get_width()
        self.height = text_image.get_height()
        # create the background
        image = pygame.Surface((self.width, self.height))
        image.fill(colour)
        # blit the text to the background
        start_pos = ((self.width - text_width) / 2, 0)
        image.blit(text_image, start_pos)
        # draw a border around the cell
        self.rect = image.get_rect()
        corners = (self.rect.topleft, self.rect.topright, self.rect.bottomright, self.rect.bottomleft)
        pygame.draw.lines(image, BLACK, True, corners, LINE_WIDTH)
        self.rect.center = self.coordinate
        return image

    def update(self):
        pass

    def get_height(self):
        return self.height

    def get_rect(self):
        return self.rect

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    # changes the background colour of the cell
    def highlight(self, colour):
        self.image = self.generate_image(colour)



# class for button sprites
class Button(Cell):
    width = CELL_WIDTH
    def __init__(self, value, coordinate):
        super().__init__(value, coordinate)
        self.image = self.generate_image(BTN_COLOUR)

    def select(self):
        self.image = self.generate_image(SELECTED_COLOUR)

    def deselect(self):
        self.image = self.generate_image(BTN_COLOUR)



# class for text box sprites
class MessageBox(Cell):
    width = MESSAGE_WIDTH
    def __init__(self, value, coordinate):
        super().__init__(value, coordinate)
        self.image = self.generate_image(WHITE)

    def set_value(self, value):
        self.value = value
        self.image = self.generate_image(WHITE)

    def get_state(self):
        return (self.value)
    
    def set_state(self, state):
        self.set_value(state)




# contains a collection of cells to model an array
class Array(pygame.sprite.Sprite):
    def __init__(self, values, group, screen_width, ycoordinate):
        super(Array, self).__init__()
        self.values = list(values)
        self.group = group
        self.screen_width = screen_width
        self.ycoordinate = ycoordinate
        self.cells = self.create_cells() # a 2D array of Cell objects
        self.highlighted = ()
        self.shadowed = (0, len(self.values)-1)
        self.image = None
        self.rect = None

    # creates a list of Cell object pairs [index_cell, value_cell]
    def create_cells(self):
        x_pos = (self.screen_width - len(self.values) * CELL_WIDTH) * 0.5
        y_pos = self.ycoordinate
        cells = []
        for i in range(len(self.values)):
            # create a cell for the index
            x = x_pos + (i + 0.5) * CELL_WIDTH
            y = y_pos
            index = Cell(str(i), (x,y))
            # create a cell for the value itself
            y += index.get_height()
            value = Cell(str(self.values[i]), (x,y))
            # add the cells to the 2D list and sprite group
            cells.append([index, value])
            self.group.add(index)
            self.group.add(value)
        return cells

    def update(self):
        pass

    def get_state(self):
        return (tuple(self.values), tuple(self.highlighted), tuple(self.shadowed))

    def set_state(self, state):
        self.highlighted = tuple(state[1])
        self.shadowed = tuple(state[2])
        self.replace_values(list(state[0]))
        self.update_colours()

    # shadows/highlights the appropriate cells according to the highlighted and shadowed properties
    def update_colours(self):
        for i in range(len(self.cells)):
            if i in self.highlighted:
                self.cells[i][1].highlight(HIGHLIGHT_COLOUR)
            elif i < self.shadowed[0] or i > self.shadowed[1]:
                self.cells[i][1].highlight(SHADOW_COLOUR)
            else:
                self.cells[i][1].highlight(BG_COLOUR)

    # these two methods update the list of highlighted/shadowed elements
    def highlight(self, indices):
        self.highlighted = tuple(indices)

    def shadow(self, start, end):
        self.shadowed = (start, end)

    # changes the current values in the array to hold the given values instead
    def update_values(self, values):
        self.values = list(values)
        for i in range(len(self.values)):
            self.cells[i][1].set_value(str(self.values[i]))
        self.update_colours()

    # destroys the current array and replaces it with a new array of given values (potentially a different size)
    def replace_values(self, values):
        self.values = list(values)
        for row in self.cells:
            row[0].kill()
            row[1].kill()
        self.cells = self.create_cells()
