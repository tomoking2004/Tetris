# coding: utf-8
"""システム定数"""

#----------Tetris----------
# フィールドの幅
FIELD_WIDTH = 10
# フィールドの高さ
FIELD_HEIGHT = 20
# プレビューの数
PREVIEW_NUMBER = 6
# プレビューの幅
PREVIEW_WIDTH = 6
# プレビューの高さ
PREVIEW_HEIGHT = 19
# ホールドの幅
HOLD_WIDTH = 6
# ホールドの高さ
HOLD_HEIGHT = 4
# ブロックカラー
BLOCK_COLOR = ["grey20", "cyan", "yellow", "green", "red", "blue", "orange", "purple", "grey40"]
# ブロック座標
BLOCK_LIST = [["座標1", "座標2", "座標3", "座標4"],
            [(FIELD_WIDTH//2-2,0), (FIELD_WIDTH//2-1,0), (FIELD_WIDTH//2,0), (FIELD_WIDTH//2+1,0)],
            [(FIELD_WIDTH//2-1,0), (FIELD_WIDTH//2,0), (FIELD_WIDTH//2-1,1), (FIELD_WIDTH//2,1)],
            [(FIELD_WIDTH//2-1,0), (FIELD_WIDTH//2,0), (FIELD_WIDTH//2-2,1), (FIELD_WIDTH//2-1,1)],
            [(FIELD_WIDTH//2-2,0), (FIELD_WIDTH//2-1,0), (FIELD_WIDTH//2-1,1), (FIELD_WIDTH//2,1)],
            [(FIELD_WIDTH//2-2,0), (FIELD_WIDTH//2-2,1), (FIELD_WIDTH//2-1,1), (FIELD_WIDTH//2,1)],
            [(FIELD_WIDTH//2,0), (FIELD_WIDTH//2-2,1), (FIELD_WIDTH//2-1,1), (FIELD_WIDTH//2,1)],
            [(FIELD_WIDTH//2-1,0), (FIELD_WIDTH//2-2,1), (FIELD_WIDTH//2-1,1), (FIELD_WIDTH//2,1)]]
# ブロック情報
BLOCK_INFO = [("原点x", "原点y", "回転範囲"),
            (FIELD_WIDTH//2-2, -1, 4),
            (FIELD_WIDTH//2-1, 0, 2),
            (FIELD_WIDTH//2-2, 0, 3),
            (FIELD_WIDTH//2-2, 0, 3),
            (FIELD_WIDTH//2-2, 0, 3),
            (FIELD_WIDTH//2-2, 0, 3),
            (FIELD_WIDTH//2-2, 0, 3)]
# 時間制限(sec)
LIMIT = 1000
# 落下速度(ms)
SPEED = 800#
#----------GUI----------
# キャンバスの幅
CANVAS_WIDTH = 780
# キャンバスの高さ
CANVAS_HEIGHT = 660
# キャンバスの色
CANVAS_COLOR = "grey10"
# フィールドの位置(x)
FIELD_X = 240
# フィールドの位置(y)
FIELD_Y = 30
# プレビューの位置(x)
PREVIEW_X = 570
# プレビューの位置(y)
PREVIEW_Y = 60
# ホールドの位置(x)
HOLD_X = 30
# ホールドの位置(y)
HOLD_Y = 60
# マスのサイズ
BLOCK_SIZE = 30
