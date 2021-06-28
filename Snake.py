import pygame
from pygame.locals import *
import time
import random

# global variables.
SIZE = 40
BACK_GROUND_COLOR = (48, 98, 105)


class food:
    def __init__(self, parent_screen):
        self.apple = pygame.image.load('icons/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE*3
        self.y = SIZE*3

    def draw_apple(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 19) * SIZE
        self.y = random.randint(0, 14) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load('icons/block_build.jpg').convert()
        self.x = [40]*length
        self.y = [40]*length
        self.direction = 'right'

    def increase_length(self):
        self.length += 1
        self.x.append(1)
        self.y.append(1)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
            pygame.display.flip()

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def walk(self):
        # follows tail
        for i in (range(self.length-1, 0, -1)):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'right':
            self.x[0] += SIZE

        if self.direction == 'left':
            self.x[0] -= SIZE

        if self.direction == 'up':
            self.y[0] -= SIZE

        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()


class Game:

    def __init__(self):
        # initialising.....
        pygame.init()
        pygame.mixer.init()

        # play background music...
        self.play_background()

        # template creator and providing basic surface.........
        self.surface = pygame.display.set_mode((1000, 700))
        self.surface.fill((48, 98, 105))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = food(self.surface)
        self.apple.draw_apple()

    def collision_control(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background(self):
        pygame.mixer.music.load("icons/bg_music.mp3")
        pygame.mixer.music.play()

    # gameplay sounds.....
    def playsound(self, sound):
        sound = pygame.mixer.Sound(f"icons/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    # game background.....
    def render_background(self):
        background = pygame.image.load("icons/background.jpg")
        self.surface.blit(background, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw_apple()
        self.score()
        pygame.display.flip()

        # for apple collision
        if self.collision_control(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.snake.increase_length()
            self.apple.move()
            self.playsound("apple")

        # for self collision
        for i in range(3, self.snake.length):
            if self.collision_control(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.playsound("hit")
                raise "Game Over"

        # to hit boundary wall .....(tried)
        if not(0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 700):
            self.playsound("hit")
            raise 'hit boundry wall exception'

        # game over message for the user.

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Ariel', 50)
        line1 = font.render(
            f"Game Over Score: {(((self.snake.length)*10)-10)}", True, (255, 255, 255))
        self.surface.blit(line1, (300, 300))
        line2 = font.render("Press Enter for New Game", True, (255, 255, 255))
        self.surface.blit(line2, (300, 350))
        pygame.display.flip()

        # stop the bg_music......
        pygame.mixer.music.pause()

    def score(self):
        font = pygame.font.SysFont('Ariel', 30)
        score = font.render(
            f"Score:{(((self.snake.length)*10)-10)}", True, (255, 255, 255))
        self.surface.blit(score, (900, 10))

    def reset_game(self):
        self.snake = Snake(self.surface, 1)
        self.apple = food(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    elif event.key == K_RETURN:
                        # resuming the paused bg_music.....
                        # pygame.mixer.music.unpause()
                        # but i want to fresh play the music......
                        self.play_background()
                        pause = False

                        # block movement.
                    if not pause:
                        if event.key == K_UP or event.key == K_w:
                            self.snake.move_up()

                        elif event.key == K_DOWN or event.key == K_s:
                            self.snake.move_down()

                        elif event.key == K_RIGHT or event.key == K_d:
                            self.snake.move_right()

                        elif event.key == K_LEFT or event.key == K_a:
                            self.snake.move_left()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset_game()

            time.sleep(0.10)


    # Main function of Python Entry.
if __name__ == "__main__":
    game = Game()
    game.run()
