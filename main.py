from pprint import pprint

import lexer
import parser


def main():
    print("starting up...")
    with open("./something.js", "r") as file:
        file_content = file.read()

    print("read file. about to lex...")
    tokens = lexer.lex(file_content)

    print("lexed. parsing...")
    pprint(parser.parse(tokens))


if __name__ == "__main__":
    main()
