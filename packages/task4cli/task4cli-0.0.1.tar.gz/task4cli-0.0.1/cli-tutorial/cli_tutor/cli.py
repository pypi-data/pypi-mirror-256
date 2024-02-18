import argparse
from collect.coll import computing
from pathlib import Path


def process_string(input_string):
    print(f"Processing string: {computing(input_string)}")

def process_file(input_path):
    input_file = 'C:\\Users\\Admin\\Desctop\\Task 4 CLI\\txtfile.txt'
    input_path = Path(input_file)
    with open(input_path, 'r') as file:
        if file:
            content = file.read()
            print(f"Processing file content: {computing(content)}")
        else:
            pass


def main():
    parser = argparse.ArgumentParser(description='Process text input.')
    parser.add_argument('--string', help='String to process.')
    parser.add_argument('--file', help='File with text to process.')

    args = parser.parse_args()

    if args.string and args.file:
        f_result = computing(process_file(args.file))
        return print(f_result)
    elif args.file:
        f_result = computing(process_file(args.file))
        return print(f_result)
    elif args.string:
        s_result = computing(process_string(args.string))
        return print(s_result)
    else:
        return print("Error: Either --string or --file must be specified.")


if __name__ == "__main__":
    main()


# Запуск тестів з pytest
if __name__ == '__main__':
    main()
