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
    def __init__(self, x, y, lr, spd):
        super().__init__(x, y, lr, spd)


#Carクラスを継承したCompCarクラスを作成
class CompCar(Car):
    #コンストラクタ
    def __init__(self, x, y, lr, spd):
        super().__init__(x, y, lr, spd)


#CompCarクラスのリストを管理するCompCarListクラスを作成
class CompCarList:
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
