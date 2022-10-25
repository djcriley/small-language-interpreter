import re
import sys

inputfile = sys.argv[1]
outputfile = sys.argv[2]
text_file = open(inputfile, "r")
f = open(outputfile, "a")

NUMBER_TOKEN = re.compile("^[0-9]+$")
IDENTIFIER = re.compile("^([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*$")
PUNCTUATION = re.compile("^(\+|\-|\*|/|\)|\(|:=|;)$")

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[0]

    def consume_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
        return self.current_token

    def parse(self):
        tree = self.expression()
        tree.preorder_print(tree)
        return tree

    def expression(self):
        tree = self.term()
        while self.current_token.op == 'add':
            token = self.current_token
            self.consume_token()
            right = self.term()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def term(self):
        tree = self.factor()
        while self.current_token.op == 'sub':
            token = self.current_token
            self.consume_token()
            right = self.factor()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def factor(self):
        tree = self.piece()
        while self.current_token.op == 'div':
            token = self.current_token
            self.consume_token()
            right = self.piece()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def piece(self):
        tree = self.element()
        while self.current_token.op == 'mult':
            token = self.current_token
            self.consume_token()
            right = self.element()
            tree = Node(tree, token.value, right, None)
            tree.type = 'Punctuation'
        return tree

    def element(self):
        if self.current_token.type == 'Number':
            token = self.current_token
            self.consume_token()
            endNode = Node(None, token.value, None, None)
            endNode.type = 'Number'
            return endNode

        elif self.current_token.type == 'Identifier':
            token = self.current_token
            self.consume_token()
            endNode = Node(None, token.value, None, None)
            endNode.type = 'Identifier'
            return endNode

        if self.current_token.value == '(':
            self.consume_token()
            tree = self.expression()
            if self.current_token.value == ')':
                self.consume_token()
                return tree

class Node:
    def __init__(self, left, value, right, middle):
        self.value = value
        self.left = left
        self.right = right
        self.middle = middle
        self.type = None

    def preorder_print(self, tree, level=0):
        if tree is None:
            return
        else:
            for n in range(level):
                print("\t", end="", file=f)

            if tree.type != None:
                print(tree.value, ':', tree.type, file=f)
            else:
                print(tree.value, file=f)
            if tree.left is not None:
                self.preorder_print(tree.left, level + 1)
            if tree.middle is not None:
                self.preorder_print(tree.middle, level + 1)
            if tree.right is not None:
                self.preorder_print(tree.right, level + 1)


class Token:
    def __init__(self, value, type):
        self.value = value
        self.type = type
        self.op = None

    def info(self):
        print(self.value, " : ", self.type, file=f)


class Evaluator:
    def __init__(self):
        self.stack = []
        self.root = None

    def printEval(self):
        print("\n-----------------------Evaluator-----------------------\n", file=f)

        print("\nOutput:", self.stack[0].value, file=f)

        print("\n-------------------------------------------------------\n", file=f)

    def eval(self, root):
        self.stack.append(root)
        if len(self.stack) >= 3:
            # 1 is for the data type
            while len(self.stack) >= 3 and self.stack[-1].type == "Number" and self.stack[-2].type == "Number" and \
                    self.stack[
                        -3].type == "Punctuation":
                num1 = self.stack.pop()
                num2 = self.stack.pop()
                punct = self.stack.pop()

                if punct.value == '+':
                    result = int(num2.value) + int(num1.value)
                    x = Node(None, result, None, None)
                    x.type = "Number"
                    self.stack.append(x)

                elif punct.value == '-':
                    result = int(num2.value) - int(num1.value)
                    x = Node(None, result, None, None)
                    x.type = "Number"
                    self.stack.append(x)

                elif punct.value == '*':
                    result = int(num2.value) * int(num1.value)
                    x = Node(None, result, None, None)
                    x.type = "Number"
                    self.stack.append(x)

                elif punct.value == '/':
                    # division by 0 throw exception
                    # if int(num2.value) == 0:
                    #     print("Divison by 0 error, failing peacefully")
                    #     return
                    try:
                        result = int(num2.value) / int(num1.value)
                        x = Node(None, result, None, None)
                        x.type = "Number"
                        self.stack.append(x)
                    except ZeroDivisionError as exception:
                        print("Division by 0", file=f)
                        raise exception

        if root.left == None:
            return
        self.eval(root.left)
        if root.right == None:
            return
        self.eval(root.right)


def main():
    token_list = []

    # read lines in and split them into proper tokens
    for line in text_file:
        line = line.strip(' ')
        print("Line:", line, file=f)
        words = line.split()
        for token in words:
            temp = []
            string = ''
            for char in token:
                temp.append(char)
                x = string.join(temp)
                id_result = re.match(IDENTIFIER, x)
                num_result = re.match(NUMBER_TOKEN, x)
                punc_result = re.match(PUNCTUATION, x)
                if (id_result is None) & (num_result is None) & (punc_result is None) & (len(x) != 1):
                    back = token[len(x) - 1:]
                    front = token[0:len(x) - 1]
                    words.insert(words.index(token), front)
                    words.insert(words.index(token), back)
                    words.remove(token)
                    break

        # adding tokens to the list for parsing
        for token in words:
            num_result = re.match(NUMBER_TOKEN, token)
            id_result = re.match(IDENTIFIER, token)
            punc_result = re.match(PUNCTUATION, token)

            # for this section I removed printing line by line and print them all at once after scanning in the file

            
            if id_result is not None:
                # print(token, ": Identifier", file=f)
                token_list.append(Token(token, "Identifier"))
            elif num_result is not None:
                # print(token, ": Number", file=f)
                token_list.append(Token(token, "Number"))
            elif punc_result is not None:
                # print(token, ": Punctuation", file=f)
                if token == '+':
                    tok = Token(token, "Punctuation")
                    tok.op = 'add'
                    token_list.append(tok)
                elif token == '-':
                    tok = Token(token, "Punctuation")
                    tok.op = 'sub'
                    token_list.append(tok)
                elif token == '*':
                    tok = Token(token, "Punctuation")
                    tok.op = 'mult'
                    token_list.append(tok)
                elif token == '/':
                    tok = Token(token, "Punctuation")
                    tok.op = 'div'
                    token_list.append(tok)
                elif token == '(':
                    tok = Token(token, "Punctuation")
                    tok.op = 'leftP'
                    token_list.append(tok)
                elif token == ')':
                    tok = Token(token, "Punctuation")
                    tok.op = 'rightP'
                    token_list.append(tok)

            else:
                print("Error reading:'", token, "'", file=f)
                # this makes it continue onto next line disregarding the characters after the error so if the line was
                # test!cooper then it would print error on ! and skip cooper and go to next line
                # you said it was fine for it to contunie reading characters but i wanted ouput to match what your output was
                break

    print("-------------------------", file=f)
    print("Tokens:", file=f)
    for token in token_list:
        token.info()
    print("\n-----------------------\n", file=f)

    print("\n-----------------------AST-----------------------\n", file=f)

    # testing the nodes from reading the file

    parser_obj = Parser(token_list)
    tree = parser_obj.parse()

    print("\n--------------------------------------------------\n", file=f)
    x = Evaluator()
    x.root = tree
    x.eval(tree)
    x.printEval()

    text_file.close()
    f.close()


if __name__ == '__main__':
    main()
