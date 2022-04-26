import pygame
import sys
import math
import random
from pygame.locals import *
from course import *
from car import *
from draw import *
from road import *
from gametransition import *


rec = [0]     #走行時間を測る変数
recbk = [0]   #ラップタイム計算用の変数
se_crash = None #衝突時の効果音を読み込む変数

#道路のカーブを作る基になるデータ
DATA_LR = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 2, 4, 2, 4, 2, 0, 0, 0, -2, -2, -4, -4, -2, -1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -2, -3, -2, -1, 0, -2, -4, -2, -4, -2, 0, 0, 0, 2, 2, 4, 4, 2, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4, 4, 4, 2, 0, 4, 4, 4, 4, 4, 0, 0, 0, -4, -4, -4, -4, -4, -2, 0, 0, 0, 0, 0, 0, 0],
    ]
#道路の起伏を作る基になるデータ
DATA_UD = [
    [0, 0, 2, 2, 3, 3, 2, 0, -3, -4, -4, 0, 0, 0, 0, 0, -2, -4, -4, -4, -4, -4, -2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -4, 3, 0, -4, 3, 0],
    [0, 0, 1, 2, 3, 2, 1, 0, -2, -4, -2, 0, 0, 0, 0, 0, -1, -2, -3, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, -4, 3, 0],
    [0, 0, -1, -2, -3, -2, -1, 0, 2, 3, 2, 0, 0, 0, 0, 0, 1, 2, 3, 3, 3, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, -3, 0, 3, -4, 0],
    ]
CLAPSLEN = len(DATA_LR[0])     #これらのデータの要素数を代入した定数
CLEN = len(DATA_LR[0])*3

# for i in range(len(DATA_LR)):
#     print(len(DATA_LR[i]))
# for j in range(len(DATA_UD)):
#     print(len(DATA_UD[j]))

BOARD = 120         #道路を描く板の枚数を定める定数
CLAPMAX = BOARD*CLAPSLEN   #1lapの長さを定める定数
CMAX = BOARD*CLEN   #コースの長さ(要素数)を定める定数
object_left = [0]*CMAX  #道路左にある物体の番号を入れるリスト
object_right = [0]*CMAX #道路右にある物体の番号を入れるリスト
BOARD_W = [0]*BOARD #板の幅を代入するリスト
BOARD_H = [0]*BOARD #板の高さを代入するリスト
BOARD_UD = [0]*BOARD    #板の起伏用の値を代入するリスト
board_x = [0]*BOARD #板のX座標を計算するためのリスト
board_ud = [0]*BOARD    #板の高低を計算し代入

CAR = 30        #車の数を定める定数
cars = CarsList(CAR)
cars.add(PlayerCar(400, 0, 0, 0, 10, 0))
for i in range(1, CAR):
    cars.add(CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200)))


LAPS = 3                    #何周すればゴールかを定める定数
laptime = ["0'00.00"]*LAPS  #ラップタイム表示用のリスト



#Courseクラスをcourse変数に格納
cdata = Course(CMAX, CLEN, CLAPSLEN, CLAPMAX, DATA_LR, 
                            DATA_UD, object_left, object_right)

#Course_typeクラスのインスタンスを作成
ctype = Course_type(LAPS, laptime)

#Courseクラスのインスタンスを格納
ctype.add(cdata)

#Boardクラスのインスタンスを作成
board = Board(BOARD, BOARD_W, BOARD_H, BOARD_UD, board_x, board_ud)
#Transitionクラスのインスタンスを作成
transi = Transition(0, 0)


def main(): #メイン処理を行う関数
    global rec, recbk, se_crash  #これらをグローバル変数とする
    pygame.init()   #pygameモジュールの初期化
    pygame.display.set_caption("Python Racer")  #ウィンドウに表示するタイトルを指定
    screen = pygame.display.set_mode((800, 600))    #描画面を初期化
    clock = pygame.time.Clock() #clockオブジェクトを作成
    fnt_ss = pygame.font.Font(None,30)  #フォントオブジェクトを作成、とても小さな文字
    fnt_s = pygame.font.Font(None, 40)  #フォントオブジェクトを作成、小さな文字
    fnt_m = pygame.font.Font(None, 50)  #フォントオブジェクトを作成、中位の文字
    fnt_l = pygame.font.Font(None, 120) #フォントオブジェクトを作成、大きな文字
    d_item = Draw(screen, fnt_ss, fnt_s, fnt_m, fnt_l) #drawオブジェクトを作成
    c = 0   #実際に走るコースの種類用のインデックス

    img_title = pygame.image.load("image_pr/title.png").convert_alpha() #タイトルロゴを読み込む変数
    img_bg = pygame.image.load("image_pr/bg.png").convert() #背景(空と地面の絵)を読み込む変数
    img_sea = pygame.image.load("image_pr/sea.png").convert_alpha() #海の画像を読み込む変数
    img_obj = [ #道路横の物体の画像を読み込むリスト
        None,
        pygame.image.load("image_pr/board.png").convert_alpha(),
        pygame.image.load("image_pr/yashi.png").convert_alpha(),
        pygame.image.load("image_pr/yacht.png").convert_alpha()
    ]
    img_car = [ #車の画像を読み込むリスト
        pygame.image.load("image_pr/car00.png").convert_alpha(),
        pygame.image.load("image_pr/car01.png").convert_alpha(),
        pygame.image.load("image_pr/car02.png").convert_alpha(),
        pygame.image.load("image_pr/car03.png").convert_alpha(),
        pygame.image.load("image_pr/car04.png").convert_alpha(),
        pygame.image.load("image_pr/car05.png").convert_alpha(),
        pygame.image.load("image_pr/car06.png").convert_alpha(),
        pygame.image.load("image_pr/car10.png").convert_alpha(),
        pygame.image.load("image_pr/car11.png").convert_alpha(),
        pygame.image.load("image_pr/car12.png").convert_alpha(),
        pygame.image.load("image_pr/car13.png").convert_alpha(),
        pygame.image.load("image_pr/car14.png").convert_alpha(),
        pygame.image.load("image_pr/car15.png").convert_alpha(),
        pygame.image.load("image_pr/car16.png").convert_alpha(),
        pygame.image.load("image_pr/car20.png").convert_alpha(),
        pygame.image.load("image_pr/car21.png").convert_alpha(),
        pygame.image.load("image_pr/car22.png").convert_alpha(),
        pygame.image.load("image_pr/car23.png").convert_alpha(),
        pygame.image.load("image_pr/car24.png").convert_alpha(),
        pygame.image.load("image_pr/car25.png").convert_alpha(),
        pygame.image.load("image_pr/car26.png").convert_alpha(),
    ]

    se_crash = pygame.mixer.Sound("sound_pr/crash.ogg") #衝突音を読み込む

    board.roadbasic()   #道路の板の基本形状を計算
    cdata.make_course(BOARD)    #コースを作成
    #車を管理するリストに初期値を代入
    cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
    for i in range(1, CAR):
        cars[i] = CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200))

    while True: #無限ループ
        for event in pygame.event.get():    #pygameのイベントを繰り返しで処理する
            if event.type == QUIT:  #ウィンドウの✖ボタンをクリック
                pygame.quit()   #pygameの初期化を解除
                sys.exit()  #プログラムを終了する
            if event.type == KEYDOWN:   #キーを押すイベントが発生した時
                if event.key == K_F1:   #F1キーなら
                    d_item = pygame.display.set_mode((800, 600), FULLSCREEN)    #フルスクリーンモードにする
                    draw.screen = screen    #インスタンスを初期化
                if event.key == K_F2 or event.key == K_ESCAPE:  #F2キーかEscキーなら
                    screen = pygame.display.set_mode((800, 600))    #通常表示に戻す
                    d_item.screen = screen    #インスタンスを初期化
        transi.tmr += 1    #tmrの値を1増やす
    

        #描画用の道路のX座標と路面の高低を計算
        board.di = 0  #道が曲がる向きを計算する変数、加えて毎回初期化
        board.ud = 0  #道の起伏を計算する変数、加えて毎回初期化
        board.make_curve(cdata, cars)   #道の曲がり具合を計算
        board.make_updown(cdata, cars) #道の起伏を計算


        d_item.make_horizon(board) #地平線のY座標を計算しhorizonに代入
        d_item.sy = d_item.horizon    #背景の垂直を計算し、道路を描き始めるY座標をsyに代入
        d_item.make_vertical(cars, board)   #背景の水平を計算

        #フィールドの描画
        d_item.screen.fill((0, 56, 255))   #指定の色で画面を塗り潰す
        d_item.screen.blit(img_bg, [d_item.vertical-800, d_item.horizon-400]) #空と地面の画像を描画(左側)
        d_item.screen.blit(img_bg, [d_item.vertical, d_item.horizon-400])  #空と地面の画像を描画(右側)
        d_item.screen.blit(img_sea, [board_x[BOARD-1]-780, d_item.sy])    #左手奥の海を描画

        #描画用データをもとに道路を描く
        d_item.draw_road(board, cars, cdata, ctype, img_obj, img_sea, img_car)

        d_item.draw_text(str(int(cars[0].spd)) + "km/h", 680, 30, d_item.RED, fnt_m)   #速度を表示
        d_item.draw_text("lap {}/{}".format(cdata.laps, ctype.LAPS), 100, 30, d_item.WHITE, fnt_m)    #周回数を表示
        d_item.draw_text("time "+time_str(rec[0]), 100, 80, d_item.GREEN, fnt_s) #タイムを表示
        for i in range(ctype.LAPS):   #繰り返しで
            d_item.draw_text(ctype.laptime[i], 80, 130+40*i, d_item.YELLOW, fnt_s)  #ラップタイムを表示

        key = pygame.key.get_pressed()  #keyに全てのキーの状態を代入
        transi.game_transition(cars, ctype, cdata, d_item, board, img_title, img_car, se_crash, rec, recbk, key)

        pygame.display.update() #画面を更新する
        clock.tick(60)  #フレームレートを指定

if __name__ == '__main__':  #このプログラムが直接実行された時に
    main()  #main()関数を呼び出す
