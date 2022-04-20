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