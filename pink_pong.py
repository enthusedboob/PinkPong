# Mini Project 2 - Pong

import pygame

def main():
    pygame.init()

    pygame.display.set_mode((500, 400))  # create display window

    pygame.display.set_caption(' ~ pink pong ~ ')  # set window title
    
    w_surface = pygame.display.get_surface()  # get display surface
    
    pygame.font.init()
    
    game = Game(w_surface)  # create game object
    
    game.play()  # start game loop
    
    pygame.quit()  # quit pygame & clean window
    
## User-defined Classes ##
    
class Game:  # An object in this class represents a complete game.
    def __init__(self, surface):  # - self is Game to initialize
        # - surface is display window surface object
        
        # === objects that are part of every game
        self.surface = surface
        self.bg_color = pygame.Color('pink')
        self.FPS = 60
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game = True
        
        # === game specific objects
        self.max_score = 11
        self.left_score = 0
        self.right_score = 0
        self.small_dot = Dot('palevioletred1', 7, [50, 50], [2, 4], self.surface)
        self.paddle_right = Paddle(430, 50, 10, 50, 'palevioletred1', self.surface)
        self.paddle_left = Paddle(50, 50, 10, 50, 'palevioletred1', self.surface)
        self.score_font = pygame.font.SysFont("Arial", 24, bold=False, italic=False)
        self.max_frames = 15000
        self.frame_counter = 0

    def play(self):  # Play the game until player presses close box
        # - self id the Game that should be continued or not
        last_frame = False
        while not self.close_clicked: # until the player clicks close box
            self.handle_events()
            if ((self.left_score < self.max_score) and (self.right_score < self.max_score)):
                self.draw()
                if self.continue_game:
                    self.update()
                    self.decide_continue()
                self.game_Clock.tick(self.FPS)  # run at most with FPS Frames Per Second
            elif last_frame == False:
                self.draw()
                last_frame = True

    def handle_events(self): # Handle each user event by changing game state appropriately
        # - self is the Game whose events will be handled
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            if event.type == pygame.KEYUP:
                self.handle_key_up(event)
            if event.type == pygame.KEYDOWN:
                self.handle_key_down(event)

    def handle_key_down(self, event):
        if event.key == pygame.K_q:  # move left paddle up
            self.paddle_left.set_velocity(-10)
        elif event.key == pygame.K_a:  # move left paddle down
            self.paddle_left.set_velocity(10)
        if event.key == pygame.K_p:  # move right paddle up
            self.paddle_right.set_velocity(-10)
        elif event.key == pygame.K_l:  # move right paddle down
            self.paddle_right.set_velocity(10)        

    def handle_key_up(self, event):
        # stop left paddle up and down
        if event.key in (pygame.K_q, pygame.K_a):
            self.paddle_left.set_velocity(0)     
        # stop right paddle up and down
        if event.key in (pygame.K_p, pygame.K_l):
            self.paddle_right.set_velocity(0)       
    
    def draw(self):  # Draw all game objects
        # - self is the Game to draw
        self.surface.fill(self.bg_color)  # clear the display surface first
        self.small_dot.draw()
        self.paddle_left.draw()
        self.paddle_right.draw()
        self.draw_score()
        pygame.display.update()  # make update surface appear on display
    
    def collisions(self):
        # paddle collisions
        if self.paddle_left.rect.collidepoint(self.small_dot.center) and self.small_dot.velocity[0] < 0:
            self.small_dot.velocity[0] = -self.small_dot.velocity[0]  
        elif self.paddle_right.rect.collidepoint(self.small_dot.center) and self.small_dot.velocity[0] > 0:
            self.small_dot.velocity[0] = -self.small_dot.velocity[0]                
    
    def keep_score(self):
        if self.small_dot.center[0] >= 500:
            self.left_score += 1
        elif self.small_dot.center[0] <= 0:
            self.right_score += 1

    def draw_score(self):
        score_font = pygame.font.Font(None, 60)
        left_score_text = score_font.render(str(self.left_score), True, (255, 130, 171))
        self.surface.blit(left_score_text, (10, 10))
        right_score_text = score_font.render(str(self.right_score), True, (255, 130, 171))
        self.surface.blit(right_score_text, (450, 10))
        pygame.display.flip()

    def update(self):  # Update the game objects for the next frame
        # - self is the Game to update
        self.small_dot.move()
        self.paddle_left.move()
        self.paddle_right.move()
        self.collisions()
        self.keep_score()
        self.frame_counter += 1
        
    def decide_continue(self):  # Check and remember if the game should continue
        # - self is the Game to check
        if self.frame_counter > self.max_frames:
            self.continue_game = False

class Paddle:  # coord is top left of paddle (x, y)
    def __init__(self, x, y, width, height, color, surface):
        self.rect = pygame.Rect(x, y, width, height) # Rect object
        self.color = pygame.Color(color)  # paddle color
        self.surface = surface  # where paddle will be created and move
        self.v_velocity = 0  # vertical velocity       

    def draw(self):
        pygame.draw.rect(self.surface, self.color, self.rect)

    def set_velocity(self, distance):
        self.v_velocity = distance
    
    def move(self):
        self.rect.move_ip(0, self.v_velocity)
        # stop at bottom of screen
        if self.rect.bottom >= self.surface.get_height():
            self.rect.bottom = self.surface.get_height()
        # stop at top of screen
        elif self.rect.y < 0:
            self.rect.y = 0

class Dot:  # An object in this class represents a moving Dot
    def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):  # Initialize a Dot.
        self.color = pygame.Color(dot_color)
        self.radius = dot_radius  # pixel radius as int
        self.center = dot_center  # [X, Y]
        self.velocity = dot_velocity  # [X, Y]
        self.surface = surface  # window's pygame.Surface object

    def move(self):  # - self is the Dot
        for i in range(0, 2):  # ball movement
            self.center[i] += (self.velocity[i])
        # wall collisions
        if self.center[0] >= 500 or self.center[0] <= 0:  # right and left wall
            self.velocity[0] = -self.velocity[0]
        elif self.center[1] > 400 or self.center[1] < 0:  # bottom and top wall
            self.velocity[1] = -self.velocity[1]

    def draw(self):  # Draw dot on surface  # - self is the Dot
        pygame.draw.circle(self.surface, self.color, self.center, self.radius)

main()