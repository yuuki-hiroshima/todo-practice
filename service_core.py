
# 作成開始日：2025年9月8日
# 作成完了日：2025年9月8日
# 著作者名：yuuki-hiroshima
# All rights reserved.

# --------------------------------
# Custom GPT「GPTs学習パート2」より
# --------------------------------

from pathlib import Path            # ファイルパスを安全に扱うための標準ライブラリ（OSの違いを気にせずパスが使える）
import json                         # タスクをJSON形式で保存/読み込みするための標準ライブラリ
from datetime import datetime       # 期限（YYYY-MM-DD）の形式チェックに使う

DATA_FILE = Path(__file__).parnet / "todo.json" # スクリプトのある場所基準に固定（VScodeの実行場所差を吸収）

def load_tasks():                               # タスク一覧をJSONファイルから読み込む（ファイルがなければ空リスト）
    if DATA_FILE.exists():                      # 指定したパスがファイルとして存在するかをチェック
        with DATA_FILE.open("r", encoding="utf-8") as f:    # 読み取りモード"r"で開き、変数"f"に格納（UTF-8に固定することで文字化け防止）
            return json.load(f)                 # JSON文字列 → Pythonのリスト/辞書へ変換
    return []                                   # 初回は空リストで開始

def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as f:        # 書き込みモード"w"で開き、変数"f"に格納（UTF-8に固定することで文字化け防止）
        json.dump(tasks, f, ensure_ascii=False, indent=2)   # 非ascii文字である日本語をそのまま出力し、json.dumpで保存。見やすい整形（indent=2）

def parse_due(text):                            # 期限入力文字列を検証し。正しければそのまま文字列、空ならNone、形式不正ならNoneを返す。
    if text is None:                            # Noneが来たときの安全対策
        return None                             # 期限なしとして扱う
    text = text.strip()                         # 前後の空白を削除（揺れ対策）
    if not text:                                # テキストは空なら
        return None                             # 期限なしとして扱う
    try:
        datetime.strptime(text, "%Y-%m-%d")     # "YYYY-MM-DD" の形式かをチェック
        return text                             # 正しい形式なので文字列をそのまま返す（JSON管理が簡単）
    except ValueError:                          # 不正形式だった場合のエラー
        return None                             # 不正形式は期限なしとして扱う
    
def format_item_for_listbox(task: dict) -> str:         # Listboxに表示する1行の見た目を統一して作る。(後半は、taskが辞書型"dict"であることを示し、文字列"str"で返すという記述)
    mark = "[x]" if task.get("done", False) else "[ ]"  # doneがTrueなら[x]、それ以外は[ ]
    title = task.get("title", "")                       # タイトル（欠損時は空文字）
    due = task.get("due")                               # 期限（YYYY-MM-DDまたはNone）
    extra = f" (期限: {due})" if due else ""             # 期限があれば括弧付きで表示
    return f"{mark} {title}{extra}"                     # 最終的な表示文字列

def add_task_core(tasks: list, title: str, due: str | None = None) -> list: # 空白タイトルを拒否し、タスクを追加して同じリストを返す。
    title_clean = (title or "").strip()                                     # None対策＋前後の空白を除去
    if not title_clean:                                                     # 空の場合はエラー
        raise ValueError("空のタスクは追加できません。")                         # GUI側でメッセージを表示する。 
    due_norm = parse_due(due)                                               # 期限は正規化（不正ならNone）
    tasks.append({"title": title_clean, "done": False, "due": due_norm})    # 新規タスクを辞書で追加
    return tasks                                                            # 更新済みリストを返す（同一オブジェクト）

def removed_task_core(tasks: list, index: int) -> tuple[list, dict]:    # tasks: listから指定index(0始まり)の要素を削除して、更新後リスト"list"と削除したタスク"dict"を返す。
    if not (0 <= index < len(tasks)):                                   # 指定したインデックスが範囲外かチェック
        raise IndexError("指定したインデックスが範囲外です。")                # GUI側でメッセージを表示する。
    removed = tasks.pop(index)                                          # "pop"で要素を取り除き、取り除いた要素を受け取る。
    return tasks, removed                                               # （更新後リスト, 削除したタスク）を返す。