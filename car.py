from pygame.locals import *
import random
import draw


#Carクラスの作成
class Car:
    #コンストラクタ
    def __init__(self, x, y, lr, spd):
        self.x = x  #車のX座標
        self.y = y  #車のY座標
        self.lr = lr    #車の左右の向き
        self.spd = spd  #車の速度

    def spd_updown(self, board):    #道の起伏によって車の速度を変えるメソッド
        if board.ud < 0:    #道が下り坂の時
            self.spd = self.spd - int(0.009 * board.ud) #速度を上げる
        elif board.ud > 0:  #道が上り坂の時
            self.spd = self.spd - int(0.009 * board.ud) #速度を下げる


#Carクラスを継承したPlayerCarクラスを作成
class PlayerCar(Car):
    #コンストラクタ
    def __init__(self, x, y, lr, spd, PLCAR_Y, mycar):
        super().__init__(x, y, lr, spd) #Carクラスのコンストラクタを使用
        self.PLCAR_Y = PLCAR_Y  #車の表示位置
        self.mycar = mycar  #選択している車の種類
        self.SPD = 320  #車の最大速度
        self.MOVE = 8    #車の操作性
        self.ACL = 8  #車の加速性


    def drive_car(self, key, transi, recbk, rec, cdata, ctype, board): #プレイヤーの車を操作、制御する関数
        if self.mycar == 0: #選択した車種が赤色なら
            self.SPD = 350   #最大速度を340㎞にする
            self.MOVE = 4    #操作性を標準より下げる
            self.ACL = 2     #加速度を標準より下げる
        elif self.mycar == 1:   #選択した車種が青色なら
            self.SPD = 320      #最大速度を320km
            self.MOVE = 12   #操作性を12
            self.ACL = 8        #加速度を8
        elif self.mycar == 2:   #選択した車種が黄色なら
            self.SPD = 320      #最大速度を320km
            self.MOVE = 8       #操作性を8
            self.ACL = 12     #加速度を12

        if key[K_LEFT] == 1:    #左キーが押されたら
            if self.lr > -3:  #向きが-3より大きければ
                self.lr -= 1  #向きを-1する(左に向かせる)
            self.x = self.x + (self.lr-3)*self.spd/100 - self.MOVE  #車の横方向の座標を計算
        elif key[K_RIGHT] == 1: #そうでなく右キーが押されたら
            if self.lr < 3:   #向きが3より小さければ
                self.lr += 1  #向きを+1する(右に向かせる)
            self.x = self.x + (self.lr+3)*self.spd/100 + self.MOVE  #車の横方向の座標を計算
        else:
            self.lr = int(self.lr*0.9)  #正面向きに近づける

        if key[K_a] == 1:   #Aキーが押されたら
            if self.spd < 180:
                self.spd += 8
            elif self.spd >= 180:
                self.spd += self.ACL #速度を増やす
        elif key[K_z] == 1: #そうでなくZキーが押されたら
            self.spd -= 10    #速度を減らす
        else:   #そうでないなら
            self.spd -= 0.25  #ゆっくり減速

        if self.spd < 0:  #速度が0未満なら
            self.spd = 0  #速度を0にする
        if self.spd > self.SPD:    #最高速度を超えたら
            self.spd = self.SPD    #最高速度にする

        self.x -= self.spd*cdata[int(self.y+self.PLCAR_Y)%cdata.CMAX].curve/50  #車の速度と道の曲がりから横方向の座標を計算
        if self.x < 0:    #左の路肩に接触したら
            self.x = 0    #横方向の座標を0にし
            self.spd *= 0.9   #減速する
        if self.x > 800:  #右の路肩に接触したら
            self.x = 800  #横方向の座標を800にし
            self.spd *= 0.9   #減速する

        self.y = self.y + self.spd/100    #車の速度からコース上の位置を計算
        if self.y > cdata.CLAPMAX*(cdata.laps+1)-1:   #コース終点を越えたら
            ctype.laptime[cdata.laps] = draw.time_str(rec[0]-recbk[0]) #ラップタイムを計算し代入
            recbk[0] = rec[0] #現在のタイムを保持
            cdata.laps = cdata.laps + 1   #周回数の値を1増やす
            if cdata.laps == 3:    #周回数がLAPSの値になったら
                transi.idx = 3 #idxを3にしてゴール処理へ
                transi.tmr = 0 #tmrを0にする
        self.spd_updown(board)




#Carクラスを継承したCompCarクラスを作成
class CompCar(Car):
    #コンストラクタ
    def __init__(self, x, y, lr, spd):
        super().__init__(x, y, lr, spd)  #Carクラスのコンストラクタを使用


#CompCarクラスのリストを管理するCompCarListクラスを作成
class CarsList(Car):
    #コンストラクタ
    def __init__(self, CAR):
        self.data = []  #車のインスタンスを管理するリスト
        self.CAR = CAR  #車の数

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

    def move_car(self, cs, CMAX, board, transi, se_crash):   #コンピュータの車を制御する関数
        for i in range(cs, self.CAR):    #繰り返しで全ての車を処理する
            if self[i].spd > 200:   #速度が200より大きいなら
                self[i].spd = 200
            if self[i].spd < 150:    #速度が100より小さいなら
                self[i].spd += 5 #速度を増やす
            if i == transi.tmr%120:    #一定時間ごとに
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
            if transi.idx == 2:    #idxが2(レース中)ならヒットチェック
                cx = self[i].x-self[0].x  #プレイヤーの車との横方向の距離
                cy = self[i].y-(self[0].y+self[0].PLCAR_Y)%CMAX   #プレイヤーの車とのコース上の距離
                if -100 <= cx and cx <= 100 and -10 <= cy and cy <= 10: #それらがこの範囲内なら
                    #衝突時の座標変化、速度の入れ替えと減速
                    self[0].x -= cx/4    #プレイヤーの車を横に移動
                    self[i].x += cx/4    #コンピュータの車を横に移動
                    self[0].spd, self[i].spd = self[i].spd*0.3, self[0].spd*0.3 #2つの車の速度を入れ替え減速
                    se_crash.play() #衝突音を出力
            self[i].spd_updown(board)   #道の起伏で車の速度を変更するメソッド