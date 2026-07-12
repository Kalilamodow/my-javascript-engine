import rich

import lexer
import parser


def main():
    print("starting up...")
    with open("./something.js", "r") as file:
        file_content = file.read()

    print("read file. about to lex...")
    tokens = lexer.lex(file_content)

    print("lexed. parsing...")
    rich.print(parser.parse(tokens))


if __name__ == "__main__":
    main()
