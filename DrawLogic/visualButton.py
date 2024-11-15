""" Button Class for Game Flow. """

import pygame

pygame.font.init()
# author: ChatGPT

class Button:
    """ Generic Button """
    
    HOVER_COLOR      = (211, 211, 211) # light gray
    BACKGROUND_COLOR = (169, 169, 169) # another gray

    def __init__(self,
                 text: str,
                 width: int,
                 height: int,
                 pos: tuple[int, int], # position on screen
                 hovered = False
                 ) -> None:
        
        self.text = text
        self.width = width
        self.height = height
        self.post = pos
        self.rect = pygame.Rect(pos[0], pos[1], width, height)
        self.hovered = hovered
        self.textColor = (70, 130, 180)
        self.font = pygame.font.Font(None, 36)

    def draw(self, screen):
        if self.hovered:
            pygame.draw.rect(screen, Button.HOVER_COLOR, self.rect)
        else:
            pygame.draw.rect(screen, Button.BACKGROUND_COLOR, self.rect)
        
        text_surface = self.font.render(self.text, True, self.textColor)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def hovering(self, mousePos):
        """ Manipulates hover status. """
        if self.rect.collidepoint(mousePos):
            self.hovered = True
        else:
            self.hovered = False

    def clicked(self, pygameEvent) -> bool:
        if pygameEvent.type == pygame.MOUSEBUTTONDOWN and self.hovered:
            return True
        else:
            return False
        

class InputBox:

    INACTIVE    = (16, 110, 111) # blue
    ACTIVE      = (0, 255, 255) # light blue
    FONT        = pygame.font.Font(None, 50)

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = InputBox.INACTIVE
        self.text = text
        self.txt_surface = InputBox.FONT.render(text, True, self.color)
        self.active = False

    def entry(self, event) -> str | None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = InputBox.ACTIVE if self.active else InputBox.INACTIVE

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    return self.text  # Return the text on pressing Enter
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = InputBox.FONT.render(self.text, True, self.color)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)