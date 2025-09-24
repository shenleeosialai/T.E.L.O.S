# Levenshtein distance function
def levenshtein_distance(seq1, seq2):
    m = len(seq1)
    n = len(seq2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if seq1[i - 1] == seq2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[m][n]


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


def suggest_words_optimized(
    input_braille_sequence_list,
    deletes_lookup_map,
    num_suggestions=5,
    max_edit_distance_for_input_deletes=1,
    max_levenshtein_threshold=3,
):
    """
    Suggests words using the optimized pre-processed dictionary.
    """
    if not input_braille_sequence_list:
        return []

    input_braille_seq_tuple = tuple(input_braille_sequence_list)

    candidate_word_data_set = set()

    input_deletes = _generate_braille_sequence_deletes_internal(
        input_braille_seq_tuple, max_edit_distance_for_input_deletes
    )

    for deleted_input_seq_tuple in input_deletes:
        if deleted_input_seq_tuple in deletes_lookup_map:
            for word_data_tuple in deletes_lookup_map[deleted_input_seq_tuple]:
                candidate_word_data_set.add(word_data_tuple)

    suggestions_with_distances = []
    for word_string, original_word_braille_seq_tuple in candidate_word_data_set:
        dist = levenshtein_distance(
            input_braille_seq_tuple, original_word_braille_seq_tuple
        )
        if dist <= max_levenshtein_threshold:
            suggestions_with_distances.append((word_string, dist))

    suggestions_with_distances.sort(key=lambda x: (x[1], x[0]))
    # return suggestions_with_distances[:num_suggestions]  # Instead of just word list


    return [word for word, dist in suggestions_with_distances[:num_suggestions]]


if __name__ == "__main__":
    from braille_utils import text_to_braille_sequence, BRAILLE_ALPHABET

    H_bs = BRAILLE_ALPHABET["H"]
    E_bs = BRAILLE_ALPHABET["E"]
    L_bs = BRAILLE_ALPHABET["L"]
    O_bs = BRAILLE_ALPHABET["O"]
    P_bs = BRAILLE_ALPHABET["P"]
    J_bs = BRAILLE_ALPHABET["J"]
    HELLO_bs_tuple = tuple(text_to_braille_sequence("HELLO"))
    HELP_bs_tuple = tuple(text_to_braille_sequence("HELP"))
    JELLO_bs_tuple = tuple(text_to_braille_sequence("JELLO"))
    test_deletes_map = {}

    dictionary_words_for_map = {
        "HELLO": HELLO_bs_tuple,
        "HELP": HELP_bs_tuple,
        "JELLO": JELLO_bs_tuple,
    }

    for word_str, original_bs_tuple in dictionary_words_for_map.items():
        deletes_for_word = _generate_braille_sequence_deletes_internal(
            original_bs_tuple, max_edits=1
        )
        for del_seq in deletes_for_word:
            if del_seq not in test_deletes_map:
                test_deletes_map[del_seq] = []
            word_data_to_add = (word_str, original_bs_tuple)
            if word_data_to_add not in test_deletes_map[del_seq]:
                test_deletes_map[del_seq].append(word_data_to_add)

    print("Corrector.py __main__ test section")
    print(f"Manually created test_deletes_map has {len(test_deletes_map)} entries.")

    print("\n--- Test Case 1: Input 'HELO' ---")
    input_helo_bs_list = text_to_braille_sequence("HELO")

    suggestions_helo = suggest_words_optimized(
        input_braille_sequence_list=input_helo_bs_list,
        deletes_lookup_map=test_deletes_map,
        num_suggestions=5,
        max_edit_distance_for_input_deletes=1,
        max_levenshtein_threshold=2,
    )
    print(f"Input Braille for 'HELO': {input_helo_bs_list}")
    print(f"Suggestions for 'HELO': {suggestions_helo}")
    print("\n--- Test Case 2: Input 'JELLO' ---")
    input_jello_bs_list = text_to_braille_sequence("JELLO")
    suggestions_jello = suggest_words_optimized(
        input_jello_bs_list,
        test_deletes_map,
        max_edit_distance_for_input_deletes=1,
        max_levenshtein_threshold=2,
    )
    print(f"Input Braille for 'JELLO': {input_jello_bs_list}")
    print(f"Suggestions for 'JELLO': {suggestions_jello}")

    print("\n--- Test Case 3: Input 'HEL' ---")
    input_hel_bs_list = text_to_braille_sequence("HEL")
    suggestions_hel = suggest_words_optimized(
        input_hel_bs_list,
        test_deletes_map,
        max_edit_distance_for_input_deletes=1,
        max_levenshtein_threshold=2,
    )
    print(f"Input Braille for 'HEL': {input_hel_bs_list}")
    print(f"Suggestions for 'HEL': {suggestions_hel}")

    print("\n--- Test Case 4: Input 'APL' ---")
    if (
        "A" not in BRAILLE_ALPHABET
        or "P" not in BRAILLE_ALPHABET
        or "L" not in BRAILLE_ALPHABET
    ):
        print(
            "Skipping Test Case 4 because A, P, or L not in Braille Alphabet for testing."
        )
    else:
        input_apl_bs_list = text_to_braille_sequence("APL")
        suggestions_apl = suggest_words_optimized(
            input_apl_bs_list,
            test_deletes_map,
            max_edit_distance_for_input_deletes=1,
            max_levenshtein_threshold=3,
        )
        print(f"Input Braille for 'APL': {input_apl_bs_list}")
        print(f"Suggestions for 'APL': {suggestions_apl}")

    print("\n--- Test Case 5: Empty Input ---")
    suggestions_empty = suggest_words_optimized([], test_deletes_map)
    print(f"Input Braille: []")
    print(f"Suggestions for empty: {suggestions_empty}")
