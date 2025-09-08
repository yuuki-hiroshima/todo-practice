
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

def refresh_listbox():                                      # 内部のtasksリストをもとに、Listboxの表示を作り直す（ズレ防止のため毎回クリア → 全再描画）
    lst.delete(0, tk.END)                                   # いったん全部消す
    for t in tasks:                                         # タスクを先頭から順に表示
        lst.insert(tk.END, format_item_for_listbox(t))      # 表示用テキストを統一フォーマットで挿入
    status_var.set(f"現在:  len{tasks}件")                   # 件数をステータスに出す


def on_add():                                               # 追加ボタン押下時（またはエンターキー）の処理：入力を検証→追加→保存→再描画
    title = title_var.get()                                 # タイトル文字列を取得
    due = due_var.get()                                     # 期限文字列（空の可能性あり）
    try:
        add_task_core(tasks,title, due)                     # コア関数でtasksを更新（空タイトルは例外）
    except ValueError as e:                                 # ValueErrorを変数"e"に割り当て
        messagebox.showwarning("入力エラー", str(e))          # 空タイトルなどをユーザーに通知
        return                                              # 追加処理を中断
    save_tasks(tasks)                                       # 変更を即保存（クラッシュに強い）
    refresh_listbox()                                       # Listboxの表示を更新
    title_var.set("")                                       # 入力欄をリセット（次の入力に備える）
    due_var.set("")                                         # 期限欄もクリア
    status_var.set("保存しました。")                           # フィードバックを表示

def on_return_key(event):                                   # タイトル欄でEnterをオスロ追加できるようにする（操作が快適になる）
    on_add()                                                # 追加処理を呼ぶ

# ====== イベントの紐づけ ======

btn_add.config(command=on_add)                              # 追加ボタン → on_addを呼ぶ
ent_title.bind("<Return>", on_return_key)                   # タイトル欄でEnterキー → on_addを呼ぶ

# ====== 起動時の初期表示 ======

refresh_listbox()                                           # 最初に一覧を描画

# ====== メインループ開始 ======

root.mainloop()                                             # イベントループ（GUIが動き続けるために必須）