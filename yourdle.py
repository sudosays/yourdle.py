#!/usr/bin/python

import sys
import random

import os

from argparse import ArgumentParser

import requests

__version__ = "0.0.2"


GREETING = """Welcome to yourdle.py!

How to play:

Try to guess the secret 5-letter word within 6 attempts.

The feedback from your guesses is a bit minimal. Upper case characters mean that
the character is both correct and in the correct place. Lower case characters
mean that the character is correct, but in the wrong position. An asterisk means
that the character was incorrect.

Example:

1. The secret word is "ISSUE".
2. Your guess is "SCENE".
3. The feedback is `s***E`.

Here 's' is correct, but in the wrong position. 'E' is also correct and in the
correct position.

Good luck!
"""


def prepare_wordlist():
    response = requests.get(
        "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
    )
    if response.ok:
        with open("wordlist-en.txt", "w") as f:
            for line in response.text.split("\n"):
                word = line.strip()
                if len(word) == 5:
                    f.write(f"{word}\n")


def valid_word(word):
    if len(word) == 5:
        return word in word_table.keys()
    else:
        return False


def check_guess(guess, available_letters):
    guess = guess.lower()
    if guess == secret_word:
        return True, secret_word.upper(), available_letters

    feedback = "?????"
    secret_word_copy = secret_word

    # Mark all correct letters and remove from secret_word_copy
    for i, c in enumerate(secret_word_copy):
        if c == guess[i]:
            feedback = feedback[:i] + c.upper() + feedback[i + 1 :]
            secret_word_copy = secret_word_copy[:i] + "*" + secret_word_copy[i + 1 :]
            guess = guess[:i] + "*" + guess[i + 1 :]

    for i, c in enumerate(guess):
        if c == "*":
            continue

        if c in secret_word_copy:
            feedback = feedback[:i] + c + feedback[i + 1 :]
            secret_word_copy = secret_word_copy.replace(c, "*", 1)
        else:
            feedback = feedback[:i] + "*" + feedback[i + 1 :]
            available_letters = available_letters.replace(c, "")

    return False, feedback, available_letters


def main(secret_word, word_table):
    attempts = 0
    max_attempts = 6

    guesses = []
    feedbacks = []
    available_letters = "abcdefghijklmnopqrstuvwxyz"

    print(GREETING)

    def show_grid():
        for i in range(max_attempts):
            if i < len(feedbacks):
                print(f"{feedbacks[i]}\t{guesses[i].upper()}")
            else:
                print("?????")

    # start yourdle
    while attempts < max_attempts:
        show_grid()
        print(f"\nAttempt {attempts+1}/{max_attempts}")
        print(f"\n{available_letters}\n----")
        guess = input("Your guess:").strip().lower()
        if valid_word(guess):
            if guess not in guesses:
                attempts += 1
                guesses.append(guess)
                done, feedback, available_letters = check_guess(
                    guess, available_letters
                )
                feedbacks.append(feedback)
                if done:
                    print("\nCongratulations!")
                    print(
                        f"\nYou guessed the secret word: {secret_word.upper()} in {attempts} attempts\n"
                    )
                    show_grid()
                    print()
                    break
                else:
                    if attempts >= max_attempts:
                        print(f"\nYou failed to guess the word: {secret_word.upper()}")
                        break
                    else:
                        continue
            else:
                print(f"You have already guessed {guess.upper()}.")
        else:
            print(f"{guess.upper()} is not a valid 5-letter word.")


if __name__ == "__main__":
    parser = ArgumentParser(
        prog="yourdle.py", description="A basic Wordle for your terminal"
    )

    parser.add_argument(
        "--word-file",
        help="Path to a wordlist with one 5 letter word per line",
        default="wordlist-en.txt",
    )
    parser.add_argument("--secret", help="A chosen word to try guess", default=None)

    args = parser.parse_args()

    if not os.path.exists(args.word_file):
        prepare_wordlist()

    word_table = {}
    # load the words into a word_table
    with open(args.word_file, "r") as f:
        word = f.readline()
        while word:
            word_table[word.strip()] = 1
            word = f.readline()

    if args.secret is None:
        secret_word = random.choice(list(word_table.keys()))
    else:
        secret_word = args.secret

    main(secret_word, word_table)
