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
currentPath = os.path.dirname(__file__)  # 현재 파일의 위치 반환
imagePath = os.path.join(currentPath, "images")  # images 폴더 위치 반환

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

# 공 만들기 (4개 크기 따로)
ballImages = [
    pygame.image.load(os.path.join(imagePath, "ball1.png")),
    pygame.image.load(os.path.join(imagePath, "ball2.png")),
    pygame.image.load(os.path.join(imagePath, "ball3.png")),
    pygame.image.load(os.path.join(imagePath, "ball4.png"))]

# 공 크기에 따른 최초 스피드
ballSpeedY = [-18, -15, -12, -9]

# 공
balls = []

# 최초 발생하는 큰 공 추가
balls.append({
    "posX": 50,  # 공의 X좌표
    "posY": 50,  # 공의 Y좌표
    "imgIdx": 0,  # 공의 이미지 인덱스
    "toX": 3,  # 공의 X축 이동방향
    "toY": -6,  # 공의 Y축 이동방향
    "initSpeedY": ballSpeedY[0]  # Y최초 속도
})

# 사라질 무기, 공 정보 저장 변수
weaponToRemove = -1
ballToRemve = -1

# font 정의
gameFont = pygame.font.Font(None, 40)
totalTime = 100
startTicks = pygame.time.get_ticks()    # 시작 시간 정의

# 게임 종료 메시지
gameResult =  "GameOver"

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
    weapons = [[w[0], w[1] - weaponSpeed] for w in weapons]  # 무기를 위로 날아가게

    # 천장에 닿은 무기 없애기
    weapons = [[w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
    for ballIdx, ballVal in enumerate(balls):
        ballPosX = ballVal["posX"]
        ballPosY = ballVal["posY"]
        ballImgIdx = ballVal["imgIdx"]

        ballSize = ballImages[ballImgIdx].get_rect().size
        ballWidth = ballSize[0]
        ballHeight = ballSize[1]

        # 가로벽에 닿았을 때 공 이동 위치 변경(튕겨나옴)
        if ballPosX <= 0 or ballPosX > screenWidth - ballWidth:
            ballVal["toX"] = ballVal["toX"] * -1

        # 세로 위치
        # 스테이지에 튕겨서 올라가는 것
        if ballPosY >= screenHeight - stageHight - ballHeight:
            ballVal["toY"] = ballVal["initSpeedY"]
        else:  # 그 외 모든 경우, 속도 증가
            ballVal["toY"] += 0.5

        ballVal["posX"] += ballVal["toX"]
        ballVal["posY"] += ballVal["toY"]

    # 4. 충돌 처리

    # 캐릭터 rect 정보 업데이트
    characterRect = character.get_rect()
    characterRect.left = characterXpos
    characterRect.top = characterYpos

    for ballIdx, ballVal in enumerate(balls):
        ballPosX = ballVal["posX"]
        ballPosY = ballVal["posY"]
        ballImgIdx = ballVal["imgIdx"]

        # 공 rect 정보 업데이트
        ballRect = ballImages[ballImgIdx].get_rect()
        ballRect.left = ballPosX
        ballRect.top = ballPosY

        # 공과 캐릭터 충돌 처리
        if characterRect.colliderect(ballRect):
            running = False
            break

        # 공과 무기들 충돌 체크
        for weaponIdx, weaponVal in enumerate(weapons):
            weaponPosX = weaponVal[0]
            weaponPosY = weaponVal[1]

            # 무기 rect 정보 업데이트
            weaponRect = weapon.get_rect()
            weaponRect.left = weaponPosX
            weaponRect.top = weaponPosY

            # 충돌 체크
            if weaponRect.colliderect(ballRect):
                weaponToRemove = weaponIdx
                ballToRemve = ballIdx

                # 가장 작은 공이 아니면, 다음 단계의 공으로 나눠준다
                if ballImgIdx < 3:
                    # 현재 공 크기 정보
                    ballWidth = ballRect.size[0]
                    ballHeight = ballRect.size[1]

                    # 나눠진 공 정보
                    smallBallRect = ballImages[ballImgIdx + 1].get_rect()
                    smallBallWidth = smallBallRect.size[0]
                    smallBallHeight = smallBallRect.size[1]

                    # 왼쪽으로 나가는 공
                    balls.append({
                        "posX": ballPosX + (ballWidth / 2) - (smallBallWidth / 2),  # 공의 X좌표
                        "posY": ballPosY + (ballHeight / 2) - (smallBallHeight / 2),  # 공의 Y좌표
                        "imgIdx": ballImgIdx + 1,  # 공의 이미지 인덱스
                        "toX": -3,  # 공의 X축 이동방향, -3이면 왼쪽
                        "toY": -6,  # 공의 Y축 이동방향
                        "initSpeedY": ballSpeedY[ballImgIdx + 1]})   # Y최초 속도

                    # 오른쪽으로 나가는 공
                    balls.append({
                        "posX": ballPosX + (ballWidth / 2) - (smallBallWidth / 2),  # 공의 X좌표
                        "posY": ballPosY + (ballHeight / 2) - (smallBallHeight / 2),  # 공의 Y좌표
                        "imgIdx": ballImgIdx + 1,  # 공의 이미지 인덱스
                        "toX": 3,  # 공의 X축 이동방향, -3이면 왼쪽
                        "toY": -6,  # 공의 Y축 이동방향
                        "initSpeedY": ballSpeedY[ballImgIdx + 1]})  # Y최초 속도


                break
        else:   # 계속 게임을 진행
            continue    # 안쪽 for문 조건이 맞지 않으면, continue, 바깥쪽 for문을 계속 수행
        break   # 안쪽 for문에서 break를 만나면, 여기로 진입 가능, 이중 for 문을 한방에 탈출

    # 충돌된 공 or 무기 없애기
    if ballToRemve > -1:
        del balls[ballToRemve]
        ballToRemve = -1

    if weaponToRemove > -1:
        del weapons[weaponToRemove]
        weaponToRemove = -1

    # 모든 공이 없어지면 게임 종료
    if len(balls) == 0:
        gameResult = "Mission Complete!"
        running = False


    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    for weaponXpos, weaponYpos in weapons:
        screen.blit(weapon, (weaponXpos, weaponYpos))

    for idx, val in enumerate(balls):
        ballPosX = val["posX"]
        ballPosY = val["posY"]
        ballImgIdx = val["imgIdx"]
        screen.blit(ballImages[ballImgIdx], (ballPosX, ballPosY))

    screen.blit(stage, (0, screenHeight - stageHight))
    screen.blit(character, (characterXpos, characterYpos))

    # 경과 시간 계산
    elapsedTime = (pygame.time.get_ticks() - startTicks) / 1000
    timer = gameFont.render("Time : {}".format(int(totalTime - elapsedTime)), True, (255, 255, 255))
    screen.blit(timer, (10, 10))

    # 시간 초과했다면?
    if totalTime - elapsedTime <= 0:
        gameResult = "Times Up!"
        running = False

    pygame.display.update()  # 게임 화면 다시 그리기(지속적 호출 필요)

msg = gameFont.render(gameResult, True, (255, 255, 0))
msgRect = msg.get_rect(center = (int(screenWidth / 2), int(screenHeight / 2)))
screen.blit(msg, msgRect)
pygame.display.update()

pygame.time.delay(2000)

# 게임 종료
pygame.quit()