# Music Analyzer and Generator

Music is present in a wide variety of daily activities. It can be studied from different perspectives, such as music theory and composition. One of the fundamental elements of all music is harmony, which studies the relationship between different notes and chords and allows us to build progressions that create musical feelings.

Chord progressions are used in all types of genres—such as pop, rock, hip-hop, jazz, and electronic music—to build the harmonic foundation of a song. However, manually analyzing a progression requires knowledge of scales, chords, and harmonic degrees, which takes time to research and learn if you aren't a musician.

This project consists of a program that can analyze and generate chord progressions based on a key selected by the user. The program identifies the corresponding chords for a scale, determines the musical degrees of an entered progression, and checks whether the chords belong to the selected key. In short, it seeks to identify the chords and musical degrees of a progression, determine if they belong to the selected key, and generate new progressions using basic rules of musical harmony.

Additionally, the program can generate chord progressions using basic harmony rules and save the created progressions to a text file for later reference. The project includes key selection (major and minor), generation of corresponding scales, identification of diatonic chords in a key, analysis of user-entered chord progressions, identification of the degree corresponding to each chord, verification of chord membership in the selected key, random progression generation, application of basic rules to generate progressions with harmonic coherence, saving progressions to text files, and viewing previously saved progressions.

Given these features, the program cannot analyze audio files or full songs, listen to a song and automatically detect its chords, generate audio or MIDI files, play chords, analyze melodies, perform advanced musical analysis of specific genres, replace the judgment of a musician or composer, or use artificial intelligence or machine learning to learn progressions.

The program runs in the terminal using Python 3 and aims to apply concepts such as algorithms, functions, data structures, loops, conditionals, random generation, and file handling.

**Algorithm**

1. Start the program and display the main menu.
2. Prompt the user to select a menu option.
3. If the user selects a key, request the root note and the scale type (major or minor).
4. Generate the notes corresponding to the selected scale.
5. Build the triads corresponding to each degree of the scale and determine whether they are major, minor, or diminished.
6. If the user chooses to analyze a progression, prompt them to enter the chords.
7. Compare each entered chord with the chords belonging to the selected key.
8. Identify the degree of each chord and determine if it belongs to the key.
9. Display the analysis of the progression.
10. If the user chooses to generate a progression, ask for the desired number of chords.
11. Select the first chord and use basic rules of harmony to determine subsequent chords.
12. Randomly select from the allowed chords until reaching the requested length.
13. Display the generated progression and its corresponding degrees.
14. Allow the user to save the progression to a text file.
15. If the user chooses to view saved progressions, read the file and display the stored progressions.
16. Return to the main menu after completing each operation.
17. Exit the program when the user selects the exit option.

