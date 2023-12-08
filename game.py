import pygame

from board import Board
from snake import Snake

from enums.cell_type import CellType
from enums.direction import Direction


class Game:
    __FPS = 60

    def __init__(self, width, height):
        self.screen = pygame.display.set_mode((width, height))
        self.__is_finished = False
        self.is_game_over = False

        self.in_game_score_font = pygame.font.Font("./assets/upheavtt.ttf", 30)
        self.header_font = pygame.font.Font("./assets/upheavtt.ttf", 60)
        self.sub_header_font = pygame.font.Font("./assets/upheavtt.ttf", 30)

        self.is_started = False

        self.init_game()

    def init_game(self):
        self.__clock = pygame.time.Clock()
        self.current_direction = Direction.DOWN

        left, top, x_size, y_size, cell_size = self.return_board_cords(30, 20, 20)
        self.game_board = Board(self.screen, left, top, x_size, y_size, cell_size)

        self.snake = Snake(self.game_board.starting_snake_cells())

        self.action_timer = pygame.time.get_ticks()

        self.score = 0

    def start_game(self):
        self.is_started = True
        self.game_board.generate_food()

    def restart_game(self):
        self.score = 0
        self.is_game_over = False
        self.snake = Snake(self.game_board.starting_snake_cells())
        self.game_board.remove_food()
        self.game_board.generate_food()

    def draw_score(self):
        text = f"Score: {self.score}"
        text_surf = self.in_game_score_font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surf, self.game_board.bottom_left_point)


    def draw_header(self, header, sub_header):
        text = header 
        text_surf = self.header_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(
            center=(self.screen.get_width() // 2, self.screen.get_height() // 2)
        )

        sub_text = sub_header
        sub_text_surf = self.sub_header_font.render(sub_text, True, (255, 255, 255))
        sub_text_rect = sub_text_surf.get_rect(
            center=(self.screen.get_width() // 2, text_rect.bottomleft[1])
        )

        self.screen.blit(text_surf, text_rect)
        self.screen.blit(sub_text_surf, sub_text_rect)

    def return_board_cords(self, x_size, y_size, cell_size):
        center_point_x = self.screen.get_width() // 2
        center_point_y = self.screen.get_height() // 2

        total_width = x_size * cell_size
        total_height = y_size * cell_size
        left = center_point_x - total_width // 2
        top = center_point_y - total_height // 2

        return left, top, x_size, y_size, cell_size

    @property
    def is_finished(self):
        return self.__is_finished

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__is_finished = True
            elif event.type == pygame.KEYDOWN:
                if (
                    event.key == pygame.K_s or event.key == pygame.K_j
                ) and self.current_direction != Direction.UP:
                    self.current_direction = Direction.DOWN
                if (
                    event.key == pygame.K_a or event.key == pygame.K_h
                ) and self.current_direction != Direction.RIGHT:
                    self.current_direction = Direction.LEFT
                if (
                    event.key == pygame.K_d or event.key == pygame.K_l
                ) and self.current_direction != Direction.LEFT:
                    self.current_direction = Direction.RIGHT
                if (
                    event.key == pygame.K_w or event.key == pygame.K_l
                ) and self.current_direction != Direction.DOWN:
                    self.current_direction = Direction.UP
                if event.key == pygame.K_r and self.is_game_over:
                    self.restart_game()
                if event.key == pygame.K_q:
                    self.__is_finished = True
                if event.key == pygame.K_SPACE and not self.is_started:
                    self.start_game()

    def update(self):
        try:
            current_timer = pygame.time.get_ticks()
            if not self.is_game_over and current_timer - self.action_timer >= 80 and self.is_started:
                next_cell = self.game_board.get_next_cell(
                    self.snake.snake_head, self.current_direction
                )
                if next_cell.cell_type == CellType.FOOD:
                    self.game_board.generate_food()
                    self.score += 1
                if self.snake.check_self_bite(next_cell):
                    self.is_game_over = True
                self.snake.move(next_cell)
                self.action_timer = current_timer
        except IndexError:
            self.is_game_over = True
        self.handle_events()

    def render(self):
        self.screen.fill(Board.EMPTY_CELL_COLOR)
        if self.is_started:
            self.game_board.draw_board()
            self.draw_score()
        else:
            self.draw_header("Wonsz The Game", "Press SPACE to start the game")

        if self.is_game_over:
            self.draw_header("Game Over", "Press R to start again or Q to exit")

        pygame.display.flip()
        self.__clock.tick(self.__FPS)


if __name__ == "__main__":
    pygame.init()
    game = Game(800, 600)

    while not game.is_finished:
        game.update()
        game.render()
    pygame.quit()
