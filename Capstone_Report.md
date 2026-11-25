# CAPSTONE PROJECT REPORT
## MAKE THE COMPUTER DRAW A BOX

**Course:** Nand to Tetris – I  
**Subject Code:** ETCNTC301 / ETCCNT301  
**Program:** B.Tech Computer Science & Engineering (AI & ML)  
**School:** School of Engineering & Technology, K.R. Mangalam University  
**Mode:** Individual Work  

---

### 1. Student Information & Personal Number ($K$)

| Field | Detail / Calculation |
| :--- | :--- |
| **Student Name** | Archita |
| **University Roll Number** | 2501730197 |
| **Course & Branch** | B.Tech CSE (AI & ML), Semester III |
| **Subject Name & Code** | Nand to Tetris – I (ETCNTC301 / ETCCNT301) |
| **Personal Number ($K$)** | Last two digits of Roll Number = **97** |
| **Assigned Assembler Feature** | $K \pmod 3 = 97 \pmod 3 = \mathbf{1}$<br>Print a clear line-numbered error message (e.g. `Line 7: invalid instruction: ...`) instead of crashing when encountering malformed syntax. |
| **Box Starting Row** | $\text{Row } K = \mathbf{97}$ |
| **Box Height** | $\mathbf{20\text{ screen rows}}$ (Rows 97 through 116 inclusive) |
| **Box Width Calculation** | $K \pmod 4 = 97 \pmod 4 = 1$<br>$\text{Width} = 16 \times ((K \pmod 4) + 1) = 16 \times (1 + 1) = \mathbf{32\text{ pixels}}$ |
| **Words per Row** | $(K \pmod 4) + 1 = 1 + 1 = \mathbf{2\text{ 16-bit words per row}}$ |
| **Screen Memory Base Address** | $\text{SCREEN} + 32 \times K = 16384 + (32 \times 97) = 16384 + 3104 = \mathbf{19488}\ (0\text{x}4C20)$ |
| **Interactive Key Control** | Memory-mapped I/O at `KBD` ($24576 / 0\text{x}6000$).<br>Key Pressed ($\text{M} \neq 0$): draw black ($-1 / 0\text{xFFFF}$).<br>Key Released ($\text{M} = 0$): erase to background ($0 / 0\text{x}0000$). |

---

### 2. Part A – Hack Computer HDL Implementation

The Hack Computer platform was constructed using the three core hardware modules developed throughout the Nand to Tetris course:

#### 2.1 Memory Chip (`Memory.hdl`)
The Hack memory space spans addresses $0$ through $24576$ ($0\text{x}0000$ to $0\text{x}6000$):
- **RAM16K ($0 - 16383$ / $0\text{x}0000 - 0\text{x}3FFF$):** Selected when `address[14] == 0`.
- **Screen Memory Map ($16384 - 24575$ / $0\text{x}4000 - 0\text{x}5FFF$):** Selected when `address[14..13] == 10`.
- **Keyboard Memory Map ($24576$ / $0\text{x}6000$):** Selected when `address[14..13] == 11`. Read-only register holding ASCII code of key currently pressed.

In `Memory.hdl`, a `DMux4Way` routes the `load` input to either `RAM16K` or `Screen`, while `Mux4Way16` selects the proper chip output based on `address[13..14]`.

#### 2.2 Central Processing Unit (`CPU.hdl`)
The Hack CPU executes 16-bit instructions categorized into two formats:
- **A-instruction (`0vvv vvvv vvvv vvvv`):** Bit 15 is 0. The 15-bit constant is loaded into the A register (`ARegister`).
- **C-instruction (`111a c1c2c3c4c5c6 d1d2d3 j1j2j3`):** Bit 15 is 1. The instruction controls:
  1. **ALU Computation (`c1..c6`):** Operates on D-register and either A-register ($a=0$) or memory input `inM` ($a=1$).
  2. **Destination Routing (`d1..d3`):** Dictates whether ALU output writes to A, D, and/or memory (`writeM = 1`).
  3. **Branching / Jump Evaluation (`j1..j3`):** Combines the ALU status flags (`zr`, `ng`) with jump condition bits to decide whether the Program Counter (`PC`) should jump to `A` or increment.

#### 2.3 Top-Level Computer (`Computer.hdl`)
Integrates `ROM32K` (program memory), `CPU`, and `Memory` (data memory and memory-mapped I/O). The CPU's `pc` bus drives the ROM address, ROM outputs the `instruction`, CPU drives `addressM`, `outM`, and `writeM`, and `Memory` supplies `inM` back to the CPU.

#### 2.4 Official HDL Test Results
All chips were tested against the official test scripts using both the Hardware Simulator and cycle-accurate verification:
- `CPU.tst` vs `CPU.cmp`: **Comparison ended successfully** (PASSED)
- `Memory.tst` vs `Memory.cmp`: **Comparison ended successfully** (PASSED)
- `ComputerAdd.tst` vs `ComputerAdd.cmp`: **Comparison ended successfully** (PASSED)

---

### 3. Part B – Two-Pass Python Assembler (`assembler.py`)

The assembler converts Hack symbolic assembly (`.asm`) into binary machine code (`.hack`) through a robust two-pass architecture.

#### 3.1 Pass 1: Label Resolution & Source Cleaning
1. Strips all inline comments (`// ...`) and blank whitespace.
2. Identifies label declarations of the form `(LABEL)`.
3. Maps each label name to the current ROM address of the immediately following instruction without advancing the ROM counter.
4. Preserves the original file line numbers to provide accurate diagnostic reporting.

#### 3.2 Pass 2: Binary Code Generation & Variable Allocation
1. **A-instructions (`@value` or `@symbol`):**
   - If decimal integer, converted directly into 15-bit binary prefixed with `0`.
   - If predefined symbol (`R0`-`R15`, `SP`, `LCL`, `ARG`, `THIS`, `THAT`, `SCREEN`, `KBD`), resolved from the symbol table.
   - If label symbol, resolved to its recorded ROM address.
   - If new variable, assigned the next free RAM address starting at address 16 ($16, 17, 18, \dots$).
2. **C-instructions (`dest=comp;jump`):**
   - Parses `dest`, `comp`, and `jump` mnemonics.
   - Maps mnemonics into their corresponding binary patterns using lookup tables.
   - Generates the 16-bit format: `111` + `comp (7 bits)` + `dest (3 bits)` + `jump (3 bits)`.

#### 3.3 Assigned Additional Feature for $K = 97$ ($97 \pmod 3 = 1$)
- **Requirement:** For an incorrect instruction, print a clear error message with the line number (e.g. `Line 7: invalid instruction: ...`) instead of crashing.
- **Implementation:**
  - Strict validation is enforced during Pass 1 and Pass 2 for label syntax, destination registers, ALU computation mnemonics, and jump conditions.
  - When an error occurs, an `AssemblyError` is raised containing the source line number and description.
  - The assembler catches the error, outputs `Line <N>: invalid instruction (<details>)` to `stderr`, and terminates gracefully with exit code 1 without any Python traceback.

#### 3.4 Assembler Benchmark Verification
The assembler was tested against official Hack benchmark programs:
- `Add.asm` $\rightarrow$ `Add.hack` (6 instructions): **100% Exact Match**
- `Max.asm` $\rightarrow$ `Max.hack` (16 instructions): **100% Exact Match**
- `Rect.asm` $\rightarrow$ `Rect.hack` (25 instructions): **100% Exact Match**
- `Pong.asm` $\rightarrow$ `Pong.hack` (27,483 instructions): **100% Exact Match**

---

### 4. Part C – Box Drawing Program (`Box.asm`)

#### 4.1 Screen Memory Geometry for $K = 97$
- Hack screen dimensions: $256\text{ rows} \times 512\text{ columns}$ pixels.
- Memory map: $8192$ 16-bit words starting at `SCREEN` ($16384 / 0\text{x}4000$).
- Each horizontal row contains $32$ consecutive 16-bit words ($32 \times 16 = 512$ pixels).
- **Starting Row:** Row $97 \implies \text{Address} = 16384 + (32 \times 97) = \mathbf{19488}\ (0\text{x}4C20)$.
- **Width:** $32\text{ pixels}$ starting from left edge $\implies \mathbf{2\text{ consecutive words}}$ per row (Word 0: pixels $0..15$; Word 1: pixels $16..31$).
- **Height:** $\mathbf{20\text{ consecutive rows}}$ (Rows 97 to 116 inclusive).
- **Total Words Rendered:** $20 \times 2 = 40\text{ memory words}$ ($640\text{ pixels}$).

#### 4.2 Algorithm & Implementation (`Box.asm`)
The program runs in an infinite polling loop:
1. **Keyboard Sense:** Reads `RAM[24576]`. If $D \neq 0$ (key pressed), sets `@color` to $-1$ (`0xFFFF`, all black pixels). If $D == 0$ (key idle), sets `@color` to $0$ (`0x0000`, all white pixels).
2. **Pointer Initialization:** Loads base address $19488$ into `@rowAddr` and loop counter $20$ into `@rowCount`.
3. **Row Drawing Loop:**
   - Writes `@color` into `M[rowAddr]` (left 16 pixels).
   - Writes `@color` into `M[rowAddr + 1]` (right 16 pixels).
   - Advances `@rowAddr` by $32$ (`rowAddr = D + M`).
   - Decrements `@rowCount` by $1$ (`rowCount = M - 1`).
   - Repeats until `@rowCount == 0`.
4. **Reactivity:** Jumps back to step 1 immediately, producing an instantaneous appearance and disappearance of the box with zero screen tearing.

#### 4.3 Screen Buffer Verification Preview
The cycle-accurate CPU simulator verified the exact state of screen memory:
```text
Row  95: ....................................
Row  96: ....................................
Row  97: ################################.... <== Box Starts at Row 97 (32 px wide)
Row  98: ################################....
... (20 rows total) ...
Row 116: ################################.... <== Box Ends at Row 116
Row 117: ....................................
```

---

### 5. Programming Mistake Encountered & Solution

During initial testing of `Box.asm`, an instruction syntax error occurred:
```text
Line 76: invalid instruction (Unknown computation mnemonic 'M+D' in 'M=M+D')
```
**Cause:** In mathematics, addition is commutative ($M+D = D+M$). However, in the Hack CPU ALU hardware architecture, the multiplexer routes the D-register to the $x$-input and the Memory/A-register to the $y$-input. The Hack machine instruction set strictly defines `D+A` and `D+M` as valid mnemonics; `M+D` does not exist in the official specification.

**Correction:** Our Python assembler's line-numbered syntax verification ($K \pmod 3 = 1$) immediately caught this error at Line 76. The assembly code was updated to `M=D+M`. In addition, to prevent vertical drifting across multiple key presses, the pointer initialization `@19488` was explicitly scoped within the `(RENDER)` block so every drawing and clearing pass starts exactly at base row 97.

---

### 6. Individual Viva Voce Preparation

| Question | Clear Answer / Demonstration |
| :--- | :--- |
| **Q1. How is RAM vs Screen addressed in Memory.hdl?** | Bits `address[14..13]` act as the chip select: `00` & `01` address the 16K data RAM ($0 - 16383$), `10` addresses the 8K Screen buffer ($16384 - 24575$), and `11` addresses the Keyboard register ($24576$). |
| **Q2. How are variables vs labels resolved in assembler.py?** | In Pass 1, labels `(LABEL)` map to the ROM address of the next instruction without using RAM. In Pass 2, unknown symbolic `@var` identifiers are allocated sequential RAM registers starting at address 16. |
| **Q3. How is the K mod 3 = 1 feature implemented?** | The assembler validates each token against valid mnemonic dictionaries. If an invalid mnemonic or format is detected, an `AssemblyError` reports `Line <N>: invalid instruction: ...` to `stderr` and exits cleanly. |
| **Q4. How would you move the box down during viva?** | In `Box.asm`, change the base address `@19488` to `@(19488 + 32 * rows_to_shift)`. For instance, to shift the box down by 10 rows, change `@19488` to `@19808` ($19488 + 320$). |
| **Q5. How would you double the width of the box?** | Draw 4 consecutive words instead of 2 by adding writes to `rowAddr + 2` and `rowAddr + 3` inside `ROW_LOOP`. |
