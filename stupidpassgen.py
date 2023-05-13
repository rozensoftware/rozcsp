from wordlist import WordList
from datetime import datetime
import utils

class StupidPasswordGenerator:
    def __init__(self, debug):
        self.debug = debug
        self.word_lists = []
        self.tmp_word_list = []
        self.mod_funcs = [self.__make_first_letter_capital, 
                          self.__change_similar_letters,
                          self.__change_similar_letter_a,
                          self.__change_similar_letter_e,
                          self.__change_similar_letter_i,
                          self.__change_similar_letter_o,
                          self.__change_similar_letter_s]

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

        #Next add extension from year 1972 to current year
        now = datetime.now()

        for array in arrays:
            for word in array:
                for n in range(1972, now.year + 1):
                    result.append(word + str(n))

        return result
    
    def save_arrays_to_file(self, arrays, output_file):
        """Save generated passwords to file"""

        print("Saving generated passwords to file: {}".format(output_file))

        with open(output_file, "w") as f:
            for array in arrays:
                for word in array:
                    f.write(word + "\n")

        print("Number of saved passwords: {}".format(self.count_passwords(arrays)))

    def run(self, initial_word_list, output_file = None):
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

    def __make_first_letter_capital(self, password):
        """Make first letter of password capital"""
        return password[0].upper() + password[1:]
    
    def __change_similar_letter_a(self, password):
        """Change letter a to @"""
        return password.replace('a', '@')

    def __change_similar_letter_e(self, password):
        """Change letter e to 3"""
        return password.replace('e', '3')

    def __change_similar_letter_i(self, password):
        """Change letter i to 1"""
        return password.replace('i', '1')

    def __change_similar_letter_o(self, password):
        """Change letter o to 0"""
        return password.replace('o', '0')

    def __change_similar_letter_s(self, password):
        """Change letter s to 5"""
        return password.replace('s', '5')
        
    def __change_similar_letters(self, password):
        """Change similar letters in password to looking like numbers or special characters"""
        similar_letters_dict = {'a': '@', 'e': '3', 'i': '1', 'o': '0', 's': '5'}
        for letter in password:
            lo_letter = letter.lower()
            if lo_letter in similar_letters_dict:
                password = password.replace(letter, similar_letters_dict[lo_letter])

        return password