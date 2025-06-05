QWERTY_TO_DOT_MAP = {
    'D': 1, 'd': 1,
    'W': 2, 'w': 2,
    'Q': 3, 'q': 3,
    'K': 4, 'k': 4,
    'O': 5, 'o': 5,
    'P': 6, 'p': 6,
}

# Standard English Grade 1 Braille Alphabet
# Each character is represented by a 6-tuple indicating active dots (1) or inactive dots (0)
# Dots are in order: 1 2 3
#                     4 5 6
# So, (d1, d2, d3, d4, d5, d6)
BRAILLE_ALPHABET = {
    'A': (1,0,0,0,0,0), 'B': (1,1,0,0,0,0), 'C': (1,0,0,1,0,0),
    'D': (1,0,0,1,1,0), 'E': (1,0,0,0,1,0), 'F': (1,1,0,1,0,0),
    'G': (1,1,0,1,1,0), 'H': (1,1,0,0,1,0), 'I': (0,1,0,1,0,0),
    'J': (0,1,0,1,1,0), 'K': (1,0,1,0,0,0), 'L': (1,1,1,0,0,0),
    'M': (1,0,1,1,0,0), 'N': (1,0,1,1,1,0), 'O': (1,0,1,0,1,0),
    'P': (1,1,1,1,0,0), 'Q': (1,1,1,1,1,0), 'R': (1,1,1,0,1,0),
    'S': (0,1,1,1,0,0), 'T': (0,1,1,1,1,0), 'U': (1,0,1,0,0,1),
    'V': (1,1,1,0,0,1), 'W': (0,1,0,1,1,1), 'X': (1,0,1,1,0,1),
    'Y': (1,0,1,1,1,1), 'Z': (1,0,1,0,1,1),
    ' ': (0,0,0,0,0,0), # Space
    # Numbers are typically prefixed by a number sign (dots 3456), 
    # but for simplicity, we'll map digits if needed or handle them as letters.
    # For this project, we'll focus on alphabetic words.
}

def qwerty_to_braille_dots(qwerty_input_str):
    """
    Converts a string of QWERTY keys (e.g., "DK") representing a single Braille character
    into a 6-tuple of Braille dots.
    Example: "DK" (dots 1 and 4) -> (1,0,0,1,0,0)
    """
    dots = [0,0,0,0,0,0]
    for char_key in qwerty_input_str:
        dot_number = QWERTY_TO_DOT_MAP.get(char_key.upper())
        if dot_number:
            dots[dot_number - 1] = 1
    return tuple(dots)

def text_to_braille_sequence(text_word):
    """
    Converts an English word (string) into a sequence (list) of Braille dot tuples.
    Unknown characters will be skipped.
    """
    braille_sequence = []
    for char_in_word in text_word.upper():
        if char_in_word in BRAILLE_ALPHABET:
            braille_sequence.append(BRAILLE_ALPHABET[char_in_word])
        # else: skip unknown characters or handle as needed
    return braille_sequence

if __name__ == '__main__':
    # Test cases
    print(f"'DK' (for C) -> {qwerty_to_braille_dots('DK')}") # Expected: (1,0,0,1,0,0)
    print(f"'d' (for A) -> {qwerty_to_braille_dots('D')}")   # Expected: (1,0,0,0,0,0)
    print(f"Word 'HI': {text_to_braille_sequence('HI')}")
    # H: (1,1,0,0,1,0), I: (0,1,0,1,0,0)
    # Expected: [(1,1,0,0,1,0), (0,1,0,1,0,0)]
    
    # Test QWERTY input for "C" from problem (D and K)
    # D=dot1, K=dot4 -> (1,0,0,1,0,0) which is 'C' in BRAILLE_ALPHABET
    test_c_qwerty = "DK"
    braille_c = qwerty_to_braille_dots(test_c_qwerty)
    print(f"QWERTY '{test_c_qwerty}' -> Braille {braille_c}")
    
    found_char = None
    for char, pattern in BRAILLE_ALPHABET.items():
        if pattern == braille_c:
            found_char = char
            break
    print(f"Braille pattern {braille_c} corresponds to letter: {found_char}")
