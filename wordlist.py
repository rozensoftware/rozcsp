class WordList:
    def __init__(self) -> None:
        self.words_list = []
        self.function_idx = []
        
    def add_word(self, word, idx = -1):
        if not word in self.words_list:
            self.words_list.append(word)
            if idx != -1 and not idx in self.function_idx:
                self.function_idx.append(idx)

    def has_word(self, word) -> bool:
        return word in self.words_list
                                   
    def get_number_of_words(self):
        return len(self.words_list)
        
    def get_word_without_function_idx(self, idx) -> str:
        if idx not in self.function_idx:
            self.function_idx.append(idx)
            for word in self.words_list:
                yield word
        else:
            return None