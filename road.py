import math

#道路を作る板の情報を持つBoardクラスを作成
class Board:
    #コンストラクタ
    def __init__(self, BOARD, BOARD_W, BOARD_H, BOARD_UD):
        self.BOARD = BOARD
        self.BOARD_W = BOARD_W
        self.BOARD_H = BOARD_H
        self.BOARD_UD = BOARD_UD

    #道路の板の基本形状を計算するメソッド
    def roadbasic(self):
        for i in range(self.BOARD):
            self.BOARD_W[i] = 10+(self.BOARD-i)*(self.BOARD-i)/12  #幅を計算
            self.BOARD_H[i] = 3.4*(self.BOARD-i)/self.BOARD    #高さを計算
            self.BOARD_UD[i] = 2*math.sin(math.radians(i*1.5))   #起伏の値を三角関数で計算

    #描画用の道路のX座標(道の曲がり具合)を計算するメソッド
    def make_curve(self, di, board_x, coursedata, cars, CMAX):
        for i in range(self.BOARD):
            di[0] += coursedata[int(cars[0].y+i)%CMAX].curve    #カーブデータから道の曲がりを計算
            board_x[i] = 400 - self.BOARD_W[i]*cars[0].x/800 + di[0]/2  #板のX座標を計算し代入
            
    #描画用の道路の路面の起伏(高低差)を計算するメソッド
    def make_updown(self, ud, board_ud, coursedata, cars, CMAX):
        for i in range(self.BOARD):
            ud[0] += coursedata[int(cars[0].y+i)%CMAX].updown   #起伏データから起伏を計算
            board_ud[i] = ud[0]/30 #板の高低を計算し代入
