import lexer


def main():
    with open("./something.js", "r") as file:
        file_content = file.read()

    for token in lexer.lex(file_content):
        print(f"{token.type.name}\t{token.content}")


if __name__ == "__main__":
    main()
