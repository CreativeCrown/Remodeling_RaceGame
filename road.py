import math

#道路を作る板の情報を持つBoardクラスを作成
class Board:
    #コンストラクタ
    def __init__(self, BOARD, BOARD_W, BOARD_H, BOARD_UD, board_x, board_ud):
        self.BOARD = BOARD  #板の数
        self.BOARD_W = BOARD_W  #板の幅
        self.BOARD_H = BOARD_H  #板の高さ
        self.BOARD_UD = BOARD_UD    #板の起伏用の値
        self.board_x = board_x  #描画用の板のX座標
        self.board_ud = board_ud    #描画用の板の高低
        self.di = None #道が曲がる向きを計算する変数
        self.ud = None #道の起伏を計算する変数

    #道路の板の基本形状を計算するメソッド
    def roadbasic(self):
        for i in range(self.BOARD):
            self.BOARD_W[i] = 10+(self.BOARD-i)*(self.BOARD-i)/12  #幅を計算
            self.BOARD_H[i] = 3.4*(self.BOARD-i)/self.BOARD    #高さを計算
            self.BOARD_UD[i] = 2*math.sin(math.radians(i*1.5))   #起伏の値を三角関数で計算

    #描画用の道路のX座標(道の曲がり具合)を計算するメソッド
    def make_curve(self, cdata, cars):
        for i in range(self.BOARD):
            self.di += cdata[int(cars[0].y+i)%cdata.CMAX].curve    #カーブデータから道の曲がりを計算
            self.board_x[i] = 400 - self.BOARD_W[i]*cars[0].x/800 + self.di/2  #板のX座標を計算し代入
            
    #描画用の道路の路面の起伏(高低差)を計算するメソッド
    def make_updown(self, cdata, cars):
        for i in range(self.BOARD):
            self.ud += cdata[int(cars[0].y+i)%cdata.CMAX].updown   #起伏データから起伏を計算
            self.board_ud[i] = self.ud/30 #板の高低を計算し代入
