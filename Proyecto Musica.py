"""
Musical Analyzer and Generator.

This program generates major scales, builds diatonic triads,
and classifies chords.
"""

# Constants
NOTES = ["C", "C#", "D", "D#", "E", "F","F#", "G", "G#", "A", "A#", "B"]

SCALE_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
TRIAD_STEPS = [0, 2, 4]


"""
 - - - - -- - - - -   - - - - - Musical functions - - - - - - - - -  - - -  - - - - - 
"""


def get_note_index(note):
    """Return the index of a note or -1 if the note is invalid."""

    if note not in NOTES:
        return -1

    return NOTES.index(note)


def transpose_note(note, semitones):
    """Calculate a note a given number of semitones from another note."""

    note_index = get_note_index(note)

    if note_index == -1:
        return None

    new_index = (note_index + semitones) % len(NOTES)

    return NOTES[new_index]


def generate_major_scale(note):
    """Generate the seven notes of a major scale."""

    if get_note_index(note) == -1:
        return None

    scale = [note]
    current_note = note

    for interval in SCALE_INTERVALS[:-1]:
        current_note = transpose_note(current_note, interval)
        scale.append(current_note)

    return scale


def build_triad(scale, degree):
    """Build a triad from a scale degree numbered from zero to six."""

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
    """Classify a triad as major, minor, diminished, or invalid."""

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


def display_major_scale(note):
    """Display a major scale and its seven diatonic triads."""

    scale = generate_major_scale(note)

    if scale is None:
        print("Invalid note. Please try again.")
        return

    print("\nMajor scale:", " - ".join(scale))
    print("\nDiatonic triads:")

    for degree in range(len(scale)):
        triad = build_triad(scale, degree)
        chord_type = identify_chord_type(triad)

        print(
            "Degree", degree + 1, ":",
            " - ".join(triad), "|", chord_type
        )


"""
- - - - - - - - - - - -  Testing functions - - - - - - - - - - - - - - - - 
"""


def tests():
    """Test note calculations, scale generation, and chord functions."""

    assert get_note_index("C") == 0
    assert get_note_index("B") == 11
    assert get_note_index("X") == -1

    assert transpose_note("C", 4) == "E"
    assert transpose_note("B", 1) == "C"
    assert transpose_note("X", 2) is None

    assert generate_major_scale("C") == ["C", "D", "E", "F", "G", "A", "B"]

    assert generate_major_scale("B") == ["B", "C#", "D#", "E", "F#", "G#", "A#"]

    c_scale = generate_major_scale("C")

    assert build_triad(c_scale, 0) == ["C", "E", "G"]
    assert build_triad(c_scale, 1) == ["D", "F", "A"]
    assert build_triad(c_scale, 6) == ["B", "D", "F"]
    assert build_triad(c_scale, 7) is None

    assert identify_chord_type(["C", "E", "G"]) == "Major"
    assert identify_chord_type(["D", "F", "A"]) == "Minor"
    assert identify_chord_type(["B", "D", "F"]) == "Diminished"
    assert identify_chord_type(["C", "E"]) == "Invalid"

    print("All tests passed.")


"""
- - - - - - - - - - - - Main program - - - - - - - - - - - - - - - 
"""


def main():
    """Run the menu until the user chooses to exit."""

    while True:
        print("\n MUSICAL ANALYZER AND GENERATOR ")
        print("1. Generate a major scale and its triads")
        print("2. Exit")

        choice = input("Select an option: ").strip()

        if choice == "1":
            note = input("Enter a note (C, C#, D, D#, E, F, F#, G, G#, A, A#, B): ").strip().upper()

            display_major_scale(note)

        elif choice == "2":
            print("Thank you for using the program!")
            break

        else:
            print("Invalid option. Please select 1 or 2.")


tests()
main()
