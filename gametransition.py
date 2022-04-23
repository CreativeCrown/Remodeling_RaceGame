from car import *
import pygame
from pygame.locals import *
class Transition:
    #コンストラクタ
    def __init__(self, idx, tmr):
        self.idx = idx
        self.tmr = tmr

    def game_trandition(self, cars, coursedata, draw, img_title, img_car, se_crash, rec, recbk, key):
        if self.idx == 0:    #idxが0の時(タイトル画面)
            draw.screen.blit(img_title, [120, 120])  #タイトルロゴを表示
            draw.draw_text("[A] Start game", 400, 320, draw.WHITE, draw.fnt_m) #[A] Start gameの文字を表示
            draw.draw_text("[S] Select your car", 400, 400, draw.WHITE, draw.fnt_m)    #[S] Select your carの文字を表示
            cars.move_car(0, coursedata.CMAX, self, se_crash) #全ての車を動かす
            if key[K_a] != 0:   #Aキーが押されたら
                #全ての車を初期位置に
                cars[0].x, cars[0].y, cars[0].lr, cars[0].spd = 400, 0, 0, 0
                for i in range(0, cars.CAR):
                    cars.add(CompCar(random.randint(50, 750), random.randint(200, coursedata.CMAX-200), 0, random.randint(100, 200)))
                self.idx = 1     #idxを1にしてカウントダウンに
                self.tmr = 0 #タイマーを0に
                coursedata.laps = 0    #周回数を0に
                rec[0] = 0     #走行時間を0に
                recbk[0] = 0   #ラップタイム計算用の変数を0に
                for i in range(coursedata.LAPS):   #繰り返しで
                    coursedata.laptime[i] = "0'00.00"  #ラップタイムを0'00.00に
            if key[K_s] != 0:   #Sキーが押されたら
                self.idx = 4     #idxを4にして車種選択に移行

        if self.idx == 1:    #idxが1の時(カウントダウン)
            n = 3-int(self.tmr/60)   #カウントダウンの数を計算しnに代入
            draw.draw_text(str(n), 400, 240, draw.YELLOW, draw.fnt_l)  #その数を表示
            if self.tmr == 179:  #tmrが179になったら
                pygame.mixer.music.load("sound_pr/bgm.ogg") #BGMを読み込み
                pygame.mixer.music.play(-1) #無限ループで出力
                self.idx = 2     #idxを2にしてレースへ
                self.tmr = 0 #tmrを0にする

        if self.idx == 2:    #idxが2の時(レース中)
            if self.tmr < 60:    #60フレームの間
                draw.draw_text("Go!", 400, 240, draw.RED, draw.fnt_l)  #Go!と表示
            rec[0] = rec[0] + 1/60    #走行時間をカウント
            cars[0].drive_car(key, self, recbk, rec, coursedata)  #プレイヤーの車を操作
            cars.move_car(1, coursedata.CMAX, self, se_crash) #COMカーを動かす


        if self.idx == 3:    #idxが3の時(ゴール)
            if self.tmr == 1:    #tmrが1なら
                pygame.mixer.music.stop()   #BGMを停止
            if self.tmr == 30:   #tmrが30になったら
                pygame.mixer.music.load("sound_pr/goal.ogg")    #ジングルを読み込み
                pygame.mixer.music.play(0)  #1回出力
            draw.draw_text("GOAL!", 400, 240, draw.GREEN, draw.fnt_l)  #GOAL!の文字を表示
            cars[0].spd = cars[0].spd*0.96    #プレイヤーの車の速度を落とす
            cars[0].y = cars[0].y + cars[0].spd/100    #コース上を進ませる
            cars.move_car(1, coursedata.CMAX, self, se_crash) #COMカーを動かす
            if self.tmr > 60*8:  #8秒経過したら
                self.idx = 0 #idxを0にしてタイトルに戻る

        if self.idx == 4:    #idxが4の時(車種選択画面)
            cars.move_car(0, coursedata.CMAX, self, se_crash) #全ての車を動かす
            draw.draw_text("Select your car", 400, 160, draw.WHITE, draw.fnt_m)    #Select your carの文字を表示
            for i in range(3):  #繰り返しで
                x = 160+240*i   #xに選択用の枠のX座標を代入
                y = 300     #yに選択用の枠のY座標を代入
                col = draw.BLACK #colに黒を代入
                if i == cars[0].mycar:  #選択している車種なら
                    col = (0, 128, 255) #colに明るい青の値を代入
                pygame.draw.rect(draw.screen, col, [x-100, y-80, 200, 160])  #colの色で枠を描く
                draw.draw_text("["+str(i+1)+"]", x, y-50, draw.WHITE, draw.fnt_m)  #[n]の文字を表示
                draw.screen.blit(img_car[3+i*7], [x-100, y-20])  #車を描く
            draw.draw_text("[Enter] OK!", 400, 440, draw.GREEN, draw.fnt_m)    #[Enter] OK!という文字を表示
            if key[K_1] == 1:   #1キーが押されたら
                cars[0].mycar = 0   #mycarに0を代入(赤い車)
            if key[K_2] == 1:   #2キーが押されたら
                cars[0].mycar = 1   #mycarに1を代入(青い車)
            if key[K_3] == 1:   #3キーが押されたら
                cars[0].mycar = 2   #mycarに2を代入(黄色の車)
            if key[K_RETURN] == 1:  #Enterキーが押されたら
                self.idx = 0 #idxを0にしてタイトル画面に戻る
