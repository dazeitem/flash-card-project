import random
from tkinter import *
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

data = pd.read_csv("./data/french_words.csv")
words_dict = data.to_dict(orient="records")

window = Tk()
window.title("Flashy")
window.config(width=800, height=1000, bg=BACKGROUND_COLOR)

word_chosen = ""

french_learn = data["French"].tolist()

try:
    words_learnt = pd.read_csv("./data/words_learnt.csv")
except FileNotFoundError:
    with open("./data/words_learnt.csv", "w") as file:
        file.write("French,English\n")
except pd.errors.EmptyDataError:
    words_learnt = []
else:
    french_learnt = words_learnt["French"].tolist()
    french_learn = [word for word in french_learn if word not in french_learnt]


def new_word():
    global word_chosen
    word_chosen = data[data["French"] == random.choice(french_learn)]
    canvas.itemconfig(current_card, image=card_back)
    lang_label.config(text="English", bg="#91C2AF", fg="white")
    word_label.config(text=word_chosen["English"].item(), bg="#91C2AF", fg="white")


def turn_card():
    global word_chosen, flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(current_card, image=card_front)
    lang_label.config(text="French", bg="white", fg="black")
    word_label.config(text=word_chosen["French"].item(), bg="white", fg="black")
    flip_timer = window.after(2000, new_word)


def to_learn():
    pass


def got_correct():
    french_learn.remove(word_chosen["French"].item())
    df = word_chosen
    df.to_csv('./data/words_learnt.csv', mode='a', header=False, index=False)
    turn_card()


flip_timer = window.after(0, new_word)

card_front = PhotoImage(file="./images/card_front.png")
card_back = PhotoImage(file="./images/card_back.png")
right = PhotoImage(file="./images/right.png")
wrong = PhotoImage(file="./images/wrong.png")

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
current_card = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=3, rowspan=2, padx=50, pady=(20, 0))

# Labels
lang_label = Label(font=("Arial", 25, "italic"), bg="white", fg="black")
lang_label.grid(column=0, row=0, columnspan=3, pady=(100, 10))
word_label = Label(font=("Arial", 40, "bold"), bg="white", fg="black")
word_label.grid(column=0, row=1, columnspan=3, pady=(10, 200))

# Buttons
wrong_mark = Button(image=wrong, command=turn_card, borderwidth=0, highlightthickness=0)
wrong_mark.grid(column=0, row=2, pady=(0, 20))
right_mark = Button(image=right, command=got_correct, borderwidth=0, highlightthickness=0)
right_mark.grid(column=2, row=2, pady=(0, 20))

window.mainloop()
