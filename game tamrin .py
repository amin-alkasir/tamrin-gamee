import pygame
import random
import math

# Game settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Shape settings
SQUARE = "square"
RECTANGLE = "rectangle"
TRIANGLE = "triangle"

# Probability of changing to different shapes
PROB_SQUARE = 0.5
PROB_RECTANGLE = 0.3
PROB_TRIANGLE = 0.2

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shape Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

class Shape:
    def __init__(self, shape_type, x, y):
        self.shape_type = shape_type
        self.x = x
        self.y = y
        self.direction = random.randint(0, 360)
        if self.shape_type == SQUARE:
            self.width, self.height = 30, 30
        elif self.shape_type == RECTANGLE:
            self.width, self.height = 50, 30
        elif self.shape_type == TRIANGLE:
            self.width, self.height = 50, 50
    
    def draw(self):
        if self.shape_type == SQUARE:
            pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, self.width, self.height))
        elif self.shape_type == RECTANGLE:
            pygame.draw.rect(screen, BLACK, pygame.Rect(self.x, self.y, self.width, self.height))
        elif self.shape_type == TRIANGLE:
            points = [
                (self.x, self.y),
                (self.x + self.width * math.cos(math.radians(self.direction)), self.y + self.height * math.sin(math.radians(self.direction))),
                (self.x + self.width * math.cos(math.radians(self.direction + 60)), self.y + self.height * math.sin(math.radians(self.direction + 60)))
            ]
            pygame.draw.polygon(screen, BLACK, points)
    
    def move(self):
        self.x += 3 * math.cos(math.radians(self.direction))  # Medium speed movement
        self.y += 3 * math.sin(math.radians(self.direction))  # Medium speed movement
        
        # Check collision with walls and border
        if self.x < 5 or self.x + self.width > WIDTH - 5:
            self.direction = 180 - self.direction
            self.change_shape()
        if self.y < 5 or self.y + self.height > HEIGHT - 5:
            self.direction = 360 - self.direction
            self.change_shape()
    
    def change_shape(self):
        rand = random.random()
        if rand < PROB_SQUARE:
            self.shape_type = SQUARE
        elif rand < PROB_SQUARE + PROB_RECTANGLE:
            self.shape_type = RECTANGLE
        else:
            self.shape_type = TRIANGLE
    
    def check_collision(self, other):
        # Check collision with other shapes
        return not (self.x > other.x + other.width or
                    self.x + self.width < other.x or
                    self.y > other.y + other.height or
                    self.y + self.height < other.y)

def main():
    shapes = [Shape(SQUARE, random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(10)]
    shapes += [Shape(RECTANGLE, random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]
    shapes += [Shape(TRIANGLE, random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(5)]
    
    running = True
    frame_count = 0
    square_count = 0
    rectangle_count = 0
    triangle_count = 0
    
    while running:
        screen.fill(WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        frame_count += 1
        if frame_count % 60 == 0:  # Count shapes every 60 frames
            # Count the number of shapes
            square_count = sum(1 for shape in shapes if shape.shape_type == SQUARE)
            rectangle_count = sum(1 for shape in shapes if shape.shape_type == RECTANGLE)
            triangle_count = sum(1 for shape in shapes if shape.shape_type == TRIANGLE)
        
        # Display the number of shapes
        square_text = font.render(f'Square: {square_count}', True, BLACK)
        rectangle_text = font.render(f'Rectangle: {rectangle_count}', True, BLACK)
        triangle_text = font.render(f'Triangle: {triangle_count}', True, BLACK)
        screen.blit(square_text, (10, 10))
        screen.blit(rectangle_text, (10, 40))
        screen.blit(triangle_text, (10, 70))
        
        # Draw border around the screen
        pygame.draw.rect(screen, BLACK, pygame.Rect(0, 0, WIDTH, HEIGHT), 5)
        
        for shape in shapes:
            shape.move()
            shape.draw()
        
        # Check collision between shapes
        for i in range(len(shapes)):
            for j in range(i + 1, len(shapes)):
                if shapes[i].check_collision(shapes[j]):
                    shapes[i].change_shape()
                    shapes[j].change_shape()
        
        pygame.display.flip()
        clock.tick(45)  # Set refresh rate to 45 FPS
    
    pygame.quit()

if __name__ == "__main__":
    main()
