
# ----------------------------------------------------
# 「command」+「/」の同時押しで一括コメントアウトと解除が可能
# ----------------------------------------------------

# 課題1:入力と空白削除＋空文字拒否
# 目的：input()strip()と"空はダメ"の判定（if not s:）
# やること：空行やスペースだけの入力を弾いて、正しい文字列だけ受け付ける。

# ----------------------------------------------------

# while True:
#     name = input("名前を入力（qで終了）：").strip()
#     if not name:
#         print("名前を入力してください。")
#         continue
#     elif name.lower() == ('q'):
#         print("終了します。")
#         break
#     else:
#         print(f"入力した名前は{name}です。")

# ----------------------------------------------------

# 課題2：番号付き一覧表示（enumerate）
# 目的：enumerate(list, start=1) の正しい使い方
# やること：リストを1からの連番で表示し、最後に合計件数も出す。

# ----------------------------------------------------

# items = ["牛乳", "卵", "パン"]

# if not items:
#     print("なにもありません。")
# else:
#     for i, t in enumerate(items, start=1):
#         print(f"{i}, {t}")
# print(f"合計：{len(items)}件")

# ----------------------------------------------------

# 課題3：削除番号の検証（isdigit→int→範囲チェック→pop）
# 目的：isdigit()・int()・1始まり→0始まり補正・範囲チェック
# やること：番号で要素を削除。無効入力は弾く。

# ----------------------------------------------------

# tasks = ["国語", "数学", "英語"]

# for i, t in enumerate(tasks, start=1):
#     print(f"{i}. {t}")

# num = input("削除する番号：").strip()

# if not num.isdigit():
#     print("数字を入力してください。")
# else:
#     idx = int(num) -1
#     if 0 <= idx < len(tasks):
#         removed = tasks.pop(idx)
#         print(f"{removed}を削除しました。")
#     else:
#         print("範囲外です。")

# ----------------------------------------------------

# 課題4：メニューとフロー整理（continue / break）
# 目的：無効入力時にその場でやり直し、終了はbreakで抜ける
# やること：1)追加 2)終了 のみの最小メニューを正しいフローで動かす。

# ----------------------------------------------------

# items = []

# while True:
#     print("\n1) 追加  2) 終了")
#     choice = input("番号：").strip()

#     if choice == "1":
#         s = input("入力内容：").strip()
#         if not s:
#             print("入力内容がないため、やり直してください。")
#             continue
#         else:
#             items.append(s)
#             print(f"{s}を追加しました。")
#     elif choice == "2":
#         print("終了します。")
#         break
#     else:
#         print("(1/2)のいずれかを入力してください。")
#         continue

# print(f"合計：{len(items)}件")
# for i, t in enumerate(items, start=1):
#     print(f"{i}. {t}")

# ----------------------------------------------------

# 課題5：リストの「見せ方」を変える
# 目的：内部表現 print(list) と、人向け表示の違いを意識
# やること：区切り文字で連結して1行で出す／1行ずつ出すの2通りを実装。

# ----------------------------------------------------

# fruits = ["りんご", "みかん", "バナナ"]

# separator = "／"
# result = separator.join(fruits)

# print(result)

# for i, t in enumerate(fruits, start=1):
#     print(f"{i}. {t}")

# ----------------------------------------------------

# 課題6：内包表記の基礎（任意・短時間）
# 目的：for版 ⇄ 内包表記 の相互変換に慣れる
# やること：偶数だけを取り出すコードを2通りで書く。

# ----------------------------------------------------

# nums = [1,2,3,4,5,6]

# evens_1= []
# for n in nums:
#     if n % 2 == 0:
#         evens_1.append(n)

# evens_2 = [n for n in nums if n % 2 == 0]   # % 2 == 0（2で割って余りが0なら偶数。%はあまりを返す演算子）

# print(evens_1)
# print(evens_2)

# ----------------------------------------------------

# 課題7：数当てゲームの自作
# 目的：ゴールやプロセスを見据えて、落ち着いてコードを書く練習
# やること：ゴールを考える→処理を考える→コードに書き起こす。

# ----------------------------------------------------

# 数当てゲームの処理

# 処理1:抽選する値の範囲を決める
# 処理2:ランダムに値を抽選する
# 処理3:ユーザーに数を入力してもらう
# 処理4:入力した数を整数に変換する
# 処理5:入力した数と抽選した値を照合する
# 処理6:当たれば結果を表示して終了
# 処理7:外れていれば正解との差分を提示し再度入力へ戻る
# 処理8:当たるまで繰り返す or 入力回数を制限する

# ----------------------------------------------------

# 疑似コード

# 1) 定数 LOW/HIGH, MAX_TRIES を決める
# 2) 正解 answer を randint で作る
# 3) tries = 0

# 4) while True:
#      a) もし tries == MAX_TRIES なら「ゲームオーバー」→ 正解を表示して break
#      b) 入力を促す（q/exit で終了可）
#      c) もし小文字化した入力が q または exit なら「中止」→ break
#      d) もし数字じゃない → 「数字を入力してね」→ continue
#      e) 整数に変換 → 範囲外なら「1〜Nの範囲」→ continue
#      f) tries を 1 増やす
#      g) もし guess == answer → 「当たり！」→ break
#         それ以外 → 差分 = abs(guess - answer) を表示
#                     お好みで「大きい/小さい」ヒントも
#                     次のループへ（continue）

# ----------------------------------------------------

import random

LOW, HIGH = 0, 20
MAX_TRIES = 5

answer = random.randint(LOW, HIGH)
tries = 0

while True:
    if tries == MAX_TRIES:
        print(f"残念！{MAX_TRIES}回で当てられませんでした。正解は{answer}です。")
        break

    raw = input(f"{LOW}〜{HIGH}の整数を入力（qで終了）：").strip()
    if raw.lower() in ("q", "exit"):
        print("ゲームを中止しました。")
        break
    elif not raw.isdigit():
        print("数字を入力してください。")
        continue

    guess = int(raw)                                    # else:の記述はなくても動作に問題ないため削除
    if not (LOW <= guess <= HIGH):
        print(f"{LOW}〜{HIGH}の整数を入力してください。")
        continue

    tries += 1 

    if guess == answer:
        print("当たり")
        break
    else:
        diff = abs(guess - answer)
        print(f"残念。差は{diff}です。")        # ヒントがほぼ答えになってしまうので、変数diff〜は削除したほうが良い
        if guess < answer:
            print("もっと大きい数です。")
            continue
        else:
            print("もっと小さい数です。")
            continue
# ----------------------------------------------------