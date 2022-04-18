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

    #追加メソッド
    def add(self, way):
        self.data.append(way)

    #ゲッター
    def __getitem__(self, key):
        return self.data[key]

    #セッター
    def __setitem__(self, key, value):
        self.data[key] = value

    #コースデータを作るメソッド
    def make_course(self, BOARD, object_right, object_left):
        for i in range(self.CLEN):  #コースの長さ分(39回)繰り返す
            lr1 = self.DATA_LR[i]       #カーブデータをlr1に代入
            lr2 = self.DATA_LR[(i+1)%self.CLEN]    #次のカーブデータをlr2に代入
            ud1 = self.DATA_UD[i]    #起伏データをudlに代入
            ud2 = self.DATA_UD[(i+1)%self.CLEN]   #次の起伏データをud2に代入
            for j in range(BOARD):  #板の数だけ(120回)繰り返す
                pos = j+BOARD*i     #リストの添え字を計算しposに代入
                self.add(Way(lr1*(BOARD-j)/BOARD + lr2*j/BOARD, ud1*(BOARD-j)/BOARD + ud2*j/BOARD)) #coursedataに道の曲がる向きと起伏を計算しリストに追加
                if j == 60: #繰り返しの変数jが60なら
                    object_right[pos] = 1   #道路右側に看板を置く
                if i%8 < 7: #繰り返しの変数i%8<7の時
                    if j%12 == 0:   #j%12が0の時に
                        object_left[pos] = 2    #ヤシの木を置く
                else:   #そうでなければ
                    if j%20 == 0:   #j%20が0の時に
                        object_left[pos] = 3    #ヨットを置く
                if j%12 == 6:   #j%12が6の時に
                    object_left[pos] = 9    #海を置く
