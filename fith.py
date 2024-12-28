import os
from sys import argv
from subprocess import run as console

START_UNDERLINE = "\x1b[4m"
END_UNDERLINE = "\x1b[24m"

RED = "\x1b[31m"
GREEN = "\x1b[32m"
RESET = "\x1b[0m"

def compile(file_name: str, output_name: str) -> None:
    with open(file_name, "r") as file:
        file_contents = [op for op in file.read().split()]

    with open("output.asm", "w") as out:
        out.write("extern printf\n")
        out.write("section .text\n")
        out.write("global main\n")
        out.write("main:\n")

        for op in file_contents:
            match op:
                case '+':
                    out.write("\t;; PLUS\n")
                    out.write("\tpop rax\n")
                    out.write("\tpop rbx\n")
                    out.write("\tadd rax, rbx\n")
                    out.write("\tpush rax\n")
                case '-':
                    out.write("\t;; MINUS\n")
                    out.write("\tpop rax\n")
                    out.write("\tpop rbx\n")
                    out.write("\tsub rbx, rax\n")
                    out.write("\tpush rbx\n")
                case '*':
                    out.write("\t;; MULT\n")
                    out.write("\tpop rax\n")
                    out.write("\tpop rbx\n")
                    out.write("\timul rax, rbx\n")
                    out.write("\tpush rax\n")
                case '/':
                    out.write("\t;; DIV\n")
                    out.write("\tpop rcx\n") # Dividend
                    out.write("\tpop rax\n") # Divisor
                    out.write("\txor rdx, rdx\n") # Clear the bits in rdx (part of the dividend)
                    out.write("\tdiv rcx\n")
                    out.write("\tpush rax\n")
                case ".":
                    out.write("\t;; OUT\n")
                    out.write("\tmov rdi, printf_format\n")
                    out.write("\tpop rsi\n")
                    out.write("\txor rax, rax\n")
                    out.write("\tand rsp, -16\n")
                    out.write("\tcall printf\n")
                case _:
                    num = int(op) # will purposefully crash if its an invalid OP
                    out.write(f"\tpush {num}\n")

        out.write("\t;; exit successfully\n")
        out.write("\tmov rax, 60\n")
        out.write("\tmov rdi, 0\n")
        out.write("\tsyscall")
        
        out.write("\n\nsection .data\n")
        out.write("\tprintf_format: db '%x',10,0\n")

    console(["nasm", "-felf64", "-o", "output.o", "output.asm"])
    console(["gcc", "-no-pie", "-o", output_name, "output.o"])
    console(["rm", "output.asm", "output.o"])
    os.system("clear")

def usage(err: str) -> None:
    print(f"{RED}{err}{RESET}")
    print(f"{START_UNDERLINE}Usage: {argv[0]} <file.fth> [output name]{END_UNDERLINE}")
    print("\tfile.fth: Fith file to compile")
    print("\toutput name: OPTIONAL name to give the finished executable (default = \"output\")\n")

if __name__ == "__main__":
    # argv[0] = fith.py
    # argv[1] = file.fth
    # argv[2] = output name
    if len(argv) < 2 or len(argv) > 3:
        usage("\nERROR: Incorrect amount of arguments provided!")
        exit(1)

    file_ext = argv[1].split(".")[1]
    if file_ext != "fth":
        usage(f"\nERROR: Invalid file format. Expected \".fth\", given \".{file_ext}\"")
        exit(1)

    if len(argv) == 3:
        output_name = argv[2]
    else:
        output_name = "output"

    compile(argv[1], output_name)
