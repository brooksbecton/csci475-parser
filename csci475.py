from Tokenizer import Tokenizer


if __name__ == '__main__':
    mrT = Tokenizer()

    mrT.get_tokens_from_file()

    mrT.print_pretty_tokens()
    mrT.print_pretty_symbol_table()