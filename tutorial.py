#チュートリアル用クラス
class Tutorial:
    #コンストラクタ
    def __init__(self):
        self.__btna = 0
        self.__btnz = 0
        self.__btnl = 0
        self.__btnr = 0
        self.__allbtn = False

    #ゲッター
    @property
    def btna(self):
        return self.__btna

    @property
    def btnz(self):
        return self.__btnz

    @property
    def btnl(self):
        return self.__btnl

    @property
    def btnr(self):
        return self.__btnr

    @property
    def allbtn(self):
        return self.__allbtn


    #セッター
    @btna.setter
    def btna(self, value):
        self.__btna = value

    @btnz.setter
    def btnz(self, value):
        self.__btnz = value

    @btnl.setter
    def btnl(self, value):
        self.__btnl = value

    @btnr.setter
    def btnr(self, value):
        self.__btnr = value

    @allbtn.setter
    def allbtn(self, value):
        self.__allbtn = value