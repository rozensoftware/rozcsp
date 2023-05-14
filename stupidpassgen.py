from wordlist import WordList
from datetime import datetime
import utils


class StupidPasswordGenerator:
    def __init__(self, debug):
        # Warn user when memory usage is higher than this value in MB
        self.warn_when_memory_usage = 1024 * 2
        self.debug = debug
        self.word_lists = []
        self.tmp_word_list = []
        self.mod_funcs = [
            self.__make_first_letter_capital,
            self.__add_exclamation_mark_at_the_beginning,
            self.__add_exclamation_mark_at_the_end,
            self.__change_similar_letters,
            self.__change_similar_letter_a,
            self.__change_similar_letter_e,
            self.__change_similar_letter_i,
            self.__change_similar_letter_o,
            self.__change_similar_letter_s,
        ]

    def remove_redundant_words(self):
        """Remove redundant words from word lists"""

        print("Removing redundant words...")

        result = []
        seen = set()

        arrays = self.word_lists.copy()
        for array in arrays:
            new_array = []

            for word in array.words_list:
                if word not in seen:
                    seen.add(word)
                    new_array.append(word)

            result.append(new_array)

        return result

    def count_passwords(self, arrays):
        """Count number of generated passwords"""

        c = 0

        for array in arrays:
            c += len(array)

        return c

    def add_number_extension(self, arrays, max_number: int):
        """Add number extension to passwords"""

        print("Adding number extension to passwords (up to {})...".format(max_number))

        result = []

        for array in arrays:
            for word in array:
                for n in range(0, max_number):
                    result.append(word + str(n))

        # Next add extension from year 'from_year' to current year
        from_year = 1990
        now = datetime.now()

        for array in arrays:
            for word in array:
                for n in range(from_year, now.year + 1):
                    result.append(word + str(n))

        return result

    def save_arrays_to_file(self, arrays, output_file):
        """Save generated passwords to a file"""

        print("Saving generated passwords to file: {}".format(output_file))

        with open(output_file, "w") as f:
            for array in arrays:
                for word in array:
                    f.write(word + "\n")

        print("Number of saved passwords: {}".format(self.count_passwords(arrays)))

    def run(self, initial_word_list, output_file=None) -> int:
        # Store current time in milliseconds
        start_time = datetime.now()

        print("Generating stupid passwords...")

        self.word_lists.append(initial_word_list)

        for p in range(0, len(self.mod_funcs)):
            print("Pass: {}".format(p))

            if self.debug:
                print("Memory used: {} MB".format(utils.memory_usage()))

            for pass_word_list in self.word_lists:
                f_idx = 0

                for mod_func in self.mod_funcs:
                    new_word_list = None

                    for password in pass_word_list.get_word_without_function_idx(f_idx):
                        if new_word_list == None:
                            new_word_list = WordList()
                            self.tmp_word_list.append(new_word_list)

                        new_password = mod_func(password)
                        if new_password != password:
                            new_word_list.add_word(new_password, f_idx)

                    f_idx += 1

            for l in self.tmp_word_list:
                if l.get_number_of_words() > 0:
                    self.word_lists.append(l)

            self.tmp_word_list = []

        usage_memory = utils.memory_usage()
        if usage_memory > self.warn_when_memory_usage:
            print("WARNING: Memory usage is high: {} MB".format(usage_memory))
            answer = input("Do you want to continue? [y/n]: ")
            if answer != "y":
                print("Aborting...")
                return 1
            
        result = self.remove_redundant_words()
        if self.debug:
            print("Memory used: {} MB".format(utils.memory_usage()))

        result.append(self.add_number_extension(result, 20))
        if self.debug:
            print("Memory used: {} MB".format(utils.memory_usage()))

        print("Number of generated passwords: {}".format(self.count_passwords(result)))

        if output_file is not None:
            self.save_arrays_to_file(result, output_file)
        else:
            print("Generated passwords:")

            for array in result:
                for word in array:
                    print(word)

        # Print elapsed time since start
        end_time = datetime.now()
        print("Elapsed time: {}".format(end_time - start_time))
        return 0
    
    def __make_first_letter_capital(self, password):
        """Make first letter of password capital"""
        return password[0].upper() + password[1:]

    def __change_similar_letter_a(self, password):
        """Change letter a to @"""
        return password.replace("a", "@")

    def __change_similar_letter_e(self, password):
        """Change letter e to 3"""
        return password.replace("e", "3")

    def __change_similar_letter_i(self, password):
        """Change letter i to 1"""
        return password.replace("i", "1")

    def __change_similar_letter_o(self, password):
        """Change letter o to 0"""
        return password.replace("o", "0")

    def __change_similar_letter_s(self, password):
        """Change letter s to $"""
        return password.replace("s", "$")

    def __add_exclamation_mark_at_the_end(self, password):
        """Add exclamation mark at the end of password"""

        # check if password already ends with exclamation mark
        if password[-1] == "!":
            return password
        else:
            return password + "!"

    def __add_exclamation_mark_at_the_beginning(self, password):
        """Add exclamation mark at the beginning of password"""

        # check if password already starts with exclamation mark
        if password[0] == "!":
            return password
        else:
            return "!" + password

    def __change_similar_letters(self, password):
        """Change similar letters in password to looking like numbers or special characters"""
        similar_letters_dict = {"a": "@", "e": "3", "i": "1", "o": "0", "s": "$"}
        for letter in password:
            lo_letter = letter.lower()
            if lo_letter in similar_letters_dict:
                password = password.replace(letter, similar_letters_dict[lo_letter])

        return password
