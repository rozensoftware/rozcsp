# rozcsp

Stupid Corporate Password Generator

Version: 1.0

## Description

The program generates simple passwords created quickly by people due to corporate requirements. Often such passwords are not particularly calculating and contain combinations of previous passwords. Frequent changes of passwords in companies are an annoying process, so the passwords quickly invented can be somewhat predictable. This program is the answer to that. You can generate combinations of passwords that can be used in a dictionary attack.

It should work on every system in which Python is installed.

## Building

Python3 is required. Additional psutil package is needed also:

```bash
sudo apt install python3-psutil
```

## Usage

In the input file, passwords should be specified, which will be transformed to obtain various permutations of them.

```bash
./rozcsp -i passtempl.txt -o pswds.txt
```

*-i* - input file with basic passwords with words e.g.: my_secret_pass, pass12, winter, john, etc. Keep all words lower case. Try to have number of input words/passwords under a thousand because output file might be big. It shouldn't be a problem having even greater number of words but I didn't tested this too much. It is recommended to be cautious in this.

*-o* - output file in which generated passwords based on the input content file will be saved.

*-d* - flag, when specified will print some debug information e.g. memory usage.

## Example

For a given word *john* the output might be as follows:

```txt
john
John
j0hn
J0hn
john0
john1
john2
john3
... etc.
```

## License

This project is licensed under either of

Apache License, Version 2.0, (LICENSE-APACHE or <http://www.apache.org/licenses/LICENSE-2.0>)
MIT license (LICENSE-MIT or <http://opensource.org/licenses/MIT>)
at your option.

## Contributing / Feedback

I am always glad to learn from anyone.
If you want to contribute, you are more than welcome to be a part of the project! Try to share you thoughts first! Feel free to open a new issue if you want to discuss new ideas.

Any kind of feedback is welcome!
