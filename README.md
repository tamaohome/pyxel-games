# pyxel-games

## ゲーム一覧

### [ball_game](https://tamaohome.github.io/pyxel-games/games/ball_game/ball_game.html)

[![ball_game](https://github.com/tamaohome/pyxel-games/blob/main/games/ball_game/ball_game.png?raw=true)](https://tamaohome.github.io/pyxel-games/games/ball_game/ball_game.html)

---

## pyxelによるブラウザゲーム作成手順

### 1. PyCharmで新規プロジェクト作成

例として、PyCharm で `~/MyProject/pyxel-games` にプロジェクトを作成する。

（今回は開発環境としてPyCharmを使用しているが、VSCodeや他エディタでもOK）

### 2. ライブラリを追加

PyCharmウインドウ下部のターミナルを開き、以下のコマンドを実行する。

```sh
pip install pyxel
```

### 3. Python ファイルを追加

以下のコードを `ball_game/main.py` として保存する。

https://github.com/tamaohome/pyxel-games/blob/main/games/ball_game/main.py

### 4. Pyxel アプリケーションファイルに変換

`ball_game` ディレクトリに移動する。

```sh
cd ball_game
```

`pyxel package` コマンドを実行すると `ball_game.pyxapp` が生成される。

```sh
pyxel package . main.py
```

### 5. HTML ファイルに変換

同様に `ball_game` ディレクトリ上で `pyxel app2html` コマンドを実行すると `ball_game.html` が生成される。

```sh
pyxel app2html ball_game.pyxapp
```
