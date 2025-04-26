from random import choice, randint

import pygame

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 10

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

class GameObject:
    """Base class for other game objects."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=APPLE_COLOR or SNAKE_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self, position, surface):
        """Abstract placeholder method for drawing the object."""
        rect = pygame.Rect(
            (position[0], position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Class representing the apple and its behavior."""

    def __init__(self, position=(randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                                 randint(0, GRID_HEIGHT - 1) * GRID_SIZE),
                 body_color=APPLE_COLOR):
        """Initializes the apple with a starting position and color."""
        super().__init__(position, body_color)

    def draw(self, surface):
        """Draws the apple on the game surface."""
        super().draw(self.position, surface)

    def randomize_position(self, taken_positions):
        """Sets a random position for the apple, avoiding occupied positions."""
        if len(taken_positions) != GRID_WIDTH * GRID_HEIGHT:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )

            while new_position in taken_positions:
                new_position = (
                    randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                    randint(0, GRID_HEIGHT - 1) * GRID_SIZE
                )

            self.position = new_position
        else:
            raise ValueError('No free positions left for the apple.')


class Snake(GameObject):
    """Class representing the snake and its behavior."""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=SNAKE_COLOR):
        """Initializes the snake with a starting position, color, and state."""
        super().__init__(position, body_color)
        self.positions = [position]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.length = 1
        self.next_direction = RIGHT
        self.last = None

    def update_direction(self):
        """Updates the snake's movement direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Updates the snake's position based on its current direction."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        )
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Draws the snake on the game surface."""
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Returns the position of the snake's head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to the initial state."""
        self.length = 1
        self.positions = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Handles key press events to control the snake."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
    pygame.display.update()


def main():
    """Main game loop and logic."""
    apple = Apple((randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                   randint(0, GRID_HEIGHT - 1) * GRID_SIZE))
    snake = Snake(((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)))
    taken_positions = snake.positions

    while True:
        clock.tick(SPEED)
        handle_keys(snake)

        if snake.get_head_position() == apple.position:
            apple.randomize_position(taken_positions)
            snake.length += 1

        snake.move()
        snake.update_direction()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(taken_positions)

        if len(taken_positions) == GRID_WIDTH * GRID_HEIGHT:
            snake.reset()

        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
