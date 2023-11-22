import pygame
import Colors as colors
from Card import Card



class App():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screenwidth = 1000
        self.screenheight = 800

        self.card = None
        self.card_direction = 'c'
        self.card_changed = False
        self.card_width = 350
        self.card_height = 450

        self.anim_vars = [0.0, 30.0, 1.0]

        self.base_card_position = ((self.screenwidth/2 - self.card_width/2), (self.screenheight/2 - self.card_height/2))
        self.card_position = self.base_card_position

        self.init_screen()
        self.init_card()
        self.draw_card()
        self.main_loop()


    def init_screen(self):
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
        pygame.display.set_caption("Corporate Conquest")
        self.screen.fill(colors.light_blue)


    def init_card(self):
        self.card = Card("Placeholder title", "Placeholder body text. This is placeholder body text as a note from your boss", "Images/landscape.png")

    
    def draw_card(self):
        self.screen.blit(self.card.card, self.card_position)

        
    def draw_background(self, background_image):
        card_background = pygame.surface.Surface((350, 450))
        pygame.draw.rect(card_background, (30, 30, 30), (0, 0, 350, 450), border_radius=10)
        self.screen.blit(card_background, self.card_position, special_flags=pygame.BLEND_ADD)

    
    def animate_card(self, reset):
        if reset:
            A = 0
            B = 1
            C = 1
        else:
            A, B, C = self.anim_vars

        value = (C * A) + ((1-C) * B)
        C /= 1.3
        self.anim_vars = [A, B, C]

        if self.card_direction == 'l':
            self.card_position = (self.base_card_position[0] - value*40, self.base_card_position[1])
        elif self.card_direction == 'r':
            self.card_position = (self.base_card_position[0] + value*40, self.base_card_position[1])
        elif self.card_direction == 'c' and self.card_position[0] < self.base_card_position[0]-2:
            self.card_position = (self.base_card_position[0] - 40 + value*40, self.base_card_position[1])
        elif self.card_direction == 'c' and self.card_position[0] > self.base_card_position[0]+2:
            self.card_position = (self.base_card_position[0] + 40 - value*40, self.base_card_position[1])


    def input_handler(self, event):
        sensitivity = 40
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            old_direction = self.card_direction
            if y > self.card_position[1] - sensitivity and y < self.base_card_position[1] + self.card_height + sensitivity:
                if x > self.base_card_position[0] - sensitivity and x < self.base_card_position[0] + (self.card_width/2) - sensitivity: # right
                    self.card_direction = 'r'
                elif x < self.base_card_position[0] + self.card_width + sensitivity and x > self.base_card_position[0] + (self.card_width/2) + sensitivity: # left
                    self.card_direction = 'l'
                else:
                    self.card_direction = 'c'
            else:
                self.card_direction = 'c'

            if old_direction != self.card_direction:
                self.card_changed = True


    
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.input_handler(event)
            
            if self.card_changed:
                self.animate_card(True)
                self.card_changed = False
            else:
                self.animate_card(False)


            self.screen.fill(colors.light_blue)
            self.draw_card()

            pygame.display.flip()
            self.clock.tick(30)


if __name__ == "__main__":
    app = App()