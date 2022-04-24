import pygame

class Draw: #描画用クラス
    #コンストラクタ
    def __init__(self, screen, fnt_s, fnt_m, fnt_l):
        self.screen = screen    #スクリーンの大きさ
        self.vertical = 0    #背景の水平方向
        self.horizon = 0      #背景の垂直方向
        self.sy = 0         #背景のY座標
        self.WHITE = (255, 255, 255)    #白色
        self.BLACK = (0, 0, 0)          #黒色
        self.RED = (255, 0, 0)          #赤色
        self.YELLOW = (255, 224, 0)     #黄色
        self.GREEN = (0, 255, 0)        #緑色
        self.fnt_s = fnt_s      #Sサイズフォント
        self.fnt_m = fnt_m      #Mサイズフォント
        self.fnt_l = fnt_l      #Lサイズフォント

    
    def make_horizon(self, board):    #背景の垂直を計算するメソッド
        self.horizon = 400 + int(board.ud/3)   #地平線のY座標を計算しhorizonに代入
        #self.sy = self.horizon      #道路を描き始めるY座標をsyに代入

    
    def make_vertical(self, cars, board):   #背景の水平を計算するメソッド
        self.vertical = self.vertical - int(cars[0].spd*board.di/8000)   #背景の垂直位置を計算
        if self.vertical < 0:    #それが0未満になったら
            self.vertical += 800 #800を足す
        if self.vertical >= 800: #800以上になったら
            self.vertical -= 800 #800を引く


    def draw_obj(self, img, x, y, sc):  # 座標とスケールを受け取り、物体を描く関数
        img_rz = pygame.transform.rotozoom(img, 0, sc)  # 拡大縮小した画像を作る
        w = img_rz.get_width()  # その画像の幅をwに代入
        h = img_rz.get_height()  # その画像の高さをhに代入
        self.screen.blit(img_rz, [x-w/2, y-h])  # 画像を描く


    def draw_shadow(self, x, y, siz):  # 影を表示する関数
        shadow = pygame.Surface([siz, siz/4])  # 描画面(サーフェイス)を用意する
        shadow.fill(self.RED)  # その描画面を赤で塗り潰す
        shadow.set_colorkey(self.RED)  # 描画面の透過色を指定
        shadow.set_alpha(128)  # 描画面の透明度を設定
        pygame.draw.ellipse(shadow, self.BLACK, [0, 0, siz, siz/4])  # 描画面に黒で楕円を描く
        self.screen.blit(shadow, [x-siz/2, y-siz/4])  # 楕円を描いた描画面をゲーム画面に転送


    def draw_text(self, txt, x, y, col, fnt):  # 影付きの文字列を表示する関数
        sur = fnt.render(txt, True, self.BLACK)  # 黒で文字列を描いたサーフェイスを生成
        x -= sur.get_width()/2  # センタリングするためX座標を計算
        y -= sur.get_height()/2  # センタリングするためY座標を計算
        self.screen.blit(sur, [x+2, y+2])  # サーフェイスを画面に転送
        sur = fnt.render(txt, True, col)  # 指定色で文字列を描いたサーフェイスを生成
        self.screen.blit(sur, [x, y])  # サーフェイスを画面に転送


    def draw_road(self, board, cars, cdata, img_obj, img_sea, img_car):  # 描画用データをもとに道路を描くメソッド
        # self.sy = self.horizon    #道路を描き始めるY座標をsyに代入
        for i in range(board.BOARD-1, 0, -1):  # 繰り返しで道路の板を描いていく
            ux = board.board_x[i]  # 台形の上底のX座標をuxに代入
            uy = self.sy - board.BOARD_UD[i]*board.board_ud[i]  # 上底のY座標をuyに代入
            uw = board.BOARD_W[i]  # 上底の幅をuwに代入
            self.sy = self.sy + board.BOARD_H[i]*(600-self.horizon)/200  # 台形を描くY座標を次の値にする
            bx = board.board_x[i-1]  # 台形の下底のX座標をbxに代入
            by = self.sy - board.BOARD_UD[i-1]*board.board_ud[i-1]  # 下底のY座標をbyに代入
            bw = board.BOARD_W[i-1]  # 下底の幅をbwに代入
            col = (160, 160, 160)  # colに板の色を代入
            if int(cars[0].y+i) % cdata.CMAX == cars[0].PLCAR_Y+10:  # ゴールの位置なら
                col = (192, 0, 0)  # 赤線の色の値を代入
            pygame.draw.polygon(
                self.screen, col, [[ux, uy], [ux+uw, uy], [bx+bw, by], [bx, by]])  # 道路の板を描く

            if int(cars[0].y+i) % 10 <= 4:  # 一定間隔で
                pygame.draw.polygon(self.screen, self.YELLOW, [[ux, uy], [
                                    ux+uw*0.02, uy], [bx+bw*0.02, by], [bx, by]])  # 道路左の黄色いラインを描く
                pygame.draw.polygon(self.screen, self.YELLOW, [
                                    [ux+uw*0.98, uy], [ux+uw, uy], [bx+bw, by], [bx+bw*0.98, by]])  # 道路右の黄色いラインを描く
            if int(cars[0].y+i) % 20 <= 10:  # 一定間隔で
                pygame.draw.polygon(self.screen, self.WHITE, [
                                    [ux+uw*0.24, uy], [ux+uw*0.26, uy], [bx+bw*0.26, by], [bx+bw*0.24, by]])  # 左側の白ラインを描く
                pygame.draw.polygon(self.screen, self.WHITE, [
                                    [ux+uw*0.49, uy], [ux+uw*0.51, uy], [bx+bw*0.51, by], [bx+bw*0.49, by]])  # 中央の白ラインを描く
                pygame.draw.polygon(self.screen, self.WHITE, [
                                    [ux+uw*0.74, uy], [ux+uw*0.76, uy], [bx+bw*0.76, by], [bx+bw*0.74, by]])  # 右側の白ラインを描く

            scale = 1.5*board.BOARD_W[i]/board.BOARD_W[0]  # 道路横の物体のスケールを計算
            obj_l = cdata.obl[int(cars[0].y+i) % cdata.CMAX]  # obj_lに左側の物体の番号を代入
            if obj_l == 2:  # ヤシの木なら
                self.draw_obj(img_obj[obj_l], ux -
                        uw*0.05, uy, scale)  # その画像を描画
            if obj_l == 3:  # ヨットなら
                self.draw_obj(img_obj[obj_l], ux -
                        uw*0.5, uy, scale)  # その画像を描画
            if obj_l == 9:  # 海なら
                self.screen.blit(img_sea, [ux-uw*0.5-780, uy])  # その画像を描画
            obj_r = cdata.obr[int(cars[0].y+i) % cdata.CMAX]  # obj_rに右側の物体の番号を代入
            if obj_r == 1:  # 看板なら
                self.draw_obj(img_obj[obj_r], ux +
                        uw*1.3, uy, scale)  # その画像を描画

            for c in range(1, cars.CAR):  # 繰り返しで
                if int(cars[c].y) % cdata.CMAX == int(cars[0].y+i) % cdata.CMAX:  # その板にCOMカーがあるか調べ
                    # プレイヤーから見たCOMカーの向きを計算し
                    lr = int(4*(cars[0].x-cars[c].x)/800)
                    if lr < -3:
                        lr = -3  # -3より小さいなら-3で
                    if lr > 3:
                        lr = 3  # 3より小さいなら3で
                    self.draw_obj(img_car[(c % 3)*7+3+lr], ux+cars[c].x *
                            board.BOARD_W[i]/800, uy, 0.05+board.BOARD_W[i]/board.BOARD_W[0])  # COMカーを描く

            if i == cars[0].PLCAR_Y:  # プレイヤーの車の位置なら
                self.draw_shadow(ux+cars[0].x*board.BOARD_W[i] / 800,
                                        uy, 200*board.BOARD_W[i]/board.BOARD_W[0])  # 車の影を描き
                self.draw_obj(img_car[3+cars[0].lr+cars[0].mycar*7], ux+cars[0].x * board.BOARD_W[i]/800,
                                        uy, 0.05+board.BOARD_W[i]/board.BOARD_W[0])  # プレイヤーの車を描く


def time_str(val):  #**'**.**という時間の文字列を作る関数
    sec = int(val)          #引数を整数の秒数にしてsecに代入
    ms = int((val-sec)*100) #秒数の小数点以下の値をmsに代入
    mi = int(sec/60)        #分をmiに代入
    return "{}'{:02}.{:02}".format(mi, sec%60, ms)  #**'**.**という文字列を返す