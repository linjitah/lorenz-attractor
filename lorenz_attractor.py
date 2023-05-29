import random
import pygame

class Lorenz:
    def __init__(self):
        self.xMin, self.xMax = -30, 30
        self.yMin, self.yMax = -30, 30
        self.zMin, self.zMax = 0, 50
        self.X, self.Y, self.Z = 0.1, 0.0, 0.0
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.dt = 0.01
        self.a, self.b, self.c = 10, 28, 8/3

    def step(self):
        self.oX, self.oY, self.oZ = self.X, self.Y, self.Z
        self.X = self.X + (self.dt * self.a *(self.Y - self.X))
        self.Y = self.Y + (self.dt * (self.X * (self.b - self.Z) - self.Y))
        self.Z = self.Z + (self.dt * (self.X * self.Y - self.c * self.Z))

    def draw(self, displaySurface, color):
        width, height = displaySurface.get_size()
        oldPos = self.ConvertToScreen(self.oX, self.oZ, self.xMin, self.xMax, self.zMin, self.zMax, width, height)
        newPos = self.ConvertToScreen(self.X, self.Z, self.xMin, self.xMax, self.zMin, self.zMax, width, height)

        # Draw the current line segment, width = 2 is optional, could be changed
        newRect = pygame.draw.line(displaySurface, color, oldPos, newPos, 1)

        #Return the bounding rectangle
        return newRect
    
    def ConvertToScreen(self, x, y, xMin, xMax, yMin, yMax, width, height):
        newX = width * ((x - xMin) / (xMax - xMin))
        newY = height * ((y - yMin) / (yMax - yMin))
        return round(newX), round(newY)
    
class Application:
    def __init__(self):
        self.isRunning = True
        self.displaySurface = None
        self.fpsClock = None
        self.attractors = []
        self.size = self.width, self.height = 1920, 1080
        self.count = 0
        self.outputCount = 1

    def on_init(self):
        pygame.init()
        pygame.display.set_caption("Lorenz Attractor")
        self.displaySurface = pygame.display.set_mode(self.size)
        self.isRunning = True
        self.fpsClock = pygame.time.Clock()

        # Configure the attractors
        colours = []
        colours.append((128, 0, 128))   # Purple
        colours.append((0, 0, 255))  # Blue
        colours.append((255, 255, 255))  # White
        

        for i in range(0, 3):
            attractor = Lorenz()
            attractor.X = random.uniform(0.1, 0.101)
            self.attractors.append((attractor, colours[i]))

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.isRunning = False

    def on_loop(self):
        # Call the step method for the attractor
        for attractor, _ in self.attractors:
            attractor.step()

    def on_render(self):
        for attractor, color in self.attractors:
            newRect = attractor.draw(self.displaySurface, color)
            pygame.display.update(newRect)

    def on_execute(self):
        if self.on_init() == False:
            self.isRunning = False

        fps_limit = 120  # Limit the FPS to 30
        while self.isRunning:
            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.on_render()

            # Delay to control the speed
            pygame.time.Clock().tick(fps_limit)
            
        pygame.quit()

if __name__ == "__main__":
    t = Application()
    t.on_execute()