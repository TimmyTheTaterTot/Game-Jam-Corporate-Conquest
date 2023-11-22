import pygame

pygame.init()
screen = pygame.display.set_mode((300, 300))

newEvent = pygame.USEREVENT+1
newEventEvent = pygame.event.Event(newEvent)

pygame.event.post(newEventEvent)

running = True
while running:
    for event in pygame.event.get():
        if event.type == newEvent:
            print('got the new event')
        if event.type == pygame.QUIT:
            running = False

        pygame.display.update()