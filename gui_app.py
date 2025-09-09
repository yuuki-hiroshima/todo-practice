
# 作成開始日：2025年9月8日
# 作成完了日：2025年9月8日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# --------------------------------
# Custom GPT「GPTs学習パート2」より
# --------------------------------

# service_core.pyがコアファイル

# --------------------------------

# 更新情報
# リストに番号を表示
# 削除ボタン実装
# 完了切替機能を実装
# 編集機能を実装
# 表示切替（フィルタ）機能を実装

# --------------------------------

import tkinter as tk                # Tkinter本体（GUIの基礎部品）
from tkinter import messagebox      # メッセージダイアログ表示用
from tkinter import simpledialog    # 追加：簡易入力ダイアログで編集時に使う
from service_core import(           # コア関数群をインポート（GUIは入出力だけ担当）
    load_tasks, save_tasks, add_task_core, remove_task_core, format_item_for_listbox, toggle_done_core, edit_task_core  # service_core.py（クラス）で作成した関数を必要医応じて追加
)

# ====== アプリ全体の初期化 ======

root = tk.Tk()                          # アプリのウィンドウを作成（Tkは1つだけ）
root.title("ToDoリスト（MVP：表示+追加）") # ウィンドウスタイル
root.geometry("520x420")                # 初期サイズ（大きすぎない値に）

tasks = load_tasks()                    # 起動時にJSONからタスク一覧を読み込む（リスト[辞書,....]）
view_indices: list[int] = []            # 追加：Listboxの行番号 →　tasksのインデックスを対応付けるリスト（変数名の理由：画面に「どのタスクをどの順番で見せているか」を覚えるための"地図"）

title_var = tk.StringVar()              # タイトル用の入力欄。Entryと値を同期させるための器。StringVarでバインドして扱いやすくなる。
due_var = tk.StringVar()                # 期限の入力欄。"YYYY-MM-DD"を受け入れる想定。MVPでもいれておくと既存データと相性がいい

FILTER_ALL = "all"                      # 追加：フィルタ定数（全部）
FILTER_UNDONE = "undone"                # 追加：フィルタ定数（未完のみ）
FILTER_DONE = "done"                    # 追加：フィルタ定数（完了のみ）
filter_var = tk.StringVar(value=FILTER_ALL) # 追加：現在の表示モードを保持

# ====== 画面部品の作成 ======

# ------ 上段：入力フォーム（タイトル＋期限＋追加ボタン） ------

frm_top = tk.Frame(root)                                    # 上段まとめ用のフレーム
frm_top.pack(fill="x", padx=12, pady=8)                     # 横いっぱいに配置し、余白を少し

lbl_title = tk.Label(frm_top, text="タイトル")                # タイトルのラベル
lbl_title.pack(side="left")                                 # 左寄せで配置
ent_title = tk.Entry(frm_top, textvariable=title_var)       # タイトル入力欄（title_varと双方向同期）
ent_title.pack(side="left", fill="x", expand=True, padx=6)  # 余白を入れて横に伸縮

lbl_due = tk.Label(frm_top, text="期限(YYYY-MM-DD)")         # 期限のラベル
lbl_due.pack(side="left")                                   # 左寄せで配置
ent_due = tk.Entry(frm_top,textvariable=due_var, width=14)  # 期限入力欄（任意）
ent_due.pack(side="left", padx=6)                           # 余白を少し

btn_add = tk.Button(frm_top, text="追加", width=8)           # 追加ボタン（クリックでタスクを追加）
btn_add.pack(side="left")                                   # 右側に配置（なのに"left"？）

# ------ 中段：リスト表示 ------

frm_mid = tk.Frame(root)                                    # 中段まとめ用のフレーム
frm_mid.pack(fill="both", expand=True, padx=12, pady=4)     # 余白＋余った領域はここに広げる

frm_filter = tk.Frame(root)                                 # 追加：フィルタ切替エリア
frm_filter.pack(fill="x", padx=12, pady=(0, 6))             # 追加：リストの直上に薄く余白を入れて配置
rb_all = tk.Radiobutton(frm_filter, text="全部", value=FILTER_ALL, variable=filter_var)
rb_undone = tk.Radiobutton(frm_filter, text="未完のみ", value=FILTER_UNDONE, variable=filter_var)
rb_done = tk.Radiobutton(frm_filter, text="完了のみ", value=FILTER_DONE, variable=filter_var)
rb_all.pack(side="left")
rb_undone.pack(side="left", padx=8)
rb_done.pack(side="left")

scroll = tk.Scrollbar(frm_mid)                              # 縦スクロールバー
scroll.pack(side="right", fill="y")                         # 右端に縦方向いっぱいで配置

lst = tk.Listbox(frm_mid, yscrollcommand=scroll.set)        # タスクリスト（文字列の一覧を表示）
lst.pack(side="left", fill="both", expand=True)             # 余った空間はリストに割り当て
scroll.config(command=lst.yview)                            # スクロールバーとリストの連携

# ------ 下段：ステータス表示 ------

frm_bottom = tk.Frame(root)                                 # 追加：操作ボタン＋ステータスをまとめる枠
frm_bottom.pack(fill="x", padx=12, pady=8)                  # 横いっぱい＋余白

btn_delete = tk.Button(frm_bottom, text="削除", width=10)    # 追加：削除実行ボタン
btn_delete.pack(side="left")                                # 左寄せ（よく使う操作は左に置くと目に入りやすい）

btn_toggle = tk.Button(frm_bottom, text="完了切替", width=10)   # 追加：完了/未完トグルボタン
btn_toggle.pack(side="left", padx=8)                        # 左寄せ＋少し余白（削除の隣に）

btn_edit = tk.Button(frm_bottom, text="編集", width=10)      # 追加：編集ボタン（タイトル/期限）
btn_edit.pack(side="left", padx=8)                          # 追加：完了切替の隣に配置

status_var = tk.StringVar()                                 # ステータス表示用の可変文字（件数/保存完了など）
lbl_status = tk.Label(root, textvariable=status_var, anchor="w")    # 左寄せのラベル
lbl_status.pack(side="left", padx=12)                       # ボタンとラベルの間に余白

# ====== 振る舞い（関数群） ======

# ------ 表示の再構築（ズレを防止するため毎回全クリア → 全挿入） ------

def refresh_listbox():                                      # 内部のtasksリストをもとに、Listboxの表示を作り直す（ズレ防止のため毎回クリア → 全再描画）
    lst.delete(0, tk.END)                                   # いったん全部消す
    view_indices.clear()                                    # 追加：地図もいったん空にする
    for i, t in enumerate(tasks):                           # 変更：タスクを先頭から順に表示
        human_index = i + 1                                 # 追加：人間向けは1始まりの番号にする
        text = f"{human_index}. {format_item_for_listbox(t)}"   # 追加：例/ human_index=2, t="買い物" → "2. 買い物" のようになります。
        lst.insert(tk.END, text)                            # 変更：Listboxに1行ずつ追加
        view_indices.append(i)                              # 追加：「この行はtasksのi番目」と記録
    status_var.set(f"現在:  {len(tasks)}件")                 # 件数をステータスに出す
    
    lst.delete(0, tk.END)                                   # 追加：表示をいったん全クリア
    view_indices.clear()                                    # 追加：行 → tasks の対応表もリセット
    mode = filter_var.get()                                 # 追加：現在の表示モードを取得（all/undone/done）
    visible_count = 0                                       # 追加：画面に出した件数カウント（ステータス表示用）
    for i, t in enumerate(tasks):                           # 追加：すべてのタスクを順にチェック
        done = t.get("done", False)                         # 追加：完了フラグを取り出す（欠損時は未完扱い）
        if mode == FILTER_UNDONE and done:                  # 追加：表示するかどうかを決める
            continue
        if mode == FILTER_DONE and not done:
            continue
        human_index = i + 1                                 # 追加：人間向けに1始まりに修正
        text = f"{human_index}. {format_item_for_listbox(t)}"   # 追加：番号＋整形テキスト
        lst.insert(tk.END,text)                             # 追加：Listboxへ追加
        view_indices.append(i)                              # 追加：「この行は tasks の i 番目」と記録
        visible_count += 1
    status_var.set(f"表示中：{visible_count}件 / 全体：{len(tasks)}件") # 追加：ステータスは「表示中 / 総件数」を明示


# ------ 追加（入力 → 検証 → 保存 → 再描画） ------

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

# ------ 削除（ボタン用） ------

def on_delete_button():                                     # 関数追加：役割/選択行のタスクを削除→保存→再描画。選択なしなら注意表示。
    sel = lst.curselection()                                # 選択されている行インデックスのタプルを取得（例：（0,））
    if not sel:                                             # なにも選ばれていない場合に早期終了
        messagebox.showinfo("削除", "削除する行を選択してください。")   # 情報タイアログを出して知らせる。selが空なら「選んでね」と表示・
        return                                              # ここで関数を終わりにします。以降は実行しません。
    row = sel[0]                                            # 選択はタプルなので先頭の要素だけを取り出して行番号 row にする。
    try:                                                    # 表示用→実データ用の番号変換での範囲エラーを受け止める。
        task_index = view_indices[row]                      # 画面の行番号 row から、tasks 内の本当の位置 task_index を引き当てる。（マッピング=対応づけ）
    except IndexError:                                      # 行ずれなどで、インデックス外になった場合の通知と中断
        messagebox.showwarning("エラー", "内部インデックスの整合性が取れませんでした。")    # 警告ダイアログを出します。例： row が配列外ならここに来る。
        return                                              # ここで処理を止める。安全のため先へは進まない。
    title = tasks[task_index].get("title", "")              # 該当タスクのタイトルを取り出す。get=「なければ既定値」。ここでは無ければ空文字 ""。
    ok = messagebox.askyesno("確認", f"本当に削除しますか？\n\n{title}")  # 確認ダイアログ（はい/いいえ）を出して、結果 True/Falseを ok に入れる。askyesno=「はいなら True」。
    if not ok:                                              # ユーザーが「いいえ」を選んだら中止する
        return                                              # なにも変更せずに終わる。
    try:                                                    # 実データからの削除で起こりうる範囲エラーを受け止める。
        remove_task_core(tasks, task_index)                 # 実際に tasks から1件削除する。core=「中心/基幹」の処理
    except IndexError:                                      # 想定外の行ずれで削除できなかった場合の通知
        messagebox.showwarning("エラー", "指定行の削除に失敗しました。")    # 警告して中断する。例：task_index が配列外ならここに来る
        return                                              # ここで処理を止める。
    save_tasks(tasks)                                       # 変更後の tasks を保存します。save=「保存」。ファイルなどへ書き出し
    refresh_listbox()                                       # 画面のリスト表示を作り直す。refresh=「更新/再読み込み」。番号も振り直される。
    status_var.set(f"{title}を削除しました。")                 # 画面下などのステータス表示を更新する。set=「値を入れる」。

# ------ 完了切替（ボタン用） ------

def on_toggle_button():                                     # 関数追加：完了/未完を反転するトグル
    sel = lst.curselection()                                # listboxから選択した行番号を取得
    if not sel:                                             # 未選択なら案内して中断
        messagebox.showinfo("完了切替", "切り替える行を選択してください。")
        return
    row = sel[0]                                            # sel から最初の要素（行番号）を取り出す。単一選択のため先頭にだけ使う。
    try:
        task_index = view_indices[row]                      # 表示されている行番号 row を、内部データ（tasksの位置）に変換する
    except IndexError:
        messagebox.showwarning("エラー", "内部インデックスの整合性が取れませんでした。")
        return                                              # もし、行番号が不正だった場合に警告を出して処理を中断する。
    try:
        toggle_done_core(tasks, task_index)                 # コア関数を呼び、tasks のtask_index 番目の「完了フラグ」を反転する。
    except IndexError:
        messagebox.showwarning("エラー", "指定行の切替に失敗しました。")
        return                                              # こちらも、もしものエラー（不正なインデックス）対策
    save_tasks(tasks)                                       # 変更された tasks をファイルなどに保存
    refresh_listbox()                                       # listbox を再描画し、表示を最新にする。チェックマークが切り替わる
    status_var.set("状態を切り替えました。")                    # 画面下部のステータス表示にメッセージを出す。

# ------ 編集（ボタン用） ------

def on_edit_button():                                       # 関数追加：選択行のタイトル/期限を編集する。
    sel = lst.curselection()                                # 選択行（例：（0,））を取得
    if not sel:                                             # 未選択なら案内して中断
        messagebox.showinfo("編集", "編集する行を選択してください。")
        return
    row = sel[0]                                            # 単一選択前提で先頭のみ使用
    try:
        task_index = view_indices[row]                      # 表示 → 実データの位置へ変換
    except IndexError:
        messagebox.showwarning("エラー", "内部インデックスの整合性が取れませんでした。")
        return
    current = tasks[task_index]                             # 現在地（辞書）を取り出す
    old_title = current.get("title", "")                    # 既存のタイトル
    old_due = current.get("due")                            # 既存の期限（None または 'YYYY-MM-DD'）

    new_title = simpledialog.askstring(                     # タイトル入力のダイアログ（キャンセル＝変更しない/空文字＝変更しない）
        "タイトル編集",
        f"新しいタイトルを入力（空欄＝変更しない）\n現在：{old_title}",
        initialvalue=old_title
    )

    due_initial = old_due if old_due is not None else ""    # 期限入力ダイアログ（edit_task_core 側で parse_due を通すので、'YYYY-MM-DD' 以外は None になる（＝期限なし））
    new_due = simpledialog.askstring(
        "期限編集",
        "新しい期限（YYYY-MM-DD）\n空欄＝期限なし／キャンセル＝変更しない",
        initialvalue=due_initial
    )

    if new_title is None and new_due is None:               # どちらもキャンセル（None）の場合は何もしない
        status_var.set("編集をキャンセルしました。")
        return
    
    title_arg = None if (new_title is None or not new_title.strip()) else new_title # 空文字は「変更しない」にしたいので None を置き換える（タイトル）。タイトルは空を許可しない設計のため、空白・空欄は「変更なし」とする。

    due_arg = new_due                                       # 期限は空欄 "" を渡すと parse_due で None（期限なし）になる。None=変更なし, ""=期限なしに変更, "YYYY-MM-DD"=その日付

    try:
        edit_task_core(tasks, task_index, title_arg, due_arg)   # コアに反映（安全な検証つき）
    except IndexError:
        messagebox.showwarning("エラー", "指定行の編集に失敗しました。")
        return
    
    save_tasks(tasks)                                       # 変更された tasks をファイルなどに保存
    refresh_listbox()                                       # listbox を再描画し、表示を最新にする。チェックマークが切り替わる
    status_var.set("編集を保存しました。")                      # 画面下部のステータス表示にメッセージを出す。

# ------ キー操作のハンドラ ------

def on_return_key(_event):                                  # タイトル欄でEnterを押すと追加できるようにする（操作が快適になる）
    on_add()                                                # 追加処理を呼ぶ

def on_delete_key(_event):                                  # キーボードのDeleteキーで削除
    on_delete_button()                                      # 削除処理を呼ぶだけ

def on_toggle_key(_event):                                  # スペースキー → 完了切替（操作が速い）
    on_toggle_button()                                      # トグル処理を呼ぶ
        
def on_double_click(_event):                                # 行のダブルクリック → 完了切替（直感的）
    on_toggle_button()                                      # トグル処理を呼ぶ

# ====== イベントの紐づけ ======

btn_add.config(command=on_add)                              # 追加ボタン → on_addを呼ぶ
btn_delete.config(command=on_delete_button)                 # 削除ボタンクリック → on_deleteを呼ぶ
btn_toggle.config(command=on_toggle_button)                 # 追加：完了切替ボタン → on_toggle
btn_edit.config(command=on_edit_button)                     # 追加：編集ボタン → on_edit_button
rb_all.config(command=lambda: refresh_listbox())            # 追加：表示切替（全体）ラジオ切替で再描画
rb_undone.config(command=lambda: refresh_listbox())         # 追加：表示切替（未完のみ）
rb_done.config(command=lambda: refresh_listbox())           # 追加：表示切替（完了のみ）
ent_title.bind("<Return>", on_return_key)                   # タイトル欄でEnterキー → on_addを呼ぶ
root.bind("<Delete>", on_delete_key)                        # ウインドウでDeleteキー → on_deleteを呼ぶ
root.bind("<space>", on_toggle_key)                         # 追加：スペースキー → 完了切替
lst.bind("<Double-Button-1>", on_double_click)              # 追加：ダブルクリック → 完了切替
root.bind("a", lambda e: (filter_var.set(FILTER_ALL), refresh_listbox()))       # 追加：Aで表示切替（全部）
root.bind("u", lambda e: (filter_var.set(FILTER_UNDONE), refresh_listbox()))    # 追加：Uで表示切替（未完）
root.bind("d", lambda e: (filter_var.set(FILTER_DONE), refresh_listbox()))      # 追加：Dで表示切替（完了）

# ====== 起動時の初期表示 ======

refresh_listbox()                                           # 最初に一覧を描画

# ====== メインループ開始 ======

root.mainloop()                                             # イベントループ（GUIが動き続けるために必須）