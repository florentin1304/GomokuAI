from gomokugui import GomokuGUI


if __name__ == "__main__":
    gomoku = GomokuGUI()
    while gomoku.running:
        print("Menu")
        gomoku.curr_menu.display_menu()
        print("Game")
        gomoku.game_loop()

#Devi capire perch`e ci sta mettendo MOLTO di pi`u a creare le nuove mosse
#Devi aggiustare la checkSequences in modo che guardi gli estremi liberi :/

#se 2 pezzi da 3 si incontrano sullo stesso punto per fare 4, si blocca wtf

