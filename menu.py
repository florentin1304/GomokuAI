import pygame

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True

        self.cursor_rect = pygame.Rect(0, 0, self.game.font_size, self.game.font_size)
        self.offset = -130


    def draw_cursor(self):
        self.game.draw_text('>', self.game.font_size, self.cursor_rect.x, self.cursor_rect.y)
        self.game.window.blit(self.game.display,(0,0))
        pygame.display.update()
        self.game.reset_keys()

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()



class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.states = ["Start game", "Options", "Exit game"]
        self.n_states = len(self.states)
        self.state = 0

        self.states_x = [ self.mid_w                              for i in range(0,self.n_states) ]
        self.states_y = [ self.mid_h + 10 + self.game.font_size*i for i in range(0,self.n_states) ]

        self.cursor_rect.midtop = (self.states_x[0] + self.offset, self.states_y[0])

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Gomoku", self.game.font_size, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 2*self.game.font_size)

            for i in range(0,self.n_states):
                self.game.draw_text(self.states[i], self.game.font_size, self.states_x[i], self.states_y[i])

            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.DOWN_KEY:
            self.state += 1
            if(self.state >= self.n_states):
                self.state = 0

            self.cursor_rect.midtop = (self.states_x[self.state] + self.offset, self.states_y[self.state])

        if self.game.UP_KEY:
            self.state -= 1
            if(self.state < 0):
                self.state = self.n_states - 1

            self.cursor_rect.midtop = (self.states_x[self.state] + self.offset, self.states_y[self.state])

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.states[self.state] == 'Start game':
                self.game.playing = True
            elif self.states[self.state] == 'Options':
                self.game.options()
            elif self.states[self.state] == 'Exit game':
                self.game.playing = False
                self.game.running = False

            self.run_display = False # <<< 'Annulla' il menu principale e da via al resto

