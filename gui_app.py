
# 作成開始日：2025年9月8日
# 作成完了日：2025年9月8日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# --------------------------------
# Custom GPT「GPTs学習パート2」より
# --------------------------------

import tlinter as tk                # Tkinter本体（GUIの基礎部品）
from tkinter import messagebox      # メッセージダイアログ表示用
from service_core import(           # コア関数群をインポート（GUIは入出力だけ担当）
    load_tasks, save_tasks, add_task_core, format_item_for_listbox
)

# ====== アプリ全体の初期化 ======

root = tk.Tk()                          # アプリのウィンドウを作成（Tkは1つだけ）
root.title("ToDoリスト（MVP：表示＋追加）") # ウィンドウスタイル
root.geometry("480x360")                # 初期サイズ（大きすぎない値に）

tasks = load_tasks()                    # 起動時にJSONからタスク一覧を読み込む（リスト[辞書,....]）

title_var = tk.StringVar()              # タイトル用の入力欄。Entryと値を同期させるための器。StringVarでバインドして扱いやすくなる。
due_var = tk.StringVar()                # 期限の入力欄。"YYYY-MM-DD"を受け入れる想定。MVPでもいれておくと既存データと相性がいい

# ====== 画面部品の作成 ======

# ------ 上段：入力フォーム（タイトル＋期限＋追加ボタン） ------

frm_top = tk.Frame(root)                                    # 上段まとめ用のフレーム
frm_top.pack(fill="x", padx=12, pady=8)                     # 横いっぱいに配置し、余白を少し

lbl_title = tk.Label(frm_top, text="タイトル")                # タイトルのラベル
lbl_title.pack(side="left")                                 # 左寄せで配置
ent_title = tk.Entry(frm_top, textvariable=title_var)       # タイトル入力欄（title_varと双方向同期）
ent_title.pack(side="left", padx=6)                         # 余白を入れて横に伸縮

lbl_due = tk.Label(frm_top, text="期限(YYYY-MM-DD)")         # 期限のラベル
lbl_due.pack(side="left")                                   # 左寄せで配置
ent_due = tk.Entry(frm_top,textvariable=due_var, width=14)  # 期限入力欄（任意）
ent_due.pack(side="left", padx=6)                           # 余白を少し

btn_add = tk.Button(frm_top, text="追加", width=8)           # 追加ボタン（クリックでタスクを追加）
btn_add.pack(side="left")                                   # 右側に配置（なのに"left"？）

# ------ 中段：リスト表示 ------

frm_mid = tk.Frame(root)                                    # 中段まとめ用のフレーム
frm_mid.pack(fill="both", expand=True, padx=12, pady=4)     # 余白＋余った領域はここに広げる

scroll = tk.Scrollbar(frm_mid)                              # 縦スクロールバー
scroll.pack(side="right", fill="y")                         # 右端に縦方向いっぱいで配置

lst = tk.Listbox(frm_mid, yscrollcommand=scroll.set)        # タスクリスト（文字列の一覧を表示）
lst.pack(side="left", fill="both", expand=True)             # 余った空間はリストに割り当て
scroll.config(command=lst.yview)                            # スクロールバーとリストの連携

# ------ 下段：ステータス表示 ------

status_var = tk.StringVar()                                 # ステータス文言のためのStringVar
lbl_status = tk.Label(root, textvariable=status_var, anchor="w")    # 左寄せのラベル
lbl_status.pack(fill="x", padx=12, pady=6)                  # 横いっぱいに配置

# ====== 振る舞い（関数群） ======