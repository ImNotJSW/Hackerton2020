import pygame

pygame.init()  # 필수적인 부분

# 화면 사이즈
screenWidth = 480  # 가로 크기
screenHeight = 640  # 세로 크기
screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("My Game")  # 게임 이름

# 배경 이미지 불러오기
background = pygame.image.load("C:/WorkSpace/Haedal/Python/Hackerton/background.png")

# 스프라이트(캐릭터) 불러오기
character = pygame.image.load("C:/WorkSpace/Haedal/Python/Hackerton/character.png")
characterSize = character.get_rect().size   # 이미지의 크기를 구해옴
characterWidth = characterSize[0]
characterHeight = characterSize[1]
characterXpos = (screenWidth - characterWidth) / 2  # 화면 가로의 절반 크기에 위치하는 곳에 위치
characterYpos = screenHeight - characterHeight   # 화면 가장 아래에 위치

# 이동할 좌표
toX = 0
toY = 0

# 이벤트 루프 이벤트 처리를 안에서 해줌
running = True  # 게임이 진행중인가?
while running:
    for event in pygame.event.get():  # 어떤 이벤트가 발생하는지 체크
        if event.type == pygame.QUIT:  # 창이 닫히는 이벤트 발생 -> 게임 종료
            running = False  # 게임이 진행중이 아님

        if event.type == pygame.KEYDOWN:    # 키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT:
                toX -= 5
            elif event.key == pygame.K_RIGHT:
                toX += 5
            elif event.key == pygame.K_UP:
                toY -= 5
            elif event.key == pygame.K_DOWN:
                toY += 5

        if event.type == pygame.KEYUP:  # 방향키 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                toX = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                toY = 0

    characterXpos += toX
    characterYpos += toY

    # 가로 경계값 처리
    if characterXpos < 0:
        characterXpos = 0
    elif characterXpos > screenWidth - characterWidth:
        characterXpos = screenWidth - characterWidth

    # 세로 경계값 정리
    if characterYpos < 0:
        characterYpos = 0
    elif characterYpos > screenHeight - characterHeight:
        characterYpos = screenHeight - characterHeight

    screen.blit(background, (0, 0)) # 배경 그리기
    screen.blit(character, (characterXpos, characterYpos))  # 캐릭터 그리기

    pygame.display.update() # 게임 화면 다시 그리기(지속적 호출 필요)

# 게임 종료
pygame.quit()