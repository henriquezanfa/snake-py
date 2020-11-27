import random
import curses

def screenConfig():
    window.border('|', '|', '-', '-', '+', '+', '+', '+')

    curses.curs_set(False)
    window.keypad(True)
    window.timeout(100)

    curses.curs_set(0)
    window.keypad(1)
    window.timeout(100)

def startSnake():
    snakeX = int(screenWidth / 4)
    snakeY = int(screenHeight / 2)
    snake = [
        [snakeY, snakeX],
        [snakeY, snakeX - 1],
        [snakeY, snakeX - 2]
    ]

    return snake

def foodPosition():
    x = random.randint(1, screenWidth - 2)
    y = random.randint(1, screenHeight - 2)

    return [y, x]


def isSnakeDead():
    if snake[0][1] >= screenWidth - 1  or snake[0][1] < 1:
        return True
    elif snake[0][0] >= screenHeight - 1  or snake[0][0] < 1:
        return True
    elif snake[0] in snake[1:]: 
        return True

    return False

def startNewGame():
    comecar = "Pressione Enter para começar"
    startKey = -1
    window.addstr(int(screenHeight/2), int((screenWidth/2) - len(comecar) / 2), comecar)
    window.refresh()

    while startKey == -1:
        startKey = window.getch()

    window.clear()


def gameLoop(snake, food, pontos):
    key = curses.KEY_UP

    while True:
        window.border('|', '|', '-', '-', '+', '+', '+', '+')
        newKey = window.getch()

        key = key if newKey == -1 else newKey

        if isSnakeDead(): 
            window.clear()
            screen.clear()

            clearPos()
            clearPontos()

            perdeu = "Você perdeu!!!"
            pontuacao = "Sua pontuação foi: " + str(pontos)
            window.addstr(int(screenHeight/2 - 5), int((screenWidth/2) - len(perdeu) / 2), perdeu)
            window.addstr(int(screenHeight/2 - 4), int((screenWidth/2) - len(pontuacao) / 2), pontuacao)
            window.refresh()
            break

        newHead = [snake[0][0], snake[0][1]]

        if key == curses.KEY_DOWN:
            newHead[0] += 1
        if key == curses.KEY_UP:
            newHead[0] -= 1
        if key == curses.KEY_LEFT:
            newHead[1] -= 1
        if key == curses.KEY_RIGHT:
            newHead[1] += 1

        snake.insert(0, newHead)

        setPos(snake[0])
        if snake[0] == food:
            food = None

            while food is None:
                newFood = foodPosition()
                food = newFood if newFood not in snake else None
            
            pontos += 1
            setPontos(pontos)
            setFoodPos(food)
            window.addch(int(food[0]), int(food[1]), '*')
        else:
            snakeTail = snake.pop()
            window.addch(int(snakeTail[0]), int(snakeTail[1]), ' ')

        window.addch(int(snake[0][0]), int(snake[0][1]), 'O')
        window.refresh()

def setPontos(pontos):
    screen.addstr(int(screenHeight/2) - 1, int(screenWidth/2), "Sua pontuação: " + str(pontos))
    screen.refresh()

    return pontos

def setFoodPos(food):
    screen.addstr(int(screenHeight/2) - 4, int(screenWidth/2), "Posição da comida: " + str(food))
    screen.refresh()

    return pontos

def clearPontos():
    screen.addstr(int(screenHeight/2) - 1, int(screenWidth/2),"                 ")
    screen.refresh()

def setPos(pos):
    screen.addstr(int(screenHeight/2) - 2, int(screenWidth/2), "Sua posição: " + str(pos))
    screen.refresh()

def clearPos():
    screen.addstr(int(screenHeight/2) - 2, int(screenWidth/2), "              ")
    screen.refresh()

if __name__ == "__main__":
    screen = curses.initscr()
    screenHeight, screenWidth = screen.getmaxyx()
    screenHeight = int(screenHeight / 2)
    screenWidth = int(screenWidth / 2)
    pontos = 0

    window = curses.newwin(screenHeight, screenWidth, int(screenHeight/2), int(screenWidth/2))   

    screenHeight, screenWidth = window.getmaxyx()

    while True:
        startNewGame()

        pontos = setPontos(0)

        screenConfig()

        food = foodPosition()
        window.addch(int(food[0]), int(food[1]), '*')

        snake = startSnake()
        
        screen.refresh()

        gameLoop(snake, food, pontos)
