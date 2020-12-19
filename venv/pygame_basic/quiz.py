import random
import pygame
##################################################################
# 기본 초기화
pygame.init()  # 필수적인 부분

# 화면 사이즈
screenWidth = 480  # 가로 크기
screenHeight = 640  # 세로 크기
screen = pygame.display.set_mode((screenWidth, screenHeight))

# 게임 이름
pygame.display.set_caption("Quiz")

# FPS
clock = pygame.time.Clock()

##################################################################
# 1. 사용자 게임 초기화 (배경, 게임 이미지, 좌표, 속도, 폰트 등
background = pygame.image.load("C:/WorkSpace/Haedal/Python/Hackerton/background.png")

character = pygame.image.load("C:/WorkSpace/Haedal/Python/Hackerton/character.png")
characterSize = character.get_rect().size
characterWidth = characterSize[0]
characterHeight = characterSize[1]
characterXpos = (screenWidth - characterWidth) / 2
characterYpos = screenHeight - characterHeight

toX = 0

poop = pygame.image.load("C:/WorkSpace/Haedal/Python/Hackerton/enemy.png")
poopSize = poop.get_rect().size
poopWidth = poopSize[0]
poopHeight = poopSize[1]
poopXpos = random.randint(0, screenWidth - poopWidth)
poopYpos = 0
poopSpeed = 10


running = True
characterSpeed = 10

while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                toX -= characterSpeed
            elif event.key == pygame.K_RIGHT:
                toX += characterSpeed

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                toX = 0

    # 3. 게임 캐릭터 위치 정의
    characterXpos += toX

    if characterXpos < 0:
        characterXpos = 0
    elif characterXpos > screenWidth - characterWidth:
        characterXpos = screenWidth - characterWidth

    poopYpos += poopSpeed
    if poopYpos > screenHeight:
        poopYpos = 0
        poopXpos = random.randint(0, screenWidth - poopWidth)
    # 4. 충돌 처리
    characterRact = character.get_rect()
    characterRact.left = characterXpos
    characterRact.top = characterYpos

    poopRact = poop.get_rect()
    poopRact.left = poopXpos
    poopRact.top = poopYpos

    if characterRact.colliderect(poopRact):
        print("충돌했어요")
        running = False

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(character, (characterXpos, characterYpos))
    screen.blit(poop, (poopXpos, poopYpos))

    pygame.display.update() # 게임 화면 다시 그리기(지속적 호출 필요)

# 게임 종료
pygame.quit()