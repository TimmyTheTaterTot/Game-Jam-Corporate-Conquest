import pygame
import Colors as colors
import Fonts as fonts


class Card():
    def __init__(self, title: str, text: str, image_path: str = None, color:tuple = colors.tan):
        self.title = title or None
        self.text = text or None
        self.color = color
        self.image_path = image_path
        self.image = pygame.transform.scale(pygame.image.load(self.image_path), (300, 185))

        self.card_width = 350
        self.card_height = 450

        pygame.font.init()
        self.title_font = fonts.title_font
        self.body_font = fonts.body_font

        self.card = self.build_card()

    
    def build_card(self):
        card_surface = pygame.Surface((self.card_width, self.card_height), pygame.SRCALPHA)
        card_surface.convert_alpha()

        card_base = pygame.draw.rect(card_surface, colors.tan, (0, 0, self.card_width, self.card_height), border_radius=10) # card base
        card_title_label = pygame.draw.rect(card_surface, colors.darker_tan, (0, 15, self.card_width, 65)) # card title label
        picture_base = pygame.draw.rect(card_surface, colors.off_white, (25, 90, self.card_width-50, 185), border_radius=10) # picture base
        body_text_base = pygame.draw.rect(card_surface, colors.darker_tan, (0, 285, self.card_width, 150))

        Card.text_renderer(card_surface, (10, 25), self.card_width-20, self.title_font, self.title) # title text
        Card.text_renderer(card_surface, (10, 295), self.card_width-20, self.body_font, self.text) # body text

        card_surface.blit(self.image, (25, 90), special_flags=pygame.BLEND_RGBA_MIN) # card image


        return card_surface

    @staticmethod
    def text_renderer(surface:pygame.Surface, pos:tuple, text_width:int, font:pygame.font.Font, text:str, color:tuple = colors.black):
        lines = []
        curr_line = ""
        line_height = font.size(' ')[1]

        for word in text.split():
            if font.size(curr_line + word)[0] < text_width:
                curr_line += word + " "
            else:
                lines.append(curr_line)
                curr_line = word + " "
        lines.append(curr_line)

        for i in range(len(lines)):
            surface.blit(font.render(lines[i], True, colors.black), ((text_width-font.size(lines[i])[0]) / 2 + pos[0], pos[1] + (i*line_height)))