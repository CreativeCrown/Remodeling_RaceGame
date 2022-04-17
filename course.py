#Wayクラスの作成
class Way:
    #コンストラクタの作成
    def __init__(self, curve, updown):
        self.curve = curve
        self.updown = updown

    def show(self):
        print(f'{self.curve},{self.updown}')



#Courseクラスの作成
class Course:
    #Wayクラスのリストを格納するための変数を作成
    def __init__(self, CLEN, DATA_LR, DATA_UD):
        self.data = []
        self.CLEN = CLEN
        self.DATA_LR = DATA_LR
        self.DATA_UD = DATA_UD

    #iterメソッド
    def __iter__(self):
        return iter(self.data)

    def add(self, way):
        self.data.append(way)

    #ゲッター
    def __getitem__(self, key):
        return self.data[key]

    #セッター
    def __setitem__(self, key, value):
        self.data[key] = value

    def make_course(self, BOARD, object_right, object_left):
        for i in range(self.CLEN):
            lr1 = self.DATA_LR[i]
            lr2 = self.DATA_LR[(i+1)%self.CLEN]
            ud1 = self.DATA_UD[i]
            ud2 = self.DATA_UD[(i+1)%self.CLEN]
            for j in range(BOARD):
                pos = j+BOARD*i 
                self.add(Way(lr1*(BOARD-j)/BOARD + lr2*j/BOARD, ud1*(BOARD-j)/BOARD + ud2*j/BOARD))
                # curve[pos] = lr1*(BOARD-j)/BOARD + lr2*j/BOARD
                # updown[pos] = ud1*(BOARD-j)/BOARD + ud2*j/BOARD
                if j == 60:
                    object_right[pos] = 1 # 看板
                if i%8 < 7:
                    if j%12 == 0:
                        object_left[pos] = 2 # ヤシの木
                else:
                    if j%20 == 0:
                        object_left[pos] = 3 # ヨット
                if j%12 == 6:
                    object_left[pos] = 9 # 海
