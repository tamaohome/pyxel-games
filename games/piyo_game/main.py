import pyxel
import random
import math

SCREEN_WIDTH, SCREEN_HEIGHT = 160, 160  # 画面解像度
SCREEN_SCALE = 2  # 画面の拡大率
TITLE = "piyo game"  # 画面タイトル
GROUND_HEIGHT = 40  # 地面の高さ
SCROLL_SPEED = 1  # スクロール速度
GRAVITY = 0.5  # 重力


class Piyo:
    """ヒヨコ（自機）のクラス"""

    # 初期設定
    WIDTH = 8
    HEIGHT = 8
    INITIAL_X = 40
    JUMP_POWER = 8

    # 地面の位置（ヒヨコの初期Y座標）
    INITIAL_Y = SCREEN_HEIGHT - GROUND_HEIGHT - HEIGHT

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.is_jumping = False

    def update(self):
        """位置を更新"""
        # 重力の適用
        self.vy += GRAVITY
        self.y += self.vy

        # 地面との衝突判定
        if self.y > self.INITIAL_Y:
            self.y = self.INITIAL_Y
            self.vy = 0
            self.is_jumping = False

    def jump(self):
        """ジャンプする"""
        self.vy = -self.JUMP_POWER
        self.is_jumping = True

    def check_ground(self):
        """地面に接しているか判定"""
        return self.y >= self.INITIAL_Y

    def draw(self):
        """ヒヨコを描画"""
        pyxel.rect(self.x, self.y, self.WIDTH, self.HEIGHT, 10)  # 体
        pyxel.pset(self.x + 6, self.y + 2, 0)  # 目
        pyxel.rect(self.x + 7, self.y + 4, 2, 2, 9)  # くちばし


class Karasu:
    """カラス（敵キャラ）のクラス"""

    # 初期設定
    WIDTH = 12
    HEIGHT = 8
    BASE_SPEED = 1.0

    def __init__(self, x, y, speed=None):
        self.x = x
        self.y = y
        # speedが指定されなければランダムな速度を設定
        if speed is None:
            self.speed = self.BASE_SPEED * (
                1 + random.random() * 0.75
            )  # 速度にばらつきを持たせる
        else:
            self.speed = speed

    def update(self, scroll_speed):
        """カラスの位置を更新"""
        self.x -= scroll_speed + self.speed

    def is_visible(self, scroll_x):
        """画面内に表示されているか判定"""
        rel_x = self.x - scroll_x
        # カラスの右端が画面内にあるか、または左端が画面内にある場合は表示
        return (rel_x + self.WIDTH > 0) and (rel_x < SCREEN_WIDTH)

    def check_collision(self, piyo, scroll_x):
        """ヒヨコとの衝突判定"""
        rel_x = self.x - scroll_x
        return (
            piyo.x + piyo.WIDTH > rel_x
            and piyo.x < rel_x + self.WIDTH
            and piyo.y + piyo.HEIGHT > self.y
            and piyo.y < self.y + self.HEIGHT
        )

    def draw(self, scroll_x):
        """カラスを描画"""
        rel_x = self.x - scroll_x
        if not self.is_visible(scroll_x):
            return

        pyxel.rect(rel_x, self.y, self.WIDTH, self.HEIGHT, 0)  # 体
        pyxel.tri(
            rel_x, self.y + 4, rel_x - 4, self.y + 6, rel_x, self.y + 7, 9
        )  # くちばし
        pyxel.pset(rel_x + 2, self.y + 2, 7)  # 目

        # 羽のアニメーション
        wing_pos = abs(math.sin(pyxel.frame_count * 0.2) * 3)
        pyxel.rect(rel_x + 2, self.y + self.HEIGHT, 8, wing_pos, 0)


class Terrain:
    """地形クラス"""

    def __init__(self, height):
        self.height = height  # 地面の高さ

    def draw(self, scroll_x):
        """地形を描画"""
        # 地面の描画
        pyxel.rect(0, SCREEN_HEIGHT - self.height, SCREEN_WIDTH, self.height, 3)


class Game:
    def __init__(self):
        """ゲームの初期化"""
        # 画面サイズとタイトルを設定
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=TITLE, display_scale=SCREEN_SCALE)

        # ゲーム変数の初期化
        self.reset_game()

        # Pyxelの実行開始
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        """ゲーム状態のリセット"""
        self.piyo = Piyo(Piyo.INITIAL_X, Piyo.INITIAL_Y)  # 自機（ヒヨコ）の位置と速度
        self.terrain = Terrain(GROUND_HEIGHT)  # 地形

        self.scroll_x = 0  # スクロール位置
        self.score = 0  # スコア
        self.game_over = False  # ゲームオーバーフラグ
        self.enemies = []  # 敵キャラ（カラス）のリスト
        self.next_crow = random.randint(5, 40)  # 次のカラスを生成するタイミング

    def update(self):
        """ゲームロジックの更新"""
        # ESCキーでゲーム終了
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()

        # ゲームオーバー時はRキーでリスタート
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # スコア更新
        self.score += 1

        # 左クリックでジャンプ（空中でもジャンプ可能）
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.piyo.jump()

        # ヒヨコの位置更新
        self.piyo.update()

        # スクロール更新
        self.scroll_x += SCROLL_SPEED

        # カラスの生成
        if self.scroll_x > self.next_crow:
            crow_y = random.randint(20, SCREEN_HEIGHT - GROUND_HEIGHT - 30)
            self.enemies.append(Karasu(self.scroll_x + SCREEN_WIDTH, crow_y))
            self.next_crow = self.scroll_x + random.randint(200, 350)

        # カラスの更新と削除
        i = 0
        while i < len(self.enemies):
            crow = self.enemies[i]

            # カラスを移動（プレイヤーより少し速く左に移動）
            crow.update(SCROLL_SPEED)

            # 画面外に出たカラスを削除
            if not crow.is_visible(self.scroll_x):
                self.enemies.pop(i)
            else:
                # カラスとの衝突判定
                if crow.check_collision(self.piyo, self.scroll_x):
                    self.game_over = True

                i += 1

    def draw(self):
        """描画処理"""
        # 画面をクリア
        pyxel.cls(7)

        # 背景の描画
        for i in range(16):
            cloud_x = (i * 80 - (self.scroll_x // 2) % 80) - 40
            pyxel.circ(cloud_x, 40, 15, 6)
            pyxel.circ(cloud_x + 10, 35, 10, 6)
            pyxel.circ(cloud_x - 10, 35, 10, 6)

        # 地形の描画
        self.terrain.draw(self.scroll_x)

        # カラスの描画
        for crow in self.enemies:
            crow.draw(self.scroll_x)

        # 自機（ヒヨコ）の描画
        self.piyo.draw()

        # スコア表示
        pyxel.text(5, 5, f"SCORE: {self.score}", 0)

        # ゲームオーバー表示
        if self.game_over:
            pyxel.text(SCREEN_WIDTH // 2 - 30, SCREEN_HEIGHT // 2, "GAME OVER", 8)
            pyxel.text(
                SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT // 2 + 10, "PRESS R TO RESTART", 8
            )


if __name__ == "__main__":
    Game()
