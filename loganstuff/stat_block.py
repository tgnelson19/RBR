import pygame
pygame.init()

class statBlock:
  

    def __init__(self,pX,pY,w,h,bg_color,text_color,font_size, stats=None):
        self.pX = pX
        self.pY = pY
        self.w = w
        self.h = h
        self.bg_color = bg_color
        self.text_color = text_color

        if stats is None:
            stats = {}
        self.stats = stats

        self.font = pygame.font.Font("media/coolveticarg.otf", font_size)


    def drawStatblock(self,screen):
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)

        # 2) Fill the overlay with (r, g, b, alpha).
        #    For example, alpha=128 means ~50% transparent.
        overlay.fill((self.bg_color.r, self.bg_color.g, self.bg_color.b, 128))

        # 3) Blit that semi-transparent overlay onto the main screen
        screen.blit(overlay, (self.pX, self.pY))

        line_height = self.font.get_height()  # The height of a single line of text
        line_spacing = 5                      # Extra spacing between lines
        offset_x = 10                         # A little offset from the left edge
        offset_y = 10                         # A little offset from the top edge

        current_y = self.pY + offset_y

        for stat_name, stat_value in self.stats.items():
            # Format the line: e.g. "HP: 100"
            line_text = f"{stat_name}: {stat_value}"
            text_surface = self.font.render(line_text, True, self.text_color)

            # Blit (draw) the text
            screen.blit(text_surface, (self.pX + offset_x, current_y))

            # Move down for next line
            current_y += line_height + line_spacing




