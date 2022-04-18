import pygame
import sys
import math
import random
from pygame.locals import *
from course import *
from car import *

WHITE = (255, 255, 255) #色の定義(白)
BLACK = (0, 0, 0)       #色の定義(黒)
RED = (255, 0, 0)       #色の定義(赤)
YELLOW = (255, 224, 0)  #色の定義(黄)
GREEN = (0, 255, 0)     #色の定義(緑)

idx = 0     #インデックスの変数
tmr = 0     #タイマーの変数
laps = 0    #何周目かを管理する変数
rec = 0     #走行時間を測る変数
recbk = 0   #ラップタイム計算用の変数
se_crash = None #衝突時の効果音を読み込む変数
mycar = 0   #車種選択用の変数

DATA_LR = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 2, 1, 0, 2, 4, 2, 4, 2, 0, 0, 0, -2, -2, -4, -4, -2, -1, 0, 0, 0, 0, 0, 0, 0]     #道路のカーブを作る下になるデータ
DATA_UD = [0, 0, 1, 2, 3, 2, 1, 0, -2, -4, -2, 0, 0, 0, 0, 0, -1, -2, -3, -4, -3, -2, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -3, 3, 0, -6, 6, 0]  #道路の起伏を作る基になるデータ
CLEN = len(DATA_LR)     #これらのデータの要素数を代入した定数

BOARD = 120         #道路を描く板の枚数を定める定数
CMAX = BOARD*CLEN   #コースの長さ(要素数)を定める定数
object_left = [0]*CMAX  #道路左にある物体の番号を入れるリスト
object_right = [0]*CMAX #道路右にある物体の番号を入れるリスト

CAR = 30        #車の数を定める定数
car_x = [0]*CAR #車の横方向の座標を管理するリスト
car_y = [0]*CAR #車のコース上の位置を管理するリスト
car_lr = [0]*CAR    #車の左右の向きを管理するリスト
car_spd = [0]*CAR   #車の速度を管理するリスト
PLCAR_Y = 10        # プレイヤーの車の表示位置　道路一番手前（画面下）が0
cars = CarsList()
cars.add(PlayerCar(400, 0, 0, 0))
for i in range(1, CAR):
    cars.add(CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200)))


LAPS = 3                    #何周すればゴールかを定める定数
laptime = ["0'00.00"]*LAPS  #ラップタイム表示用のリスト

coursedata = Course(CLEN, DATA_LR, DATA_UD)     #Courseクラスのオブジェクトを作成


def time_str(val):  #**'**.**という時間の文字列を作る関数
    sec = int(val)          #引数を整数の秒数にしてsecに代入
    ms = int((val-sec)*100) #秒数の小数点以下の値をmsに代入
    mi = int(sec/60)        #分をmiに代入
    return "{}'{:02}.{:02}".format(mi, sec%60, ms)  #**'**.**という文字列を返す


def draw_obj(bg, img, x, y, sc):    #座標とスケールを受け取り、物体を描く関数
    img_rz = pygame.transform.rotozoom(img, 0, sc)  #拡大縮小した画像を作る
    w = img_rz.get_width()          #その画像の幅をwに代入
    h = img_rz.get_height()         #その画像の高さをhに代入
    bg.blit(img_rz, [x-w/2, y-h])   #画像を描く


def draw_shadow(bg, x, y, siz): #影を表示する関数
    shadow = pygame.Surface([siz, siz/4])   #描画面(サーフェイス)を用意する
    shadow.fill(RED)            #その描画面を赤で塗り潰す
    shadow.set_colorkey(RED)    #描画面の透過色を指定
    shadow.set_alpha(128)       #描画面の透明度を設定
    pygame.draw.ellipse(shadow, BLACK, [0, 0, siz, siz/4])  #描画面に黒で楕円を描く
    bg.blit(shadow, [x-siz/2, y-siz/4]) #楕円を描いた描画面をゲーム画面に転送


# def init_car(): #車を管理するリストに初期値を代入する関数
#     for i in range(1, CAR):                 #繰り返しでCOMカーの
#         car_x[i] = random.randint(50, 750)  #横方向の座標をランダムに決める
#         car_y[i] = random.randint(200, CMAX-200)    #コース上の位置をランダムに決める
#         car_lr[i] = 0   #左右の向きを0に(正面向きにする)
#         car_spd[i] = random.randint(100, 200)   #速度をランダムに決める
#     car_x[0] = 400  #プレイヤーの車の横方向の座標を画面中央に
#     car_y[0] = 0    #プレイヤーの車のコース上の位置を初期値に
#     car_lr[0] = 0   #プレイヤーの車の向きを0に
#     car_spd[0] = 0  #プレイヤーの車の速度を0に


def drive_car(key): #プレイヤーの車を操作、制御する関数
    global idx, tmr, laps, recbk     #これらをグローバル変数とする
    if key[K_LEFT] == 1:    #左キーが押されたら
        if cars[0].lr > -3:  #向きが-3より大きければ
            cars[0].lr -= 1  #向きを-1する(左に向かせる)
        cars[0].x = cars[0].x + (cars[0].lr-3)*cars[0].spd/100 - 5  #車の横方向の座標を計算
    elif key[K_RIGHT] == 1: #そうでなく右キーが押されたら
        if cars[0].lr < 3:   #向きが3より小さければ
            cars[0].lr += 1  #向きを+1する(右に向かせる)
        cars[0].x = cars[0].x + (cars[0].lr+3)*cars[0].spd/100 + 5  #車の横方向の座標を計算
    else:
        cars[0].lr = int(cars[0].lr*0.9)  #正面向きに近づける

    if key[K_a] == 1:   #Aキーが押されたら
        cars[0].spd += 3 #速度を増やす
    elif key[K_z] == 1: #そうでなくZキーが押されたら
        cars[0].spd -= 10    #速度を減らす
    else:   #そうでないなら
        cars[0].spd -= 0.25  #ゆっくり減速

    if cars[0].spd < 0:  #速度が0未満なら
        cars[0].spd = 0  #速度を0にする
    if cars[0].spd > 320:    #最高速度を超えたら
        cars[0].spd = 320    #最高速度にする

    cars[0].x -= cars[0].spd*coursedata[int(cars[0].y+PLCAR_Y)%CMAX].curve/50  #車の速度と道の曲がりから横方向の座標を計算
    if cars[0].x < 0:    #左の路肩に接触したら
        cars[0].x = 0    #横方向の座標を0にし
        cars[0].spd *= 0.9   #減速する
    if cars[0].x > 800:  #右の路肩に接触したら
        cars[0].x = 800  #横方向の座標を800にし
        cars[0].spd *= 0.9   #減速する

    cars[0].y = cars[0].y + cars[0].spd/100    #車の速度からコース上の位置を計算
    if cars[0].y > CMAX-1:   #コース終点を越えたら
        cars[0].y -= CMAX    #コースの頭に戻す
        laptime[laps] = time_str(rec-recbk) #ラップタイムを計算し代入
        recbk = rec #現在のタイムを保持
        laps += 1   #周回数の値を1増やす
        if laps == LAPS:    #周回数がLAPSの値になったら
            idx = 3 #idxを3にしてゴール処理へ
            tmr = 0 #tmrを0にする


def move_car(cs):   #コンピュータの車を制御する関数
    for i in range(cs, CAR):    #繰り返しで全ての車を処理する
        if cars[i].spd < 100:    #速度が100より小さいなら
            cars[i].spd += 3 #速度を増やす
        if i == tmr%120:    #一定時間ごとに
            cars[i].lr += random.choice([-1, 0, 1])  #向きをランダムに変える
            if cars[i].lr < -3:  cars[i].lr = -3  #向きが-3未満なら-3にする
            if cars[i].lr > 3:   cars[i].lr = 3   #向きが3を超えたら3にする
        cars[i].x = cars[i].x + cars[i].lr*cars[i].spd/100  #車の向きと速度から横方向の座標を計算
        if cars[i].x < 50:   #左の路肩に近づいたら
            cars[i].x = 50   #それ以上行かないようにし
            cars[i].lr = int(cars[i].lr*0.9)  #正面向きに近づける
        if cars[i].x > 750:  #右の路肩に近づいたら
            cars[i].x = 750  #それ以上行かないようにし
            cars[i].lr = int(cars[i].lr*0.9)  #正面向きに近づける
        cars[i].y += cars[i].spd/100  #車の速度からコース上の位置を計算
        if cars[i].y > CMAX-1:   #コース終点を越えたら
            cars[i].y -= CMAX    #コースの頭に戻す
        if idx == 2:    #idxが2(レース中)ならヒットチェック
            cx = cars[i].x-cars[0].x  #プレイヤーの車との横方向の距離
            cy = cars[i].y-(cars[0].y+PLCAR_Y)%CMAX   #プレイヤーの車とのコース上の距離
            if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10: #それらがこの範囲内なら
                #衝突時の座標変化、速度の入れ替えと減速
                cars[0].x -= cx/4    #プレイヤーの車を横に移動
                cars[i].x += cx/4    #コンピュータの車を横に移動
                cars[0].spd, cars[i].spd = cars[i].spd*0.3, cars[0].spd*0.3 #2つの車の速度を入れ替え減速
                se_crash.play() #衝突音を出力

        
def draw_text(scrn, txt, x, y, col, fnt):   #影付きの文字列を表示する関数
    sur = fnt.render(txt, True, BLACK)  #黒で文字列を描いたサーフェイスを生成
    x -= sur.get_width()/2  #センタリングするためX座標を計算
    y -= sur.get_height()/2 #センタリングするためY座標を計算
    scrn.blit(sur, [x+2, y+2])  #サーフェイスを画面に転送
    sur = fnt.render(txt, True, col)    #指定色で文字列を描いたサーフェイスを生成
    scrn.blit(sur, [x, y])  #サーフェイスを画面に転送



def main(): #メイン処理を行う関数
    global idx, tmr, laps, rec, recbk, se_crash, mycar  #これらをグローバル変数とする
    pygame.init()   #pygameモジュールの初期化
    pygame.display.set_caption("Python Racer")  #ウィンドウに表示するタイトルを指定
    screen = pygame.display.set_mode((800, 600))    #描画面を初期化
    clock = pygame.time.Clock() #clockオブジェクトを作成
    fnt_s = pygame.font.Font(None, 40)  #フォントオブジェクトを作成、小さな文字
    fnt_m = pygame.font.Font(None, 50)  #フォントオブジェクトを作成、中位の文字
    fnt_l = pygame.font.Font(None, 120) #フォントオブジェクトを作成、大きな文字

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

    #道路の板の基本形状を計算
    BOARD_W = [0]*BOARD #板の幅を代入するリスト
    BOARD_H = [0]*BOARD #板の高さを代入するリスト
    BOARD_UD = [0]*BOARD    #板の起伏用の値を代入するリスト
    for i in range(BOARD):  #繰り返しで
        BOARD_W[i] = 10+(BOARD-i)*(BOARD-i)/12  #幅を計算
        BOARD_H[i] = 3.4*(BOARD-i)/BOARD    #高さを計算
        BOARD_UD[i] = 2*math.sin(math.radians(i*1.5))   #起伏の値を三角関数で計算

    coursedata.make_course(BOARD, object_right, object_left)
      #車を管理するリストに初期値を代入
    cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
    for i in range(0, CAR):
        cars.add(CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200)))

    vertical = 0    #背景の横方向の位置を管理する変数

    while True: #無限ループ
        for event in pygame.event.get():    #pygameのイベントを繰り返しで処理する
            if event.type == QUIT:  #ウィンドウの✖ボタンをクリック
                pygame.quit()   #pygameの初期化を解除
                sys.exit()  #プログラムを終了する
            if event.type == KEYDOWN:   #キーを押すイベントが発生した時
                if event.key == K_F1:   #F1キーなら
                    screen = pygame.display.set_mode((800, 600), FULLSCREEN)    #フルスクリーンモードにする
                if event.key == K_F2 or event.key == K_ESCAPE:  #F2キーかEscキーなら
                    screen = pygame.display.set_mode((800, 600))    #通常表示に戻す
        tmr += 1    #tmrの値を1増やす

        #描画用の道路のX座標と路面の高低を計算
        di = 0  #道が曲がる向きを計算する変数
        ud = 0  #道の起伏を計算する変数
        board_x = [0]*BOARD #板のX座標を計算するためのリスト
        board_ud = [0]*BOARD    #板の高低を計算し代入
        for i in range(BOARD):  #繰り返しで
            di += coursedata[int(cars[0].y+i)%CMAX].curve    #カーブデータから道の曲がりを計算
            ud += coursedata[int(cars[0].y+i)%CMAX].updown   #起伏データから起伏を計算
            board_x[i] = 400 - BOARD_W[i]*cars[0].x/800 + di/2  #板のX座標を計算し代入
            board_ud[i] = ud/30 #板の高低を計算し代入

        horizon = 400 + int(ud/3)   #地平線のY座標を計算しhorizonに代入
        sy = horizon    #道路を描き始めるY座標をsyに代入

        vertical = vertical - int(cars[0].spd*di/8000)   #背景の垂直位置を計算
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
        for i in range(BOARD-1, 0, -1): #繰り返しで道路の板を描いていく
            ux = board_x[i] #台形の上底のX座標をuxに代入
            uy = sy - BOARD_UD[i]*board_ud[i]   #上底のY座標をuyに代入
            uw = BOARD_W[i] #上底の幅をuwに代入
            sy = sy + BOARD_H[i]*(600-horizon)/200    #台形を描くY座標を次の値にする
            bx = board_x[i-1]   #台形の下底のX座標をbxに代入
            by = sy - BOARD_UD[i-1]*board_ud[i-1]   #下底のY座標をbyに代入
            bw = BOARD_W[i-1]   #下底の幅をbwに代入
            col = (160, 160, 160)   #colに板の色を代入
            if int(cars[0].y+i)%CMAX == PLCAR_Y+10:  #ゴールの位置なら
                col = (192, 0, 0)   #赤線の色の値を代入
            pygame.draw.polygon(screen, col, [[ux, uy], [ux+uw, uy], [bx+bw, by], [bx, by]])    #道路の板を描く

            if int(cars[0].y+i)%10 <= 4:    #一定間隔で
                pygame.draw.polygon(screen, YELLOW, [[ux, uy], [ux+uw*0.02, uy], [bx+bw*0.02, by], [bx, by]])   #道路左の黄色いラインを描く
                pygame.draw.polygon(screen, YELLOW, [[ux+uw*0.98, uy], [ux+uw, uy], [bx+bw, by], [bx+bw*0.98, by]]) #道路右の黄色いラインを描く
            if int(cars[0].y+i)%20 <= 10:   #一定間隔で
                pygame.draw.polygon(screen, WHITE, [[ux+uw*0.24, uy], [ux+uw*0.26, uy], [bx+bw*0.26, by], [bx+bw*0.24, by]])    #左側の白ラインを描く
                pygame.draw.polygon(screen, WHITE, [[ux+uw*0.49, uy], [ux+uw*0.51, uy], [bx+bw*0.51, by], [bx+bw*0.49, by]])    #中央の白ラインを描く
                pygame.draw.polygon(screen, WHITE, [[ux+uw*0.74, uy], [ux+uw*0.76, uy], [bx+bw*0.76, by], [bx+bw*0.74, by]])    #右側の白ラインを描く

            scale = 1.5*BOARD_W[i]/BOARD_W[0]   #道路横の物体のスケールを計算
            obj_l = object_left[int(cars[0].y+i)%CMAX]  #obj_lに左側の物体の番号を代入
            if obj_l == 2:  #ヤシの木なら
                draw_obj(screen, img_obj[obj_l], ux-uw*0.05, uy, scale) #その画像を描画
            if obj_l == 3:  #ヨットなら
                draw_obj(screen, img_obj[obj_l], ux-uw*0.5, uy, scale)  #その画像を描画
            if obj_l == 9:  #海なら
                screen.blit(img_sea, [ux-uw*0.5-780, uy])   #その画像を描画
            obj_r = object_right[int(cars[0].y+i)%CMAX] #obj_rに右側の物体の番号を代入
            if obj_r == 1:  #看板なら
                draw_obj(screen, img_obj[obj_r], ux+uw*1.3, uy, scale)  #その画像を描画

            for c in range(1, CAR): #繰り返しで
                if int(cars[c].y)%CMAX == int(cars[0].y+i)%CMAX:  #その板にCOMカーがあるか調べ
                    lr = int(4*(cars[0].x-cars[c].x)/800) #プレイヤーから見たCOMカーの向きを計算し
                    if lr < -3: lr = -3 #-3より小さいなら-3で
                    if lr > 3:  lr = 3  #3より小さいなら3で
                    draw_obj(screen, img_car[(c%3)*7+3+lr], ux+cars[c].x*BOARD_W[i]/800, uy, 0.05+BOARD_W[i]/BOARD_W[0]) #COMカーを描く

            if i == PLCAR_Y:    #プレイヤーの車の位置なら
                draw_shadow(screen, ux+cars[0].x*BOARD_W[i]/800, uy, 200*BOARD_W[i]/BOARD_W[0])  #車の影を描き
                draw_obj(screen, img_car[3+cars[0].lr+mycar*7], ux+cars[0].x*BOARD_W[i]/800, uy, 0.05+BOARD_W[i]/BOARD_W[0])  #プレイヤーの車を描く

        draw_text(screen, str(int(cars[0].spd)) + "km/h", 680, 30, RED, fnt_m)   #速度を表示
        draw_text(screen, "lap {}/{}".format(laps, LAPS), 100, 30, WHITE, fnt_m)    #周回数を表示
        draw_text(screen, "time "+time_str(rec), 100, 80, GREEN, fnt_s) #タイムを表示
        for i in range(LAPS):   #繰り返しで
            draw_text(screen, laptime[i], 80, 130+40*i, YELLOW, fnt_s)  #ラップタイムを表示

        key = pygame.key.get_pressed()  #keyに全てのキーの状態を代入
        
        if idx == 0:    #idxが0の時(タイトル画面)
            screen.blit(img_title, [120, 120])  #タイトルロゴを表示
            draw_text(screen, "[A] Start game", 400, 320, WHITE, fnt_m) #[A] Start gameの文字を表示
            draw_text(screen, "[S] Select your car", 400, 400, WHITE, fnt_m)    #[S] Select your carの文字を表示
            move_car(0) #全ての車を動かす
            if key[K_a] != 0:   #Aキーが押されたら
                #全ての車を初期位置に
                cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
                for i in range(0, CAR):
                    cars.add(CompCar(random.randint(50, 750), random.randint(200, CMAX-200), 0, random.randint(100, 200)))
                idx = 1     #idxを1にしてカウントダウンに
                tmr = 0 #タイマーを0に
                laps = 0    #周回数を0に
                rec = 0     #走行時間を0に
                recbk = 0   #ラップタイム計算用の変数を0に
                for i in range(LAPS):   #繰り返しで
                    laptime[i] = "0'00.00"  #ラップタイムを0'00.00に
            if key[K_s] != 0:   #Sキーが押されたら
                idx = 4     #idxを4にして車種選択に移行

        if idx == 1:    #idxが1の時(カウントダウン)
            n = 3-int(tmr/60)   #カウントダウンの数を計算しnに代入
            draw_text(screen, str(n), 400, 240, YELLOW, fnt_l)  #その数を表示
            if tmr == 179:  #tmrが179になったら
                pygame.mixer.music.load("sound_pr/bgm.ogg") #BGMを読み込み
                pygame.mixer.music.play(-1) #無限ループで出力
                idx = 2     #idxを2にしてレースへ
                tmr = 0 #tmrを0にする

        if idx == 2:    #idxが2の時(レース中)
            if tmr < 60:    #60フレームの間
                draw_text(screen, "Go!", 400, 240, RED, fnt_l)  #Go!と表示
            rec = rec + 1/60    #走行時間をカウント
            drive_car(key)  #プレイヤーの車を操作
            move_car(1) #COMカーを動かす

        if idx == 3:    #idxが3の時(ゴール)
            if tmr == 1:    #tmrが1なら
                pygame.mixer.music.stop()   #BGMを停止
            if tmr == 30:   #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")    #ジングルを読み込み
                pygame.mixer.music.play(0)  #1回出力
            draw_text(screen, "GOAL!", 400, 240, GREEN, fnt_l)  #GOAL!の文字を表示
            cars[0].spd = cars[0].spd*0.96    #プレイヤーの車の速度を落とす
            cars[0].y = cars[0].y + cars[0].spd/100    #コース上を進ませる
            move_car(1) #COMカーを動かす
            if tmr > 60*8:  #8秒経過したら
                idx = 0 #idxを0にしてタイトルに戻る

        if idx == 4:    #idxが4の時(車種選択画面)
            move_car(0) #全ての車を動かす
            draw_text(screen, "Select your car", 400, 160, WHITE, fnt_m)    #Select your carの文字を表示
            for i in range(3):  #繰り返しで
                x = 160+240*i   #xに選択用の枠のX座標を代入
                y = 300     #yに選択用の枠のY座標を代入
                col = BLACK #colに黒を代入
                if i == mycar:  #選択している車種なら
                    col = (0, 128, 255) #colに明るい青の値を代入
                pygame.draw.rect(screen, col, [x-100, y-80, 200, 160])  #colの色で枠を描く
                draw_text(screen, "["+str(i+1)+"]", x, y-50, WHITE, fnt_m)  #[n]の文字を表示
                screen.blit(img_car[3+i*7], [x-100, y-20])  #車を描く
            draw_text(screen, "[Enter] OK!", 400, 440, GREEN, fnt_m)    #[Enter] OK!という文字を表示
            if key[K_1] == 1:   #1キーが押されたら
                mycar = 0   #mycarに0を代入(赤い車)
            if key[K_2] == 1:   #2キーが押されたら
                mycar = 1   #mycarに1を代入(青い車)
            if key[K_3] == 1:   #3キーが押されたら
                mycar = 2   #mycarに2を代入(黄色の車)
            if key[K_RETURN] == 1:  #Enterキーが押されたら
                idx = 0 #idxを0にしてタイトル画面に戻る

        pygame.display.update() #画面を更新する
        clock.tick(60)  #フレームレートを指定

if __name__ == '__main__':  #このプログラムが直接実行された時に
    main()  #main()関数を呼び出す
