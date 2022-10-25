# small-language-interpreter
This is a small language interpreter created using Python

This program, first tokenizes the input which is read from a file. It then parses the tokens to create an AST of the function. This tree is then passed to the Evualator which evualtes the expression. 

## How to run:
```bash
python3 token_scanner.py input.txt output.txt
```

## Example input
```text
3 * (5 + 10 / 3 - 1)
```

## Example Output:
```text
Output: 
Line: 3 * (5 + 10 / 3 - 1)
-------------------------
Tokens:
3  :  Number
*  :  Punctuation
(  :  Punctuation
5  :  Number
+  :  Punctuation
10  :  Number
/  :  Punctuation
3  :  Number
-  :  Punctuation
1  :  Number
)  :  Punctuation

-----------------------


-----------------------AST-----------------------

* : Punctuation
	3 : Number
	+ : Punctuation
		5 : Number
		- : Punctuation
			/ : Punctuation
				10 : Number
				3 : Number
			1 : Number

--------------------------------------------------


-----------------------Evaluator-----------------------


Output: 21

-------------------------------------------------------
```

### Rules for the language:
