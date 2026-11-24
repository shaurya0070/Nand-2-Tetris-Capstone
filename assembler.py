#!/usr/bin/env python3
"""Two-pass assembler for the Nand2Tetris Hack computer.

Usage:
    python assembler.py input.asm [output.hack]

Duplicate label declarations produce a warning; the first definition is retained.
"""
from pathlib import Path
import re
import sys

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    "SCREEN": 16384, "KBD": 24576,
}
PREDEFINED.update({f"R{i}": i for i in range(16)})

DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001",
    "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111",
    "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010",
    "D-A": "0010011", "D-M": "1010011",
    "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000",
    "D|A": "0010101", "D|M": "1010101",
}
SYMBOL_RE = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AssemblyError(Exception):
    pass


def clean_source(path):
    """Return (original_line_number, instruction) pairs."""
    result = []
    with open(path, "r", encoding="utf-8") as source:
        for line_no, raw in enumerate(source, 1):
            line = raw.split("//", 1)[0].strip()
            if line:
                result.append((line_no, re.sub(r"\s+", "", line)))
    return result


def first_pass(lines):
    """Build label table; duplicate labels warn and keep the first address."""
    symbols = PREDEFINED.copy()
    instructions = []
    rom_address = 0

    for line_no, line in lines:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if not label or not SYMBOL_RE.match(label):
                raise AssemblyError(f"Line {line_no}: invalid label declaration")
            if label in symbols:
                print(f"Warning: Line {line_no}: duplicate label '{label}' "
                      f"(first definition/address retained)")
            else:
                symbols[label] = rom_address
        else:
            if "(" in line or ")" in line:
                raise AssemblyError(f"Line {line_no}: invalid label syntax")
            instructions.append((line_no, line))
            rom_address += 1

    if rom_address > 32768:
        raise AssemblyError("Program exceeds the 32K ROM address space")
    return symbols, instructions


def assemble(lines):
    symbols, instructions = first_pass(lines)
    next_variable = 16
    output = []

    for line_no, instruction in instructions:
        try:
            if instruction.startswith("@"):
                value = instruction[1:]
                if not value:
                    raise AssemblyError("empty A-instruction")
                if value.isdigit():
                    address = int(value)
                else:
                    if not SYMBOL_RE.match(value):
                        raise AssemblyError(f"invalid symbol '{value}'")
                    if value not in symbols:
                        if next_variable > 32767:
                            raise AssemblyError("no available RAM addresses for variables")
                        symbols[value] = next_variable
                        next_variable += 1
                    address = symbols[value]
                if not 0 <= address <= 32767:
                    raise AssemblyError(f"A-instruction value {address} is outside 0..32767")
                output.append(f"{address:016b}")
            else:
                if instruction.count("=") > 1 or instruction.count(";") > 1:
                    raise AssemblyError("malformed C-instruction")
                if ";" in instruction:
                    left, jump = instruction.split(";", 1)
                else:
                    left, jump = instruction, ""
                if "=" in left:
                    dest, comp = left.split("=", 1)
                else:
                    dest, comp = "", left
                if comp not in COMP:
                    raise AssemblyError(f"unknown computation '{comp}'")
                if dest not in DEST:
                    raise AssemblyError(f"invalid destination '{dest}'")
                if jump not in JUMP:
                    raise AssemblyError(f"invalid jump '{jump}'")
                output.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
        except AssemblyError as exc:
            raise AssemblyError(f"Line {line_no}: {exc}") from exc

    return output, symbols


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python assembler.py input.asm [output.hack]")
        raise SystemExit(2)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) == 3 else input_path.with_suffix(".hack")

    try:
        lines = clean_source(input_path)
        machine_code, symbols = assemble(lines)
        output_path.write_text("\n".join(machine_code) + "\n", encoding="utf-8")
        print(f"Success: wrote {len(machine_code)} instructions to {output_path}")
        print("Duplicate-label warning: enabled (first definition is retained).")
    except (OSError, AssemblyError) as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
