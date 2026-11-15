"""
Musical Analyzer and Generator.

This program generates major scales, builds diatonic triads,
and classifies chords.
"""

# Constants
NOTES = ["C", "C#", "D", "D#", "E", "F","F#", "G", "G#", "A", "A#", "B"]

SCALE_INTERVALS = [2, 2, 1, 2, 2, 2, 1]
TRIAD_STEPS = [0, 2, 4]


import random 


"""
--------------------------------------------------------------------------------------
 - - - - -- - - - -   - - - - - Musical functions - - - - - - - - -  - - -  - - - - - 
--------------------------------------------------------------------------------------
"""

def get_note_index(note):
    """Return the index of a note or None if the note is invalid."""

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
    
    
"""
-----------------------------------------------------------------------------
- - - - -- - - - - - -  List and matrix functions - - - - - - - - - - - - - - 
-----------------------------------------------------------------------------
"""


def get_chord_symbol(root, chord_type):
    """Create a chord symbol from its root note and quality."""

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
    """Build a matrix containing all seven diatonic triads."""

    if scale is None or len(scale) != 7:
        return None

    chord_matrix = []

    for degree in range(len(scale)):
        triad = build_triad(scale, degree)
        chord_type = identify_chord_type(triad)
        chord_symbol = get_chord_symbol(triad[0], chord_type)

        chord_row = [ degree + 1, triad, chord_type, chord_symbol]

        chord_matrix.append(chord_row)

    return chord_matrix


def normalize_chord(chord_text):
    """Clean and validate a chord symbol entered as text."""

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
    """Convert a progression string into a validated list of chords."""

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
    """Generate a random progression using diatonic chords."""

    if chord_matrix is None or len(chord_matrix) != 7:
        return None

    if number_of_chords < 2:
        return None

    progression = []

    for i in range(number_of_chords):
        chord_row = random.choice(chord_matrix)
        progression.append(chord_row[3])

    return progression


def save_progression(note, progression, analysis, file_name="progressions.txt"):
    """Save a chord progression, its key and analysis in a text file."""

    with open(file_name, "a", encoding="utf-8") as file:
        progression_text = " - ".join(progression)

        analysis_text = "; ".join(
            ", ".join(str(item) for item in chord_analysis)
            for chord_analysis in analysis
        )

        file.write(note + "|" + progression_text + "|" + analysis_text + "\n")

    print("Progression saved successfully!")
    
    

def read_progressions(file_name="progressions.txt"):
    """Read saved progressions and separate their stored information."""

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            progressions = file.readlines()

        progression_data = []

        for line in progressions:
            data = line.strip().split("|", 2)

            if len(data) == 3:
                progression_data.append(data)

        return progression_data

    except FileNotFoundError:
        print("No saved progressions found.")
        return []
    
    
    
def delete_progression(file_name="progressions.txt"):
    """Delete a selected progression from the text file."""

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
    """Compare each chord against a matrix of diatonic triads."""

    if progression is None or chord_matrix is None:
        return None

    analysis = []

    for chord in progression:
        found = False

        for chord_row in chord_matrix:
            if chord == chord_row[3]:
                analysis.append([chord ,chord_row[0] ,"Inside the key"])

                found = True
                break

        if not found:
            analysis.append([chord ,"-" ,"Outside the key"])

    return analysis


"""
------------------------------------------------------------------------------
- - - - - - - - - - - - -  Display functions - - - - - - - - - - - - - - - - - 
------------------------------------------------------------------------------
"""


def display_chord_matrix(chord_matrix):
    """Display all chords stored in the matrix."""

    print("\nDIATONIC CHORDS")

    for chord_row in chord_matrix:
        print(
            "Degree:", chord_row[0],
            "| Notes:", " - ".join(chord_row[1]),
            "| Type:", chord_row[2],
            "| Symbol:", chord_row[3]
        )
        

def display_analysis(analysis):
    """Display the results of a chord progression analysis."""

    print("\nPROGRESSION ANALYSIS")

    for chord_data in analysis:
        print(
            "Chord:", chord_data[0],
            "| Degree:", chord_data[1],
            "| Result:", chord_data[2]
        )
        

def display_major_scale(note):
    """Display a major scale and its seven diatonic triads."""

    scale = generate_major_scale(note)

    if scale is None:
        print("Invalid note. Please try again.")
        return

    print("\nMajor scale:", " - ".join(scale))
    
    chord_matrix = build_chord_matrix(scale)

    display_chord_matrix(chord_matrix)
    


def display_progression_library():
    """Display all progressions stored in the text file."""

    progressions = read_progressions()

    if len(progressions) == 0:
        print("The progression library is empty.")
        return

    print("\nSAVED PROGRESSIONS")

    for progression_data in progressions:
        print("\nKey:", progression_data[0])
        print("Progression:", progression_data[1])
        print("Analysis:", progression_data[2])
        
        
def display_music_theory():
    """Display basic music theory concepts to help users understand the program."""

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
            print("The starting note gives the scale its name.")

        elif option == "3":
            print("\n--- CHORDS AND TRIADS ---")
            print("A chord is formed by playing multiple notes together.")
            print("A triad is a chord made of three notes:")
            print("Root, Third and Fifth.")
            print("Example: C major = C - E - G")
            print("Major triads have a major third and a perfect fifth.")
            print("Minor triads have a minor third and a perfect fifth.")
            print("Diminished triads have a minor third and a diminished fifth.")

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
            print("In a C major scale, the diatonic chords are:")
            print("I - C major")
            print("ii - D minor")
            print("iii - E minor")
            print("IV - F major")
            print("V - G major")
            print("vi - A minor")
            print("vii° - B diminished")
            print("Uppercase Roman numerals represent major chords.")
            print("Lowercase Roman numerals represent minor chords.")
            print("The degree helps identify the harmonic function of a chord.")

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
    """Test musical calculations, matrix construction, and strings."""

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

    print("All tests passed.")
    

"""
------------------------------------------------------------------------------
- - - - - - - - - - - - Main program - - - - - - - - - - - - - - - - - - - - - 
------------------------------------------------------------------------------
"""


def main():
    """Run the musical analyzer menu until the user chooses to exit."""

    progression_library = []

    while True:
        print("\n===== MUSICAL ANALYZER AND GENERATOR =====")
        print("1. Generate a major scale and its triads")
        print("2. Analyze a chord progression")
        print("3. Generate a chord progression")
        print("4. Music theory fundamentals")
        print("5. View saved progressions")
        print("6. Delete a saved progression")
        print("7. Exit")

        option = input("\nSelect an option: ").strip()

        if option == "1":
            note = input("Enter the starting note: ").strip().upper()

            display_major_scale(note)
        
        elif option == "2":

            note = input("Enter the key note: ").strip().upper()
            scale = generate_major_scale(note)

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


        elif option == "3":
            
            note = input("Enter the key note: ").strip().upper()

            scale = generate_major_scale(note)

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

                    progression = generate_progression(chord_matrix, number_of_chords)


                    if progression is None:
                        print("The progression must have at least 2 chords.")

                    else:
                        print("\nGenerated progression:")
                        print(" - ".join(progression))

                        analysis = analyze_progression(progression, chord_matrix)

                        display_analysis(analysis)

                        progression_library.append([note, " - ".join(progression), analysis])

                        save_progression(note, progression, analysis)

                        print("Progression saved in the current session and in the file.")

        
        elif option == "4":
            display_music_theory()

        elif option == "5":
            display_progression_library()
            
        elif option == "6":
            delete_progression()
            
        elif option == "7":
            print("Thank you for using the program!")
            break

        else:
            print("Invalid option. Please select 1, 2, 3, 4, 5 or 6")



tests()
main()
