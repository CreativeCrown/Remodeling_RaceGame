import pygame
import sys
import math
import random
from pygame.locals import *
from course import *
from car import Car, PlayerCar, CompCar, CarsList
from infomaition import *
from draw import *
from road import *

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

coursedata = Course(CMAX, CLEN, DATA_LR, DATA_UD, object_left, object_right)     #Courseクラスのオブジェクトを作成
board = Board(BOARD, BOARD_W, BOARD_H, BOARD_UD, board_x, board_ud)



def main(): #メイン処理を行う関数
    global idx, tmr, laps, rec, recbk, se_crash, mycar  #これらをグローバル変数とする
    pygame.init()   #pygameモジュールの初期化
    pygame.display.set_caption("Python Racer")  #ウィンドウに表示するタイトルを指定
    screen = pygame.display.set_mode((800, 600))    #描画面を初期化
    clock = pygame.time.Clock() #clockオブジェクトを作成
    fnt_s = pygame.font.Font(None, 40)  #フォントオブジェクトを作成、小さな文字
    fnt_m = pygame.font.Font(None, 50)  #フォントオブジェクトを作成、中位の文字
    fnt_l = pygame.font.Font(None, 120) #フォントオブジェクトを作成、大きな文字
    draw = Draw(screen) #drawオブジェクトを作成

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
        tmr[0] += 1    #tmrの値を1増やす

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

        # #描画用データをもとに道路を描く
        draw.draw_road(board, cars, coursedata, img_obj, img_sea, img_car, horizon)
        # for i in range(BOARD-1, 0, -1): #繰り返しで道路の板を描いていく
        #     ux = board_x[i] #台形の上底のX座標をuxに代入
        #     uy = sy - BOARD_UD[i]*board_ud[i]   #上底のY座標をuyに代入
        #     uw = BOARD_W[i] #上底の幅をuwに代入
        #     sy = sy + BOARD_H[i]*(600-horizon)/200    #台形を描くY座標を次の値にする
        #     bx = board_x[i-1]   #台形の下底のX座標をbxに代入
        #     by = sy - BOARD_UD[i-1]*board_ud[i-1]   #下底のY座標をbyに代入
        #     bw = BOARD_W[i-1]   #下底の幅をbwに代入
        #     col = (160, 160, 160)   #colに板の色を代入
        #     if int(cars[0].y+i)%CMAX == PLCAR_Y+10:  #ゴールの位置なら
        #         col = (192, 0, 0)   #赤線の色の値を代入
        #     pygame.draw.polygon(screen, col, [[ux, uy], [ux+uw, uy], [bx+bw, by], [bx, by]])    #道路の板を描く

        #     if int(cars[0].y+i)%10 <= 4:    #一定間隔で
        #         pygame.draw.polygon(screen, YELLOW, [[ux, uy], [ux+uw*0.02, uy], [bx+bw*0.02, by], [bx, by]])   #道路左の黄色いラインを描く
        #         pygame.draw.polygon(screen, YELLOW, [[ux+uw*0.98, uy], [ux+uw, uy], [bx+bw, by], [bx+bw*0.98, by]]) #道路右の黄色いラインを描く
        #     if int(cars[0].y+i)%20 <= 10:   #一定間隔で
        #         pygame.draw.polygon(screen, WHITE, [[ux+uw*0.24, uy], [ux+uw*0.26, uy], [bx+bw*0.26, by], [bx+bw*0.24, by]])    #左側の白ラインを描く
        #         pygame.draw.polygon(screen, WHITE, [[ux+uw*0.49, uy], [ux+uw*0.51, uy], [bx+bw*0.51, by], [bx+bw*0.49, by]])    #中央の白ラインを描く
        #         pygame.draw.polygon(screen, WHITE, [[ux+uw*0.74, uy], [ux+uw*0.76, uy], [bx+bw*0.76, by], [bx+bw*0.74, by]])    #右側の白ラインを描く

        #     scale = 1.5*BOARD_W[i]/BOARD_W[0]   #道路横の物体のスケールを計算
        #     obj_l = object_left[int(cars[0].y+i)%CMAX]  #obj_lに左側の物体の番号を代入
        #     if obj_l == 2:  #ヤシの木なら
        #         draw_obj(screen, img_obj[obj_l], ux-uw*0.05, uy, scale) #その画像を描画
        #     if obj_l == 3:  #ヨットなら
        #         draw_obj(screen, img_obj[obj_l], ux-uw*0.5, uy, scale)  #その画像を描画
        #     if obj_l == 9:  #海なら
        #         screen.blit(img_sea, [ux-uw*0.5-780, uy])   #その画像を描画
        #     obj_r = object_right[int(cars[0].y+i)%CMAX] #obj_rに右側の物体の番号を代入
        #     if obj_r == 1:  #看板なら
        #         draw_obj(screen, img_obj[obj_r], ux+uw*1.3, uy, scale)  #その画像を描画

        #     for c in range(1, CAR): #繰り返しで
        #         if int(cars[c].y)%CMAX == int(cars[0].y+i)%CMAX:  #その板にCOMカーがあるか調べ
        #             lr = int(4*(cars[0].x-cars[c].x)/800) #プレイヤーから見たCOMカーの向きを計算し
        #             if lr < -3: lr = -3 #-3より小さいなら-3で
        #             if lr > 3:  lr = 3  #3より小さいなら3で
        #             draw_obj(screen, img_car[(c%3)*7+3+lr], ux+cars[c].x*BOARD_W[i]/800, uy, 0.05+BOARD_W[i]/BOARD_W[0]) #COMカーを描く

        #     if i == PLCAR_Y:    #プレイヤーの車の位置なら
        #         draw_shadow(screen, ux+cars[0].x*BOARD_W[i]/800, uy, 200*BOARD_W[i]/BOARD_W[0])  #車の影を描き
        #         draw_obj(screen, img_car[3+cars[0].lr+mycar*7], ux+cars[0].x*BOARD_W[i]/800, uy, 0.05+BOARD_W[i]/BOARD_W[0])  #プレイヤーの車を描く


        draw.draw_text(str(int(cars[0].spd)) + "km/h", 680, 30, RED, fnt_m)   #速度を表示
        draw.draw_text("lap {}/{}".format(laps[0], LAPS), 100, 30, WHITE, fnt_m)    #周回数を表示
        draw.draw_text("time "+time_str(rec[0]), 100, 80, GREEN, fnt_s) #タイムを表示
        for i in range(LAPS):   #繰り返しで
            draw.draw_text(laptime[i], 80, 130+40*i, YELLOW, fnt_s)  #ラップタイムを表示

        key = pygame.key.get_pressed()  #keyに全てのキーの状態を代入
        
        if idx[0] == 0:    #idxが0の時(タイトル画面)
            screen.blit(img_title, [120, 120])  #タイトルロゴを表示
            draw.draw_text("[A] Start game", 400, 320, WHITE, fnt_m) #[A] Start gameの文字を表示
            draw.draw_text("[S] Select your car", 400, 400, WHITE, fnt_m)    #[S] Select your carの文字を表示
            cars.move_car(0, CMAX, tmr, idx, se_crash) #全ての車を動かす
            if key[K_a] != 0:   #Aキーが押されたら
                #全ての車を初期位置に
                cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
                for i in range(0, CAR):
                    cars.add(CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200)))
                idx[0] = 1     #idxを1にしてカウントダウンに
                tmr[0] = 0 #タイマーを0に
                laps[0] = 0    #周回数を0に
                rec[0] = 0     #走行時間を0に
                recbk[0] = 0   #ラップタイム計算用の変数を0に
                for i in range(LAPS):   #繰り返しで
                    laptime[i] = "0'00.00"  #ラップタイムを0'00.00に
            if key[K_s] != 0:   #Sキーが押されたら
                idx[0] = 4     #idxを4にして車種選択に移行

        if idx[0] == 1:    #idxが1の時(カウントダウン)
            n = 3-int(tmr[0]/60)   #カウントダウンの数を計算しnに代入
            draw.draw_text(str(n), 400, 240, YELLOW, fnt_l)  #その数を表示
            if tmr[0] == 179:  #tmrが179になったら
                pygame.mixer.music.load("sound_pr/bgm.ogg") #BGMを読み込み
                pygame.mixer.music.play(-1) #無限ループで出力
                idx[0] = 2     #idxを2にしてレースへ
                tmr[0] = 0 #tmrを0にする

        if idx[0] == 2:    #idxが2の時(レース中)
            if tmr[0] < 60:    #60フレームの間
                draw.draw_text("Go!", 400, 240, RED, fnt_l)  #Go!と表示
            rec[0] = rec[0] + 1/60    #走行時間をカウント
            cars[0].drive_car(key, idx, tmr, recbk, rec, laps, laptime, CMAX, coursedata)  #プレイヤーの車を操作
            cars.move_car(1, CMAX, tmr, idx, se_crash) #COMカーを動かす


        if idx[0] == 3:    #idxが3の時(ゴール)
            if tmr[0] == 1:    #tmrが1なら
                pygame.mixer.music.stop()   #BGMを停止
            if tmr[0] == 30:   #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")    #ジングルを読み込み
                pygame.mixer.music.play(0)  #1回出力
            draw.draw_text("GOAL!", 400, 240, GREEN, fnt_l)  #GOAL!の文字を表示
            cars[0].spd = cars[0].spd*0.96    #プレイヤーの車の速度を落とす
            cars[0].y = cars[0].y + cars[0].spd/100    #コース上を進ませる
            cars.move_car(1, CMAX, tmr, idx, se_crash) #COMカーを動かす
            if tmr[0] > 60*8:  #8秒経過したら
                idx[0] = 0 #idxを0にしてタイトルに戻る

        if idx[0] == 4:    #idxが4の時(車種選択画面)
            cars.move_car(0, CMAX, tmr, idx, se_crash) #全ての車を動かす
            draw.draw_text("Select your car", 400, 160, WHITE, fnt_m)    #Select your carの文字を表示
            for i in range(3):  #繰り返しで
                x = 160+240*i   #xに選択用の枠のX座標を代入
                y = 300     #yに選択用の枠のY座標を代入
                col = BLACK #colに黒を代入
                if i == cars[0].mycar:  #選択している車種なら
                    col = (0, 128, 255) #colに明るい青の値を代入
                pygame.draw.rect(screen, col, [x-100, y-80, 200, 160])  #colの色で枠を描く
                draw.draw_text("["+str(i+1)+"]", x, y-50, WHITE, fnt_m)  #[n]の文字を表示
                screen.blit(img_car[3+i*7], [x-100, y-20])  #車を描く
            draw.draw_text("[Enter] OK!", 400, 440, GREEN, fnt_m)    #[Enter] OK!という文字を表示
            if key[K_1] == 1:   #1キーが押されたら
                cars[0].mycar = 0   #mycarに0を代入(赤い車)
            if key[K_2] == 1:   #2キーが押されたら
                cars[0].mycar = 1   #mycarに1を代入(青い車)
            if key[K_3] == 1:   #3キーが押されたら
                cars[0].mycar = 2   #mycarに2を代入(黄色の車)
            if key[K_RETURN] == 1:  #Enterキーが押されたら
                idx[0] = 0 #idxを0にしてタイトル画面に戻る

        pygame.display.update() #画面を更新する
        clock.tick(60)  #フレームレートを指定

if __name__ == '__main__':  #このプログラムが直接実行された時に
    main()  #main()関数を呼び出す
