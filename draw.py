import pygame

WHITE = (255, 255, 255) #色の定義(白)
BLACK = (0, 0, 0)       #色の定義(黒)
RED = (255, 0, 0)       #色の定義(赤)
YELLOW = (255, 224, 0)  #色の定義(黄)
GREEN = (0, 255, 0)     #色の定義(緑)

def draw_obj(bg, img, x, y, sc):    #座標とスケールを受け取り、物体を描く関数
    img_rz = pygame.transform.rotozoom(img, 0, sc)  #拡大縮小した画像を作る
    w = img_rz.get_width()          #その画像の幅をwに代入
    h = img_rz.get_height()         #その画像の高さをhに代入
    bg.blit(img_rz, [x-w/2, y-h])   #画像を描く


def draw_shadow(bg, x, y, siz): #影を表示する関数
    shadow = pygame.Surface([siz, siz/4])   #描画面(サーフェイス)を用意する
    shadow.fill(RED)            #その描画面を赤で塗り潰す
    shadow.set_colorkey(RED)    #描画面の透過色を指定
    shadow.set_alpha(128)       #描画面の透明度を設定
    pygame.draw.ellipse(shadow, BLACK, [0, 0, siz, siz/4])  #描画面に黒で楕円を描く
    bg.blit(shadow, [x-siz/2, y-siz/4]) #楕円を描いた描画面をゲーム画面に転送


        
def draw_text(scrn, txt, x, y, col, fnt):   #影付きの文字列を表示する関数
    sur = fnt.render(txt, True, BLACK)  #黒で文字列を描いたサーフェイスを生成
    x -= sur.get_width()/2  #センタリングするためX座標を計算
    y -= sur.get_height()/2 #センタリングするためY座標を計算
    scrn.blit(sur, [x+2, y+2])  #サーフェイスを画面に転送
    sur = fnt.render(txt, True, col)    #指定色で文字列を描いたサーフェイスを生成
    scrn.blit(sur, [x, y])  #サーフェイスを画面に転送