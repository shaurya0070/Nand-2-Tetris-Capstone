// Nand to Tetris Capstone: Make the Computer Draw a Box
// Personal number K = 70
// Start row = 70; height = 20 rows; width = 48 pixels (three words).
// Draw while any key is pressed; clear when no key is pressed.

(START)
    @KBD
    D=M
    @DRAW
    D;JNE
    @CLEAR
    0;JMP

(DRAW)
    @18624       // SCREEN + 32*70 = 16384 + 2240
    D=A
    @ROW_PTR
    M=D
    @20
    D=A
    @ROWS_LEFT
    M=D

(DRAW_LOOP)
    // Draw 48 pixels: three consecutive 16-bit screen words.
    @ROW_PTR
    A=M
    M=-1
    @ROW_PTR
    A=M+1
    M=-1
    @ROW_PTR
    A=M+1
    A=A+1
    M=-1

    @32
    D=A
    @ROW_PTR
    M=D+M
    @ROWS_LEFT
    MD=M-1
    @DRAW_LOOP
    D;JGT
    @START
    0;JMP

(CLEAR)
    @18624
    D=A
    @ROW_PTR
    M=D
    @20
    D=A
    @ROWS_LEFT
    M=D

(CLEAR_LOOP)
    // Clear the same three consecutive screen words.
    @ROW_PTR
    A=M
    M=0
    @ROW_PTR
    A=M+1
    M=0
    @ROW_PTR
    A=M+1
    A=A+1
    M=0

    @32
    D=A
    @ROW_PTR
    M=D+M
    @ROWS_LEFT
    MD=M-1
    @CLEAR_LOOP
    D;JGT
    @START
    0;JMP
