from braille_utils import text_to_braille_sequence


def _generate_braille_sequence_deletes_internal(braille_sequence_tuple, max_edits=1):
    """
    Generates a set of all unique Braille sequences that can be obtained by deleting
    up to max_edits characters from the input braille_sequence_tuple.
    Includes the original sequence (0 deletes).
    """
    deletes = {braille_sequence_tuple}
    current_level_sequences = {braille_sequence_tuple}
    for edit_count in range(max_edits):
        next_level_deletes = set()
        if not current_level_sequences:
            break
        for seq_tuple in current_level_sequences:
            if not seq_tuple:
                continue
            seq_list = list(seq_tuple)
            if not seq_list:
                continue
            for i in range(len(seq_list)):
                deleted_list = seq_list[:i] + seq_list[i + 1 :]
                next_level_deletes.add(tuple(deleted_list))
        deletes.update(next_level_deletes)
        current_level_sequences = next_level_deletes
        if not current_level_sequences and edit_count < max_edits - 1:
            break
    return deletes


def load_dictionary(file_path="dictionary.txt"):
    """
    Loads words from a text file and converts them to (word, braille_sequence) tuples.
    Each line in the file is expected to be a single word.
    This is the non-optimized version.
    """
    processed_dictionary = []
    try:
        with open(file_path, "r") as f:
            for line in f:
                word = line.strip().upper()
                if word:
                    braille_seq_list = text_to_braille_sequence(word)
                    if braille_seq_list:
                        processed_dictionary.append((word, tuple(braille_seq_list)))
    except FileNotFoundError:
        print(f"Error: Dictionary file '{file_path}' not found.")
    return processed_dictionary


def load_dictionary_optimized(file_path="dictionary.txt", max_dictionary_deletes=1):
    """
    Loads words from a text file, converts them to Braille sequences,
    and creates a lookup map of delete variations for optimized suggestions.

    Args:
        file_path (str): Path to the dictionary text file.
        max_dictionary_deletes (int): The maximum number of deletes to generate
                                      for each dictionary word's Braille sequence
                                      to populate the lookup map.

    Returns:
        tuple: (deletes_lookup_map, dictionary_word_count)
               deletes_lookup_map: dict where keys are deleted Braille sequence tuples,
                                   and values are lists of (word_string, original_full_braille_seq_tuple).
               dictionary_word_count: int, number of words successfully processed.
    """
    deletes_lookup_map = {}
    dictionary_word_count = 0
    try:
        with open(file_path, "r") as f:
            for line in f:
                word_string = line.strip().upper()
                if not word_string:
                    continue

                original_braille_seq_list = text_to_braille_sequence(word_string)
                if not original_braille_seq_list:
                    continue

                original_braille_seq_tuple = tuple(original_braille_seq_list)
                dictionary_word_count += 1

                deletes_for_word = _generate_braille_sequence_deletes_internal(
                    original_braille_seq_tuple, max_edits=max_dictionary_deletes
                )

                for deleted_seq_tuple in deletes_for_word:
                    if deleted_seq_tuple not in deletes_lookup_map:
                        deletes_lookup_map[deleted_seq_tuple] = []

                    word_data_to_add = (word_string, original_braille_seq_tuple)
                    if word_data_to_add not in deletes_lookup_map[deleted_seq_tuple]:
                        deletes_lookup_map[deleted_seq_tuple].append(word_data_to_add)

    except FileNotFoundError:
        print(f"Error: Dictionary file '{file_path}' not found.")
        return {}, 0

    return deletes_lookup_map, dictionary_word_count


if __name__ == "__main__":
    print("Testing dictionary_loader.py...")

    dummy_dict_file = "dummy_dict_loader_test.txt"
    with open(dummy_dict_file, "w") as f:
        f.write("HELLO\n")
        f.write("HELP\n")
        f.write("WORLD\n")
        f.write("PYTHON\n")
        f.write("INVALID CHARS %$%\n")
        f.write("\n")
        f.write("TEST\n")

    print("\n--- Testing load_dictionary (original) ---")
    original_dict_data = load_dictionary(dummy_dict_file)
    print(f"Loaded {len(original_dict_data)} words with original load_dictionary.")
    if original_dict_data:
        print("First few entries (word, braille_sequence_tuple):")
        for i in range(min(3, len(original_dict_data))):
            print(original_dict_data[i])

    print("\n--- Testing load_dictionary_optimized ---")

    deletes_map, word_count = load_dictionary_optimized(
        dummy_dict_file, max_dictionary_deletes=1
    )
    print(f"Optimized load processed {word_count} words.")
    print(
        f"Deletes lookup map contains {len(deletes_map)} unique delete patterns as keys."
    )

    if deletes_map:
        print("Sample entries from deletes_lookup_map (for one delete patterns):")

        hello_bs_tuple = tuple(text_to_braille_sequence("HELLO"))
        if hello_bs_tuple in deletes_map:
            print(
                f"Original 'HELLO' ({hello_bs_tuple}) maps to: {deletes_map[hello_bs_tuple]}"
            )
        hell_bs_tuple = tuple(text_to_braille_sequence("HELL"))
        if hell_bs_tuple in deletes_map:
            print(
                f"1-delete 'HELL' ({hell_bs_tuple}) maps to: {deletes_map[hell_bs_tuple]}"
            )
        else:
            print(
                f"'HELL' pattern not found as a key (or HELLO was too short to produce it with 1 delete)."
            )

        help_bs_tuple = tuple(text_to_braille_sequence("HELP"))
        if help_bs_tuple in deletes_map:
            print(
                f"Original 'HELP' ({help_bs_tuple}) maps to: {deletes_map[help_bs_tuple]}"
            )

        hlp_bs_tuple = (
            BRAILLE_ALPHABET["H"],
            BRAILLE_ALPHABET["L"],
            BRAILLE_ALPHABET["P"],
        )
        if hlp_bs_tuple in deletes_map:
            print(
                f"1-delete 'HLP' ({hlp_bs_tuple}) maps to: {deletes_map[hlp_bs_tuple]}"
            )

    # Clean up dummy file
    import os

    os.remove(dummy_dict_file)
    print(f"\nCleaned up {dummy_dict_file}.")
