# Braille QWERTY Helper: Type Braille, Get Suggestions
![Python](https://img.shields.io/badge/Python-3.x-blue)
![Contributions Welcome](https://img.shields.io/badge/Contributions-Welcome-brightgreen)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Issues](https://img.shields.io/github/issues/garv999/Braille-Autocorrect-and-Suggestion-System)
![Forks](https://img.shields.io/github/forks/garv999/Braille-Autocorrect-and-Suggestion-System)
![Stars](https://img.shields.io/github/stars/garv999/Braille-Autocorrect-and-Suggestion-System)
![Last Commit](https://img.shields.io/github/last-commit/garv999/Braille-Autocorrect-and-Suggestion-System)


Hey there! This little project is all about making it easier to type in Braille using a regular QWERTY keyboard. If you've ever tried six-key Braille input, you know it can be tricky to get every dot perfect. This tool helps by suggesting the correct words even if you make a small typo.

## What's Inside?

Here's a quick look at the main parts:

* **`braille_utils.py`**: This is the brains behind understanding Braille. It knows which QWERTY keys (D, W, Q, K, O, P) match which Braille dots and can translate letters to their dot patterns.
* **`dictionary.txt`**: Just a simple list of English words we use to check against your input. Feel free to add more!
* **`dictionary_loader.py`**: This guy reads `dictionary.txt` and gets it ready for the suggestion engine by turning all those words into Braille dot patterns.
* **`corrector.py`**: This is where the magic happens! It compares your Braille input to the dictionary words (using something called Levenshtein distance, which is just a fancy way to measure "closeness") and figures out the best suggestions.
* **`main.py`**: This is the script you'll run. It asks for your QWERTY-Braille input and then shows you the suggestions.

## Typing Braille with Your QWERTY Keyboard

It's pretty straightforward. We use these keys for the 6 Braille dots:

* `D` = Dot 1
* `W` = Dot 2
* `Q` = Dot 3
* `K` = Dot 4
* `O` = Dot 5
* `P` = Dot 6

To type a single Braille character, you'll type the QWERTY keys for its dots all at once (like "DK" for 'C', which uses dots 1 and 4). Then, just hit space to move to the next Braille character.

## How to Get Started

1. Make sure you have Python 3 on your computer.
2. Put all these files in the same folder:
    * `braille_utils.py`
    * `dictionary_loader.py`
    * `corrector.py`
    * `main.py`
    * `dictionary.txt`
3. Open your terminal (or command prompt), go to that folder.
4. Type `python main.py` and hit Enter.
5. The program will guide you. For example, to type "HELLO":
    * H (dots 1,2,5) -> `DWO` (or `DWK`)
    * E (dots 1,5) -> `DO`
    * L (dots 1,2,3) -> `DWQ`
    * L (dots 1,2,3) -> `DWQ`
    * O (dots 1,3,5) -> `DQO`
    So you'd type: `DWO DO DWQ DWQ DQO`

The system will then try its best to suggest what word you meant!

## What It Does (The Basics)

* Lets you type Braille using QWERTY keys.
* Suggests words from the dictionary if you make a small mistake.
* It's built with a clear structure, so hopefully, it's easy to understand.

## Things We Could Do Next (Ideas!)

* Make it faster for *really* big dictionaries (maybe with a Trie or something similar).
* Get smarter about common Braille typos.
* Let it learn from your choices to give even better suggestions over time.
* Add support for Grade 2 Braille (contractions).
* Maybe even a simple graphical interface!

Hope you find it useful!
Garv Agarwal
<agarwalgarv494@gmail.com>
