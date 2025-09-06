
# 作成開始日：2025年9月6日
# 作成完了日：2025年9月6日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# -------------------------------
# Custom GPT「ToDoリスト学習」より
# -------------------------------

# ルール：なるべく参考資料を見ず作成
# 実装する機能「追加」「一覧」「削除」「終了」

tasks = []

while True:
    print("\n1) 追加  2) 一覧  3) 削除  4) 終了")
    choice = input("番号を入力: ")

    if choice == "1":
        task_name = input("タスクを入力してください：").strip() # ストリップメソッドで空白を削除
        if task_name(""):
            print("タスクを入力してください。")
        else:
            tasks.append(task_name)
            print(f"タスク名：{task_name}を追加しました。")
    
    elif choice == "2":
        all(tasks)
        print(f"{tasks}")
    
    elif choice == "3":
        delete_num = input("削除する番号：")
        tasks.pop(delete_num)
        print(f"{delete_num}を削除しました。")
    
    elif choice == "4":
        print("終了します。")
        break

    else:
        print("入力した番号が間違っています。")