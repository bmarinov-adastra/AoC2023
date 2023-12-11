def process_file(filename):
    def convert_to_2_digits(line):
        if len(line) == 1:
            number = str(line) + str(line)
        else:
            number = str(line[0]) + str(line[-1])
        return number

    def convert_words_to_numbers(line):
        number_mapping = {
            "one": "1",
            "two": "2",
            "three": "3",
            "four": "4",
            "five": "5",
            "six": "6",
            "seven": "7",
            "eight": "8",
            "nine": "9"
        }

        word_to_compare = ""
        for char in line:
            if char.isalpha():
                word_to_compare += char
                word_to_compare = word_to_compare.lower()
                if any(number_mapping in word_to_compare for number_mapping in number_mapping):
                    for number in number_mapping:
                        if number in word_to_compare:
                            line = line.replace(word_to_compare, number_mapping[number])
                            break
            else:
                break

        word_to_compare = ""
        for char in line[::-1]:
            if char.isalpha():
                word_to_compare += char
                word_to_compare = word_to_compare.lower()
                if any(number_mapping in word_to_compare[::-1] for number_mapping in number_mapping):
                    for number in number_mapping:
                        if number in word_to_compare[::-1]:
                            line = line.replace(word_to_compare[::-1], number_mapping[number])
                            break
            else:
                break
        return line

    numbers = []
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.readlines()]
        for line in lines:
            print('-------------')
            print("Before: ", line)
            line = convert_words_to_numbers(line)
            print("In between: ", line)
            for char in line:
                if not char.isdigit():
                    line = line.replace(char, "")
            line = convert_to_2_digits(line)
            print("After: ", line)
            numbers.append(int(line))
    sum_of_numbers = sum(numbers)
    print(sum_of_numbers)

if __name__ == '__main__':
    process_file("trebuchet.txt")
