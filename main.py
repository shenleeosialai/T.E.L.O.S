from braille_utils import qwerty_to_braille_dots # Keep this
from dictionary_loader import load_dictionary_optimized # CHANGED
from corrector import suggest_words_optimized      # CHANGED

def main():
    print("Loading dictionary using OPTIMIZED method...")
    # CHANGED: Load the deletes_lookup_map
    # You can adjust max_dictionary_deletes if needed, 1 or 2 is common.
    deletes_map, word_count = load_dictionary_optimized(file_path="dictionary.txt", max_dictionary_deletes=1) 
    
    if not deletes_map or word_count == 0:
        print("Failed to load dictionary or dictionary is empty. Exiting.")
        return
    print(f"Successfully loaded {word_count} words into optimized dictionary structure.")

    print("\nBraille Auto-Correct/Suggestion System (Optimized)")
    print("Enter QWERTY key combinations for each Braille character, separated by spaces.")
    print("For example, to type 'C' (dots 1&4), use 'DK'. To type 'A' (dot 1), use 'D'.")
    print("So, to input the Braille for 'CA', you might type: DK D")
    print("Type 'exit' to quit.")

    while True:
        user_input_str = input("\nEnter Braille sequence (QWERTY keys, space-separated): ").strip()

        if user_input_str.lower() == 'exit':
            break

        if not user_input_str:
            continue

        qwerty_char_inputs = user_input_str.split()
        input_braille_sequence_list = [] # Keep as list for suggest_words_optimized
        
        for qwerty_char_input in qwerty_char_inputs:
            braille_dots_tuple = qwerty_to_braille_dots(qwerty_char_input)
            input_braille_sequence_list.append(braille_dots_tuple)
        
        if not input_braille_sequence_list and user_input_str:
             print("No valid QWERTY groups found in input.")
             continue
        if not input_braille_sequence_list:
            continue

        print(f"Interpreted input Braille sequence: {input_braille_sequence_list}")
        
        # CHANGED: Call suggest_words_optimized
        # Adjust parameters as needed:
        # - max_edit_distance_for_input_deletes: how many deletes to make from user input (usually same as max_dictionary_deletes)
        # - max_levenshtein_threshold: final filter for suggestions
        suggestions = suggest_words_optimized(
            input_braille_sequence_list=input_braille_sequence_list, 
            deletes_lookup_map=deletes_map, 
            num_suggestions=5,
            max_edit_distance_for_input_deletes=1, # Should match how deletes_map was built
            max_levenshtein_threshold=2 # Max Levenshtein distance for a word to be considered
        )

        if suggestions:
            print("Suggestions:")
            for i, word in enumerate(suggestions):
                print(f"{i+1}. {word}")
        else:
            print("No suggestions found.")

if __name__ == '__main__':
    main()