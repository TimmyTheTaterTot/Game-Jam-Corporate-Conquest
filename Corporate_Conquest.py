import pygame
import Colors as colors
import Fonts as fonts
import random as rand
from Card import Card



class App():
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()

        self.music_channel = pygame.mixer.Channel(1)
        self.sfx_channel = pygame.mixer.Channel(2)
        self.soundtrack = pygame.mixer.Sound("Sound/Game music.mp3")
        self.soundtrack.set_volume(0.4)
        self.flip_card_sfx = pygame.mixer.Sound("Sound/Card Flip.mp3")

        self.screenwidth = 1000
        self.screenheight = 800

        self.background_image = None
        self.backgrounds = ["Images/Backgrounds/Cubicle Background.png", "Images/Backgrounds/Office Background.png", "Images/Backgrounds/CEO Office Background.png"]
        self.card_background = None

        self.old_card = None
        self.card = None
        self.card_active = False
        self.card_direction = 'c'
        self.card_width = 350
        self.card_height = 450

        self.base_card_position = ((self.screenwidth/2 - self.card_width/2), (self.screenheight/2 - self.card_height/2))
        self.card_position = self.base_card_position
        self.card_rotation = 0
        self.old_card_position = None
        self.old_card_rotation = None

        self.player_karma = 60
        self.player_greed = 0
        self.player_happiness = 0

        self.player_level = 0
        self.card_number = 1
        self.level1_cards = rand.sample([i for i in range(7, 15)], 8)
        self.level2_cards = rand.sample([i for i in range(15, 30)], 15)
        self.level3_cards = rand.sample([i for i in range(30, 45)], 15)

        self.change_card_event_type = pygame.USEREVENT+1
        self.change_card_event = pygame.event.Event(self.change_card_event_type)

        self.game_active = False
        self.game_over = False
        self.title_screen = True

        self.init_screen()
        self.main_loop()


    def init_screen(self):
        self.screen = pygame.display.set_mode((self.screenwidth, self.screenheight))
        pygame.display.set_caption("Corporate Conquest")

        self.set_background_image("Images/Backgrounds/Title Screen.png")
        self.music_channel.play(self.soundtrack, -1, fade_ms=1000)
        

    def init_game_screen(self):
        self.init_cards()
        self.set_background_image(self.backgrounds[0])

        self.card_background = pygame.surface.Surface((350, 450))
        pygame.draw.rect(self.card_background, (30, 30, 30), (0, 0, 350, 450), border_radius=10)


    def init_cards(self):
        with open("Card_Data/card_data.txt", "r") as card_file:
            self.cards = []
            card_file_data = card_file.read()
            for data_block in card_file_data.split("~"):
                card_data = []
                for line in data_block.split('\n'):
                    card_data.append(line)
                self.cards.append(card_data[1:7]) # remove the empty strings at the end of each list from splittin the lines

        self.card = Card(*self.cards[self.card_number])
        self.card_active = True


    def load_new_card(self):
        if self.player_level == 0:
            if self.card_number < 6:
                self.card_number += 1
            else:
                self.card_number += 1
                self.player_level += 1

        elif self.player_level == 1:
            if len(self.level1_cards) == 0:
                self.level1_cards = rand.sample([i for i in range(7, 15)], 8)
            self.card_number = self.level1_cards.pop(0)

        elif self.player_level == 2:
            if len(self.level2_cards) == 0:
                self.level2_cards = rand.sample([i for i in range(15, 30)], 15)
            self.card_number = self.level2_cards.pop(0)

        elif self.player_level == 3:
            if len(self.level3_cards) == 0:
                self.level3_cards = rand.sample([i for i in range(30, 45)], 15)
            self.card_number = self.level3_cards.pop(0)

        self.sfx_channel.play(self.flip_card_sfx, 0)
        return Card(*self.cards[self.card_number])
            


    def set_background_image(self, image_path):
        self.background_image = pygame.transform.scale(pygame.image.load(image_path), (1000, 800))

    
    def draw_card(self):
        if self.card_rotation < 0.1 and self.card_rotation > -0.1:
            self.screen.blit(self.card.card, self.card_position)
        else:
            self.screen.blit(pygame.transform.rotate(self.card.card, self.card_rotation), self.card_position)

        if self.old_card != None:
            self.screen.blit(pygame.transform.rotate(self.old_card.card, self.old_card_rotation), self.old_card_position)

        
    def draw_background(self):
        self.screen.blit(self.background_image, (0, 0))
        if self.game_active:
            self.screen.blit(self.card_background, self.base_card_position, special_flags=pygame.BLEND_ADD)
            Card.text_renderer(self.screen, (10, 10), 600, fonts.score, f"Greed: {self.player_greed} Happiness: {self.player_happiness}", False)

    
    def animate_card_tilt(self):
        if self.card_direction == 'l':
            self.card_rotation = (self.card_rotation + (7 - self.card_rotation) * 0.15)
            self.card_position = (self.card_position[0] + (self.base_card_position[0] - 140 - self.card_position[0]) * 0.15, self.base_card_position[1])
        elif self.card_direction == 'r':
            self.card_rotation = (self.card_rotation + (-7 - self.card_rotation) * 0.15)
            self.card_position = (self.card_position[0] + (self.base_card_position[0] + 60 - self.card_position[0]) * 0.15, self.base_card_position[1])
        elif self.card_direction == 'c':
            self.card_rotation = (self.card_rotation + (-self.card_rotation) * 0.15)
            self.card_position = (self.card_position[0] + (self.base_card_position[0] - self.card_position[0]) * 0.15, self.base_card_position[1])


    def animate_card_change(self):
        self.card_rotation = (self.card_rotation + (-self.card_rotation) * 0.075)
        self.card_position = (self.card_position[0] + (self.base_card_position[0] - self.card_position[0]) * 0.075, self.base_card_position[1])
        
        if self.card_direction == "l":
            self.old_card_rotation = (self.old_card_rotation + (90-self.old_card_rotation) * 0.05)
            self.old_card_position = (self.old_card_position[0] + (-550 - self.old_card_position[0]) * 0.05, self.old_card_position[1] + (1000 - self.old_card_position[1])*0.05)
        if self.card_direction == "r":
            self.old_card_rotation = (self.old_card_rotation + (-90-self.old_card_rotation) * 0.05)
            self.old_card_position = (self.old_card_position[0] + (900 - self.old_card_position[0]) * 0.05, self.old_card_position[1] + (1000 - self.old_card_position[1])*0.05)


    def input_handler(self, event):
        sensitivity = 60
        if event.type == pygame.MOUSEMOTION:
            if self.card_active:
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
            if self.card_active:
                if self.card_direction == 'l' or self.card_direction == 'r':
                    self.make_choice()


        # REMOVE BEFORE FINAL GAME DEPLOYMENT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.win_game()
            elif event.key == pygame.K_l:
                self.fail_game()


    def check_stats(self):
        if self.player_level == 0:
            pass
        elif self.player_level == 1:
            if self.player_karma < 0:
                self.fail_game()
            elif self.player_greed >= 100:
                self.player_level += 1
                self.player_karma = 60
                self.promotion()
        elif self.player_level == 2:
            if self.player_karma < 0:
                self.fail_game()
            elif self.player_greed >= 200:
                self.player_level += 1
                self.player_karma = 60
                self.promotion()
        elif self.player_level == 3:
            if self.player_karma < 0:
                self.fail_game()
            elif self.player_greed >= 300:
                self.win_game()


    def make_choice(self):
        if self.card_direction == 'l':
            self.player_karma += int(self.card.left_choice_stats[0])
            self.player_greed += int(self.card.left_choice_stats[1])
            self.player_happiness += int(self.card.left_choice_stats[2])
        elif self.card_direction == 'r':
            self.player_karma += int(self.card.right_choice_stats[0])
            self.player_greed += int(self.card.right_choice_stats[1])
            self.player_happiness += int(self.card.right_choice_stats[2])


        self.check_stats()


        pygame.time.set_timer(self.change_card_event, 1200, 1)
        self.card_active = False

        if self.card != None:
            self.old_card_position = self.card_position
            self.old_card_rotation = self.card_rotation
            self.old_card = self.card

        self.card = self.load_new_card()
        self.card_position = (-350, self.base_card_position[1])
        self.card_rotation = 180


    def fail_game(self):
        self.game_active = False
        self.game_over = True
        self.set_background_image("Images/Backgrounds/Fail Screen.png")


    def win_game(self):
        self.game_active = False
        self.game_over = True
        self.set_background_image("Images/Backgrounds/Win Screen.png")


    def promotion(self):
        self.game_active = False
        self.set_background_image("Images/Backgrounds/Promotion Screen.png")

    
    def main_loop(self):
        running = True
        while running:
            if self.game_active:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == self.change_card_event_type:
                        self.old_card = None
                        self.card_active = True
                    else:
                        self.input_handler(event)
                
                if self.card_active:
                    self.animate_card_tilt()
                else:
                    self.animate_card_change()

                self.draw_background()
                self.draw_card()
            else:
                if self.game_over:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                running = False
                    self.draw_background()
                elif self.title_screen:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.init_game_screen()
                                self.game_active = True
                                self.title_screen = False

                    self.draw_background()
                else:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        elif event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_RETURN:
                                self.game_active = True
                                self.old_card = None
                                self.card_active = True
                                self.set_background_image(self.backgrounds[self.player_level-1])

                    self.draw_background()


            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    app = App()