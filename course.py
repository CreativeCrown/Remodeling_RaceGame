#Wayクラスの作成
class Way:
    #コンストラクタの作成
    def __init__(self, curve, updown):
        self.curve = curve  #道が曲がる向き
        self.updown = updown    #道の起伏

    def show(self):
        print(f'{self.curve},{self.updown}')


#Courseクラスの作成
class Course:
    #Wayクラスのリストを格納するための変数を作成
    def __init__(self, CMAX, CLEN, DATA_LR, DATA_UD, object_left, object_right):
        self.data = []  #Wayクラスのインスタンスを格納するリスト
        self.CMAX = CMAX    #コースの長さ
        self.CLEN = CLEN    #コースのデータの量
        self.DATA_LR = DATA_LR  #カーブを作る基になるデータ
        self.DATA_UD = DATA_UD  #起伏を作る基になるデータ
        self.obl = object_left  #道路左に置く物体の番号を入れる
        self.obr = object_right #道路右に置く物体の番号を入れる
        self.laps = 0   #コースのラップ数を管理する


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
    def make_course(self, BOARD):
        for i in range(0, 3):
            for j in range(self.CLEN):  #コースの長さ分(39回)繰り返す
                lr1 = self.DATA_LR[i][j]       #カーブデータをlr1に代入
                lr2 = self.DATA_LR[i][(j+1)%self.CLEN]    #次のカーブデータをlr2に代入
                ud1 = self.DATA_UD[i][j]    #起伏データをudlに代入
                ud2 = self.DATA_UD[i][(j+1)%self.CLEN]   #次の起伏データをud2に代入
                for k in range(BOARD):  #板の数だけ(120回)繰り返す
                    pos = k+BOARD*j     #リストの添え字を計算しposに代入
                    self.add(Way(lr1*(BOARD-k)/BOARD + lr2*k/BOARD, ud1*(BOARD-k)/BOARD + ud2*k/BOARD)) #coursedataに道の曲がる向きと起伏を計算しリストに追加
                    if k == 60: #繰り返しの変数jが60なら
                        self.obr[pos] = 1   #道路右側に看板を置く
                    if j%8 < 7: #繰り返しの変数i%8<7の時
                        if k%12 == 0:   #j%12が0の時に
                            self.obl[pos] = 2    #ヤシの木を置く
                    else:   #そうでなければ
                        if k%20 == 0:   #j%20が0の時に
                            self.obl[pos] = 3    #ヨットを置く
                    if k%12 == 6:   #j%12が6の時に
                        self.obl[pos] = 9    #海を置く


class Course_type:  #コースの種類をもつクラス
    #コンストラクタ
    def __init__(self, LAPS, laptime):
        self.type = []  #Courseクラスのインスタンスを格納するリスト
        self.LAPS = LAPS    #何周でゴールになるかを決める
        self.laptime = laptime  #ラップタイム表示用

    
    #iterメソッド
    def __iter__(self):
        return self.type

    #追加メソッド
    def add(self, course):
        self.type.append(course)

    
    #ゲッター
    def __getitem__(self, key):
        return self.type[key]

    
    #セッター
    def __setitem__(self, key, value):
        self.type[key] = value