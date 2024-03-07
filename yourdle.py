#!/usr/bin/python

import sys
import random

import os

from argparse import ArgumentParser

import requests

__version__ = "0.0.2"


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
        return True, secret_word.upper()

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

    guesses = {}
    feedbacks = []
    available_letters = "abcdefghijklmnopqrstuvwxyz"

    def show_grid():
        for i in range(max_attempts):
            if i < len(feedbacks):
                print(feedbacks[i])
            else:
                print("?????")

        print(f"\nAttempt {attempts+1}/{max_attempts}")
        print(f"\n{available_letters}\n----")

    # start yourdle
    while attempts < max_attempts:
        show_grid()
        guess = input("Your guess:").strip()
        if valid_word(guess):
            if guess not in guesses.keys():
                attempts += 1
                guesses[guess] = 1
                done, feedback, available_letters = check_guess(
                    guess, available_letters
                )
                feedbacks.append(feedback)
                if done:
                    print(
                        f"You guessed the secret word: {secret_word.upper()} in {attempts} attempts"
                    )
                    show_grid()
                    break
                else:
                    if attempts >= max_attempts:
                        print(f"You failed to guess the word: {secret_word.upper()}")
                        break
                    else:
                        continue
            else:
                print(f"You have already guessed {guess.upper()}.")
        else:
            print(f"{guess.upper()} is not a valid word.")


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
