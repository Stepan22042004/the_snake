from random import choice, randint

import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


# Тут опишите все классы игры
class GameObject():
    """Базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self):
        """Это абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс унаследованный от GameObject,
    описывающий яблоко и действия с ним.
    """

    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле"""
        self.position = (randint(0, GRID_WIDTH) * GRID_SIZE,
                         randint(0, GRID_HEIGHT) * GRID_SIZE)

    def __init__(self):
        self.body_color = (255, 0, 0)
        self.randomize_position()
        super().__init__()

    def draw(self, surface):
        """Отрисовывает яблоко на игровой поверхности"""
        rect = pygame.Rect((self.position[0], self.position[1]),
                           (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс, унаследованный от GameObject,
    описывающий змейку и её поведение.
    """

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = (1, 0)
        self.next_direction = None
        self.body_color = (0, 255, 0)
        self.last = None

    def reset(self, screen):
        """Сбрасывает змейку в начальное состояние
        после столкновения с собой.
        """
        self.length = 1
        self.positions.clear()
        self.positions.append(self.position)
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.direction = choice(directions)
        screen.fill(BOARD_BACKGROUND_COLOR)

    def update_direction(self):
        """Обновляет направление движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Возвращает позицию головы змейки"""
        return self.positions[0]

    def move(self, screen):
        """Обновляет позицию змейки (координаты каждой секции),
        добавляя новую голову в начало списка positions и
        удаляя последний элемент,
        если длина змейки не увеличилась.
        """
        head_position = self.get_head_position()
        new_head_position_x = head_position[0] + self.direction[0] * GRID_SIZE
        new_head_position_y = head_position[1] + self.direction[1] * GRID_SIZE

        if new_head_position_x < 0:
            new_head_position_x = 620
        elif new_head_position_x > 620:
            new_head_position_x = 0
        elif new_head_position_y < 0:
            new_head_position_y = 460
        elif new_head_position_y > 460:
            new_head_position_y = 0
        new_head_position = (new_head_position_x, new_head_position_y)

        if new_head_position in self.positions[2:]:
            self.reset(screen)
        else:
            self.positions.insert(0, new_head_position)
            self.last = self.positions[-1]
            if len(self.positions) > self.length:
                self.positions.pop()

    def draw(self, surface):
        """Отрисовывает змейку на экране, затирая след"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)


def handle_keys(game_object):
    """Обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main"""
    snake = Snake()
    apple = Apple()
    ...

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move(screen)
        if snake.positions[0] == apple.position:
            apple.randomize_position()
            snake.length += 1
        apple.draw(screen)
        snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()
