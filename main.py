import csv
import random
import tkinter as tk
import jaconv

# --- CSVから問題を読み込む処理 ---
dic = {}
try:
    # Windowsなら encoding='shift-jis' にしてみて
    with open("kanji.csv", mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)  # ★1行目（漢字,読み,ヒント）をスキップする

        for row in reader:
            # row[0]=漢字, row[1]=読み, row[2]=ヒント
            if len(row) >= 2:
                # 読みとヒントをセットで保存しておく
                dic[row[0]] = {
                    "yomi": row[1],
                    "hint": row[2] if len(row) > 2 else "ヒントはないよ",
                }
except Exception as e:
    print(f"読み込みエラー: {e}")

# もし読み込みに失敗して空だったら、エラー防止にダミーを入れる
if not dic:
    dic = {"豹": {"yomi": "ヒョウ", "hint": "体に斑点があるよ"}}


def next_question():
    global toi, kotae, hint_text
    toi = random.choice(list(dic.keys()))
    kotae = dic[toi]["yomi"]
    hint_text = dic[toi]["hint"]  # ヒントを取得

    text2.config(text=toi)
    text.config(text="なんて読む？")
    text_hint.config(text="")  # ヒントは最初は隠しておく
    box.delete(0, tk.END)


def show_hint():
    """ヒントを表示するボタン用"""
    text_hint.config(text=f"ヒント：{hint_text}")


def myfunc():
    ans = box.get()
    ans = jaconv.hira2kata(ans)

    if ans == kotae:
        text.config(text=f"正解！「{kotae}」だよ！")
        root.after(2000, next_question)
    else:
        text.config(text=f"不正解...正解は「{kotae}」だよ。")
        root.after(2000, next_question)


# --- GUI ---
root = tk.Tk()
root.title("ヒント付き！漢字クイズ")
root.minsize(500, 400)

text = tk.Label(root, text="", font=("Meiryo", 15))
text.pack(pady=10)

text2 = tk.Label(root, text="", font=("Meiryo", 40, "bold"))
text2.pack(pady=10)

# ヒント表示用のラベル
text_hint = tk.Label(root, text="", font=("Meiryo", 10), fg="blue")
text_hint.pack()

# ヒントボタン
btn_hint = tk.Button(
    root,
    text="💡 ヒントを見る",
    height=1,
    font=("Meiryo", 10, "bold"),
    fg="#333333",
    command=show_hint,
)
btn_hint.config(bg="#FBFEA9", relief="raised")


def on_enter(e):
    btn_hint.config(bg="#FBFF82")


def on_leave(e):
    btn_hint.config(bg="#FBFEA9")


btn_hint.bind("<Enter>", on_enter)
btn_hint.bind("<Leave>", on_leave)
btn_hint.pack(pady=8)

box = tk.Entry(root, font=("Meiryo", 20))
box.pack(pady=10)

button = tk.Button(
    root,
    text="答える！",
    width=10,
    height=1,
    font=("Meiryo", 11),
    command=myfunc,
)
button.config(bg="#f0f0f0", relief="raised")


def on_enter(e):
    button.config(bg="#e0e0e0")


def on_leave(e):
    button.config(bg="#f0f0f0")


button.bind("<Enter>", on_enter)
button.bind("<Leave>", on_leave)
button.pack(pady=10)

next_question()
root.mainloop()
