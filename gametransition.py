from car import *
import pygame
from pygame.locals import *
from tutorial import *


class Transition:
    #コンストラクタ
    def __init__(self, idx, tmr):
        self.idx = idx  #画面遷移用インデックス
        self.tmr = tmr  #タイマー

    def game_transition(self, cars, ctype, cdata, d_item, board, img_title, img_car, se_crash, rec, recbk, key, tuto):
        if self.idx == 0:    #idxが0の時(タイトル画面)
            d_item.screen.blit(img_title, [120, 120])  #タイトルロゴを表示
            d_item.draw_text("[A] Start game", 400, 320, d_item.WHITE, d_item.fnt_m) #[A] Start gameの文字を表示
            d_item.draw_text("[S] Select your car", 400, 400, d_item.WHITE, d_item.fnt_m)    #[S] Select your carの文字を表示
            d_item.draw_text("[T] Start tutorial", 400, 480, d_item.WHITE, d_item.fnt_m)    #[T] Start tutorialの文字を表示
            cars.move_car(0, cdata.CMAX, board, self, se_crash) #全ての車を動かす
            if key[K_a] != 0:   #Aキーが押されたら
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
            if key[K_s] != 0:   #Sキーが押されたら
                self.idx = 4     #idxを4にして車種選択に移行
            if key[K_t] != 0:   #Tキーが押されたら
                self.idx = 5    #idxを5にしてチュートリアル画面に移行

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
            d_item.draw_text("Select your car", 400, 100, d_item.WHITE, d_item.fnt_m)    #Select your carの文字を表示
            for i in range(3):  #繰り返しで
                x = 160+240*i   #xに選択用の枠のX座標を代入
                y = 240     #yに選択用の枠のY座標を代入
                col = d_item.BLACK #colに黒を代入
                if i == cars[0].mycar:  #選択している車種なら
                    col = (0, 128, 255) #colに明るい青の値を代入
                pygame.draw.rect(d_item.screen, col, [x-100, y-80, 200, 230])  #colの色で枠を描く
                d_item.draw_text("["+str(i+1)+"]", x, y-50, d_item.WHITE, d_item.fnt_m)  #[n]の文字を表示
                d_item.draw_text("speed", x-30, y+90, d_item.WHITE, d_item.fnt_ss)  #speedを表示
                d_item.draw_text("usability", x-45, y+113, d_item.WHITE, d_item.fnt_ss) #usabilityを表示
                d_item.draw_text("axel", x-25, y+137, d_item.WHITE, d_item.fnt_ss)  #axelを表示
                for j in range(SPD[i]):     #speedの数の分繰り返し
                    pygame.draw.rect(d_item.screen, d_item.YELLOW, [(x-36)+(38+(j*12)), y+82, 10, 16])  #■を描画
                for j in range(MOVE[i]):    #usabilityの数の分繰り返し
                    pygame.draw.rect(d_item.screen, d_item.YELLOW, [(x-36)+(38+(j*12)), y+105, 10, 16]) #■を描画
                for j in range(ACL[i]):     #axelの数の分繰り返し
                    pygame.draw.rect(d_item.screen, d_item.YELLOW, [(x-36)+(38+(j*12)), y+128, 10, 16]) #■を描画
                d_item.screen.blit(img_car[3+i*7], [x-100, y-20])  #車を描く
            d_item.draw_text("[Enter] OK!", 400, 440, d_item.GREEN, d_item.fnt_m)    #[Enter] OK!という文字を表示
            if key[K_1] == 1:   #1キーが押されたら
                cars[0].mycar = 0   #mycarに0を代入(赤い車)
            if key[K_2] == 1:   #2キーが押されたら
                cars[0].mycar = 1   #mycarに1を代入(青い車)
            if key[K_3] == 1:   #3キーが押されたら
                cars[0].mycar = 2   #mycarに2を代入(黄色の車)
            if key[K_RETURN] == 1:  #Enterキーが押されたら
                self.idx = 0 #idxを0にしてタイトル画面に戻る

        if self.idx == 5:   #idxが5の時
            cola = d_item.WHITE   #灰色
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
            d_item.draw_text("push [A] button to move", 126, 300, cola, d_item.fnt_ss)
            d_item.draw_text("push [Z] button to stop", 118, 330, colz, d_item.fnt_ss)
            d_item.draw_text("push [LEFT] button", 100, 360, coll, d_item.fnt_ss)
            d_item.draw_text("to turn left", 140, 380, coll, d_item.fnt_ss)
            d_item.draw_text("push [RIGHT] button", 110, 410, colr, d_item.fnt_ss)
            d_item.draw_text("to turn right", 140, 430, colr, d_item.fnt_ss)
            cars[0].drive_car(key, self, recbk, rec, cdata, ctype, board)  #プレイヤーの車を操作
            if tuto.btna == 1 and tuto.btnz == 1 and tuto.btnl == 1 and tuto.btnr == 1:
                self.tmr = 0
                self.idx = 6

        if self.idx == 6:
            d_item.draw_text("That's it!", 400, 300, d_item.YELLOW, d_item.fnt_m)
            d_item.draw_text("Let's Start Game!", 400, 400, d_item.YELLOW, d_item.fnt_m)
            if self.tmr > 60*5:
                tuto.btna, tuto.btnz, tuto.btnl, tuto.btnr = 0, 0, 0, 0
                self.tmr = 0
                self.idx = 0
            
