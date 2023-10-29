import pygame
import sys
import math

SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300
LINE_INTERVAL = 100
BOARD_LINE_NUMS = 3
LINE_LENGTH = BOARD_LINE_NUMS * LINE_INTERVAL
CIRCLE_RADIUS = 40
LINE_WIDTH = 3
FPS = 20

# 颜色定义
BOARD_COLOR = (0xE3, 0x92, 0x65)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class Board():
    """
    井字棋：
    vs_cpu：是否和计算机对战
    cpu_first：计算机是否先攻
    """
    board_map = [[0] * BOARD_LINE_NUMS for _ in range(BOARD_LINE_NUMS)] # 棋盘上存储每个位置棋的内容的map
    user_step = 1 # 1 -- O,  -1 -- X
    vs_cpu = False
    winner = None
    depth = 9
    cpu_chess = 1
    def __init__(self, vs_cpu:bool, cpu_first=None) -> None:
        self.vs_cpu = vs_cpu
        self.cpu_chess = self.user_step if cpu_first else -self.user_step
        if self.vs_cpu and self.user_step == self.cpu_chess:
            move = self.get_best_move()
            if move:
                self.board_map[move[0]][move[1]] = self.cpu_chess
                self.user_step = -self.user_step

    def get_best_move(self):
        best_move = None
        max_eval = -math.inf
        for move in self.get_available_moves():
            i, j = move
            self.board_map[i][j] = self.cpu_chess
            move_eval = self.minimax(self.depth, -math.inf, math.inf, False)
            self.board_map[i][j] = 0
            if move_eval > max_eval:
                max_eval = move_eval
                best_move = move
        return best_move
    
    def get_available_moves(self):
        moves = set()
        for i in range(BOARD_LINE_NUMS):
            for j in range(BOARD_LINE_NUMS):
                if self.board_map[i][j] == 0:
                    moves.add((i, j))
        return moves
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        if depth == 0 or self.board_is_full() or self.check_win():
            return self.get_current_score()
        if maximizing_player:
            # ai player
            max_eval = -math.inf
            for move in self.get_available_moves():
                i, j = move
                self.board_map[i][j] = self.cpu_chess
                eval = self.minimax(depth - 1, alpha, beta, False)
                self.board_map[i][j] = 0
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            # user player
            min_eval = math.inf
            for move in self.get_available_moves():
                i, j = move
                self.board_map[i][j] = -self.cpu_chess
                eval = self.minimax(depth - 1, alpha, beta, True)
                self.board_map[i][j] = 0
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval
    def board_is_full(self):
        for i in range(BOARD_LINE_NUMS):
            for j in range(BOARD_LINE_NUMS):
                if self.board_map[i][j] == 0:
                    return False
        return True
    
    def get_current_score(self):
        score = 0
        for i in range(BOARD_LINE_NUMS):
            # 横向检查三连
            cpu_chess_sums = sum([self.board_map[i][0] == self.cpu_chess, self.board_map[i][1] == self.cpu_chess, self.board_map[i][2] == self.cpu_chess])
            user_chess_sums = sum([self.board_map[i][0] == -self.cpu_chess, self.board_map[i][1] == -self.cpu_chess, self.board_map[i][2] == -self.cpu_chess])
            if cpu_chess_sums == 3 and user_chess_sums == 0:
                score += 100 # ai三连
            elif cpu_chess_sums == 0 and user_chess_sums == 3:
                score -= 100 # user三连
            elif cpu_chess_sums == 2 and user_chess_sums == 0:
                score += 50 # 活2
            elif cpu_chess_sums == 0 and user_chess_sums == 2:
                score -= 50
            elif cpu_chess_sums == 1 and user_chess_sums == 0:
                score += 10
            elif cpu_chess_sums == 0 and user_chess_sums == 1:
                score -= 10
            # 纵向检查三连
            cpu_chess_sums = sum([self.board_map[0][i] == self.cpu_chess, self.board_map[1][i] == self.cpu_chess, self.board_map[2][i] == self.cpu_chess])
            user_chess_sums = sum([self.board_map[0][i] == -self.cpu_chess, self.board_map[1][i] == -self.cpu_chess, self.board_map[2][i] == -self.cpu_chess])
            if cpu_chess_sums == 3 and user_chess_sums == 0:
                score += 100 # ai三连
            elif cpu_chess_sums == 0 and user_chess_sums == 3:
                score -= 100 # user三连
            elif cpu_chess_sums == 2 and user_chess_sums == 0:
                score += 50 # 活2
            elif cpu_chess_sums == 0 and user_chess_sums == 2:
                score -= 50
            elif cpu_chess_sums == 1 and user_chess_sums == 0:
                score += 10
            elif cpu_chess_sums == 0 and user_chess_sums == 1:
                score -= 10
        # 两个斜向检查
        cpu_chess_sums = sum([self.board_map[0][0] == self.cpu_chess, self.board_map[1][1] == self.cpu_chess, self.board_map[2][2] == self.cpu_chess])
        user_chess_sums = sum([self.board_map[0][0] == -self.cpu_chess, self.board_map[1][1] == -self.cpu_chess, self.board_map[2][2] == -self.cpu_chess])
        if cpu_chess_sums == 3 and user_chess_sums == 0:
            score += 100 # ai三连
        elif cpu_chess_sums == 0 and user_chess_sums == 3:
            score -= 100 # user三连
        elif cpu_chess_sums == 2 and user_chess_sums == 0:
            score += 50 # 活2
        elif cpu_chess_sums == 0 and user_chess_sums == 2:
            score -= 50
        elif cpu_chess_sums == 1 and user_chess_sums == 0:
            score += 10
        elif cpu_chess_sums == 0 and user_chess_sums == 1:
            score -= 10
        
        cpu_chess_sums = sum([self.board_map[2][0] == self.cpu_chess, self.board_map[1][1] == self.cpu_chess, self.board_map[0][2] == self.cpu_chess])
        user_chess_sums = sum([self.board_map[2][0] == -self.cpu_chess, self.board_map[1][1] == -self.cpu_chess, self.board_map[0][2] == -self.cpu_chess])
        if cpu_chess_sums == 3 and user_chess_sums == 0:
            score += 100 # ai三连
        elif cpu_chess_sums == 0 and user_chess_sums == 3:
            score -= 100 # user三连
        elif cpu_chess_sums == 2 and user_chess_sums == 0:
            score += 50 # 活2
        elif cpu_chess_sums == 0 and user_chess_sums == 2:
            score -= 50
        elif cpu_chess_sums == 1 and user_chess_sums == 0:
            score += 10
        elif cpu_chess_sums == 0 and user_chess_sums == 1:
            score -= 10
        return score

    def flip(self, screen):
        screen.fill(WHITE)
        left, top = 0, 0
        for i in range(1, BOARD_LINE_NUMS):
            self.draw_line(screen, (left + i * LINE_INTERVAL, top), (left + i * LINE_INTERVAL, top + LINE_LENGTH))
            self.draw_line(screen, (left, top + i * LINE_INTERVAL), (left + LINE_LENGTH, top + i * LINE_INTERVAL))
        
        for i in range(BOARD_LINE_NUMS):
            for j in range(BOARD_LINE_NUMS):
                if self.board_map[i][j] == 1:
                    self.draw_chess_o(screen, i, j)
                elif self.board_map[i][j] == -1:
                    self.draw_chess_x(screen, i, j)
    
    # 画棋盘线条
    def draw_line(self, screen, start, end):
        pygame.draw.line(screen, BLACK, start, end, LINE_WIDTH)
    
    def draw_user_mouse_position(self, screen, mouse_pos, mouse_pressed):
        left_mouse_pressed = mouse_pressed[0]
        mouse_left, mouse_top = mouse_pos[0], mouse_pos[1]

        j, i = mouse_left // LINE_INTERVAL, mouse_top // LINE_INTERVAL
        if self.board_map[i][j] != 0:
            return None
        if not left_mouse_pressed:
            self.draw_user_chess(screen, i, j)
        else:
            self.board_map[i][j] = self.user_step
            if self.check_win():
                return self.user_step
            if self.board_is_full():
                return 0
            self.user_step = -self.user_step
            if self.vs_cpu and self.user_step == self.cpu_chess:
                move = self.get_best_move()
                if move:
                    self.board_map[move[0]][move[1]] = self.cpu_chess
                    self.user_step = -self.user_step
                if self.check_win():
                    return self.cpu_chess
                if self.board_is_full():
                    return 0
        return None
    
    def draw_user_chess(self, screen, idx_i, idx_j):
        if self.user_step == 1:
            # draw circle
            self.draw_chess_o(screen, idx_i, idx_j)
        else:
            self.draw_chess_x(screen, idx_i, idx_j)
    
    def draw_chess_o(self, screen, idx_i, idx_j):
        left, top = idx_j * LINE_INTERVAL + LINE_INTERVAL // 2, idx_i * LINE_INTERVAL + LINE_INTERVAL // 2
        # draw circle
        pygame.draw.circle(screen, BLACK, (left, top), CIRCLE_RADIUS)
        pygame.draw.circle(screen, WHITE, (left, top), CIRCLE_RADIUS - LINE_WIDTH)

    def draw_chess_x(self, screen, idx_i, idx_j):
        left, top = idx_j * LINE_INTERVAL + LINE_INTERVAL // 2, idx_i * LINE_INTERVAL + LINE_INTERVAL // 2
        # draw X
        length = CIRCLE_RADIUS // 2 + 10
        for direction in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            pygame.draw.line(screen, BLACK, (left, top), (left + direction[0] * length, top + direction[1] * length), LINE_WIDTH)
    
    def check_win(self):
        for i in range(BOARD_LINE_NUMS):
            if self.board_map[i][0] == self.board_map[i][1] == self.board_map[i][2] == 1:
                self.winner = 1
                return True
            elif self.board_map[i][0] == self.board_map[i][1] == self.board_map[i][2] == -1:
                self.winner = -1
                return True
            elif self.board_map[0][i] == self.board_map[1][i] == self.board_map[2][i] == 1:
                self.winner = 1
                return True
            elif self.board_map[0][i] == self.board_map[1][i] == self.board_map[2][i] == -1:
                self.winner = -1
                return True
        if self.board_map[0][0] == self.board_map[1][1] == self.board_map[2][2] == 1:
            self.winner = 1
            return True
        elif self.board_map[0][0] == self.board_map[1][1] == self.board_map[2][2] == -1:
            self.winner = -1
            return True
        elif self.board_map[2][0] == self.board_map[1][1] == self.board_map[0][2] == 1:
            self.winner = 1
            return True
        elif self.board_map[2][0] == self.board_map[1][1] == self.board_map[0][2] == -1:
            self.winner = -1
            return True
        
        return False


# 程序入口
if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('井字棋')
    board = Board(True, False) # 更改此处选择人机还是人人对战，以及计算机先走还是后走
    res = None
    # 主循环
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if res != None:
            if board.vs_cpu:
                if res == board.cpu_chess:
                    print('CPU WIN!!')
                elif res == -board.cpu_chess:
                    print("Player WIN!!")
                else:
                    print('Draw Game!!')
            elif res != 0:
                print('User ' + ('O' if res == 1 else 'X') + ' WIN!!')
            else:
                print('Draw Game!!')
            pygame.quit()
            sys.exit()
        
        board.flip(screen)

        # 获取鼠标输入位置并显示
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        res = board.draw_user_mouse_position(screen, mouse_pos, mouse_pressed)
        
        # 屏幕刷新
        pygame.display.flip()
        clock.tick(FPS)