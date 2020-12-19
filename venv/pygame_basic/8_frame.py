import pygame
##################################################################
# 기본 초기화
pygame.init()  # 필수적인 부분

# 화면 사이즈
screenWidth = 480  # 가로 크기
screenHeight = 640  # 세로 크기
screen = pygame.display.set_mode((screenWidth, screenHeight))

# 게임 이름
pygame.display.set_caption("My Game")

# FPS
clock = pygame.time.Clock()

##################################################################
# 1. 사용자 게임 초기화 (배경, 게임 이밎, 좌표, 속도, 폰트 등


running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기 

    pygame.display.update() # 게임 화면 다시 그리기(지속적 호출 필요)

# 게임 종료
pygame.quit()