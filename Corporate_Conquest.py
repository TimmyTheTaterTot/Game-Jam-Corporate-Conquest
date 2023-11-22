import pygame
import Colors as colors
from Card import Card



class App():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screenwidth = 1000
        self.screenheight = 800

        self.background_image = None
        self.card_background = None

        self.card = None
        self.card_direction = 'c'
        self.card_changed = False
        self.card_width = 350
        self.card_height = 450

        self.base_card_position = ((self.screenwidth/2 - self.card_width/2), (self.screenheight/2 - self.card_height/2))
        self.card_position = self.base_card_position

        self.card_rotation = 0

        self.anim_vars = [self.base_card_position[0], self.base_card_position[0], 1.0]

        self.init_screen()
        self.init_card()
        self.draw_card()
        self.main_loop()


    def init_screen(self):
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
        pygame.display.set_caption("Corporate Conquest")
        self.set_background_image("Images/beach1.jpg")

        self.card_background = pygame.surface.Surface((350, 450))
        pygame.draw.rect(self.card_background, (30, 30, 30), (0, 0, 350, 450), border_radius=10)


    def init_card(self):
        self.card = Card("Placeholder title", "Placeholder body text. This is placeholder body text as a note from your boss", "Images/landscape.png")


    def set_background_image(self, image_path):
        self.background_image = pygame.transform.scale(pygame.image.load(image_path), (1000, 800))

    
    def draw_card(self):
        if self.card_rotation < 0.1 and self.card_rotation > -0.1:
            self.screen.blit(self.card.card, self.card_position)
        else:
            self.screen.blit(pygame.transform.rotate(self.card.card, self.card_rotation), self.card_position)

        
    def draw_background(self, background_image):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.card_background, self.base_card_position, special_flags=pygame.BLEND_ADD)

    
    def animate_card(self):
        if self.card_direction == 'l':
            self.card_rotation = (self.card_rotation + (7 - self.card_rotation) * 0.15)
            self.card_position = (self.card_position[0] + (self.base_card_position[0] - 140 - self.card_position[0]) * 0.15, self.base_card_position[1])
        elif self.card_direction == 'r':
            self.card_rotation = (self.card_rotation + (-7 - self.card_rotation) * 0.15)
            self.card_position = (self.card_position[0] + (self.base_card_position[0] + 60 - self.card_position[0]) * 0.15, self.base_card_position[1])
        elif self.card_direction == 'c':
            self.card_rotation = (self.card_rotation + (-self.card_rotation) * 0.15)
            self.card_position = (self.card_position[0] + (self.base_card_position[0] - self.card_position[0]) * 0.15, self.base_card_position[1])


    def input_handler(self, event):
        sensitivity = 60
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            if y > self.card_position[1] - sensitivity and y < self.base_card_position[1] + self.card_height + sensitivity:
                if x > self.base_card_position[0] - sensitivity and x < self.base_card_position[0] + (self.card_width/2) - sensitivity/2: # right
                    self.card_direction = 'r'
                elif x < self.base_card_position[0] + self.card_width + sensitivity and x > self.base_card_position[0] + (self.card_width/2) + sensitivity/2: # left
                    self.card_direction = 'l'
                else:
                    self.card_direction = 'c'
            else:
                self.card_direction = 'c'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.card_direction == 'l' or self.card_direction == 'r':
                self.make_choice()


    def make_choice(self):
        pass

    
    def main_loop(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.input_handler(event)
            
            
            self.animate_card()

            self.draw_background('Images/beach1.jpg')
            self.draw_card()

            pygame.display.flip()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()