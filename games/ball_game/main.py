import pyxel
import random
import math

# 画面解像度
SCREEN_WIDTH, SCREEN_HEIGHT = 160, 120

# 画面タイトル
TITLE = "Ball Game"

class Game:
    def __init__(self):
        """ゲームの初期化"""
        # 画面サイズとタイトルを設定
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE)

        pyxel.mouse(True)  # マウスカーソルを表示

        # ボールの初期位置、半径
        self.ball_x = SCREEN_WIDTH // 2
        self.ball_y = SCREEN_HEIGHT // 2
        self.ball_r = 5

        # Pyxelの実行開始
        pyxel.run(self.update, self.draw)

    def update(self):
        """ゲームロジックの更新"""
        # 画面クリック発生かつカーソルがボールに接触する場合
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and self.is_mouse_on_ball():
            # ボールを移動
            self.move_ball_randomly()

    def draw(self):
        """描画処理"""
        # 画面をクリア
        pyxel.cls(7)

        # ボールを描画
        pyxel.circ(self.ball_x, self.ball_y, self.ball_r, 1)

        # プレイヤー座標を表示
        player_pos_text = f"PLAYER: ({pyxel.mouse_x}, {pyxel.mouse_y})"
        pyxel.text(5, 5, player_pos_text, 5)

        # ボールの座標を表示
        player_pos_text = f"BALL: ({pyxel.mouse_x}, {pyxel.mouse_y})"
        pyxel.text(5, 15, player_pos_text, 5)

    def is_mouse_on_ball(self):
        """カーソルがボールに接触する場合は True を返す"""
        dx = pyxel.mouse_x - self.ball_x
        dy = pyxel.mouse_y - self.ball_y
        distance = math.hypot(dx, dy)
        return distance <= self.ball_r

    def move_ball_randomly(self):
        """ボールをランダムな位置に移動する"""
        self.ball_x = random.randint(self.ball_r, SCREEN_WIDTH - self.ball_r)
        self.ball_y = random.randint(self.ball_r, SCREEN_HEIGHT - self.ball_r)


if __name__ == "__main__":
    Game()
