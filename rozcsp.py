#!/usr/bin/env python3

# Desc: ROZCSP - ROZEN CORPORATE STUPID PASSWORDS GENERATOR

import argparse
from wordlist import WordList
from stupidpassgen import StupidPasswordGenerator

INPUT_NUMBER_PASSWORD_LIMIT = 1000

def parse_args():
    parser = argparse.ArgumentParser(description = "ROZCSP v1.0 - ROZEN CORPORATE STUPID PASSWORDS")
    parser.add_argument("-i", "--input", required = True, help = "Input source file list")
    parser.add_argument("-o", "--output", required = False, help = "Output file with generated stupid passwords")
    parser.add_argument("-d", "--debug", required = False, action="store_true", help = "Print memory usage")

    return parser.parse_args()

def generate_passwords(word_list, output_file, debug) -> int:
    stupid_pass_gen = StupidPasswordGenerator(debug)
    return stupid_pass_gen.run(word_list, output_file)

def main(args):
    word_list = WordList()

    #read input file line by line and store words in the array
    try:
        with open(args.input, "r") as f:
            print("Reading input file...")
            for line in f:
                word_list.add_word(line.strip())

            read_passwords_number = word_list.get_number_of_words()
            print("Number of words imported from input file: {}".format(read_passwords_number))

            if read_passwords_number > INPUT_NUMBER_PASSWORD_LIMIT:
                print("Number of passwords in input file might be too big. Set limit is: {}".format(INPUT_NUMBER_PASSWORD_LIMIT))

                #ask user if he wants to continue
                answer = input("Do you want to continue? [y/n]: ")
                if answer != "y":
                    exit(1)

            return generate_passwords(word_list, args.output, args.debug)        
    except FileNotFoundError:
        print("Input file not found")
        exit(1)
    except Exception as e:
        print("Error: {}".format(e))
        exit(1)

if __name__ == "__main__":
    exit(main(parse_args()))