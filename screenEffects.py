import pygame

class ScreenEffects:

    class ExplosionEffect:
        """
        A nested class representing a single explosion effect on screen.
        """
        def __init__(self, x, y, radius, duration_frames):
            """
            x, y           = center of the explosion
            radius         = how big the circle is
            duration_frames= how many frames to display this effect
            """
            self.x = x
            self.y = y
            self.radius = radius
            self.duration = duration_frames  # frames left to live

        def update_and_draw(self, screen,cx,cy,radius):
            """
            Draw the explosion (e.g., a red ring) and decrement the lifetime.
            Returns True if still alive, False if done and should be removed.
            """
            overlay = pygame.Surface((2*radius, 2*radius), pygame.SRCALPHA)


            # Example: a red outline circle
            pygame.draw.circle(
            overlay,
            (255, 0, 0, 128),     # RGBA
            (radius, radius),               # circle center relative to overlay
            radius                     # radius
            )

            screen.blit(overlay, (cx - radius, cy - radius))

            self.duration -= 1
            return (self.duration > 0)

    # ---------------------------------------------------------------
    # End of ExplosionEffect definition; now the rest of ScreenEffects
    # ---------------------------------------------------------------



    def __init__(self):
        self.effects = []  # a list of effect objects (e.g., ExplosionEffect)

    def add_explosion(self, x, y, radius, duration_frames):
        """
        Create a new ExplosionEffect and add it to our internal list.
        """
        new_effect = self.ExplosionEffect(x, y, radius, duration_frames)
        self.effects.append(new_effect)

    def update_and_draw(self, screen):
        """
        Loop over each effect, update/draw it, remove when done.
        """
        for effect in self.effects[:]:
            still_alive = effect.update_and_draw(screen)
            if not still_alive:
                self.effects.remove(effect)
