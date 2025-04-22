import os
import random
import time
import sys
import pygame as pg

WIDTH, HEIGHT = 1100, 650
center_x = 550
center_y = 300

DELTA = {
    pg.K_UP : (0,-5),
    pg.K_DOWN : (0,+5),
    pg.K_LEFT : (-5,0),
    pg.K_RIGHT : (+5,0)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))



def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：タプル判定結果タプル（縦, 横）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:
        yoko = False
    if rct.top <0 or HEIGHT < rct.bottom:
        tate = False
    return yoko, tate

# 演習2(実装中)
# def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
#     bb_accs = [a for a in range(1, 11)]
    
#     for r in range(1, 11):
#         bb_img = pg.Surface((20*r, 20*r))
#         pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)


#gameover実装
def gameover(screen: pg.Surface) -> None:
    loseback_img = pg.Surface((1100,650))
    pg.draw.rect(loseback_img,(0,0,0),(0,0,1100,650))
    pg.Surface.set_alpha(loseback_img, (100))
    # lose文字
    lose_fonto = pg.font.Font(None, 120)
    Gameover_txt = lose_fonto.render("Game Over",True, (255, 255, 255))
    # loseこうかとん
    j_x = 350 # 左右対称用座標
    lose_img = pg.transform.rotozoom(pg.image.load("fig/8.png"),0 ,1)
    loseL_rct = lose_img.get_rect()
    loseR_rct = lose_img.get_rect()
    screen.blit(loseback_img,[0,0]) # 黒画面
    screen.blit(lose_img,[center_x - j_x,center_y]) # L
    screen.blit(lose_img,[center_x + j_x,center_y]) # R
    screen.blit(Gameover_txt, [center_x - 200, center_y])



def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # こうかとん
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    
    # Bomb
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img, (255,0,0), (10,10),10 )
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    bb_img.set_colorkey((0, 0, 0))
    vx, vy = +5, +5

    # 演習2(実装中)
    # bb_imgs, bb_accs = init_bb_imgs()
    # avx = vx*bb_accs[min(tmr//500, 9)]
    # bb_img = bb_imgs[min(tmr//500, 9)]


    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        
        if kk_rct.colliderect(bb_rct):
            print("Game Over")
            gameover(screen)
            pg.display.update()
            time.sleep(5)
            # time.sleep(3)
            return

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]

        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0] # 左右
                sum_mv[1] += mv[1] # 上下

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True): # 画面外だったら
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) # 画面内に戻す
        screen.blit(kk_img, kk_rct)
        bb_rct.move_ip(vx, vy)  # 爆弾の移動
        yoko, tate = check_bound(bb_rct)
        if not yoko:  # 左右出ていたら
             vx *= -1
        if not tate:  # 上下出ていたら
             vy *= -1
        screen.blit(bb_img, bb_rct)  # 爆弾描画
        pg.display.update()
        tmr += 1
        # print("tmr",tmr)
        clock.tick(50)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
