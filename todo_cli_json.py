
# 作成開始日：2025年9月5日
# 作成完了日：2025年9月6日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# -------------------------------
# Custom GPT「GPTs学習パート1」より
# -------------------------------

#「追加」「一覧」「削除」に加えてJSONで「保存」機能を実装
# 機能を追加：表示フィルタ（全部/未完/完了）
# 機能を追加：削除前の確認（y/n）
# 機能を追加：編集（タイトルを変更）
# 機能を追加：期限
# 機能を追加：並べ替え（ソート）

import json                 # JSON形式で保存/読み込みをするための標準ライブラリ
from pathlib import Path    # OS差を気にせず安全にパスを扱える便利なクラス

from datetime import datetime   # プログラムで日付や時間を扱うための標準ライブラリ

DATA_FILE = Path("todo.json")   # 保存ファイルのパス（プロジェクト直下）

def parse_due(text):            # 期限文字列を検証して有効ならそのまま返す関数
    if not text.strip():        # 日付が空ならNone（期限なし）を返す
        return None
    
    text = text.strip()         # 呼び出し側の漏れに強くなる（エラーになりにくくするため）

    try:
        datetime.strptime(text, "%Y-%m-%d")    # 文字列をdatetime型に変換し日時を返す（JSONで管理しやすくするため）
        return text
    except ValueError:                          # datetime型に変換できない場合のエラー処理（形式不正や存在しない日付の時）
        print("無効です。期限なしで登録しました。")
        return None
    
def sort_key(t):                                # 並べ替えのルールを1ヶ所に集約する関数
    done_key = 0 if not t.get("done", False) else 1 # 未完は0、完了は1 → 未完が先にくる
    due = t.get("due")                          # 期限文字列（YYYY-MM-DD or None）を取得
    due_key = (due is None, due or "")          # （True/False, 文字列）で比較 → None(期限なし)は末尾へ
    title_key = t.get("title", "")              # 同点字のタイブレークとしてタイトルの昇順にする
    return (done_key, due_key, title_key)       # このタプル順に昇順ソートされる

def sort_and_list(tasks):                       # 並べ替えを実行してから一覧表示する関数
    tasks_sorted = sorted(tasks, key=sort_key)  # 先に定義した sort_ key を使って並び替え（sortedは元のリストを変更せず、新しいリストを返す（＝表示だけ並び替え））
    print("\n(並び替え) 未完優先 → 期限昇順 → タイトル昇順")    # なに順かをユーザーに明示
    list_tasks(tasks_sorted)                    # 既存の一覧表示関数を再利用（DRYの原則）

def search_tasks_cs(tasks):                     # 大文字小文字を区別（Case Sensitive）する検索
    if not tasks:                               # データが無ければ早期リターン
        print("タスクはありません。")
        return
    q = input("検索キーワード（大文字・小文字区別）：").strip() # キーワードをそのまま保持
    if not q:                                             # 空入力は弾く
        print("キーワードを入力してください。")
        return
    
    hits = [t for t in tasks if q in t.get("title", "")]    # 欠損に備えて .get(..., "")で保険

    if not hits:                                            # ヒットなしのときの案内
        print("該当するタスクはありません。")
        return
    print(f"\n[検索結果] キーワード： {q}    ({len(hits)}件)")  # ヒットした件数を明示
    list_tasks(hits)                                        # 既存の一覧表示を再利用（DRY）

def load_tasks():               # タスク一覧をファイルから読み込む
    if DATA_FILE.exists():      # ファイルが存在する場合だけ読み込む
        with DATA_FILE.open("r", encoding="utf-8") as f:    # 文字コードは文字化け対策でUTF-8で統一（"r"は読み取りモード（Readのr）、as fは開いたファイルオブジェクトに名前をつける（fはFileのf））
            return json.load(f) # JSON文字列→Pythonオブジェクト（リスト/辞書）に変換
    return []                   # 初回などファイルがない場合は空のリストを返す

def save_tasks(tasks):          # タスク一覧をファイルへ保存する
    with DATA_FILE.open("w", encoding="utf-8") as f:       # 書き込み専用で開く
        json.dump(tasks, f, ensure_ascii=False, indent=2)   # ensure_ascii=False: 日本語をそのまま保存。indent=2: 見やすい整形出力

def show_menu(tasks):           # メニュー表示を関数にまとめて可能性を上げる
    print(f"\n1) 追加  2) 一覧  3) 削除  4) 完了切替  5) 終了  6) 表示切替  7) 編集  8) 並べ替え  9) 検索   (現在: {len(tasks)}件)")   # 機能の追加にともない、「6) 表示切替」「7) 編集」「8) 並べ替え」「9) 検索」を追加

def list_tasks(tasks):          # タスク一覧を番号付きで表示
    if not tasks:               # リストが空なら
        print("タスクはありません。")
        return
    for i, t in enumerate(tasks, start=1):      # 1から番号を振る( i はenumerateで受け取った番号でタスクの「番号付け」に使われる。)
        mark = "✔" if t.get("done") else "・"   # 完了ならチェックマーク( t は1件のタスクを表す辞書。t.get("done")は、tの中からdoneという値を取り出す。)
        due = t.get("due")                      # 期限のデータを取得
        extra = f" (期限: {due})" if due else ""    # 期限のデータがあれば括弧で表示
        print(f"{i}. {mark} {t.get('title')}{extra}")  # 文字列で整形( i:タスク番号 mark:タスクの完了状態 t:タスクのタイトル)
    print(f"合計 {len(tasks)}件")                # 最後に件数を表示

def add_task(tasks):                           # タスクを追加し、その場で保存
    title = input("タスク名: ").strip()          # 前後の空白を除去
    if not title:                               # 空入力の拒否
        print("空のタスクは追加できません。")
        return
    due_raw = input("期限(YYYY-MM-DD, 空でなし)：")   # 期限を入力（任意）
    due = parse_due(due_raw)                        # due_rawの日時をparse_due関数でチェックし変数dueへ格納
    tasks.append({"title": title, "done": False, "due": due})   # 辞書で状態も一緒に保持
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
        candidate = tasks.pop(idx)                # 機能追加：削除前に確認する機能。popは取り除いた要素を返す
        title = candidate.get("title")
        confirm = input(f"本当に削除しますか？（y/n）：{title} > ").strip().lower()
        if confirm == "y":
            save_tasks(tasks)                       # 保存
            print(f"削除しました：{title}")
        else:                                   # 取り消す場合は元の位置に戻す（UX的に親切）
            tasks.insert(idx, candidate)
            print("削除を取り消しました。")
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
        tasks[idx]["done"] = not tasks[idx].get("done", False)   # True/Falseを反転
        save_tasks(tasks)
        state = "完了" if tasks[idx]["done"] else "未完"
        print(f"切り替えました：{tasks[idx]['title']} → {state}")
    else:
        print("その番号はありません。")

def filter_and_list(tasks):                     # 機能追加：表示フィルタ
    print("表示モードを選択してください：A) 全部  U) 未完のみ  D) 完了のみ")
    mode = input("A/U/D: ").strip().lower()     # 前後の空白を削除し、小文字化

    if mode == "u":                             # 条件に応じてフィルタリング（リスト内包表現）
        filtered = [t for t in tasks if not t.get("done", False)]    # 未完だけ（done が False(未完) のもの）
    elif mode == "d":
        filtered = [t for t in tasks if t.get("done", False)]        # 完了だけ（done が True(完了) のもの）
    else:
        filtered = tasks                                             # それ以外の入力は全部表示（デフォルト）

    list_tasks(filtered)                                          # 既存の一覧表示回数を再利用（DRYの考え方）

def edit_tasks(tasks):                          # 機能追加：編集（タスクのタイトルを編集する処理をまとめた関数）
    if not tasks:                               # タスクが空リストなら編集できないと判断し、すぐに終了する
        print("編集できるタスクがありません。")
        return
    num = input("編集する番号: ")                 # ユーザーに編集したいタスクの番号を聞く
    if not num.isdigit():                       # 入力が数字かどうかを判定。数字でなければ処理を中止する。
        print("数字を入力してください。")
        return
    idx = int(num) - 1                          # 入力された番号（1始まり）をPythonのリスト用インデックス（0始まり）に変換
    if 0 <= idx < len(tasks):                   # インデックスが有効範囲内かチェック
        old_title = tasks[idx].get("title")     # 指定したタスクの現在のタイトルを取得
        old_due = tasks[idx].get("due")         # 指定したタスクの現在の期限を取得

        new_title = input(f"新しいタイトル（空でキャンセル）：（現在：{old_title}）>").strip()  #ユーザーに新しいタイトルを入力させる。空白は削除して扱う。
        if not new_title:                             # 新しいタイトルが空文字なら編集をやめる
            print("タイトルの編集をキャンセルしました。")
        else:
            tasks[idx]["title"] = new_title     # タイトルの上書き
            print(f"タイトルを変更しました。{old_title} → {new_title}") # 変更の可視化

        due_change = input(f"期限を変更しますか？(y/n) 現在：{old_due} > ").strip().lower() # "y"のときのみ編集
        if due_change == "y":
            while True:                         # 入力が不正なとき再入力できるようループ
                raw = input("新しい期限を入力（YYYY-MM-DD、空で期限なし）：").strip()   # 任意で期限入力
                new_due = parse_due(raw)        # ここで形式の検証。空ならNone、形式不正ならメッセージを出してNoneを返す設計
                if raw and new_due is None:     # なにかを入力したが不正な形式のとき
                    print("もう一度、YYYY-MM-DD 形式で入力してください。例：2025-01-01")
                    continue

                tasks[idx]["due"] = new_due     # 期限を上書き
                print(f"期限を更新しました：{old_due} → {new_due}") # 変更結果を表示
                break                           # 期限の編集を終了
        elif due_change == "n":                 # 変更しない明示
            print("期限の変更はありません。")
        else:
            print("y または n を入力してください。（今回は期限変更なしとして続行します）")  # 想定外入力のフォールバック
        
        save_tasks(tasks)                       # タイトル/期限のいずれかを変更した可能性があるので保存
        print("編集を保存しました。")              # 保存完了のフィードバック

        # idx_due = idx.get("due")                                     # 独自で追記するも動作せず
        # due_change = input(f"期限：{idx_due}も変更しますか？(y/n):")
        # if due_change == "y":
        #     new_due = input(f"新しい期限（YYYY-MM-DD）：(現在：{idx_due}) >")
        #     if not new_due:
        #         print("期限の編集はキャンセルしました。")
        #         return
        #     tasks["due"] = new_due
        #     save_tasks(tasks)
        #     print(f"期限を{idx_due}から{new_due}に変更しました。")
        # else:
        #     print("期限の変更はなしです。")                              # 追記終わり
        
    else:                                       # もし入力番号が範囲外だった場合のエラーメッセージ
        print("その番号はありません。")

def main():                                     # アプリの入口
    tasks = load_tasks()                        # 起動時に保存ファイルから読み込み
    while True:                                 # メニューを繰り返し表示
        show_menu(tasks)                        # メニュー内容
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
        elif choice == "6":
            filter_and_list(tasks)
        elif choice == "7":
            edit_tasks(tasks)
        elif choice == "8":
            sort_and_list(tasks)
        elif choice == "9":
            search_tasks_cs(tasks)
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
# フィルタは"絞り込み→表示"の2段構え。表示ロジックは既存関数に任せ、役割分担をはっきりさせている。
# リスト内包表現（[t for t in tasks if 条件]）は、読みやすい条件抽出の基本形
# 「危険な操作は確認」がUIの基本
# いったん pop してから戻せるようにしているのは、元に戻すのを簡単にするため（insert(idx, candidate)）
# 編集について：入力→検証→反映→保存の型を身につけるため。今後GUIでも同じ発想を使う。


# ------------------------------------------------------------

# 期限の機能を追加

# 擬似コード

# from datetime import datetime

# def 期限の関数を作る
#     if 空白のみなら期限としてNoneを返す
#         return
#     try:
#         文字列の時間をdatetime型のオブジェクトに変換
#     except エラー用のメッセージを用意

# ------------------------------------------------------------

# 擬似コード（改良版）

# 関数 parse_due(text):
#     入力 text から前後の空白を取り除く
#     if text が空文字なら:
#         return None   ← 期限なし

#     try:
#         text を "YYYY-MM-DD" 形式として datetime に変換
#         return text   ← 検証OKなのでそのまま返す
#     except 変換エラー:
#         return "INVALID"   ← 呼び出し側でエラーメッセージを表示させる

# ------------------------------------------------------------