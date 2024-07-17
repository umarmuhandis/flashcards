import tkinter as tk
from tkinter import PhotoImage
import pandas as pd
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
FLIP_TIME = 3000
DATA_FILE = "data/french_words.csv"
WORDS_TO_LEARN_FILE = "data/words_to_learn.csv"

def load_data():
    if os.path.exists(WORDS_TO_LEARN_FILE) and os.path.getsize(WORDS_TO_LEARN_FILE) > 0:
        data = pd.read_csv(WORDS_TO_LEARN_FILE)
        if data.empty:
            data = pd.read_csv(DATA_FILE)
    else:
        data = pd.read_csv(DATA_FILE)
    return data.to_dict(orient="records")

def save_data(words):
    df = pd.DataFrame(words)
    df.to_csv(WORDS_TO_LEARN_FILE, index=False)

def create_ui():
    window = tk.Tk()
    window.title("Flash Cards")
    window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

    card_front_img = PhotoImage(file="images/card_front.png")
    card_back_img = PhotoImage(file="images/card_back.png")
    right_img = PhotoImage(file="images/right.png")
    wrong_img = PhotoImage(file="images/wrong.png")

    canvas = tk.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
    card_background = canvas.create_image(400, 263, image=card_front_img)
    card_title = canvas.create_text(400, 150, text="", font=LANGUAGE_FONT, fill="black")
    card_word = canvas.create_text(400, 263, text="", font=WORD_FONT, fill="black")
    canvas.grid(row=0, column=0, columnspan=2)

    wrong_button = tk.Button(window, image=wrong_img, highlightthickness=0)
    wrong_button.grid(row=1, column=0)

    right_button = tk.Button(window, image=right_img, highlightthickness=0)
    right_button.grid(row=1, column=1)

    window.card_front_img = card_front_img
    window.card_back_img = card_back_img
    window.right_img = right_img
    window.wrong_img = wrong_img

    return window, canvas, card_background, card_title, card_word, wrong_button, right_button

def next_card(words, canvas, card_background, card_title, card_word, window, wrong_button, right_button):
    window.after_cancel(window.flip_timer)
    current_card = random.choice(words)
    canvas.itemconfig(card_background, image=window.card_front_img)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    wrong_button.config(state="disabled")
    right_button.config(state="disabled")
    window.flip_timer = window.after(FLIP_TIME, flip_card, canvas, card_background, card_title, card_word, current_card, window, wrong_button, right_button)
    return current_card

def flip_card(canvas, card_background, card_title, card_word, current_card, window, wrong_button, right_button):
    canvas.itemconfig(card_background, image=window.card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    wrong_button.config(state="normal")
    right_button.config(state="normal")

def main():
    words = load_data()
    if not words:
        print("No words loaded. Exiting application.")
        return

    window, canvas, card_background, card_title, card_word, wrong_button, right_button = create_ui()

    current_card = None

    def wrong_button_click():
        nonlocal current_card
        current_card = next_card(words, canvas, card_background, card_title, card_word, window, wrong_button, right_button)

    def right_button_click():
        nonlocal current_card
        words.remove(current_card)
        save_data(words)
        if words:
            current_card = next_card(words, canvas, card_background, card_title, card_word, window, wrong_button, right_button)
        else:
            canvas.itemconfig(card_title, text="Congratulations!", fill="black")
            canvas.itemconfig(card_word, text="You've learned all the words!", fill="black")
            wrong_button.config(state="disabled")
            right_button.config(state="disabled")

    wrong_button.config(command=wrong_button_click)
    right_button.config(command=right_button_click)

    window.flip_timer = window.after(0, lambda: None)

    current_card = next_card(words, canvas, card_background, card_title, card_word, window, wrong_button, right_button)

    window.mainloop()

if __name__ == "__main__":
    main()