from typing import List

import arcade
import random
from random import randint
from arcade import color

WIDTH = 384  # 3072
HEIGHT = 512  # 4096
TITLE = "Démineur"

BACKGROUND_IMAGE = "Sprites/cave_bg.PNG"
CURSEUR_IMAGE = "Sprites/curseur.png"
CASE_VIERGE_IMAGE = "Sprites/panel_wood.png"
CASE_VIDE_IMAGE = "Sprites/panel_woodPaper.png"


class Demineur(arcade.Window):
    """
    Fenêtre principale
    """
    gridSprites: List[List[arcade.Sprite]]
    curseur: arcade.Sprite

    def __init__(self, width: int, height: int, title: str):
        super().__init__(width, height, title)
        self.background = None
        self.grid = None
        self.gridSprites = None
        self.cases = None
        self.hauteur_grille = 0
        self.largeur_grille = 0
        self.offsetX = 40
        self.offsetY = 40
        self.curseur = None
        self.case_vierge_texture = arcade.load_texture(CASE_VIERGE_IMAGE)
        self.case_vide_texture = arcade.load_texture(CASE_VIDE_IMAGE)
        # self.set_mouse_visible(False)

    def setup(self, largeur_grille: int, hauteur_grille: int):
        """
        :param largeur_grille:
        :param hauteur_grille:
        Valeurs :
            0 : vide
            1 : mine
        """
        self.largeur_grille = largeur_grille
        self.hauteur_grille = hauteur_grille
        self.background = arcade.load_texture(BACKGROUND_IMAGE)
        self.cases = arcade.SpriteList()
        self.grid = [[0] * largeur_grille for i in range(hauteur_grille)]
        self.gridSprites = [[arcade.Sprite(CASE_VIERGE_IMAGE)
                             for i in range(largeur_grille)]
                            for j in range(hauteur_grille)]
        self.curseur = arcade.Sprite(CURSEUR_IMAGE)
        largeur_case = WIDTH // (self.largeur_grille + 2)
        hauteur_case = HEIGHT // (self.hauteur_grille + 2)
        for y in range(hauteur_grille):
            for x in range(largeur_grille):
                boite = arcade.Sprite(CASE_VIERGE_IMAGE)
                # print(boite.width, boite.height)
                boite.width = largeur_case
                boite.height = hauteur_case
                boite.center_x = (x + 1.5) * largeur_case
                boite.center_y = (y + 1.5) * hauteur_case
                self.gridSprites[y][x] = boite
                self.cases.append(boite)

    def on_draw(self):
        # print("draw")
        arcade.start_render()
        arcade.draw_texture_rectangle(WIDTH // 2, HEIGHT // 2, WIDTH, HEIGHT, self.background)
        # self.cases.draw()
        for y in range(self.hauteur_grille):
            for x in range(self.largeur_grille):
                center_x, center_y, largeur_case, hauteur_case = self.coordonnees_grille_vers_image(x, y)
                if self.grid[y][x] == 0:
                    texture = self.case_vierge_texture
                else:
                    texture = self.case_vide_texture

                arcade.draw_texture_rectangle(center_x, center_y, largeur_case, hauteur_case, texture)
        self.curseur.draw()

        # arcade.draw_lrtb_rectangle_filled(
        #     x * largeur_case + largeur_case,
        #     (x + 1) * largeur_case + largeur_case,
        #     (y + 1) * hauteur_case + hauteur_case,
        #     y * hauteur_case + hauteur_case,
        #     (randint(0, 255), randint(0, 255), randint(0, 255)))

        # pas besoin de finish_render(), il est appelé automatiquement

    def get_case_la_plus_proche(self, x: float, y: float) -> (int, int):
        largeur_case = WIDTH // (self.largeur_grille + 2)
        hauteur_case = HEIGHT // (self.hauteur_grille + 2)

        case_x = 0
        case_y = 0
        if x < largeur_case * 2:
            case_x = 0
        elif x > WIDTH - largeur_case * 2:
            case_x = self.largeur_grille - 1
        else:
            case_x = x // largeur_case - 1

        if y < hauteur_case * 2:
            case_y = 0
        elif y > HEIGHT - hauteur_case * 2:
            case_y = self.hauteur_grille - 1
        else:
            case_y = y // hauteur_case - 1

        # print(case_x)
        # return self.gridSprites[case_y][case_x]
        return case_x, case_y

    def coordonnees_grille_vers_image(self, x, y) -> (int, int, int, int):
        largeur_case = WIDTH // (self.largeur_grille + 2)
        hauteur_case = HEIGHT // (self.hauteur_grille + 2)
        center_x = (x + 1.5) * largeur_case
        center_y = (y + 1.5) * hauteur_case

        return center_x, center_y, largeur_case, hauteur_case

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        # print("mouse motion")
        super().on_mouse_motion(x, y, dx, dy)
        case_proche = self.get_case_la_plus_proche(x, y)
        # print(case_proche.center_x, case_proche.center_y)
        curseur_x, curseur_y, _, _ = self.coordonnees_grille_vers_image(case_proche[0], case_proche[1])
        self.curseur.set_position(curseur_x, curseur_y)
        # self.curseur.set_position(x, y)

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        super().on_mouse_press(x, y, button, modifiers)
        # print(x, y, button, modifiers)
        case_x, case_y = self.get_case_la_plus_proche(x, y)
        self.grid[case_y][case_x] = 1
        print(self.grid[case_y][case_x])


if __name__ == '__main__':
    window = Demineur(WIDTH, HEIGHT, TITLE)
    window.setup(8, 10)
    arcade.run()
