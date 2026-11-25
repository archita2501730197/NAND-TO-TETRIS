// Box.asm
// Course: Nand to Tetris - I (ETCNTC301)
// Student: Archita (Roll No: 2501730197)
// Personal Number: K = 97
// 
// Specifications:
// - Starting row: K = 97
// - Screen base address: SCREEN + (32 * 97) = 16384 + 3104 = 19488
// - Height: 20 rows (Rows 97 to 116)
// - Width: 16 * ((K mod 4) + 1) = 16 * (1 + 1) = 32 pixels (2 words per row)
// - Behavior: 
//     While any key is pressed (RAM[24576] != 0), renders black rectangle (-1).
//     When no key is pressed (RAM[24576] == 0), erases the rectangle (0).

(MAIN_LOOP)
    // 1. Read keyboard register KBD (RAM[24576])
    @KBD
    D=M

    // If key is pressed (D != 0), draw black; else erase (draw white)
    @DRAW_BLACK
    D;JNE

(DRAW_WHITE)
    @color
    M=0
    @RENDER
    0;JMP

(DRAW_BLACK)
    @color
    M=-1

(RENDER)
    // Initialize starting row screen address: 16384 + 32 * 97 = 19488
    @19488
    D=A
    @rowAddr
    M=D

    // Initialize row count to 20
    @20
    D=A
    @rowCount
    M=D

(ROW_LOOP)
    // Check if 20 rows are completed
    @rowCount
    D=M
    @MAIN_LOOP
    D;JEQ

    // Draw Word 0 (First 16 pixels of current row)
    @color
    D=M
    @rowAddr
    A=M
    M=D

    // Draw Word 1 (Next 16 pixels of current row, total 32 pixels)
    @rowAddr
    D=M+1
    @col1Addr
    M=D
    @color
    D=M
    @col1Addr
    A=M
    M=D

    // Advance to next row: rowAddr = rowAddr + 32
    @32
    D=A
    @rowAddr
    M=D+M

    // Decrement row count: rowCount = rowCount - 1
    @rowCount
    M=M-1

    // Repeat for next row
    @ROW_LOOP
    0;JMP
