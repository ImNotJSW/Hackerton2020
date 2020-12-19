import os
import pygame
##################################################################
# 기본 초기화
pygame.init()  # 필수적인 부분

# 화면 사이즈
screenWidth = 640  # 가로 크기
screenHeight = 480  # 세로 크기
screen = pygame.display.set_mode((screenWidth, screenHeight))

# 게임 이름
pygame.display.set_caption("Pang")

# FPS
clock = pygame.time.Clock()

##################################################################
# 1. 사용자 게임 초기화 (배경, 게임 이밎, 좌표, 속도, 폰트 등
currentPath = os.path.dirname(__file__) # 현재 파일의 위치 반환
imagePath = os.path.join(currentPath, "images") # images 폴더 위치 반환

background = pygame.image.load(os.path.join(imagePath, "background.png"))

stage = pygame.image.load(os.path.join(imagePath, "stage.png"))
stageSize = stage.get_rect().size
stageHight = stageSize[1]

character = pygame.image.load(os.path.join(imagePath, "character.png"))
characterSize = character.get_rect().size
characterWidth = characterSize[0]
characterHeight = characterSize[1]
characterXpos = (screenWidth - characterWidth) / 2
characterYpos = screenHeight - characterHeight - stageHight

characterToX = 0

characterSpeed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(imagePath, "weapon.png"))
weaponSize = weapon.get_rect().size
weaponWidth = weaponSize[0]

# 무기는 한 번에 여러 발 발사 가능
weapons = []

# 무기 이동 속도
weaponSpeed = 10


running = True
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                characterToX -= characterSpeed
            elif event.key == pygame.K_RIGHT:
                characterToX += characterSpeed
            elif event.key == pygame.K_SPACE:
                weaponXpos = characterXpos + ((characterWidth - weaponWidth) / 2)
                weaponYpos = characterYpos
                weapons.append([weaponXpos, weaponYpos])

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                characterToX = 0

    # 3. 게임 캐릭터 위치 정의
    characterXpos += characterToX

    if characterXpos < 0:
        characterXpos = 0
    elif characterXpos > screenWidth - characterWidth:
        characterXpos = screenWidth - characterWidth

    # 무기 위치 조정
    weapons = [[w[0], w[1] - weaponSpeed] for w in weapons] # 무기를 위로 날아가게

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    for weaponXpos, weaponYpos in weapons:
        screen.blit(weapon, (weaponXpos, weaponYpos))
    screen.blit(stage, (0, screenHeight - stageHight))
    screen.blit(character, (characterXpos, characterYpos))



    pygame.display.update() # 게임 화면 다시 그리기(지속적 호출 필요)

# 게임 종료
pygame.quit()