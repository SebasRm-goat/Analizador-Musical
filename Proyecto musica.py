"""
Musical Analyzer and Generator.

This program generates major scales, builds diatonic triads,
analyzes chord progressions, and saves
musical information in text files.

Author: Sebas RM
"""

import random
import matplotlib.pyplot as plt

# Constants
NOTES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]

SCALE_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
MINOR_SCALE_INTERVALS = [2, 1, 2, 2, 1, 2, 2]
TRIAD_STEPS = [0, 2, 4]
"""
--------------------------------------------------------------------------------------
Musical functions
--------------------------------------------------------------------------------------
"""


def get_note_index(note):
    """Find the position of a note in the chromatic list.

    Inputs:
        note: A musical note to search for.

    Process:
        Check whether the note exists in NOTES. If it exists, return its
        zero position; otherwise, return -1.

    Outputs:
        The note's index, or -1 when the note is invalid.
    """

    if note not in NOTES:
        return -1

    return NOTES.index(note)


def transpose_note(note, semitones):
    """Calculate a note after adding a number of semitones.

    Inputs:
        note: The starting musical note.
        semitones: The number of steps to move from the starting note.

    Process:
        Find the starting note's index, add the semitone count, get
        result around the 12-notes list with arithmetic.

    Outputs:
        str or None: The transposed note, or None for an invalid starting note.
    """

    note_index = get_note_index(note)

    if note_index == -1:
        return None

    new_index = (note_index + semitones) % len(NOTES)

    return NOTES[new_index]


def generate_major_scale(note):
    """Generate the seven notes of a major scale.

    Inputs:
        note: The tonic, or starting note, of the scale.

    Process:
        Validate the note, add it first, and apply the remaining major-scale
        intervals to write the following six notes.

    Outputs:
        list or None: Seven scale notes, or None for an invalid note.
    """

    if get_note_index(note) == -1:
        return None

    scale = [note]
    current_note = note

    for interval in SCALE_INTERVALS[:-1]:
        current_note = transpose_note(current_note, interval)
        scale.append(current_note)

    return scale


def generate_minor_scale(note):
    """Generate the seven notes of a natural minor scale.

    Inputs:
        note: The tonic, or starting note, of the scale.

    Process:
        Validate the note, add it first, and apply the remaining minor
        scale intervals to make the following six notes.

    Outputs:
        list or None: Seven scale notes, or None for an invalid note.
    """

    if get_note_index(note) == -1:
        return None

    scale = [note]
    current_note = note

    for interval in MINOR_SCALE_INTERVALS[:-1]:
        current_note = transpose_note(current_note, interval)
        scale.append(current_note)

    return scale


def build_triad(scale, degree):
    """Build a triad from a scale degree.

    Inputs:
        scale: A seven-note musical scale.
        degree: A degree between 0 and 6.

    Process:
        Validate the scale length and degree. Select the root, third, and
        fifth notes.

    Outputs:
        list or None: A three-note triad, or None for invalid inputs.
    """

    if scale is None or len(scale) != 7:
        return None

    if degree < 0 or degree > 6:
        return None

    triad = []

    for step in TRIAD_STEPS:
        note = scale[(degree + step) % len(scale)]
        triad.append(note)

    return triad


def identify_chord_type(triad):
    """Classify a triad as major, minor, diminished, or other.

    Inputs:
        triad: A three-note chord beginning with its root.

    Process:
        Validate the triad and calculate the third and fifth intervals relative
        to the root. Compare those intervals with standard chord patterns.

    Outputs:
        str: "Major", "Minor", "Diminished", "Other", or "Invalid".
    """

    if triad is None or len(triad) != 3:
        return "Invalid"

    root_index = get_note_index(triad[0])
    third_index = get_note_index(triad[1])
    fifth_index = get_note_index(triad[2])

    if -1 in [root_index, third_index, fifth_index]:
        return "Invalid"

    third_interval = (third_index - root_index) % len(NOTES)
    fifth_interval = (fifth_index - root_index) % len(NOTES)

    if third_interval == 4 and fifth_interval == 7:
        return "Major"

    elif third_interval == 3 and fifth_interval == 7:
        return "Minor"

    elif third_interval == 3 and fifth_interval == 6:
        return "Diminished"

    else:
        return "Other"


"""
-----------------------------------------------------------------------------
- - - - -- - - - - - -  List and matrix functions - - - - - - - - - - - - - -
-----------------------------------------------------------------------------
"""


def get_chord_symbol(root, chord_type):
    """Create a text symbol for a chord.

    Inputs:
        root: The root note of the chord.
        chord_type: "Major", "Minor", "Diminished", or another quality.

    Process:
        Select an empty suffix for major, "m" for minor, or "dim" for
        diminished.

    Outputs:
        str or None: The combined root and suffix, or None for unsupported
        chord types.
    """

    if chord_type == "Major":
        suffix = ""

    elif chord_type == "Minor":
        suffix = "m"

    elif chord_type == "Diminished":
        suffix = "dim"

    else:
        return None

    return root + suffix


def build_chord_matrix(scale):
    """Build a matrix containing all seven diatonic triads.

    Inputs:
        scale: A valid seven-note musical scale.

    Process:
        Validate the scale and for every degree, build a triad, identify its
        type and symbol and store it.

    Outputs:
        list or None: A seven-row chord matrix, or None for an invalid
        scale.
    """

    if scale is None or len(scale) != 7:
        return None

    chord_matrix = []

    for degree in range(len(scale)):
        triad = build_triad(scale, degree)
        chord_type = identify_chord_type(triad)
        chord_symbol = get_chord_symbol(triad[0], chord_type)

        chord_row = [degree + 1, triad, chord_type, chord_symbol]

        chord_matrix.append(chord_row)

    return chord_matrix


def normalize_chord(chord_text):
    """Clean and validate a chord symbol entered as text.
    """

    chord_text = chord_text.strip()

    if len(chord_text) == 0:
        return None

    if len(chord_text) >= 2 and chord_text[1] == "#":
        root = chord_text[:2].upper()
        suffix = chord_text[2:].lower()

    else:
        root = chord_text[0].upper()
        suffix = chord_text[1:].lower()

    if get_note_index(root) == -1:
        return None

    if suffix not in ["", "m", "dim"]:
        return None

    return root + suffix


def parse_progression(progression_text):
    """Convert a progression string into a validated chord list.
    """

    if progression_text == "":
        return None

    chord_texts = progression_text.split("-")
    progression = []

    if len(chord_texts) < 2:
        return None

    for chord_text in chord_texts:
        chord = normalize_chord(chord_text)

        if chord is None:
            return None

        progression.append(chord)

    return progression


def generate_progression(chord_matrix, number_of_chords):
    """Generate a random progression using diatonic chords.

    Inputs:
        chord_matrix: A valid seven-row diatonic chord matrix.
        number_of_chords: The requested number of chords.

    Process:
        Validate the matrix and then choose a matrix
        row for each requested chord and append its symbol.

    Outputs:
        list or None: Random chord symbols, or None for invalid input.
    """

    if chord_matrix is None or len(chord_matrix) != 7:
        return None

    if number_of_chords < 2:
        return None

    progression = []

    for i in range(number_of_chords):
        chord_row = random.choice(chord_matrix)
        progression.append(chord_row[3])

    return progression


def save_progression(note, scale_type, progression, analysis,
                     file_name="progressions.txt"):
    """Save a chord progression and its analysis to a text file.

    Inputs:
        note: The key or starting note.
        scale_type: The scale name, such as "Major" or "Minor".
        progression: The chord symbols in the progression.
        analysis: Chord, degree, and key-location results.
        file_name: The destination file name. The default is
            "progressions.txt".

    Process:
        Convert the progression and analysis to a text with pipes like a
        separation, append the record to the file.

    Outputs:
        None (the function writes to a file and displays a success message)
    """

    with open(file_name, "a", encoding="utf-8") as file:
        progression_text = " - ".join(progression)

        analysis_text = "; ".join(
            ", ".join(str(item) for item in chord_analysis)
            for chord_analysis in analysis
        )

        file.write(
            note + "|" + scale_type + "|" +
            progression_text + "|" + analysis_text + "\n"
        )

    print("Progression saved successfully!")


def read_progressions(file_name="progressions.txt"):
    """Read and parse saved chord progression records.
    """

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            progressions = file.readlines()

        progression_data = []

        for line in progressions:
            data = line.strip().split("|", 3)

            if len(data) == 4:
                progression_data.append(data)

        return progression_data

    except FileNotFoundError:
        print("No saved progressions found.")
        return []


def delete_progression(file_name="progressions.txt"):
    """Delete one saved progression selected by the user.

    Inputs:
        file_name: The text file containing saved progressions. The
            default is "progressions.txt".

    Process:
        Read the file, display what is stored, and remove the
        selected line and rewrite the remaining lines.

    Outputs:
        None (the function displays information and may rewrite the file)
    """

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            progressions = file.readlines()

        if len(progressions) == 0:
            print("The progression library is empty.")
            return

        print("\nSAVED PROGRESSIONS")

        for i in range(len(progressions)):
            print(i + 1, "-", progressions[i].strip())

        option = input("\nEnter the number of the progression to delete: ")

        if not option.isdigit():
            print("Please enter a valid number.")
            return

        option = int(option)

        if option < 1 or option > len(progressions):
            print("Invalid progression number.")
            return

        deleted_progression = progressions.pop(option - 1)

        with open(file_name, "w", encoding="utf-8") as file:
            file.writelines(progressions)

        print("Progression deleted successfully!")
        print("Deleted:", deleted_progression.strip())

    except FileNotFoundError:
        print("No saved progressions found.")


def analyze_progression(progression, chord_matrix):
    """Compare a progression with a diatonic chord matrix.

    Inputs:
        progression: Chord symbols to analyze.
        chord_matrix: Seven diatonic chord rows.

    Process:
        Search the matrix for a matching symbol. Append its
        degree and "Inside the key" for a match, or "-" and "Outside the key"
        for no match.

    Outputs:
        list or None
    """

    if progression is None or chord_matrix is None:
        return None

    analysis = []

    for chord in progression:
        found = False

        for chord_row in chord_matrix:
            if chord == chord_row[3]:
                analysis.append([chord, chord_row[0], "Inside the key"])

                found = True
                break

        if not found:
            analysis.append([chord, "-", "Outside the key"])

    return analysis


"""
------------------------------------------------------------------------------
- - - - - - - - - - - - -  Display functions - - - - - - - - - - - - - - - - -
------------------------------------------------------------------------------
"""


def display_progression_chart(analysis):
    """Display a bar chart of the analyzed progression.
    """

    chords = []
    degrees = []

    for chord_data in analysis:
        chords.append(chord_data[0])

        if chord_data[1] == "-":
            degrees.append(0)
        else:
            degrees.append(chord_data[1])

    plt.bar(chords, degrees)

    plt.title("Chord Progression Analysis")
    plt.xlabel("Chords")
    plt.ylabel("Musical Degree")

    plt.show()


def display_chord_matrix(chord_matrix):
    """Display every row stored in a diatonic chord matrix.
    """

    print("\nDIATONIC CHORDS")

    for chord_row in chord_matrix:
        print(
            "Degree:", chord_row[0],
            "| Notes:", " - ".join(chord_row[1]),
            "| Type:", chord_row[2],
            "| Symbol:", chord_row[3]
        )


def display_analysis(analysis):
    """Display the results of a chord progression analysis.
    """

    print("\nPROGRESSION ANALYSIS")

    for chord_data in analysis:
        print(
            "Chord:", chord_data[0],
            "| Degree:", chord_data[1],
            "| Result:", chord_data[2]
        )


def display_major_scale(note):
    """Display a major scale and all of its diatonic triads.
    """

    scale = generate_major_scale(note)

    if scale is None:
        print("Invalid note. Please try again.")
        return

    print("\nMajor scale:", " - ".join(scale))

    chord_matrix = build_chord_matrix(scale)

    display_chord_matrix(chord_matrix)


def display_minor_scale(note):
    """Display a minor scale and all of its diatonic triads.
    """

    scale = generate_minor_scale(note)

    if scale is None:
        print("Invalid note. Please try again.")
        return

    print("\nNatural minor scale:", " - ".join(scale))

    chord_matrix = build_chord_matrix(scale)

    display_chord_matrix(chord_matrix)


def display_progression_library():
    """Display saved progressions and analyze them.

    """

    progressions = read_progressions()

    if len(progressions) == 0:
        print("The progression library is empty.")
        return

    print("\nSAVED PROGRESSIONS")

    for i in range(len(progressions)):
        print(
            i + 1, "-",
            progressions[i][0],
            progressions[i][1],
            "|",
            progressions[i][2]
        )

    option = input(
        "\nEnter the number of a progression to analyze "
        "(0 to return): "
    ).strip()

    if not option.isdigit():
        print("Please enter a valid number.")
        return

    option = int(option)

    if option == 0:
        return

    if option < 1 or option > len(progressions):
        print("Invalid progression number.")
        return

    selected_progression = progressions[option - 1]

    note = selected_progression[0]
    scale_type = selected_progression[1]
    progression_text = selected_progression[2]

    if scale_type == "Major":
        scale = generate_major_scale(note)

    else:
        scale = generate_minor_scale(note)

    chord_matrix = build_chord_matrix(scale)

    progression = parse_progression(progression_text)

    analysis = analyze_progression(
        progression, chord_matrix
    )

    display_analysis(analysis)

    display_progression_chart(analysis)


def display_music_theory():
    """Show a menu of basic music theory topics.
    """

    while True:
        print("\n===== MUSIC THEORY FUNDAMENTALS =====")
        print("1. Musical Notes")
        print("2. Scales")
        print("3. Chords and Triads")
        print("4. Chord Progressions")
        print("5. Musical Degrees")
        print("6. Return to main menu")

        option = input("\nSelect a topic: ").strip()

        if option == "1":
            print("\n--- MUSICAL NOTES ---")
            print("Musical notes are the basic elements of music.")
            print("There are 12 different notes in the chromatic system:")
            print("C, C#, D, D#, E, F, F#, G, G#, A, A#, B")
            print("A sharp (#) raises a note by one semitone.")
            print("A semitone is the distance between two consecutive notes.")

        elif option == "2":
            print("\n--- SCALES ---")
            print("A scale is an organized sequence of musical notes.")
            print("A major scale contains seven different notes.")
            print("Its interval pattern is:")
            print("Whole, Whole, Half, Whole, Whole, Whole, Half")
            print("Example: C major = C - D - E - F - G - A - B")
            print()
            print("--------------------------------------------")
            print()
            print("A minor scale contains seven different notes.")
            print("Its interval pattern is:")
            print("Whole, Half, Whole, Whole, Half, Whole, Whole")
            print("Example: C minor = C - D - Eb - F - G - Ab - Bb")
            print("The starting note gives the scale its name.")

        elif option == "3":
            print("\n--- CHORDS AND TRIADS ---")
            print("A chord is formed by playing multiple notes together.")
            print("A triad is a chord made of three notes:")
            print("Root, Third and Fifth.")
            print("Example: C major = C - E - G")
            print("Example: C minor = C - Eb - G")
            print("Major triads have a major third and a perfect fifth.")
            print("Minor triads have a minor third and a perfect fifth.")
            print(
                "Diminished triads have a minor third and a diminished fifth."
            )

        elif option == "4":
            print("\n--- CHORD PROGRESSIONS ---")
            print("A chord progression is a sequence of chords.")
            print("It provides the harmonic foundation of a song.")
            print("Example: C - G - Am - F")
            print("You can enter progressions in this format")
            print("when using the Analyze a chord progression option.")
            print("Separate each chord with a hyphen.")

        elif option == "5":
            print("\n--- MUSICAL DEGREES ---")
            print("Musical degrees indicate the position of a chord")
            print("within a scale.")
            print("In a major scale, the diatonic chords are:")
            print("I - major")
            print("ii - minor")
            print("iii - minor")
            print("IV - major")
            print("V - major")
            print("vi - minor")
            print("vii° - diminished")
            print("Uppercase Roman numerals represent major chords.")
            print("Lowercase Roman numerals represent minor chords.")
            print()
            print("--------------------------------------------")
            print()
            print("In a minor scale, the diatonic chords are:")
            print("i - minor")
            print("ii - diminished")
            print("III - major")
            print("iv - minor")
            print("v - minor")
            print("VI - major")
            print("VII° - major")
            print("Uppercase Roman numerals represent major chords.")
            print("Lowercase Roman numerals represent minor chords.")
            print(
                "The degree helps identify the harmonic function of a chord."
            )

        elif option == "6":
            break

        else:
            print("Invalid option. Please select a number from 1 to 6.")


"""
--------------------------------------------------------------------------
- - - - - - - - - - - -  Testing functions - - - - - - - - - - - - - - - -
--------------------------------------------------------------------------
"""


def tests():
    """Run assertions for musical calculations and file handling.

    Inputs:
        None

    Process:
        Check notes and transposition, major and minor scales, chord
        matrices and symbols, progression generation.
        Clear the test file after is verified and
        print a success message.

    Outputs:
        The function does test and prints "All tests passed."
    """

    assert get_note_index("C") == 0
    assert get_note_index("X") == -1

    assert transpose_note("B", 1) == "C"

    c_scale = generate_major_scale("C")

    assert c_scale == ["C", "D", "E", "F", "G", "A", "B"]

    c_matrix = build_chord_matrix(c_scale)

    assert len(c_matrix) == 7
    assert c_matrix[0][3] == "C"
    assert c_matrix[1][3] == "Dm"
    assert c_matrix[6][3] == "Bdim"

    progression = generate_progression(c_matrix, 4)

    assert len(progression) == 4

    for chord in progression:
        assert chord in [
            chord_row[3] for chord_row in c_matrix
        ]

    analysis = analyze_progression(progression, c_matrix)

    assert len(analysis) == 4

    for chord_data in analysis:
        assert chord_data[2] == "Inside the key"

    a_minor_scale = generate_minor_scale("A")

    assert a_minor_scale == ["A", "B", "C", "D", "E", "F", "G"]

    a_minor_matrix = build_chord_matrix(a_minor_scale)

    assert a_minor_matrix[0][3] == "Am"
    assert a_minor_matrix[1][3] == "Bdim"
    assert a_minor_matrix[2][3] == "C"
    assert a_minor_matrix[4][3] == "Em"

    minor_progression = generate_progression(a_minor_matrix, 4)

    assert len(minor_progression) == 4

    minor_analysis = analyze_progression(
        minor_progression, a_minor_matrix
    )

    assert len(minor_analysis) == 4

    for chord_data in minor_analysis:
        assert chord_data[2] == "Inside the key"

    assert normalize_chord(" C ") == "C"
    assert normalize_chord("am") == "Am"
    assert normalize_chord("F#DIM") == "F#dim"
    assert normalize_chord("") is None
    assert normalize_chord("X") is None
    assert normalize_chord("Cmaj7") is None

    # Progression parsing tests
    assert parse_progression("C - G - Am - F") == [
        "C", "G", "Am", "F"
    ]

    assert parse_progression("C") is None
    assert parse_progression("C - X - G") is None

    # Progression analysis tests
    assert analyze_progression(
        ["C", "G", "Am", "F"], c_matrix
    ) == [
        ["C", 1, "Inside the key"],
        ["G", 5, "Inside the key"],
        ["Am", 6, "Inside the key"],
        ["F", 4, "Inside the key"]
    ]

    # File handling tests
    test_file = "test_progressions.txt"

    test_progression = ["C", "G", "Am", "F"]
    test_analysis = analyze_progression(
        test_progression, c_matrix
    )

    save_progression(
        "C", "Major", test_progression,
        test_analysis, test_file
    )

    saved_data = read_progressions(test_file)

    assert len(saved_data) == 1
    assert saved_data[0][0] == "C"
    assert saved_data[0][1] == "Major"
    assert saved_data[0][2] == "C - G - Am - F"

    with open(test_file, "w", encoding="utf-8") as file:
        file.write("")

    print("All tests passed.")


"""
------------------------------------------------------------------------------
- - - - - - - - - - - - Main program - - - - - - - - - - - - - - - - - - - - -
------------------------------------------------------------------------------
"""


def main():
    """Run the musical analyzer menu.

    Inputs:
        None

    Process:
        Repeat the main menu, read the user's choice and
        do valid choices for each option

    Outputs:
        The function displays menus and results.
    """

    while True:
        print("\n===== MUSICAL ANALYZER AND GENERATOR =====")
        print("1. Music theory fundamentals")
        print("2. Generate a major scale and its triads")
        print("3. Generate a minor scale and its triads")
        print("4. Analyze a chord progression")
        print("5. Generate a chord progression")
        print("6. View saved progressions")
        print("7. Delete a saved progression")
        print("8. Exit")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            display_music_theory()

        elif option == "2":
            note = input("Enter the starting note: ").strip().upper()

            display_major_scale(note)

        elif option == "3":

            note = input("Enter the starting note: ").strip().upper()

            display_minor_scale(note)

        elif option == "4":
            note = input("Enter the key note: ").strip().upper()

            scale_type = input(
                "Select scale type (1. Major / 2. Minor): "
            ).strip()

            if scale_type == "1":
                scale = generate_major_scale(note)

            elif scale_type == "2":
                scale = generate_minor_scale(note)

            else:
                print("Invalid scale type.")
                continue

            if scale is None:
                print("Invalid key. Please try again.")

            else:
                chord_matrix = build_chord_matrix(scale)

                user_input = input(
                    "Enter the chord progression  (example: C - G - Am - F) : "
                )

                progression = parse_progression(user_input)

                if progression is None:
                    print("Invalid progression. Please try again.")

                else:
                    analysis = analyze_progression(
                        progression, chord_matrix
                    )

                    display_analysis(analysis)
                    display_progression_chart(analysis)

        elif option == "5":
            note = input("Enter the key note: ").strip().upper()

            scale_type = input(
                "Select scale type (1. Major / 2. Minor): "
            ).strip()

            if scale_type == "1":
                scale = generate_major_scale(note)

            elif scale_type == "2":
                scale = generate_minor_scale(note)

            else:
                print("Invalid scale type.")
                continue

            if scale is None:
                print("Invalid key. Please try again.")

            else:
                chord_matrix = build_chord_matrix(scale)

                number_of_chords = input(
                    "Enter the number of chords: "
                )

                if not number_of_chords.isdigit():
                    print("Please enter a valid number.")

                else:
                    number_of_chords = int(number_of_chords)

                    progression = generate_progression(
                        chord_matrix, number_of_chords
                    )

                    if progression is None:
                        print("The progression must have at least 2 chords.")

                    else:
                        print("\nGenerated progression:")
                        print(" - ".join(progression))

                        analysis = analyze_progression(
                            progression, chord_matrix
                        )

                        display_analysis(analysis)
                        display_progression_chart(analysis)

                        if scale_type == "1":
                            scale_name = "Major"
                        else:
                            scale_name = "Minor"

                        save_progression(
                            note, scale_name, progression, analysis
                        )

                        print(
                            "Progression successfully stored in the library."
                        )

        elif option == "6":
            display_progression_library()

        elif option == "7":
            delete_progression()

        elif option == "8":
            print("Thank you for using the program!")
            break

        else:
            print(
                "Invalid option. Please select a number from 1 to 8."
            )


if __name__ == "__main__":
    tests()
    main()
