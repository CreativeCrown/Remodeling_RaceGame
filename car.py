from pygame.locals import *
import random

def time_str(val):  #**'**.**という時間の文字列を作る関数
    sec = int(val)          #引数を整数の秒数にしてsecに代入
    ms = int((val-sec)*100) #秒数の小数点以下の値をmsに代入
    mi = int(sec/60)        #分をmiに代入
    return "{}'{:02}.{:02}".format(mi, sec%60, ms)  #**'**.**という文字列を返す

#Carクラスの作成
class Car:
    #コンストラクタ
    def __init__(self, x, y, lr, spd):
        self.x = x
        self.y = y
        self.lr = lr
        self.spd = spd


#Carクラスを継承したPlayerCarクラスを作成
class PlayerCar(Car):
    #コンストラクタ
    def __init__(self, x, y, lr, spd, PLCAR_Y):
        super().__init__(x, y, lr, spd)
        self.PLCAR_Y = PLCAR_Y



    def drive_car(self, key, idx, tmr, recbk, rec, laps, laptime, CMAX, coursedata): #プレイヤーの車を操作、制御する関数
        #global idx, tmr, laps, recbk     #これらをグローバル変数とする
        if key[K_LEFT] == 1:    #左キーが押されたら
            if self.lr > -3:  #向きが-3より大きければ
                self.lr -= 1  #向きを-1する(左に向かせる)
            self.x = self.x + (self.lr-3)*self.spd/100 - 5  #車の横方向の座標を計算
        elif key[K_RIGHT] == 1: #そうでなく右キーが押されたら
            if self.lr < 3:   #向きが3より小さければ
                self.lr += 1  #向きを+1する(右に向かせる)
            self.x = self.x + (self.lr+3)*self.spd/100 + 5  #車の横方向の座標を計算
        else:
            self.lr = int(self.lr*0.9)  #正面向きに近づける

        if key[K_a] == 1:   #Aキーが押されたら
            self.spd += 3 #速度を増やす
        elif key[K_z] == 1: #そうでなくZキーが押されたら
            self.spd -= 10    #速度を減らす
        else:   #そうでないなら
            self.spd -= 0.25  #ゆっくり減速

        if self.spd < 0:  #速度が0未満なら
            self.spd = 0  #速度を0にする
        if self.spd > 320:    #最高速度を超えたら
            self.spd = 320    #最高速度にする

        self.x -= self.spd*coursedata[int(self.y+self.PLCAR_Y)%CMAX].curve/50  #車の速度と道の曲がりから横方向の座標を計算
        if self.x < 0:    #左の路肩に接触したら
            self.x = 0    #横方向の座標を0にし
            self.spd *= 0.9   #減速する
        if self.x > 800:  #右の路肩に接触したら
            self.x = 800  #横方向の座標を800にし
            self.spd *= 0.9   #減速する

        self.y = self.y + self.spd/100    #車の速度からコース上の位置を計算
        if self.y > CMAX-1:   #コース終点を越えたら
            self.y -= CMAX    #コースの頭に戻す
            laptime[laps[0]] = time_str(rec[0]-recbk[0]) #ラップタイムを計算し代入
            recbk[0] = rec[0] #現在のタイムを保持
            laps[0] = laps[0] + 1   #周回数の値を1増やす
            if laps[0] == 3:    #周回数がLAPSの値になったら
                idx[0] = 3 #idxを3にしてゴール処理へ
                tmr[0] = 0 #tmrを0にする



#Carクラスを継承したCompCarクラスを作成
class CompCar(Car):
    #コンストラクタ
    def __init__(self, x, y, lr, spd):
        super().__init__(x, y, lr, spd)


#CompCarクラスのリストを管理するCompCarListクラスを作成
class CarsList:
    #コンストラクタ
    def __init__(self):
        self.data = []

    #イテレータ
    def __iter__(self):
        return iter(self.data)

    #追加メソッド
    def add(self, CompCar):
        self.data.append(CompCar)

    #ゲッター
    def __getitem__(self, key):
        return self.data[key]

    #セッター
    def __setitem__(self, key, value):
        self.data[key] = value

    def move_car(self, cs, CAR, CMAX, tmr, idx, se_crash):   #コンピュータの車を制御する関数
        for i in range(cs, CAR):    #繰り返しで全ての車を処理する
            if self[i].spd < 100:    #速度が100より小さいなら
                self[i].spd += 3 #速度を増やす
            if i == tmr[0]%120:    #一定時間ごとに
                self[i].lr += random.choice([-1, 0, 1])  #向きをランダムに変える
                if self[i].lr < -3:  self[i].lr = -3  #向きが-3未満なら-3にする
                if self[i].lr > 3:   self[i].lr = 3   #向きが3を超えたら3にする
            self[i].x = self[i].x + self[i].lr*self[i].spd/100  #車の向きと速度から横方向の座標を計算
            if self[i].x < 50:   #左の路肩に近づいたら
                self[i].x = 50   #それ以上行かないようにし
                self[i].lr = int(self[i].lr*0.9)  #正面向きに近づける
            if self[i].x > 750:  #右の路肩に近づいたら
                self[i].x = 750  #それ以上行かないようにし
                self[i].lr = int(self[i].lr*0.9)  #正面向きに近づける
            self[i].y += self[i].spd/100  #車の速度からコース上の位置を計算
            if self[i].y > CMAX-1:   #コース終点を越えたら
                self[i].y -= CMAX    #コースの頭に戻す
            if idx[0] == 2:    #idxが2(レース中)ならヒットチェック
                cx = self[i].x-self[0].x  #プレイヤーの車との横方向の距離
                cy = self[i].y-(self[0].y+self[0].PLCAR_Y)%CMAX   #プレイヤーの車とのコース上の距離
                if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10: #それらがこの範囲内なら
                    #衝突時の座標変化、速度の入れ替えと減速
                    self[0].x -= cx/4    #プレイヤーの車を横に移動
                    self[i].x += cx/4    #コンピュータの車を横に移動
                    self[0].spd, self[i].spd = self[i].spd*0.3, self[0].spd*0.3 #2つの車の速度を入れ替え減速
                    se_crash.play() #衝突音を出力