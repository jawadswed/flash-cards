from tkinter import *
from tkinter import messagebox
import pandas as pd
import random
import time

BACKGROUND_COLOR = "#B1DDC6"
data_list = {}

try:
    data_file = pd.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    try:
        data_file = pd.read_csv("./data/french_words.csv")
    except FileNotFoundError:
        messagebox.showerror(title="File Error",
                             message="Failed to load the dictionary file.\n"
                                     "Please make sure you have the csv file in the data directory")
    else:
        data_list = data_file.to_dict(orient="records")
        from_trans = list(data_list[0].keys())[0]
        to_trans = list(data_list[0].keys())[1]
except:
    messagebox.showerror(title="File is empty",
                         message="Seems you have learned all the words.\n"
                                 "the game has finished.\n"
                                 "add new files to the data directory to play again.")

else:
    data_list = data_file.to_dict(orient="records")
    from_trans = list(data_list[0].keys())[0]
    to_trans = list(data_list[0].keys())[1]

random_card = {}



def remove_word():
    data_list.remove(random_card)
    change_frensh_word()


def change_frensh_word():
    global random_card, flip_timer

    window.after_cancel(flip_timer)
    random_card = random.choice(data_list)
    fr_word = random_card[from_trans]
    canvas.itemconfigure(language_text, text=from_trans, fill="black")
    canvas.itemconfigure(word_text, text=fr_word, fill="black")
    canvas.itemconfigure(canvas_img, image=card_front_img)
    flip_timer = window.after(ms=3000, func=flip_card)


def flip_card():
    global random_card
    en_word = random_card[to_trans]
    canvas.itemconfigure(canvas_img, image=card_back_img)
    canvas.itemconfigure(language_text, text=to_trans, fill="white")
    canvas.itemconfigure(word_text, text=en_word, fill="white")


window = Tk()
window.title("Flashy Cards")
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(ms=3000, func=flip_card)

card_front_img = PhotoImage(file="./images/card_front.png")
card_back_img = PhotoImage(file="./images/card_back.png")
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(column=0, row=0, columnspan=2)
canvas_img = canvas.create_image(400, 263, image=card_front_img)
language_text = canvas.create_text(400, 150, font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, font=("Arial", 60, "bold"))

wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, highlightthickness=0, command=change_frensh_word)
wrong_button.grid(column=0, row=1)

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, highlightthickness=0, command=remove_word)
right_button.grid(column=1, row=1)

change_frensh_word()

window.mainloop()

data = pd.DataFrame(data_list)

data.to_csv("./data/words_to_learn.csv", index=False)
