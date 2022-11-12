import pygame
from menu import *
from board import Board

class GomokuGUI():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Gomoku')
        #pygame.display.set_icon():

        self.running = True
        self.playing = False

        # Game options
        self.checkers = 15
        self.players = 1
        self.difficulty = 7 #depth, only if: 1 PLAYER
        self.debug = 1


        # Dimensions and display
        self.DISPLAY_W, self.DISPLAY_H = 1000,                       600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H)) #Il display totale

        self.GAME_W, self.GAME_H       = self.DISPLAY_H, self.DISPLAY_H
        self.GAME_POS = (0,0)
        self.PLAYABLE_W = (self.GAME_POS[0], self.GAME_POS[0] + self.GAME_W)
        self.PLAYABLE_H = (self.GAME_POS[1], self.GAME_POS[1] + self.GAME_H)
        self.QUAD_W, self.QUAD_H       = self.GAME_W/self.checkers, self.GAME_H/self.checkers
        self.PIECE_DIM = self.QUAD_H/2 - 2
        self.game_rect = pygame.Rect(self.GAME_POS[0], self.GAME_POS[1], self.GAME_W, self.GAME_H)
        self.game_display = self.display.subsurface(self.game_rect) #Il display della board

        self.INFO_W = self.DISPLAY_W - self.GAME_W
        self.INFO_H = self.DISPLAY_H
        self.INFO_POS = (self.GAME_POS[0] + self.GAME_W, self.GAME_POS[1])
        self.info_rect = pygame.Rect(self.INFO_POS[0], self.INFO_POS[1], self.INFO_W, self.INFO_H)
        self.info_display = self.display.subsurface(self.info_rect) #Il display delle info

        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))

        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


        # Details
        self.font_name = 'font/Satisfy-Regular.ttf'
        self.font_size = 45
        self.font_size_info = 30
        self.color1 = (87, 65, 47)
        self.color2 = (195, 156, 107)
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.fps = 30
        self.clock = pygame.time.Clock()
        self.time = pygame.time.get_ticks()//1000
        self.time_start = 0
        self.move_time = 0

        # Game parts
        self.main_menu = MainMenu(self)
        self.curr_menu = self.main_menu

    def game_loop(self):
        self.b = Board(self.checkers, self.players, self.difficulty)
        self.time_start = pygame.time.get_ticks()//1000


        while(self.playing):
            self.check_events() # Verifica i tasti
            self.check_inputs()

            self.update_window()

            self.reset_keys() # Resetta i tasti

    def check_events(self):
        for event in pygame.event.get():
            # Per uscire
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False
                self.curr_menu.run_display = False

            # Per capire le frecce
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

            # Per capire il click
            if event.type == pygame.MOUSEBUTTONUP:
                self.MOUSE_KEY = True



    def check_inputs(self):
        if self.BACK_KEY:
            self.playing = False

        if self.b.win == -1:
            if(self.b.players == 2 or (self.b.players == 1 and self.b.turn == 0)):
                if self.MOUSE_KEY:
                    pos = pygame.mouse.get_pos() #(col, row)

                    if (pos[0] > self.PLAYABLE_W[0] and pos[0] < self.PLAYABLE_W[1]):
                        if (pos[1] > self.PLAYABLE_H[0] and pos[1] < self.PLAYABLE_H[1]):
                            pick_pos = (int((pos[0] - self.GAME_POS[0]) // self.QUAD_W),
                                        int((pos[1] - self.GAME_POS[1]) // self.QUAD_H))

                            #TO-DO: Check game-mode / alternate players if 1v1
                            self.b.move(pick_pos[1], pick_pos[0])

            # Se si gioca da soli ed è il turno dell'ai
            else:
                self.b.getAiMove(self)

    def reset_keys(self):
        self.START_KEY, self.BACK_KEY =  False, False
        self.UP_KEY, self.DOWN_KEY =False, False
        self.LEFT_KEY, self.RIGHT_KEY = False, False
        self.MOUSE_KEY = False





    def update_window(self):
        self.clock.tick(self.fps)
        pygame.event.pump()
        self.time = pygame.time.get_ticks()//1000
        self.draw_canvas()
        self.window.blit(self.display, self.GAME_POS)
        pygame.display.update()

    def draw_canvas(self):

        # Disegna il gioco
        self.game_display.fill(self.color2)
        for i in range(0, self.checkers * self.checkers):
            if (i%2 == 0):

                r = pygame.Rect( self.QUAD_W*(i % self.checkers), self.QUAD_H*(i//self.checkers), self.QUAD_W, self.QUAD_H)
                pygame.draw.rect(self.game_display, self.color1, r, width=0)

        for i in range(self.checkers):
            for j in range(self.checkers):
                if self.b.board[i][j] == self.b.playerSymbol[0]:
                    pygame.draw.circle(self.game_display, self.WHITE,
                                        (j*self.QUAD_W + self.QUAD_W/2, i*self.QUAD_H + self.QUAD_H/2),
                                        self.PIECE_DIM)

                if self.b.board[i][j] == self.b.playerSymbol[1]:
                    pygame.draw.circle(self.game_display, self.BLACK,
                                        (j*self.QUAD_W + self.QUAD_W/2, i*self.QUAD_H + self.QUAD_H/2),
                                        self.PIECE_DIM)

        #SOLO PER TEST E DEBUG -----------------------------------------------------------------------
        if self.debug == 1:
            for sq in self.b.getNearSquares():
                pygame.draw.circle(self.game_display, (200,200,200),
                                    (sq[1]*self.QUAD_W + self.QUAD_W/2, sq[0]*self.QUAD_H + self.QUAD_H/2),
                                    self.PIECE_DIM/2)
            #Godlike squares
            for s in self.b.sequences[self.b.turn][3-1]:
                if(s['openEnds'] > 1):
                    for sq in s['emptySquares']:
                        pygame.draw.circle(self.game_display, (0,255,0),
                                        (sq[1]*self.QUAD_W + self.QUAD_W/2, sq[0]*self.QUAD_H + self.QUAD_H/2),
                                        self.PIECE_DIM/2)
            for s in self.b.sequences[self.b.turn][4-1]:
                for sq in s['emptySquares']:
                    pygame.draw.circle(self.game_display, (0,255,0),
                                    (sq[1]*self.QUAD_W + self.QUAD_W/2, sq[0]*self.QUAD_H + self.QUAD_H/2),
                                    self.PIECE_DIM/2)
            #Danger squares
            for s in self.b.sequences[(self.b.turn + 1) % 2][3-1]:
                if(s['openEnds'] > 1):
                    for sq in s['emptySquares']:
                        pygame.draw.circle(self.game_display, (255,0,0),
                                        (sq[1]*self.QUAD_W + self.QUAD_W/2, sq[0]*self.QUAD_H + self.QUAD_H/2),
                                        self.PIECE_DIM/2)
            for s in self.b.sequences[(self.b.turn + 1) % 2][4-1]:
                for sq in s['emptySquares']:
                    pygame.draw.circle(self.game_display, (255,0,0),
                                    (sq[1]*self.QUAD_W + self.QUAD_W/2, sq[0]*self.QUAD_H + self.QUAD_H/2),
                                    self.PIECE_DIM/2)



        #Last placement
        if(self.b.board[self.b.lastMove[0]][self.b.lastMove[1]] == self.b.playerSymbol[0] and self.b.lastMove != [-1, -1]):
            pygame.draw.circle(self.game_display, self.BLACK,
                                (self.b.lastMove[1]*self.QUAD_W + self.QUAD_W/2, self.b.lastMove[0]*self.QUAD_H + self.QUAD_H/2),
                                self.PIECE_DIM/2)
            pygame.draw.circle(self.game_display, self.WHITE,
                                (self.b.lastMove[1]*self.QUAD_W + self.QUAD_W/2, self.b.lastMove[0]*self.QUAD_H + self.QUAD_H/2),
                                self.PIECE_DIM/3)

        elif(self.b.board[self.b.lastMove[0]][self.b.lastMove[1]] == self.b.playerSymbol[1] and self.b.lastMove != [-1, -1]):
            pygame.draw.circle(self.game_display, self.WHITE,
                                (self.b.lastMove[1]*self.QUAD_W + self.QUAD_W/2, self.b.lastMove[0]*self.QUAD_H + self.QUAD_H/2),
                                self.PIECE_DIM/2)
            pygame.draw.circle(self.game_display, self.BLACK,
                                (self.b.lastMove[1]*self.QUAD_W + self.QUAD_W/2, self.b.lastMove[0]*self.QUAD_H + self.QUAD_H/2),
                                self.PIECE_DIM/3)

        # Disegna le info
        self.info_display.fill(self.BLACK)
        if(self.b.win != -1):
            self.draw_text_info(f"Player {self.b.win + 1} wins!", self.font_size_info, 0, self.font_size_info)
        else:
            self.draw_text_info(f"[Player { self.b.turn + 1}]", self.font_size_info, 0, self.font_size_info)
            self.draw_text_info(f"AI checked { self.b.count[0] }", self.font_size_info, 0, 4*self.font_size_info)
            self.draw_text_info("scenarios for last move", self.font_size_info, 0, 6*self.font_size_info)
            self.draw_text_info(f"in {self.move_time} second(s)", self.font_size_info, 0, 8*self.font_size_info)
            self.draw_text_info(f"AI thinks he is {'winning' if self.b.scores[1] - self.b.scores[0] > 0 else 'losing' }", self.font_size_info, 0, 12*self.font_size_info)
            self.draw_text_info(f"by {(self.b.scores[1] - self.b.scores[0]) if (self.b.scores[1] - self.b.scores[0]) > 0 else -(self.b.scores[1] - self.b.scores[0]) } points", self.font_size_info, 0, 14*self.font_size_info)

            # self.draw_text_info("--------------------------", self.font_size_info, 0, 4*self.font_size_info)
            # self.draw_text_info(f"Score player 1 = { self.b.scores[0] }", self.font_size_info, 0, 6*self.font_size_info)
            # self.draw_text_info(f"Score player 2 = { self.b.scores[1] }", self.font_size_info, 0, 8*self.font_size_info)
            # self.draw_text_info("--------------------------", self.font_size_info, 0, 10*self.font_size_info)



        #self.draw_text_info(f"Timer: 10:36", self.font_size_info, 0 , self.INFO_H - self.font_size_info)
        self.draw_text_info(f"Timer: {(self.time - self.time_start)//60}:{(self.time - self.time_start)%60}", self.font_size_info, 0 , self.INFO_H - self.font_size_info)


        pygame.display.update()

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def draw_text_info(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x + text_rect.w/2 + 10, y)
        self.info_display.blit(text_surface, text_rect)
