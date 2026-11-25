#!/usr/bin/env python3
"""
Hack Computer Assembler (Nand to Tetris - Project 6 / Capstone)
Author: Archita (Roll No: 2501730197)
Personal Number: K = 97 (97 mod 3 = 1)

Assigned Feature (K mod 3 = 1):
For an incorrect instruction, print a clear error message with the line number
(e.g., Line 7: invalid instruction: ...) instead of crashing with a Python traceback.

Additional Features Supported:
- Full symbol table export to 'symbols.txt'
- Warning for duplicate labels
- Supports command line execution:
    python assembler.py <prog.asm> [output.hack] [K]
"""

import sys
import os
import re

# Predefined Symbols in Hack Platform
PREDEFINED_SYMBOLS = {
    'SP': 0,
    'LCL': 1,
    'ARG': 2,
    'THIS': 3,
    'THAT': 4,
    'R0': 0, 'R1': 1, 'R2': 2, 'R3': 3,
    'R4': 4, 'R5': 5, 'R6': 6, 'R7': 7,
    'R8': 8, 'R9': 9, 'R10': 10, 'R11': 11,
    'R12': 12, 'R13': 13, 'R14': 14, 'R15': 15,
    'SCREEN': 16384,
    'KBD': 24576
}

# Computation code mapping: 7-bit binary (a c1 c2 c3 c4 c5 c6)
COMP_TABLE = {
    # a = 0 (operations on D and A)
    "0":   "0101010",
    "1":   "0111111",
    "-1":  "0111010",
    "D":   "0001100",
    "A":   "0110000",
    "!D":  "0001101",
    "!A":  "0110001",
    "-D":  "0001111",
    "-A":  "0110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "D+A": "0000010",
    "D-A": "0010011",
    "A-D": "0000111",
    "D&A": "0000000",
    "D|A": "0010101",

    # a = 1 (operations on D and M)
    "M":   "1110000",
    "!M":  "1110001",
    "-M":  "1110011",
    "M+1": "1110111",
    "M-1": "1110010",
    "D+M": "1000010",
    "D-M": "1010011",
    "M-D": "1000111",
    "D&M": "1000000",
    "D|M": "1010101"
}

# Destination code mapping: 3-bit binary (d1 d2 d3 for A, D, M)
DEST_TABLE = {
    None:  "000",
    "":    "000",
    "M":   "001",
    "D":   "010",
    "MD":  "011",
    "A":   "100",
    "AM":  "101",
    "AD":  "110",
    "AMD": "111"
}

# Jump code mapping: 3-bit binary (j1 j2 j3)
JUMP_TABLE = {
    None:  "000",
    "":    "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

VALID_SYMBOL_REGEX = re.compile(r'^[a-zA-Z_.$:][a-zA-Z0-9_.$:]*$')


class AssemblyError(Exception):
    def __init__(self, line_num, message):
        self.line_num = line_num
        self.message = message
        super().__init__(f"Line {line_num}: invalid instruction: {message}")


class HackAssembler:
    def __init__(self, k_val=97):
        self.k = k_val
        self.symbol_table = dict(PREDEFINED_SYMBOLS)
        self.variable_address = 16
        self.labels = {}
        self.variables = {}
        self.errors = []
        self.warnings = []

    def clean_line(self, raw_line):
        """Strip comments and surrounding whitespace."""
        line = raw_line.split('//')[0].strip()
        # Remove intra-instruction whitespace
        return "".join(line.split())

    def first_pass(self, lines):
        """
        First Pass:
        Parse labels like (LABEL), record ROM instruction address,
        and track original line numbers for diagnostics.
        """
        rom_address = 0
        cleaned_instructions = []

        for line_idx, raw_line in enumerate(lines, start=1):
            line = self.clean_line(raw_line)
            if not line:
                continue

            if line.startswith('(') and line.endswith(')'):
                label_name = line[1:-1].strip()
                if not label_name or not VALID_SYMBOL_REGEX.match(label_name):
                    msg = f"Invalid label syntax '{line}'"
                    self.errors.append((line_idx, msg, raw_line.strip()))
                    continue

                if label_name in self.symbol_table:
                    warn_msg = f"Duplicate label declaration '({label_name})'"
                    self.warnings.append((line_idx, warn_msg))
                    if self.k % 3 == 2:
                        print(f"Warning: Line {line_idx}: {warn_msg}", file=sys.stderr)

                self.symbol_table[label_name] = rom_address
                self.labels[label_name] = rom_address
            else:
                cleaned_instructions.append((line_idx, line, raw_line.strip()))
                rom_address += 1

        return cleaned_instructions

    def parse_a_instruction(self, line_num, symbol_str, raw_line):
        """Parse @value or @symbol instruction into 16-bit binary."""
        if not symbol_str:
            raise AssemblyError(line_num, f"Empty address in A-instruction '{raw_line}'")

        if symbol_str.isdigit():
            val = int(symbol_str)
            if val < 0 or val > 32767:
                raise AssemblyError(line_num, f"Address value {val} out of 15-bit range [0, 32767]")
            return f"0{val:015b}"
        else:
            if not VALID_SYMBOL_REGEX.match(symbol_str):
                raise AssemblyError(line_num, f"Invalid symbol name '{symbol_str}' in '{raw_line}'")

            if symbol_str not in self.symbol_table:
                self.symbol_table[symbol_str] = self.variable_address
                self.variables[symbol_str] = self.variable_address
                self.variable_address += 1

            addr = self.symbol_table[symbol_str]
            return f"0{addr:015b}"

    def parse_c_instruction(self, line_num, line, raw_line):
        """Parse dest=comp;jump C-instruction into 16-bit binary."""
        dest_part = ""
        comp_part = ""
        jump_part = ""

        # Syntax check for '=' and ';'
        remaining = line
        if '=' in remaining:
            parts = remaining.split('=', 1)
            dest_part = parts[0]
            remaining = parts[1]

        if ';' in remaining:
            parts = remaining.split(';', 1)
            comp_part = parts[0]
            jump_part = parts[1]
        else:
            comp_part = remaining

        # Validate comp
        if comp_part not in COMP_TABLE:
            raise AssemblyError(line_num, f"Unknown computation mnemonic '{comp_part}' in '{raw_line}'")

        # Validate dest (normalize ordering if standard permutation)
        norm_dest = dest_part
        if norm_dest and norm_dest not in DEST_TABLE:
            # Check if valid set of {A, D, M}
            sorted_chars = "".join(sorted(norm_dest))
            alt_map = {"A": "A", "D": "D", "M": "M", "AD": "AD", "AM": "AM", "DM": "MD", "ADM": "AMD"}
            if sorted_chars in alt_map:
                norm_dest = alt_map[sorted_chars]
            else:
                raise AssemblyError(line_num, f"Unknown destination mnemonic '{dest_part}' in '{raw_line}'")

        # Validate jump
        if jump_part and jump_part not in JUMP_TABLE:
            raise AssemblyError(line_num, f"Unknown jump mnemonic '{jump_part}' in '{raw_line}'")

        comp_bits = COMP_TABLE[comp_part]
        dest_bits = DEST_TABLE[norm_dest]
        jump_bits = JUMP_TABLE[jump_part]

        return f"111{comp_bits}{dest_bits}{jump_bits}"

    def assemble(self, asm_code):
        """Assemble Hack assembly string into list of 16-bit binary instructions."""
        lines = asm_code.splitlines()
        instructions = self.first_pass(lines)

        binary_output = []
        for line_num, line, raw_line in instructions:
            try:
                if line.startswith('@'):
                    symbol_str = line[1:]
                    code = self.parse_a_instruction(line_num, symbol_str, raw_line)
                else:
                    code = self.parse_c_instruction(line_num, line, raw_line)
                binary_output.append(code)
            except AssemblyError as err:
                self.errors.append((line_num, err.message, raw_line))

        if self.errors:
            # Report formatted errors without crashing
            for line_num, msg, raw in self.errors:
                print(f"Line {line_num}: invalid instruction ({msg})", file=sys.stderr)
            return None

        return binary_output

    def export_symbols(self, filepath="symbols.txt"):
        """Save labels and variables with their addresses."""
        with open(filepath, "w") as f:
            f.write(f"# Symbol Table for Hack Assembly (K = {self.k})\n")
            f.write("----------------------------------------\n")
            f.write("SYMBOL NAME                  ADDRESS (DEC)  ADDRESS (HEX)\n")
            f.write("----------------------------------------\n")
            for sym in sorted(self.symbol_table.keys()):
                addr = self.symbol_table[sym]
                f.write(f"{sym:<28} {addr:<14} 0x{addr:04X}\n")


def assemble_file(input_file, output_file=None, k_val=97):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        return False

    if output_file is None:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}.hack"

    with open(input_file, "r") as f:
        asm_code = f.read()

    assembler = HackAssembler(k_val=k_val)
    binary_lines = assembler.assemble(asm_code)

    if binary_lines is None:
        print(f"\nAssembly failed with {len(assembler.errors)} error(s).", file=sys.stderr)
        return False

    with open(output_file, "w") as f:
        for code in binary_lines:
            f.write(f"{code}\n")

    # Export symbol table
    symbols_path = os.path.join(os.path.dirname(output_file) or ".", "symbols.txt")
    assembler.export_symbols(symbols_path)

    print(f"Success: Assembled '{input_file}' -> '{output_file}' ({len(binary_lines)} instructions).")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py <input.asm> [output.hack] [K]")
        print("Example: python assembler.py Box.asm Box.hack 97")
        sys.exit(1)

    in_file = sys.argv[1]
    out_file = None
    k_arg = 97

    if len(sys.argv) >= 3:
        if sys.argv[2].isdigit():
            k_arg = int(sys.argv[2])
        else:
            out_file = sys.argv[2]

    if len(sys.argv) >= 4 and sys.argv[3].isdigit():
        k_arg = int(sys.argv[3])

    success = assemble_file(in_file, out_file, k_val=k_arg)
    sys.exit(0 if success else 1)
