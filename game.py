import pygame
import random

pygame.init()

WIDTH, HEIGHT = 900, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

PIXEL = 30
FPS = 15

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 255, 0

SCORE = 0
SCORE_FONT = pygame.font.SysFont("comicsans", 30)


class Snake:
    VEL = PIXEL

    def __init__(self):
        self.head = Head(WIDTH//2 - Tile.SIDE//2, HEIGHT//2 - Tile.SIDE//2)
        self.body = [self.head]
    
    def get_positions(self):
        return [(tile.x, tile.y) for tile in self.body]

    def move(self):
        new_tile = Tile(self.head.x, self.head.y)

        if self.head.direction == "UP":
            self.head.y -= self.VEL
        
        elif self.head.direction == "DOWN":
            self.head.y += self.VEL
        
        elif self.head.direction == "LEFT":
            self.head.x -= self.VEL
        
        elif self.head.direction == "RIGHT":
            self.head.x += self.VEL
        
        self.body.insert(1, new_tile)
        self.body = self.body[:-1]
    
    def new_tile(self):
        self.body.insert(1, Tile(self.head.x, self.head.y))


class Tile:
    COLOR = WHITE
    SIDE = PIXEL
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        pygame.draw.rect(WINDOW, WHITE, (self.x, self.y, self.SIDE, self.SIDE))


class Head(Tile):
    def __init__(self, x, y, direction="DOWN"):
        super().__init__(x, y)
        self.direction = direction
    
    def change_direction(self, new_direction):
        if self.direction == "UP" and new_direction != "DOWN":
            self.direction = new_direction
        
        elif self.direction == "DOWN" and new_direction != "UP":
            self.direction = new_direction
        
        elif self.direction == "LEFT" and new_direction != "RIGHT":
            self.direction = new_direction
        
        elif self.direction == "RIGHT" and new_direction != "LEFT":
            self.direction = new_direction


class Border:
    COLOR = WHITE
    SIZE = PIXEL / 6

    def draw(self):
        pygame.draw.rect(WINDOW, self.COLOR, (self.SIZE, self.SIZE, WIDTH - (2 * self.SIZE), self.SIZE))
        pygame.draw.rect(WINDOW, self.COLOR, (self.SIZE, self.SIZE, self.SIZE, HEIGHT - (2 * self.SIZE)))
        pygame.draw.rect(WINDOW, self.COLOR, (self.SIZE, HEIGHT - (2 * self.SIZE), WIDTH - (2 * self.SIZE), self.SIZE))
        pygame.draw.rect(WINDOW, self.COLOR, (WIDTH - (2 * self.SIZE), self.SIZE, self.SIZE, HEIGHT - (2 * self.SIZE)))


class Food:
    COLOR = WHITE
    RADIUS = PIXEL / 4

    def __init__(self):
        self.x = random.randrange(PIXEL, WIDTH - PIXEL, PIXEL)
        self.y = random.randrange(PIXEL, HEIGHT - PIXEL, PIXEL)
        

    def draw(self):
        pygame.draw.circle(WINDOW, self.COLOR, (self.x, self.y), self.RADIUS)
    
    def reset(self, taken_pos):
        self.__init__()
        while (self.x, self.y) in taken_pos:
            self.__init__()

        self.draw()


def draw(snake, border, food):
    WINDOW.fill(BLACK)
    
    for tile in snake.body:
        tile.draw()

    border.draw()
    food.draw()

    score_text = SCORE_FONT.render(f"{SCORE}", 1, GREEN)
    WINDOW.blit(score_text, (WIDTH * 15 // 16 - score_text.get_width() // 2, 20))

    pygame.display.update()


def handle_movement(keys, snake):
    head = snake.head

    if keys[pygame.K_w]:
        head.change_direction("UP")
    
    elif keys[pygame.K_s]:
        head.change_direction("DOWN")
    
    elif keys[pygame.K_a]:
        head.change_direction("LEFT")
    
    elif keys[pygame.K_d]:
        head.change_direction("RIGHT")

    
    if head.direction == "UP" and head.y >= head.SIDE // 2:
        snake.move()
    
    elif head.direction == "DOWN" and (head.y + head.SIDE) <= (HEIGHT - head.SIDE // 2):
        snake.move()
    
    elif head.direction == "LEFT" and head.x >= head.SIDE // 2:
        snake.move()
    
    elif head.direction == "RIGHT" and (head.x + head.SIDE) <= (WIDTH - head.SIDE // 2):
        snake.move()


def handle_collisions(snake, food):
    global SCORE

    head = snake.head

    # Collisions with border
    if head.direction == "UP" and head.y < head.SIDE // 2:
        return False
    
    elif head.direction == "DOWN" and (head.y + head.SIDE) > (HEIGHT - head.SIDE // 2):
        return False
    
    elif head.direction == "LEFT" and head.x < head.SIDE // 2:
        return False
    
    elif head.direction == "RIGHT" and (head.x + head.SIDE) > (WIDTH - head.SIDE // 2):
        return False

    # Collisions with food
    if head.x <= food.x <= head.x + head.SIDE and head.y <= food.y <= head.y + head.SIDE:
        SCORE += 1
        snake.new_tile()
        food.reset(snake.get_positions())
        return True
    
    # Collisions with itself
    if len(snake.body) > 4:
        for tile in snake.body[1:]:
            if head.x == tile.x and head.y == tile.y:
                return False
    
    return True


def main():
    running = True
    clock = pygame.time.Clock()

    snake = Snake()    
    border = Border()

    food = Food()

    while running:
        clock.tick(FPS)
        draw(snake, border, food)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        handle_movement(pygame.key.get_pressed(), snake)
        running = handle_collisions(snake, food)
        

        
    
    pygame.quit()

if __name__ == "__main__":
    main()