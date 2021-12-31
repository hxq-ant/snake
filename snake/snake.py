import sys
import time
import pygame
# 导入random库所有函数
from random import *

# Snake类，通过构造函数设置蛇头蛇神的位置
class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Food类，通过构造函数设置食物的位置和颜色
class Food:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

# 生成一个坐标随机的食物（不与蛇头重合）
def new_food(head,snake_body):
    while True:
        tage = 1
        # 循环，不断实例化new_food对象直到生成一个不与蛇头和蛇身重合的食物
        new_food = Food(randint(0, 45) * 20, randint(0, 28) * 20, (255, 0, 0))
        # 若new_food和蛇头重合则不创键
        if new_food.x != head.x and new_food.y != head.y:
            #判断是否与蛇身重合
            for body in snake_body:
                if new_food.x !=body.x and new_food.y != body.y:
                    continue
                else:
                    tage = 0    #重合了tage=0
                if tage == 0:
                    break
            if tage == 1:
                break
            else:
                continue
        else:
            continue
    return new_food


# 在窗体中绘制贪吃蛇
# 形参：一个是颜色另一个是实例化对象
def draw_snake(color, object):
    pygame.draw.circle(window, color, (object.x, object.y), 10)


# 在窗体中绘制食物
# 形参：实例化对象
def draw_food(food):
    pygame.draw.circle(window, food.color, (food.x, food.y), 10)


# 初始界面和游戏中途点击退出游戏时
def exit_end():
    pygame.quit()
    quit()


# 游戏结束时，显示得分的窗体的设置
def show_end():
    while True:
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 定义标题
        pygame.display.set_caption("Greedy snake")
        # 定义提示文字
        font = pygame.font.SysFont("simHei", 40)
        fontsurf = font.render('Game Over! Your Source: %s' % score, False, black)
        window.blit(fontsurf, (250, 100))
        button("Return to main menu", 370, 300, 200, 40, blue, brightred, into_game)
        button("One more", 370, 370, 200, 40, blue, brightred, start_kgame)
        button("Quit", 370, 440, 200, 40, red, brightred, exit_end)
        pygame.display.update()
        clock.tick(60)





def through_snake(head, snake_body):
    
    die_flag = False
    for body in snake_body:
        if head.x == body.x and head.y == body.y:
            die_flag = True
    if die_flag:
        show_end()
    else: 
        
        if head.x < 0:
            head.x = 960
        elif head.x > 960:
            head.x = 0
        elif head.y < 0:
            head.y = 600
        elif head.y > 600:
            head.y = 0


def start_kgame():
    global score
    score = 0
    # 定义存放玩家键盘输入运动方向的变量，初始为向右
    run_direction = "right"
    # 定义贪吃蛇运动方向的变量，初始为玩家键入方向
    run = run_direction
    # 实例化蛇头、蛇身、食物对象
    head = Snake(160, 160)
    # 实例化蛇身
    snake_body = [Snake(head.x, head.y + 20), Snake(head.x, head.y + 40), Snake(head.x, head.y + 60)]
    # 实例化食物列表，列表随着其中食物被吃掉应该不断缩短
    food_list = []
    food = new_food(head,snake_body)
    food_list.append(food)
    # 死循环，监听键盘键值
    while True:
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                show_end()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    run_direction = "up"
                elif event.key == pygame.K_RIGHT or event.key == ord('d'):
                    run_direction = "right"
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    run_direction = "left"
                elif event.key == pygame.K_DOWN or event.key == ord('s'):
                    run_direction = "down"
                elif event.key == ord('b'):
                    show_end()
        # 绘制食物图像
        draw_food(food)
        # 绘制蛇头图像
        draw_snake(black, head)
        # 绘制蛇身图像
        for item in snake_body:
            draw_snake(blue, item)
        # 判断贪吃蛇原运动方向与玩家键盘输入的运动方向是否违反正常运动情况
        if run == "up" and not run_direction == "down":  # 若运动方向为向上，玩家输入运动方向向下，则违背贪吃蛇正常运动情况
            run = run_direction
        elif run == "down" and not run_direction == "up":
            run = run_direction
        elif run == "left" and not run_direction == "right":
            run = run_direction
        elif run == "right" and not run_direction == "left":
            run = run_direction
        # 插入蛇头位置到蛇身列表中
        snake_body.insert(0, Snake(head.x, head.y))
        # 根据玩家键入方向进行蛇头xy的更新
        if run == "up":
            head.y -= 20
        elif run == "down":
            head.y += 20
        elif run == "left":
            head.x -= 20
        elif run == "right":
            head.x += 20
        # 穿墙实现
        through_snake(head, snake_body)#是否死亡
        # 判断蛇头和食物坐标，若相等，则加分，并生成新的食物
        # 定义标志，表明是否找到和蛇头相等的事物
        global flag
        flag = 0
        # 如果蛇头和食物重合
        for item in food_list:
            if head.x == item.x and head.y == item.y or head.x == food.x and head.y == food.y:
                flag = 1
                score += 1
                # 弹出被吃掉的这个食物
                food_list.pop(food_list.index(item))
                # 再产生一个食物
                food = new_food(head,snake_body)
                # 把新食物插入food_list，下一次循环中会更新绘制食物全体
                food_list.append(food)
                break
        if flag == 0:
            snake_body.pop()
        font = pygame.font.SysFont("simHei", 25)
        socre_title = font.render('sorce: %s' % score, False, grey)
        window.blit(socre_title, (50, 30))
        # 绘制更新
        pygame.display.update()
        # 通过帧率设置贪吃蛇速度
        clock.tick(20)


# 监听函数，监听鼠标输入
# msg: 按钮信息，x: 按钮的x轴，y: 按钮的y轴，w: 按钮的宽，h: 按钮的高，ic: 按钮初始颜色，ac: 按钮按下颜色，action: 按钮按下的动作
def button(msg, x, y, w, h, ic, ac, action=None):
    # 获取鼠标位置
    mouse = pygame.mouse.get_pos()
    # 获取鼠标点击情况
    click = pygame.mouse.get_pressed()
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(window, ac, (x, y, w, h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(window, ic, (x, y, w, h))
    # 设置按钮中的文字样式和居中对齐
    font = pygame.font.SysFont('simHei', 20)
    smallfont = font.render(msg, True, white)
    smallrect = smallfont.get_rect()
    smallrect.center = ((x + (w / 2)), (y + (h / 2)))
    window.blit(smallfont, smallrect)


# 游戏初始界面，选择模式
def into_game():
    while True:
        window.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_end()
        # 设置字体
        font = pygame.font.SysFont("simHei", 50)
        # 初始界面显示文字
        fontsurf = font.render('Greedy snake!', True, black)  # 文字
        fontrect = fontsurf.get_rect()
        fontrect.center = ((480), 200)
        window.blit(fontsurf, fontrect)
        button("play", 370, 370, 200, 40, violte, brightred, start_kgame)
        button("quit", 370, 420, 200, 40, red, brightred, exit_end)
        pygame.display.update()
        clock.tick(20)


if __name__ == '__main__':
    # 定义需要用到的颜色
    white = (255, 255, 255)
    red = (200, 0, 0)
    green = (0, 128, 0)
    blue = (0, 202, 254)
    violte = (194, 8, 234)
    brightred = (255, 0, 0)
    brightgreen = (0, 255, 0)
    black = (0, 0, 0)
    grey = (129, 131, 129)
    # 设计窗口
    window = pygame.display.set_mode((960, 600))
    # 定义标题
    pygame.display.set_caption("Greedy snake")
    # 定义背景图片
    background = pygame.image.load("image/bgimg.jpg")
    # 创建时钟
    clock = pygame.time.Clock()
    # 初始化，自检所有模块是否完整
    pygame.init()
    # 初始界面
    into_game()
