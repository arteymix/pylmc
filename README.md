pylmc
=====

LMC interpreter writter in Python

## Basic syntax
The basic syntax is 
<label> <instruction> <address>

Label or address can be ommited
<instruction> <address>
<label> <instruction>

Or both can be ommited
<instruction>

### Label
A label refers to an address in the program memory. Referencing a defined label will have its value replaced by the address of the targeted instruction.

### Instruction
Valid instructions are:
LDA
STO
IN
OUT
HLT
BR
BRZ
BRP
ADD
SUB

### Address
<address> must either be an interger or match a label. Yet, labels are resolved simply: multiple levels of labels will not work.

Label and address are optionals. If no address is used, None will be used internally, which may lead to exceptions.

### Comments
A comment like have to start with the # character. Comments are ignored from the first hashtag of a line to its end.

# this is a comment
LDA top # this is another comment

## Preprocessing
It is sometimes useful to preprocess assembly code in order to avoir repetition. m4 is used in examples and suits very well the requirements.
