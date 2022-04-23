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

WHITE = (255, 255, 255) #色の定義(白)
BLACK = (0, 0, 0)       #色の定義(黒)
RED = (255, 0, 0)       #色の定義(赤)
YELLOW = (255, 224, 0)  #色の定義(黄)
GREEN = (0, 255, 0)     #色の定義(緑)

idx = [0]     #インデックスの変数
tmr = [0]     #タイマーの変数
laps = [0]    #何周目かを管理する変数
rec = [0]     #走行時間を測る変数
recbk = [0]   #ラップタイム計算用の変数
se_crash = None #衝突時の効果音を読み込む変数
mycar = 0   #車種選択用の変数

DATA_LR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 2, 4, 2, 4, 2, 0, 0, 0, -2, -2, -4, -4, -2, -1, 0, 0, 0, 0, 0, 0, 0]     #道路のカーブを作る下になるデータ
DATA_UD = [0, 0, 1, 2, 3, 2, 1, 0, -2, -4, -2, 0, 0, 0, 0, 0, -1, -2, -3, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, -6, 6, 0]  #道路の起伏を作る基になるデータ
CLEN = len(DATA_LR)     #これらのデータの要素数を代入した定数

BOARD = 120         #道路を描く板の枚数を定める定数
CMAX = BOARD*CLEN   #コースの長さ(要素数)を定める定数
object_left = [0]*CMAX  #道路左にある物体の番号を入れるリスト
object_right = [0]*CMAX #道路右にある物体の番号を入れるリスト
BOARD_W = [0]*BOARD #板の幅を代入するリスト
BOARD_H = [0]*BOARD #板の高さを代入するリスト
BOARD_UD = [0]*BOARD    #板の起伏用の値を代入するリスト
board_x = [0]*BOARD #板のX座標を計算するためのリスト
board_ud = [0]*BOARD    #板の高低を計算し代入

CAR = 30        #車の数を定める定数
car_x = [0]*CAR #車の横方向の座標を管理するリスト
car_y = [0]*CAR #車のコース上の位置を管理するリスト
car_lr = [0]*CAR    #車の左右の向きを管理するリスト
car_spd = [0]*CAR   #車の速度を管理するリスト
PLCAR_Y = 10        # プレイヤーの車の表示位置　道路一番手前（画面下）が0
cars = CarsList(CAR)
cars.add(PlayerCar(400, 0, 0, 0, 10, 0))
for i in range(1, CAR):
    cars.add(CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200)))


LAPS = 3                    #何周すればゴールかを定める定数
laptime = ["0'00.00"]*LAPS  #ラップタイム表示用のリスト

coursedata = Course(CMAX, CLEN, 3, 0, ["0'00.00"]*LAPS, DATA_LR, DATA_UD, object_left, object_right)     #Courseクラスのオブジェクトを作成
board = Board(BOARD, BOARD_W, BOARD_H, BOARD_UD, board_x, board_ud)

transi = Transition(0, 0)


def main(): #メイン処理を行う関数
    global idx, tmr, laps, rec, recbk, se_crash, mycar  #これらをグローバル変数とする
    pygame.init()   #pygameモジュールの初期化
    pygame.display.set_caption("Python Racer")  #ウィンドウに表示するタイトルを指定
    screen = pygame.display.set_mode((800, 600))    #描画面を初期化
    clock = pygame.time.Clock() #clockオブジェクトを作成
    fnt_s = pygame.font.Font(None, 40)  #フォントオブジェクトを作成、小さな文字
    fnt_m = pygame.font.Font(None, 50)  #フォントオブジェクトを作成、中位の文字
    fnt_l = pygame.font.Font(None, 120) #フォントオブジェクトを作成、大きな文字
    draw = Draw(screen, fnt_s, fnt_m, fnt_l) #drawオブジェクトを作成

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
    coursedata.make_course(BOARD, object_right, object_left)    #コースを作成
    #車を管理するリストに初期値を代入
    cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
    for i in range(1, CAR):
        cars[i] = CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200))

    vertical = 0    #背景の横方向の位置を管理する変数

    while True: #無限ループ
        for event in pygame.event.get():    #pygameのイベントを繰り返しで処理する
            if event.type == QUIT:  #ウィンドウの✖ボタンをクリック
                pygame.quit()   #pygameの初期化を解除
                sys.exit()  #プログラムを終了する
            if event.type == KEYDOWN:   #キーを押すイベントが発生した時
                if event.key == K_F1:   #F1キーなら
                    screen = pygame.display.set_mode((800, 600), FULLSCREEN)    #フルスクリーンモードにする
                    draw.screen = screen
                if event.key == K_F2 or event.key == K_ESCAPE:  #F2キーかEscキーなら
                    screen = pygame.display.set_mode((800, 600))    #通常表示に戻す
                    draw.screen = screen
        transi.tmr += 1    #tmrの値を1増やす

        #描画用の道路のX座標と路面の高低を計算
        di = [0]  #道が曲がる向きを計算する変数
        ud = [0]  #道の起伏を計算する変数
        board.make_curve(di, coursedata, cars, CMAX)   #道の曲がり具合を計算
        board.make_updown(ud, coursedata, cars, CMAX) #道の起伏を計算

        horizon = 400 + int(ud[0]/3)   #地平線のY座標を計算しhorizonに代入
        sy = horizon    #道路を描き始めるY座標をsyに代入

        vertical = vertical - int(cars[0].spd*di[0]/8000)   #背景の垂直位置を計算
        if vertical < 0:    #それが0未満になったら
            vertical += 800 #800を足す
        if vertical >= 800: #800以上になったら
            vertical -= 800 #800を引く

        #フィールドの描画
        screen.fill((0, 56, 255))   #指定の色で画面を塗り潰す
        screen.blit(img_bg, [vertical-800, horizon-400]) #空と地面の画像を描画(左側)
        screen.blit(img_bg, [vertical, horizon-400])  #空と地面の画像を描画(右側)
        screen.blit(img_sea, [board_x[BOARD-1]-780, sy])    #左手奥の海を描画

        #描画用データをもとに道路を描く
        draw.draw_road(board, cars, coursedata, img_obj, img_sea, img_car, horizon)

        draw.draw_text(str(int(cars[0].spd)) + "km/h", 680, 30, RED, fnt_m)   #速度を表示
        draw.draw_text("lap {}/{}".format(coursedata.laps, coursedata.LAPS), 100, 30, WHITE, fnt_m)    #周回数を表示
        draw.draw_text("time "+time_str(rec[0]), 100, 80, GREEN, fnt_s) #タイムを表示
        for i in range(coursedata.LAPS):   #繰り返しで
            draw.draw_text(coursedata.laptime[i], 80, 130+40*i, YELLOW, fnt_s)  #ラップタイムを表示

        key = pygame.key.get_pressed()  #keyに全てのキーの状態を代入
        transi.game_trandition(cars, coursedata, draw, img_title, img_car, se_crash, rec, recbk, key)
        
        pygame.display.update() #画面を更新する
        clock.tick(60)  #フレームレートを指定

if __name__ == '__main__':  #このプログラムが直接実行された時に
    main()  #main()関数を呼び出す
