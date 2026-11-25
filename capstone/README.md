# Nand to Tetris – I (ETCNTC301 / ETCCNT301)
## Capstone Project: Make the Computer Draw a Box
**School of Engineering & Technology, K.R. Mangalam University**

---

### 🌐 Live Deployment & Project Links
- 🚀 **Live Interactive Dashboard (Vercel):** [https://archita-capstone.vercel.app](https://archita-capstone.vercel.app)
- 🌐 **Live Interactive Dashboard (GitHub Pages):** [https://archita2501730197.github.io/NAND-TO-TETRIS/](https://archita2501730197.github.io/NAND-TO-TETRIS/)
- 📦 **GitHub Repository:** [https://github.com/archita2501730197/NAND-TO-TETRIS](https://github.com/archita2501730197/NAND-TO-TETRIS)

---

### Student Information
- **Name:** Archita
- **Roll Number:** 2501730197
- **Course & Branch:** B.Tech CSE (AI / ML)
- **Semester:** III
- **Personal Number ($K$):** **97** (last two digits of 2501730197)

---

### Project Parameters for $K = 97$

| Parameter | Formula / Condition | Value for $K = 97$ |
| :--- | :--- | :--- |
| **Personal Number ($K$)** | Last two digits of Roll Number | **97** |
| **Assembler Feature ($K \pmod 3$)** | $97 \pmod 3 = 1$ | **Line-numbered error reporting** (e.g. `Line 7: invalid instruction`) instead of crashing |
| **Box Starting Row** | Row $K$ | **Row 97** |
| **Box Height** | Fixed specification | **20 screen rows** (Rows 97 to 116 inclusive) |
| **Box Width Calculation** | $16 \times ((K \pmod 4) + 1)$ | $97 \pmod 4 = 1 \implies 16 \times (1 + 1) = \mathbf{32\text{ pixels}}$ |
| **Words per Row** | $(K \pmod 4) + 1$ | **2 words** (Word 0 & Word 1 from left edge) |
| **Screen Base Memory Address** | $\text{SCREEN} + 32 \times K$ | $16384 + (32 \times 97) = 16384 + 3104 = \mathbf{19488}\ (0\text{x}4C20)$ |
| **Interactive Key Control** | Memory-mapped I/O at `KBD` (24576) | Key Pressed ($\text{M} \neq 0$): draw black box ($-1$).<br>Key Released ($\text{M} = 0$): erase box ($0$). |

---

### Directory & File Structure

```text
capstone/
├── CPU.hdl                     # Hack Central Processing Unit implementation
├── Memory.hdl                  # Memory chip (RAM16K + Screen + Keyboard)
├── Computer.hdl                # Top-level Hack Computer chip
├── CPU.tst, CPU.cmp            # Official CPU test script & comparison file
├── Memory.tst, Memory.cmp      # Official Memory test script & comparison file
├── ComputerAdd.tst, .cmp       # Official ComputerAdd test script & comparison file
├── assembler.py                # Two-pass Python Assembler with K mod 3 = 1 feature
├── symbols.txt                 # Exported symbol table (labels & variables)
├── Box.asm                     # Hack Assembly program tailored for K = 97 (32x20 box at row 97)
├── Box.hack                    # Assembled 16-bit binary machine code
├── Add.asm, Add.hack           # Benchmark test program & binary
├── Max.asm, Max.hack           # Benchmark test program & binary
├── Rect.asm, Rect.hack         # Benchmark test program & binary
├── Pong.asm, Pong.hack         # Benchmark test program & binary
├── verify_capstone.py          # Complete test runner & CPU simulator
├── build_capstone_pdf.py       # Generates the official printable PDF report
├── Capstone_Report.md          # 3-4 page project report in Markdown
├── Archita_2501730197_Capstone_Report.pdf  # Generated submission PDF report
└── README.md                   # This documentation file
```

---

### How to Run and Test

#### 1. Run Complete Automated Verification Suite
Runs all tests across HDL logic, assembler benchmarks, $K \pmod 3 = 1$ syntax error handling, and simulates `Box.hack` on the Hack screen:
```bash
python3 verify_capstone.py
```

#### 2. Run the Python Assembler
Convert any `.asm` file to `.hack`:
```bash
python3 assembler.py Box.asm Box.hack 97
```
This generates `Box.hack` and exports all symbol addresses to `symbols.txt`.

#### 3. Test Invalid Instruction Error Reporting ($K \pmod 3 = 1$)
Feed an invalid assembly line to observe clear, non-crashing diagnostics:
```bash
echo "Line7_Invalid_Instruction" > bad.asm
python3 assembler.py bad.asm bad.hack 97
```
Output:
```text
Line 1: invalid instruction (Unknown computation mnemonic 'Line7_Invalid_Instruction' in 'Line7_Invalid_Instruction')
Assembly failed with 1 error(s).
```

#### 4. Load in Official Hardware Simulator / CPU Emulator
1. **Hardware Simulator**:
   - Load `CPU.tst`, `Memory.tst`, or `ComputerAdd.tst`.
   - Run in fast mode. Output displays `Comparison ended successfully`.
2. **CPU Emulator**:
   - Load `Box.hack` (or load `Computer.hdl` and then `Box.hack`).
   - Run at fast speed (`No display` or `Fast`).
   - Press and hold any key on the simulator keyboard: the 32×20 black box immediately appears at row 97.
   - Release the key: the box immediately clears back to white.

---

### Viva Preparation (Quick Review)

1. **How does Memory.hdl direct addresses?**
   - Address bits `14` and `13` split the address space:
     - `00` or `01` ($0 - 16383$): RAM16K
     - `10` ($16384 - 24575$): Screen memory map (8K words)
     - `11` ($24576$): Keyboard register (read-only)
2. **How does CPU.hdl handle A- vs C-instructions?**
   - Bit 15 determines instruction type:
     - Bit $15 = 0$: A-instruction, loads bits $0..14$ into the A register.
     - Bit $15 = 1$: C-instruction, controls ALU computation (`c1..c6`), destination routing (`d1..d3`), and jump conditions (`j1..j3`).
3. **How does your Python assembler work in two passes?**
   - **Pass 1:** Cleans comments and blank lines, locates `(LABEL)` definitions, and maps them to ROM addresses without advancing the ROM program counter.
   - **Pass 2:** Translates instructions into 16-bit binary codes. Resolves labels, assigns new variable symbols to RAM addresses starting at 16, and maps C-instruction mnemonics.
4. **How did you implement the extra feature for $K = 97$?**
   - $97 \pmod 3 = 1$: Validates destination, computation, and jump fields against official specification dictionaries. When an invalid mnemonic or format is found, it raises an `AssemblyError` with the line number and prints `Line <N>: invalid instruction: ...` rather than throwing an unhandled exception.
5. **How does Box.asm work and how would you move the box down during viva?**
   - The box starts at address `19488` ($16384 + 32 \times 97$).
   - To move the box down by $N$ rows on the spot during viva: change `@19488` to `@(19488 + 32 * N)`. For example, to move it down 10 rows, change `@19488` to `@19808`.
