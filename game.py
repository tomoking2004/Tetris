# coding: utf-8
import random, copy
import tkinter as tk
import tkinter.messagebox as ms

from config import *


class Tetris:
    """ゲームシステム"""

    def __init__(self, gui):
        # ゲーム環境変数
        self.gui = gui
        self.field = [[0 for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)] #フィールド状態
        self.learn_field = [[0 for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)] #学習用フィールド状態
        self.preview = [[0 for x in range(PREVIEW_WIDTH)] for y in range(PREVIEW_HEIGHT)] #プレビュー状態
        self.holding = [[0 for x in range(HOLD_WIDTH)] for y in range(HOLD_HEIGHT)] #ホルディング状態
        self.block_code = [None] #ブロックコード
        self.block_list = [None] #ブロック座標
        self.block_info = [None] #ブロック情報
        self.hold_block_code = None #ホールドブロックコード
        self.hold_block_list = None #ホールドブロック座標
        self.hold_block_info = None #ホールドブロック情報
        self.loop = False #ゲーム進行
        self.holdable = True #ホールド可否
        self.level = 0 #レベル
        self.limit = LIMIT #残り時間
        self.score = 0 #スコア
        self.lines = 0 #ライン
        self.spin = False #設置直前スピンの有無
        self.combo = 0 #コンボ数
        self.lock_down = 0 #連続操作回数
        # 実行関数
        self.make_cycle()
        self.make_preview()

    def auto_start(self):
        """自動でゲームを起動する"""
        self.loop = True
        self.gui.title("Tetris")
        self.limiter()
        self.game()

    def limiter(self):
        """残り時間を刻んでいく"""
        if self.loop:
            if self.limit > 0: #時間以内
                self.limit -= 1
                self.gui.label_update()
            else: #時間切れ
                self.finish()
            self.gui.after(1000, self.limiter)

    def game(self):
        """ゲームを進行する"""
        if self.loop:
            self.lock_down = 0
            direction = (0,1)
            if self.block_code[0] is None: #発生
                self.spawn_block()
            elif self.movable(direction): #自由落下
                self.move_block(direction)
            elif self.spawnable(): #列破壊＆発生
                self.crush_line()
                self.spawn_block()
            else: #列破壊＆終了
                self.finish()
            self.game_timer = self.gui.after(500, self.game)

    def reset_game_timer(self):
        """ゲームタイマーをリセットする"""
        self.lock_down += 1
        if self.lock_down==15: #強制的に設置
            direction = (0,1)
            while self.movable(direction):
                self.move_block(direction)
            print("Lock Down")
        if self.lock_down<=15: #タイマーリセット
            self.gui.after_cancel(self.game_timer)
            self.game_timer = self.gui.after(500, self.game)

    def spawnable(self):
        """発生可能か判定する"""
        for x,y in self.block_list[1]:
            if self.field[y][x]!=0: #ブロック隣接
                return False
        return True

    def spawn_block(self):
        """ランダムなブロックを発生させる"""
        # 更新
        del self.block_code[0]
        del self.block_list[0]
        del self.block_info[0]
        if len(self.block_code)==PREVIEW_NUMBER:
            self.make_cycle()
        # 発生
        for x,y in self.block_list[0]:
            self.field[y][x] = self.block_code[0]
        # 候補発生
        self.make_preview()
        # 画面更新
        self.gui.canvas_update()

    def make_cycle(self):
        """候補の一周期を生成する"""
        cycle = [n for n in range(1,8)]
        random.shuffle(cycle)
        for code in cycle:
            self.block_code.append(code)
            self.block_list.append(copy.deepcopy(BLOCK_LIST[code]))
            self.block_info.append(copy.deepcopy(BLOCK_INFO[code]))

    def make_learn_field(self):
        """学習用フィールドを作成する"""
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.field[y][x]==0: #空ブロック
                    self.learn_field[y][x] = 0
                elif self.block_list[0] is not None and (x,y) in self.block_list[0]: #移動ブロック
                    self.learn_field[y][x] = 1
                else: #停止ブロック
                    self.learn_field[y][x] = 2

    def make_preview(self):
        """プレビューを作成する"""
        # 初期化
        for y in range(PREVIEW_HEIGHT):
            for x in range(PREVIEW_WIDTH):
                self.preview[y][x] = 0
        # 発生
        for i in range(PREVIEW_NUMBER):
            ox,oy,_ = self.block_info[i+1]
            for x,y in self.block_list[i+1]:
                self.preview[y-oy+i*3+1][x-ox+1] = self.block_code[i+1]

    def make_holding(self):
        """ホルディングを作成する"""
        # 初期化
        for y in range(HOLD_HEIGHT):
            for x in range(HOLD_WIDTH):
                self.holding[y][x] = 0
        # 発生
        ox,oy,_ = self.hold_block_info
        for x,y in self.hold_block_list:
            self.holding[y-oy+1][x-ox+1] = self.hold_block_code

    def movable(self, direction):
        """ブロックが可動か判定する"""
        dx,dy = direction
        for x,y in self.block_list[0]:
            if (x+dx,y+dy) in self.block_list[0]: #自身のブロック隣接
                continue
            if not(0<=x+dx<FIELD_WIDTH and 0<=y+dy<FIELD_HEIGHT): #場外
                return False
            if self.field[y+dy][x+dx]!=0: #ブロック隣接
                return False
        return True

    def move_block(self, direction):
        """ブロックを動かす"""
        self.spin = False
        dx,dy = direction
        # 消す
        for x,y in self.block_list[0]:
            self.field[y][x] = 0
        # 座標を更新
        ox,oy,_ = self.block_info[0]
        self.block_info[0] = ox+dx,oy+dy,_
        for i in range(len(self.block_list[0])):
            x,y = self.block_list[0][i]
            self.block_list[0][i] = x+dx,y+dy
        # 発生
        for x,y in self.block_list[0]:
            self.field[y][x] = self.block_code[0]
        # 画面更新
        self.gui.canvas_update()

    def fallpoint(self):
        """落下地点の座標を返す"""
        dy = 0
        while self.movable((0, dy+1)):
            dy += 1
        new_block_list = []
        for x,y in self.block_list[0]:
            if (x, y+dy) in self.block_list[0]:
                continue
            new_block_list.append((x, y+dy))
        return new_block_list

    def rotate_coordinates(self, direction):
        """ブロックを90°回転したときの座標を返す"""
        ox,oy,size = self.block_info[0]
        new_block_list = []
        for x,y in self.block_list[0]:
            x -= ox; y-= oy
            if direction=="left":
                _x,_y = y,size-x-1
            else:
                _x,_y = size-y-1,x
            new_block_list.append((_x+ox,_y+oy))
        return new_block_list

    def rotatable(self, direction):
        """ブロックが回転可能か判定する"""
        for _x,_y in self.rotate_coordinates(direction):
            if (_x,_y) in self.block_list[0]: #自身のブロック隣接
                continue
            if not(0<=_x<FIELD_WIDTH and 0<=_y<FIELD_HEIGHT): #場外
                return False
            if self.field[_y][_x]!=0: #ブロック隣接
                return False
        return True
    
    def rotate_block(self, direction):
        """ブロックを回転する"""
        self.spin = True
        # 消す
        for x,y in self.block_list[0]:
            self.field[y][x] = 0
        # 座標を更新
        self.block_list[0] = self.rotate_coordinates(direction)
        # 発生
        for x,y in self.block_list[0]:
            self.field[y][x] = self.block_code[0]
        # 画面更新
        self.gui.canvas_update()

    def hold_block(self):
        """ブロックを保留/交換する"""
        self.holdable = False
        # 消す
        for x,y in self.block_list[0]:
            self.field[y][x] = 0
        # 交換
        block_code = self.block_code[0]
        self.block_code[0] = self.hold_block_code
        self.block_list[0] = self.hold_block_list
        self.block_info[0] = self.hold_block_info
        self.hold_block_code = block_code
        self.hold_block_list = copy.deepcopy(BLOCK_LIST[block_code])
        self.hold_block_info = copy.deepcopy(BLOCK_INFO[block_code])
        # 発生
        if self.block_code[0] is not None:
            for x,y in self.block_list[0]:
                self.field[y][x] = self.block_code[0]
        # 保留発生
        self.make_holding()
        # 画面更新
        self.gui.label_update()
        self.gui.canvas_update()

    def crush_line(self):
        """揃った列を破壊する"""
        # TSpin判定
        tspin = 0
        if self.spin and self.block_code[0]==7:
            ox,oy,size = self.block_info[0]
            cx,cy = ox+size//2, oy+size//2
            for dx,dy in [(-1,-1), (1,-1), (-1,1), (1,1)]:
                if self.field[cy+dy][cx+dx]!=0:
                    tspin += 1
        # ライン消し
        lines = 0
        for y in range(FIELD_HEIGHT):
            if 0 not in self.field[y]:
                lines += 1
                del self.field[y]
                self.field = [[0 for _ in range(FIELD_WIDTH)]] + self.field
        # Perfect Clear判定
        perfect_clear = True
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                if self.field[y][x]!=0:
                    perfect_clear = False
        # テクニックボーナス
        if lines>0:
            self.combo += 1
            if self.combo>1:
                self.score += 100 * self.combo* (self.level+1)
                print("{} Combo".format(self.combo-1))
        else:
            self.combo = 0
        if lines==4:
            print("Tetris")
        if tspin==2:
            self.score += 400 * (self.level+1)
            print("TSpin Mini")
        if tspin==3:
            if lines==1:
                self.score += 900 * (self.level+1)
                print("TSpin Single")
            if lines==2:
                self.score += 1600 * (self.level+1)
                print("TSpin Double")
            if lines==3:
                self.score += 2500 * (self.level+1)
                print("TSpin Triple")
        if perfect_clear:
            self.score += 3600 * (self.level+1)
            print("Perfect Clear")
        # 基本ステータス更新
        self.score += 100 * lines * lines * (self.level+1)
        self.lines += lines
        self.level = self.lines//10
        self.holdable = True
        # 画面更新
        self.gui.label_update()
        self.gui.canvas_update()

    def finish(self):
        """最後の処理をする"""
        self.loop = False
        self.crush_line()
        self.gui.show_result()
        self.gui.restart_ask()

    def restart(self):
        """ゲームを再起動する"""
        self.__init__(self.gui)
        self.gui.canvas_update()

    # コントローラー
    def rotate_left(self):
        """可能であれば左に回転する"""
        direction = "left"
        if self.loop and self.lock_down<15 and self.rotatable(direction):
            self.rotate_block(direction)
            self.reset_game_timer()

    def rotate_right(self):
        """可能であれば右に回転する"""
        direction = "right"
        if self.loop and self.lock_down<15 and self.rotatable(direction):
            self.rotate_block(direction)
            self.reset_game_timer()

    def hold(self):
        """可能であればブロックを保留する"""
        if self.loop and self.lock_down<15 and self.holdable:
            self.hold_block()
            self.reset_game_timer()

    def move_down(self):
        """可能であれば下に動かす"""
        direction = (0, 1)
        if self.loop and self.lock_down<15 and self.movable(direction):
            self.move_block(direction)
            self.score += 10
            self.reset_game_timer()
            self.gui.label_update()

    def move_left(self):
        """可能であれば左に動かす"""
        direction = (-1, 0)
        if self.loop and self.lock_down<15 and self.movable(direction):
            self.move_block(direction)
            self.reset_game_timer()

    def move_right(self):
        """可能であれば右に動かす"""
        direction = (1, 0)
        if self.loop and self.lock_down<15 and self.movable(direction):
            self.move_block(direction)
            self.reset_game_timer()

    def move_most_down(self):
        """可能であれば最下に動かす"""
        direction = (0, 1)
        while self.loop and self.lock_down<15 and self.movable(direction):
            self.move_block(direction)
            self.score += 10
            self.gui.label_update()
            if self.movable(direction)==False:
                self.reset_game_timer()

    def pause(self):
        """ゲームを開始/中断/再開する"""
        if self.loop:
            self.loop = False
            self.gui.title("Tetris(Pause)")
        else:
            self.auto_start()


class GUI(tk.Tk):
    """グラフィカル・ユーザ・インターフェース"""

    def __init__(self, tetris):
        super().__init__()
        # GUI変数
        self.tetris = tetris #ゲームシステム
        self.canvas = tk.Canvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_COLOR, highlightthickness=0) #キャンバス
        self.coordinates = [[(FIELD_X+BLOCK_SIZE*x, FIELD_Y+BLOCK_SIZE*y) 
                        for x in range(FIELD_WIDTH)] for y in range(FIELD_HEIGHT)] #フィールド座標
        self.coordinates2 = [[(PREVIEW_X+BLOCK_SIZE*x, PREVIEW_Y+BLOCK_SIZE*y)
                        for x in range(PREVIEW_WIDTH)] for y in range(PREVIEW_HEIGHT)] #プレビュー座標
        self.coordinates3 = [[(HOLD_X+BLOCK_SIZE*x, HOLD_Y+BLOCK_SIZE*y)
                        for x in range(HOLD_WIDTH)] for y in range(HOLD_HEIGHT)] #ホールド座標
        self.holdable = tk.StringVar()
        self.limit = tk.StringVar()
        self.score = tk.StringVar()
        self.lines = tk.StringVar()
        self.level = tk.StringVar()
        # 実行関数
        self.settings()

    def settings(self):
        """初期設定をする"""
        self.canvas.pack()
        self.label_update()
        self.canvas_update()
        self.bind("<Button-1>", self.rotate_left)
        self.bind("<Button-2>", self.rotate_right)
        self.bind("<Button-3>", self.hold)
        self.bind("<Down>", self.move_down)
        self.bind("<Left>", self.move_left)
        self.bind("<Right>", self.move_right)
        self.bind("<Return>", self.move_most_down)
        self.bind("<space>", self.pause)
        self.title("Tetris(Press space to start.)")
        tk.Label(self.canvas, text="NEXT BLOCK", bg=CANVAS_COLOR, fg="grey70").place(x=605, y=30)
        tk.Label(self.canvas, text="HOLD BLOCK", bg=CANVAS_COLOR, fg="grey70").place(x=75, y=30)
        tk.Label(self.canvas, textvariable=self.holdable, bg=CANVAS_COLOR, fg="grey70").place(x=70, y=185)
        tk.Label(self.canvas, textvariable=self.level, bg=CANVAS_COLOR, fg="grey90").place(x=85, y=240)
        tk.Label(self.canvas, textvariable=self.limit, bg=CANVAS_COLOR, fg="grey90").place(x=85, y=270)
        tk.Label(self.canvas, textvariable=self.score, bg=CANVAS_COLOR, fg="grey90").place(x=85, y=300)
        tk.Label(self.canvas, textvariable=self.lines, bg=CANVAS_COLOR, fg="grey90").place(x=85, y=330)

    def canvas_update(self):
        """キャンバスを更新する"""
        # 消去
        self.canvas.delete("canvas")
        # フィールド更新
        for y in range(FIELD_HEIGHT):
            for x in range(FIELD_WIDTH):
                _x,_y = self.coordinates[y][x]
                code = self.tetris.field[y][x]
                fill = BLOCK_COLOR[code]
                self.canvas.create_rectangle(_x,_y,_x+BLOCK_SIZE,_y+BLOCK_SIZE,fill=fill,tag="canvas")
        # プレビュー更新
        for y in range(PREVIEW_HEIGHT):
            for x in range(PREVIEW_WIDTH):
                _x,_y = self.coordinates2[y][x]
                code = self.tetris.preview[y][x]
                fill = BLOCK_COLOR[code] if code else CANVAS_COLOR
                width = 1 if code else 0
                self.canvas.create_rectangle(_x,_y,_x+BLOCK_SIZE,_y+BLOCK_SIZE,fill=fill,width=width,tag="canvas")
        # ホールド更新
        for y in range(HOLD_HEIGHT):
            for x in range(HOLD_WIDTH):
                _x,_y = self.coordinates3[y][x]
                code = self.tetris.holding[y][x]
                fill = BLOCK_COLOR[code]
                width = 1 if code else 0
                self.canvas.create_rectangle(_x,_y,_x+BLOCK_SIZE,_y+BLOCK_SIZE,fill=fill,width=width,tag="canvas")
        # ゴースト更新
        if self.tetris.block_code[0] is not None:
            for x,y in self.tetris.fallpoint():
                _x,_y = self.coordinates[y][x]
                fill = BLOCK_COLOR[-1]
                self.canvas.create_rectangle(_x,_y,_x+BLOCK_SIZE,_y+BLOCK_SIZE,fill=fill,tag="canvas")
    
    def label_update(self):
        """ラベルを更新する"""
        self.holdable.set("holdable: {}".format(self.tetris.holdable))
        self.level.set("level: {}".format(self.tetris.level))
        self.limit.set("time: {}".format(self.tetris.limit))
        self.score.set("score: {}".format(self.tetris.score))
        self.lines.set("lines: {}".format(self.tetris.lines))

    def on_field(self, event):
        """マウスがフィールド上にあるか判定する"""
        if FIELD_X<=event.x<=FIELD_X+BLOCK_SIZE*FIELD_WIDTH and FIELD_Y<=event.y<=FIELD_Y+BLOCK_SIZE*FIELD_HEIGHT:
            return True
        return False

    def show_result(self):
        """結果を表示する"""
        ms.showinfo("System", "Your Score is {}".format(self.tetris.score))

    def restart_ask(self):
        """もう一度プレイするか尋ねる"""
        ans = ms.askyesno("System", "Do you try again？")
        if ans: self.after(10, self.tetris.restart)

    # コントローラー
    def rotate_left(self, event):
        if self.on_field(event):
            self.tetris.rotate_left()

    def rotate_right(self, event):
        if self.on_field(event):
            self.tetris.rotate_right()

    def hold(self, event):
        if self.on_field(event):
            self.tetris.hold()

    def move_down(self, event):
        self.tetris.move_down()

    def move_left(self, event):
        self.tetris.move_left()

    def move_right(self, event):
        self.tetris.move_right()

    def move_most_down(self, event):
        self.tetris.move_most_down()

    def pause(self, event):
        self.tetris.pause()

