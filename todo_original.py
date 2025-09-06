
# 作成開始日：2025年9月6日
# 作成完了日：2025年9月6日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# -------------------------------
# Custom GPT「ToDoリスト学習」より
# -------------------------------

# ルール：なるべく参考資料を見ず作成
# 実装する機能「追加」「一覧」「削除」「終了」
# 自己採点：30点

tasks = []  # タスク名（文字列）を入れるための空リスト

while True:  # 「終了」を選ぶまでメニューを繰り返す
    print("\n1) 追加  2) 一覧  3) 削除  4) 終了")  # メニュー表示
    choice = input("番号を入力: ")  # ユーザーの選択は常に「文字列」で入る

    if choice == "1":  # 追加
        task_name = input("タスクを入力してください：").strip()  # 前後の空白を除去して受け取る
        if not task_name:  # 空文字なら True（= 何も入力していない）
            print("タスクを入力してください。")  # 入力不備の案内
            continue  # 次のループへ（この回の追加は中止）
        tasks.append(task_name)  # リストの末尾に追加
        print(f"タスク名「{task_name}」を追加しました。")  # 追加のフィードバック

    elif choice == "2":  # 一覧
        if not tasks:  # 空リストなら表示するものがない
            print("タスクはありません。")  # 早期リターン
        else:
            # 番号付きで1行ずつ表示。enumerate(..., start=1) で 1,2,3... と振る
            for i, t in enumerate(tasks, start=1):
                print(f"{i}. {t}")
            print(f"合計: {len(tasks)}件")  # 最後に件数を出す（forの外に置く）

    elif choice == "3":  # 削除
        if not tasks:  # 何もないなら削除できない
            print("削除できるタスクがありません。")
            continue  # 次のループへ

        delete_num = input("削除する番号：").strip()  # 番号は文字列で入る
        if not delete_num.isdigit():  # 数字だけかチェック（マイナスや小数は不可）
            print("数字を入力してください。")
            continue  # 無効入力なのでやり直し

        idx = int(delete_num) - 1  # 表示は1始まり、リストは0始まりなので -1 する
        if 0 <= idx < len(tasks):  # 有効範囲のチェック
            removed = tasks.pop(idx)  # 指定位置の要素を取り除き、その値を受け取る
            print(f"「{removed}」を削除しました。")  # 何を消したかを明示
        else:
            print("その番号はありません。")  # 範囲外

    elif choice == "4":  # 終了
        print("終了します。")
        break  # while ループを抜ける（プログラム終了）

    else:
        print("1〜4の番号を入力してください。")  # 想定外の入力への案内