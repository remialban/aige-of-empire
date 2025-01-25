from tkinter import messagebox

import tkinter as tk
from PIL import Image, ImageTk

from core import Game, Player, Map
from core.map import RessourceModes, PlayerModes
from ui import UI
from ui.enums import UIList
from ui.ui_manager import UIManager


class MENU(UI):
    def __init__(self):
        super().__init__()

    def setup(self):
        self.root = tk.Tk()


    def update(self):
        pass  # No dynamic updates needed for this screen

    def cleanup(self):
        self.root.quit()


    def loop(self):
        menu = MenuTkinter(self.root)
        self.root.mainloop()


class MenuTkinter:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Menu")
        self.master.geometry("800x600")

        self.bg_image = Image.open("assets/background.jpg")
        self.bg_image = self.bg_image.resize((900, 700), Image.Resampling.LANCZOS)

        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {"bg": "white", "font": ("Helvetica", 14), "fg": "black", "relief": "solid", "borderwidth": 2}

        self.new_game_button = tk.Button(self.master, text="New Game", command=self.new_game, **button_style)
        self.new_game_button.pack(pady=10)

        self.load_game_button = tk.Button(self.master, text="Load Game", command=self.load_game, **button_style)
        self.load_game_button.pack(pady=10)

        self.quit_button = tk.Button(self.master, text="Quit", command=self.quit_game, **button_style)
        self.quit_button.pack(pady=10)

    def new_game(self):
        self.clear_menu()
        NewGameMenu(self.master, self.bg_photo)

    def load_game(self):
        print("Load game selected.")
        messagebox.showinfo("Load Game", "Game loaded!")

    def quit_game(self):
        print("Quit game selected.")
        self.master.quit()
        UIManager.stop()

    def clear_menu(self):
        for widget in self.master.winfo_children():
            widget.destroy()

class NewGameMenu:
    def __init__(self, master, bg_photo):
        self.master = master
        self.bg_photo = bg_photo
        self.bg_image = Image.open("assets/background.jpg")  # Vérifie si ce fichier existe
        self.bg_image = self.bg_image.resize((1000, 800), Image.Resampling.LANCZOS)  # Taille agrandie
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = tk.Label(self.master, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        button_style = {"bg": "white", "font": ("Helvetica", 14), "fg": "black", "relief": "solid", "borderwidth": 2}

        # Section pour le nombre de joueurs
        self.players_label = tk.Label(self.master, text="Number of Players:", **button_style)
        self.players_label.pack(pady=5)
        self.players_var = tk.IntVar(value=1)
        self.players_option1 = tk.Radiobutton(self.master, text="1 Player", variable=self.players_var, value=1, **button_style)
        self.players_option2 = tk.Radiobutton(self.master, text="2 Players", variable=self.players_var, value=2, **button_style)
        self.players_option1.pack(pady=2)
        self.players_option2.pack(pady=2)

        # Section pour la taille de la carte
        self.map_size_label = tk.Label(self.master, text="Map Size:", **button_style)
        self.map_size_label.pack(pady=5)
        self.map_width_slider = tk.Scale(self.master, from_=50, to=400, resolution=10, orient=tk.HORIZONTAL, label="Width", length=300, **button_style)
        self.map_width_slider.pack(pady=10)
        self.map_height_slider = tk.Scale(self.master, from_=50, to=400, resolution=10, orient=tk.HORIZONTAL, label="Height", length=300, **button_style)
        self.map_height_slider.pack(pady=10)

        # Menu déroulant pour Resource Variation
        self.resource_mode_label = tk.Label(self.master, text="Resource Variation:", **button_style)
        self.resource_mode_label.pack(pady=5)

        self.resource_mode_option_var = tk.StringVar(value="Gold Rush")
        self.resource_mode_option_menu = tk.OptionMenu(self.master, self.resource_mode_option_var, "Gold Rush", "Generous", "Normal")
        self.resource_mode_option_menu.config(**button_style)
        self.resource_mode_option_menu.pack(pady=10)

        # Menu déroulant pour Starting Resources
        self.starting_resources_label = tk.Label(self.master, text="Starting Resources:", **button_style)
        self.starting_resources_label.pack(pady=5)

        self.starting_resources_option_var = tk.StringVar(value="Lean")
        self.starting_resources_option_menu = tk.OptionMenu(self.master, self.starting_resources_option_var, "Lean", "Mean", "Marines")
        self.starting_resources_option_menu.config(**button_style)
        self.starting_resources_option_menu.pack(pady=10)

        # Boutons Start et Back
        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, **button_style)
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(self.master, text="Back", command=self.back_to_main_menu, **button_style)
        self.back_button.pack(pady=10)

    def start_game(self):
        # Obtenir les valeurs des sliders et autres options
        players = self.players_var.get()
        map_width = self.map_width_slider.get()
        map_height = self.map_height_slider.get()
        resource_mode = self.resource_mode_option_var.get()
        starting_resources = self.starting_resources_option_var.get()

        print(f"Starting game with {players} player(s), map size {map_width}x{map_height}, resource mode {resource_mode}, starting resources {starting_resources}.")

        # Logique du jeu ici
        player1 = Player("eee", "MAGENTA")
        player2 = Player("eee", "RED")

        if players == 1:
            players_set = {player1}
        else:
            players_set = {player1, player2}

        map = Map(map_width, map_height, RessourceModes.NORMAL, PlayerModes.LEAN, players_set)

        game = Game(players=players_set, map=map)

        UIManager.set_game(game)
        UIManager.get_current_ui().cleanup()
        UIManager.change_ui(UIList.GUI)

    def back_to_main_menu(self):
        self.cleanup()
        MenuTkinter(self.master)

    def cleanup(self):
        for widget in self.master.winfo_children():
            widget.destroy()
