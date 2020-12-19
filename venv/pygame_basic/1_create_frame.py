import pygame

pygame.init()   # 필수적인 부분

# 화면 사이즈
screenWidth = 480   # 가로 크기
screenHeight = 640  # 세로 크기
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("My Game")   # 게임 이름

# 이벤트 루프 이벤트 처리를 안에서 해줌
running = True  # 게임이 진행중인가?
while running:
    for event in pygame.event.get():    # 어떤 이벤트가 발생하는지 체크
        if event.type == pygame.QUIT:   # 창이 닫히는 이벤트 발생 -> 게임 종료
            running = False # 게임이 진행중이 아님


# 게임 종료
pygame.quit()