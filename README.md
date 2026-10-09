# Music Analyzer and Generator

Music is present in a lot of activities that we do in our daily lives. It has two mainly parts for it to be comprehended, which are: music theory and composition. One of the fundamental elements of music is harmony, which is the sound that created when different notes and chords are played, and how much dimension, depth, and richness it adds to music. It allows us to build progressions that create musical feelings.

Chord progressions are used in all types of genres: pop, rock, hip-hop, jazz, electronic music, etc. It is the one that the musician has to create in order to build the harmonic foundation of a song. This is why analyzing a progression requires knowledge of scales, chords, and harmonic degrees, which takes time to research and learn if you aren't a musician.

This project consists of a code that analyzes and generates chord progressions based on a key note which the user selects. The program identifies the corresponding chords for a scale, determines the musical degrees of an entered progression and checks whether the chords belong to the key. In short, it identifies the chords and musical degrees of a progression, determines if they belong to the selected key, and generate new progressions using rules of musical harmony, that are basically the organization and the core blocks for something to sound nice; triads (root note, a third and a fifth), consonance/dissonance and interval stability are some examples of it.

The program can select major and minor keys, generate scales and chords, analyze chord progressions, identify the degree of each chord, check if chords belong to the selected key, generate random progressions, create simple harmonic progressions, save progressions in text files, and view saved progressions. Although, it can't analyze audio files or listen something, detect chords from a song, create audio or MIDI files, do a more advanced music analysis or use AI or machine learning to learn progressions.

The program runs in the terminal using Python 3. It applies algorithms, functions, data structures, loops, conditionals, random generation, and file handling.

**Algorithm**

Input: 
Menu option.    
Root note and scale type (major or minor).    
Chords for progression analysis.    
Number of chords for a generated progression.    
Option to save or view progressions.   

Process:
1. Start the program and display the main menu.
2. Ask for a menu option.
3. If the user selects a key, ask for the root note and the scale type (if it is major or minor).
4. Generate the notes according to the given scale.
5. Build the triads for each degree of the scale and determine whether they are major, minor, or diminished.
6. If the user chooses to analyze a progression, ask them to enter the chords.
7. Compare each entered chord with the chords belonging to the selected key.
8. Identify the degree of each chord and say if it belongs to the key.
9. Display the analysis of the progression.
10. If the user chooses to generate a progression, ask for the number of chords that they want.
11. Select the first chord and give subsequent chords.
12. Select randomly from the allowed chords until reaching the requested length.
13. Display the generated progression and its corresponding degrees.
14. Allow the user to save the progression to a text file.
15. If the user chooses to view saved progressions, read the file and display the progressions.
16. Return to the main menu after each operation.
17. Exit the program if they select exit option.

Output:
Generated scale and chords.   
Chord progression analysis.   
Degree of each chord.   
Whether each chord belongs to the key.   
Generated chord progression.   
Saved or previously saved progressions.   
