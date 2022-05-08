from car import *
import pygame
from pygame.locals import *
from tutorial import *


class Transition:
    #コンストラクタ
    def __init__(self, idx, tmr):
        self.idx = idx  #画面遷移用インデックス
        self.tmr = tmr  #タイマー
        self.snum = 0   #選択した番号の変数(SelectNum)
        self.scnum = 0  #選択した車番号の範囲の変数(SelectCarNum)
        self.judge = 0  #選択した部分の色を変更するための判定をする変数

    def game_transition(self, cars, ctype, cdata, d_item, board, img_title, img_car, se_crash, rec, recbk, key, tuto):
        if self.idx == 0:    #idxが0の時(タイトル画面)
            sgcol = d_item.WHITE    #Start Gameの色の変数(StartGameColor)
            sccol = d_item.WHITE    #Select your carの色の変数(SelectCarColor)
            stcol = d_item.WHITE    #Start tutorialの色の変数(StartTutorialColor)
            d_item.screen.blit(img_title, [120, 120])  #タイトルロゴを表示
            cars.move_car(0, cdata.CMAX, board, self, se_crash) #全ての車を動かす
            if self.snum == 0:   #選択した範囲が0~6なら
                stcol = d_item.GRAY #文字の色を灰色にする
                judge = 0   #judgeの値を0にする
            elif self.snum == 1:  #選択した範囲が7~13なら
                sgcol = d_item.GRAY     #文字の色を灰色にする
                judge = 1   #judgeの値を1にする
            elif self.snum == 2: #選択した範囲が14~20なら
                sccol = d_item.GRAY #文字の色を灰色にする
                judge = 2   #judgeの値を2にする
            d_item.draw_text("ゲームスタート", 400, 400, sgcol, d_item.fnt_m) #[A] Start gameの文字を表示
            d_item.draw_text("車種選択", 400, 480, sccol, d_item.fnt_m)    #[S] Select your carの文字を表示
            d_item.draw_text("チュートリアル", 400, 320, stcol, d_item.fnt_m)    #[T] Start tutorialの文字を表示
            if self.tmr > 10:   #タイマーが0.1秒以上経ったら
                if key[K_UP]:   #上キーが押されたら
                    if self.snum == 0:    #もしsnumが0であれば
                        self.snum = 3  #snumの値を20にする
                    self.snum -= 1  #snumの値を1減らす
                    self.tmr = 0
                if key[K_DOWN]: #下キーが押されたら
                    self.snum = (self.snum + 1) % 3
                    self.tmr = 0
                if key[K_RETURN]:   #Enterキーが押されたら
                    if judge == 1:   #Aキーが押されたら
                        #全ての車を初期位置に
                        cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
                        for i in range(0, cars.CAR):
                            cars.add(CompCar(random.randint(50, 750), random.randint(200, cdata.CMAX-200), 0, random.randint(100, 200)))
                        self.idx = 1     #idxを1にしてカウントダウンに
                        self.tmr = 0 #タイマーを0に
                        cdata.laps = 0    #周回数を0に
                        rec[0] = 0     #走行時間を0に
                        recbk[0] = 0   #ラップタイム計算用の変数を0に
                        for i in range(ctype.LAPS):   #繰り返しで
                            ctype.laptime[i] = "0'00.00"  #ラップタイムを0'00.00に
                    elif judge == 2:   #Sキーが押されたら
                        self.idx = 4     #idxを4にして車種選択に移行
                        self.tmr = 0    #タイマーを初期化
                    elif judge == 0:   #Tキーが押されたら
                        self.idx = 5    #idxを5にしてチュートリアル画面に移行
                    judge = 0   #judgeを初期化する
                    self.tmr = 0

        if self.idx == 1:    #idxが1の時(カウントダウン)
            n = 3-int(self.tmr/60)   #カウントダウンの数を計算しnに代入
            d_item.draw_text(str(n), 400, 240, d_item.YELLOW, d_item.fnt_l)  #その数を表示
            if self.tmr == 179:  #tmrが179になったら
                pygame.mixer.music.load("sound_pr/bgm.ogg") #BGMを読み込み
                pygame.mixer.music.play(-1) #無限ループで出力
                self.idx = 2     #idxを2にしてレースへ
                self.tmr = 0 #tmrを0にする

        if self.idx == 2:    #idxが2の時(レース中)
            if self.tmr < 60:    #60フレームの間
                d_item.draw_text("Go!", 400, 240, d_item.RED, d_item.fnt_l)  #Go!と表示
            rec[0] = rec[0] + 1/60    #走行時間をカウント
            cars[0].drive_car(key, self, recbk, rec, cdata, ctype, board)  #プレイヤーの車を操作
            cars.move_car(1, cdata.CMAX, board, self, se_crash) #COMカーを動かす


        if self.idx == 3:    #idxが3の時(ゴール)
            if self.tmr == 1:    #tmrが1なら
                pygame.mixer.music.stop()   #BGMを停止
            if self.tmr == 30:   #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")    #ジングルを読み込み
                pygame.mixer.music.play(0)  #1回出力
            d_item.draw_text("GOAL!", 400, 240, d_item.GREEN, d_item.fnt_l)  #GOAL!の文字を表示
            cars[0].spd = cars[0].spd*0.96    #プレイヤーの車の速度を落とす
            cars[0].y = cars[0].y + cars[0].spd/100    #コース上を進ませる
            cars.move_car(1, cdata.CMAX, board, self, se_crash) #COMカーを動かす
            if self.tmr > 60*8:  #8秒経過したら
                self.idx = 0 #idxを0にしてタイトルに戻る

        if self.idx == 4:    #idxが4の時(車種選択画面)
            SPD = [8,5,5]
            MOVE = [2,6,4]
            ACL = [1,4,6]
            cars.move_car(0, cdata.CMAX, board, self, se_crash) #全ての車を動かす
            d_item.draw_text("車を選ぼう！", 400, 100, d_item.WHITE, d_item.fnt_m)    #Select your carの文字を表示
            for i in range(3):  #繰り返しで
                x = 160+240*i   #xに選択用の枠のX座標を代入
                y = 240     #yに選択用の枠のY座標を代入
                col = d_item.BLACK #colに黒を代入
                if i == cars[0].mycar:  #選択している車種なら
                    col = (0, 128, 255) #colに明るい青の値を代入
                pygame.draw.rect(d_item.screen, col, [x-100, y-80, 200, 230])  #colの色で枠を描く
                d_item.draw_text("最大速度", x-55, y+90, d_item.WHITE, d_item.fnt_ss)  #speedを表示
                d_item.draw_text("操作性", x-60, y+113, d_item.WHITE, d_item.fnt_ss) #usabilityを表示
                d_item.draw_text("加速度", x-60, y+137, d_item.WHITE, d_item.fnt_ss)  #axelを表示
                for j in range(SPD[i]):     #speedの数の分繰り返し
                    pygame.draw.rect(d_item.screen, d_item.YELLOW, [(x-36)+(38+(j*12)), y+82, 10, 16])  #■を描画
                for j in range(MOVE[i]):    #usabilityの数の分繰り返し
                    pygame.draw.rect(d_item.screen, d_item.YELLOW, [(x-36)+(38+(j*12)), y+105, 10, 16]) #■を描画
                for j in range(ACL[i]):     #axelの数の分繰り返し
                    pygame.draw.rect(d_item.screen, d_item.YELLOW, [(x-36)+(38+(j*12)), y+128, 10, 16]) #■を描画
                d_item.screen.blit(img_car[3+i*7], [x-100, y-20])  #車を描く
            d_item.draw_text("[← →]で選択", 200, 440, d_item.GREEN, d_item.fnt_m)    #[← →]で選択という文字を表示
            d_item.draw_text("[Enter]で決定", 600, 440, d_item.GREEN, d_item.fnt_m)    #[Enter]で決定という文字を表示
            
            if self.tmr > 10:   #画面が切り替わり、0.1秒経ったら
                if key[K_RETURN]:   #Enterキーが押されたら
                    self.idx = 0    #idxを初期化
                    self.tmr = 0    #tmrを初期化
                if key[K_LEFT]: #左キーが押されたら
                    if cars[0].mycar == 0: #cars[0].mycarの値が0だったら
                        cars[0].mycar = 3 #cars[0].mycarの値を3にする
                    cars[0].mycar -= 1 #cars[0].mycarの値を1減らす
                    self.tmr = 0
                if key[K_RIGHT]:    #右キーが押されたら
                    cars[0].mycar = (cars[0].mycar + 1) % 3  #cars[0].mycarの値を0～2まで増やす
                    self.tmr = 0


        if self.idx == 5:   #idxが5の時
            cola = d_item.WHITE   #
            colz = d_item.WHITE    
            coll = d_item.WHITE
            colr = d_item.WHITE
            if key[K_a] != 0:
                tuto.btna = 1
            if key[K_z] != 0:
                tuto.btnz = 1
            if key[K_LEFT] != 0:
                tuto.btnl = 1
            if key[K_RIGHT] != 0:
                tuto.btnr = 1
            if tuto.btna == 1:
                cola = (128, 128, 128)
            if tuto.btnz == 1:
                colz = (128, 128, 128)
            if tuto.btnl == 1:
                coll = (128, 128, 128)
            if tuto.btnr == 1:
                colr = (128, 128, 128)
            d_item.draw_text("Aボタン：アクセル", 650, 100, cola, d_item.fnt_ss)
            d_item.draw_text("Zボタン：ブレーキ", 650, 140, colz, d_item.fnt_ss)
            d_item.draw_text("左カーソルキー：左に曲がる", 650, 180, coll, d_item.fnt_ss)
            d_item.draw_text("右カーソルキー：右に曲がる", 650, 220, colr, d_item.fnt_ss)
            cars[0].drive_car(key, self, recbk, rec, cdata, ctype, board)  #プレイヤーの車を操作
            if tuto.btna == 1 and tuto.btnz == 1 and tuto.btnl == 1 and tuto.btnr == 1:
                if tuto.allbtn == False:
                    self.tmr = 0
                tuto.allbtn = True
                if self.tmr > 30:
                    self.tmr = 0
                    self.idx = 6

        if self.idx == 6:
            d_item.draw_text("チュートリアル終了！", 400, 300, d_item.YELLOW, d_item.fnt_m)
            d_item.draw_text("ゲームスタートで遊ぼう！", 400, 400, d_item.YELLOW, d_item.fnt_m)
            if self.tmr > 60*5:
                tuto.btna, tuto.btnz, tuto.btnl, tuto.btnr = 0, 0, 0, 0
                self.tmr = 0
                self.idx = 0
            
