# Capstone Project: Make the Computer Draw a Box

**Course:** Nand to Tetris – I  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Name:** Shaurya Pratap Singh
**Roll number:** 2501730070  
**Personal number:** K = 70

## 1. Objective
The objective is to integrate a Hack computer using HDL, implement a two-pass assembler in Python, and write a Hack assembly program that displays a black rectangle while a keyboard key is pressed.

## 2. Part A — Hack computer implementation
`CPU.hdl` connects the A and D registers, ALU, memory interface and program counter. The A register supplies addresses and jump targets; the D register stores an ALU operand; the ALU performs the computation selected by the instruction bits. The CPU asserts `writeM` for memory-write instructions and updates the program counter according to the jump condition.

`Memory.hdl` selects RAM, screen or keyboard according to the address. `Computer.hdl` connects the instruction ROM, CPU and memory.

**Evidence to insert:** screenshots of successful CPU, Memory and Computer official tests.  
**Important:** only state that a test passed after running the supplied test script.

## 3. Part B — Python assembler
The assembler uses two passes. In pass one, it removes comments/blank lines, records labels at the current ROM instruction address, and excludes label declarations from the instruction count. In pass two, it translates A-instructions and C-instructions into 16-bit binary. Predefined symbols are loaded first; new variables receive RAM addresses beginning at 16.

Duplicate label declarations produce a warning, and the assembler retains the first definition.

**Evidence to insert:** terminal screenshot showing assembly success and a duplicate-label warning test. Also insert comparisons for Add.asm, Max.asm, Rect.asm and Pong.asm.

## 4. Part C — Box program and calculations
`K = 70`, therefore the starting row is 70. The height is 20 rows. The width is `16 × ((70 mod 4) + 1) = 48` pixels, which is three screen words per row. Screen row 70 begins at `SCREEN + 32 × 70 = 18624`. The program checks the keyboard memory-mapped address `KBD` repeatedly. When a key is pressed, it writes `-1` to three consecutive words in each of 20 rows; when no key is pressed, it writes `0` to those same words. The rectangle therefore occupies rows 70 through 89 and is 48 pixels wide.

**Evidence to insert:** screenshot of the running box in CPU Emulator, plus a screenshot after releasing the key showing the cleared area.

## 5. Mistake encountered and correction
Replace this paragraph with a real mistake you encountered. Example structure: “Initially, my box appeared on the wrong row because I calculated the screen address incorrectly. I checked the memory map, used `SCREEN + 32 × row`, corrected the starting address to 18624 for row 70, and reran the program.”

## 6. Conclusion
The project demonstrates the connection between Hack hardware, machine-language translation and memory-mapped screen I/O. The final demonstration should show the 48-pixel-wide box appearing while a key is held and disappearing after release.

## Submission evidence checklist
- [ ] Official HDL test screenshots
- [ ] Assembler comparison evidence for Add, Max, Rect and Pong
- [ ] Duplicate-label warning evidence
- [ ] CPU Emulator screenshot with box visible
- [ ] CPU Emulator screenshot after key release
- [ ] GitHub repository URL
