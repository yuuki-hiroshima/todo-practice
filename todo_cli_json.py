
# 作成開始日：2025年9月5日
# 作成完了日：2025年9月5日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# -------------------------------
# Custom GPT「ToDoリスト学習」より
# -------------------------------

#「追加」「一覧」「削除」に加えてJSONで「保存」機能を実装

import json                 # JSON形式で保存/読み込みをするための標準ライブラリ
from pathlib import Path    # OS差を気にせず安全にパスを扱える便利なクラス

DATA_FILE = Path("todo.json")   # 保存ファイルのパス（プロジェクト直下）

def load_tasks():               # タスク一覧をファイルから読み込む
    if DATA_FILE.exists():      # ファイルが存在する場合だけ読み込む
        with DATA_FILE.open("r", encoding="utf-8") as f:    # 文字コードは文字化け対策でUTF-8で統一（"r"は読み取りモード（Readのr）、as fは開いたファイルオブジェクトに名前をつける（fはFileのf））
            return json.load(f) # JSON文字列→Pythonオブジェクト（リスト/辞書）に変換
    return []                   # 初回などファイルがない場合は空のリストを返す

def save_tasks(tasks):          # タスク一覧をファイルへ保存する
    with DATA_FILE.open("w", encoding="utf-8") as f:       # 書き込み専用で開く
        json.dump(tasks, f, ensure_ascii=False, indent=2)   # ensure_ascii=False: 日本語をそのまま保存。indent=2: 見やすい整形出力

def show_menu(tasks):           # メニュー表示を関数にまとめて可能性を上げる
    print(f"\n1) 追加  2) 一覧  3) 削除  4) 完了切替  5) 終了   (現在: {len(tasks)}件)")

def list_tasks(tasks):          # タスク一覧を番号付きで表示
    if not tasks:               # リストが空なら
        print("タスクはありません。")
        return
    for i, t in enumerate(tasks, start=1):      # 1から番号を振る( i はenumerateで受け取った番号でタスクの「番号付け」に使われる。)
        mark = "✔" if t.get("done") else "・"   # 完了ならチェックマーク( t は1件のタスクを表す辞書。t.get("done")は、tの中からdoneという値を取り出す。)
        print(f"{i}. {mark} {t.get('title')}")  # 文字列で整形( i:タスク番号 mark:タスクの完了状態 t:タスクのタイトル)
    print(f"合計 {len(tasks)}件")                # 最後に件数を表示

def add_task(tasks):                           # タスクを追加し、その場で保存
    title = input("タスク名: ").strip()          # 前後の空白を除去
    if not title:                               # 空入力の拒否
        print("空のタスクは追加できません。")
        return
    tasks.append({"title": title, "done": False})   # 辞書で状態も一緒に保持
    save_tasks(tasks)                               # 変更を即保存（クラッシュに強い）
    print("追加しました！")

def remove_task(tasks):                         # 指定番号のタスクを削除して保存
    if not tasks:
        print("削除できるタスクはありません。")
        return
    num = input("削除する番号: ")
    if not num.isdigit():                       # 数字チェック
        print("数字を入力してください。")
        return
    idx = int(num) -1                           # 0ではなく1からカウントするため
    if 0 <= idx < len(tasks):                   # 範囲のチェック
        removed = tasks.pop(idx)                # 要素を取り除く
        save_tasks(tasks)                       # 保存
        print(f"削除しました：{removed.get('title')}")
    else:
        print("その番号はありません。")

def toggle_done(tasks):                         # 指定番号の完了/未完了を切り替えて保存
    if not tasks:
        print("切り替えできるタスクがありません。")
        return
    num = input("完了切替する番号: ")
    if not num.isdigit():
        print("数字を入力してください。")
        return
    idx = int(num) - 1
    if 0 <= idx < len(tasks):
        tasks[idx]["done"] = not tasks[idx].get("done,False")   # True/Falseを反転
        save_tasks(tasks)
        state = "完了" if tasks[idx]["done"] else "未完"
        print(f"切り替えました：{tasks[idx]['title']} → {state}")
    else:
        print("その番号はありません。")

def main():                                     # アプリの入口
    tasks = load_tasks()                        # 起動時に保存ファイルから読み込み
    while True:                                 # メニューを繰り返し表示
        show_menu(tasks)                        # 現在件数つきメニュー???
        choice = input("番号を入力: ")            # ユーザーの選択
        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            list_tasks(tasks)
        elif choice == "3":
            remove_task(tasks)
        elif choice == "4":
            toggle_done(tasks)
        elif choice == "5":
            print("終了します。")
            break
        else:
            print("1〜5の番号を入力してください。")

if __name__ == "__main__":                      # このファイルを直接実行したときだけ
    main()                                      # main()を呼ぶ（他ファイルからimportしても実行されないおまじない）

# --- なぜこの書き方？ ---
# list：順序がある・重複OK・追加/削除が簡単
# while True：メニュー式のCLIは「選択→処理→再表示」を繰り返すのが自然
# enumerate：番号付き表示が楽
# if/elif/else：分岐でメニューを表現（読みやすい）
# jsonとpathlib.Path:：標準ライブラリだけで安全
# 辞書型{title, done}：将来「期限(due)」「タグ」などの拡張がしやすい
# 操作のたびにsave_tasks：不意の終了でもデータ消失を最小化