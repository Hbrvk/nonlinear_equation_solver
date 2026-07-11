#import sys

"""
first run was assuming the input is correct and numbers are whole
TODO:
do it in the syntax they use on the job
print statement, co se prave vykonava
test edge cases
make it work on složené functions
test properly the 0 - x solution to sin(-x)
"""


def load_input() -> str:
    equation = input("Insert equation:")
    return equation


def process_equation(raw_equation: str) -> str:
    raw_equation = raw_equation.replace(" ", "")
    left_and_right_equation = raw_equation.split("=")

    if len(left_and_right_equation) != 2:
        raise ValueError("Invalid format: Equation must contain exactly one '=' sign.")

    if left_and_right_equation[1] == "0":
        raw_expression = left_and_right_equation[0]
        return raw_expression

    else:
        raw_expression = left_and_right_equation[0] + f"-({left_and_right_equation[1]})"
        return raw_expression


def process_expression(raw_expression: str) -> list[str]:
    tuple_of_functions = ('exp', 'log', 'sin', 'cos')
    expression: list[str] = list()
    raw_length = len(raw_expression)

    i = 0
    while i < raw_length:
        character = raw_expression[i]

        matched_function = False
        for function in tuple_of_functions:
            if raw_expression.startswith(function, i):
                expression.append(function)
                i += len(function)
                matched_function = True
                break
        if matched_function == True:
            continue

        if character.isalpha():
            starting_index = i
            while raw_expression[i].isalpha():
                i += 1
            expression.append(raw_expression[starting_index:i])
            continue

        if character.isdigit():
            starting_index = i
            while raw_expression[i].isdigit():
                i += 1
            expression.append(raw_expression[starting_index:i])
            continue

        if character == '-':
            if not expression or expression[-1] == '(':
                expression.append('0')
            expression.append('-')
            i += 1
            continue

        expression.append(character)
        i += 1

    return expression


def process_expression_to_postfix(expression: list[str]) -> list[str]:
    priority_dictionary = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    functions = ('exp', 'log', 'sin', 'cos')
    postfix_expression: list[str] = list()
    operator_stack: list[str] = list()

    for term in expression:
        if term.isdigit() or (term.isalpha() and term not in functions):
            postfix_expression.append(term)

        elif term in functions:
            operator_stack.append(term)

        elif term in priority_dictionary:
            while len(operator_stack) > 0 and operator_stack[-1] != '(' and \
                  (operator_stack[-1] in functions or \
                   priority_dictionary.get(operator_stack[-1], 0) >= priority_dictionary[term]):
                postfix_expression.append(operator_stack.pop())
            operator_stack.append(term)

        elif term == '(':
            operator_stack.append(term)

        elif term == ')':
            while len(operator_stack) > 0 and operator_stack[-1] != '(':
                postfix_expression.append(operator_stack.pop())
            if len(operator_stack) > 0 and operator_stack[-1] == '(':
                _ = operator_stack.pop()
            if len(operator_stack) > 0 and operator_stack[-1] in functions:
                postfix_expression.append(operator_stack.pop())

    while len(operator_stack) > 0:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression


class node:
    def __init__(self: "node", value: str) -> None:
        self.value: str = value
        self.left: "node | None" = None
        self.right: "node | None" = None
        return None


    def derive(self: "node") -> "node":
        return node("")


    def evaluate(self: "node", value_of_x: float) -> float:
        return value_of_x


class binarytree:
    def __init__(self: "binarytree") -> None:
        self.root: node | None = None
        return None


def build_arithmetic_tree_from_expression(postfix_expression: list[str]) -> binarytree:
    helper_stack: list[node] = list()

    for term in postfix_expression:
        if term.isdigit() or term == "x":
            helper_stack.append(node(term))
        else:
            right = helper_stack.pop()
            left  = helper_stack.pop()
            new_term_node = node(term)
            new_term_node.right = right
            new_term_node.left = left
            helper_stack.append(new_term_node)

    arithmetic_tree = binarytree()
    arithmetic_tree.root = helper_stack[0]
    return arithmetic_tree


def newton_method(
        expression_tree: binarytree,
        approximate_result: float,
        result_tolerance: float = 1e-7,
        numerical_zero_tolerance: float = 1e-12,
        number_of_iteratioins: int = 50) -> float | None:

    arithmetic_tree_root = expression_tree.root
    derivative_of_root = arithmetic_tree_root.derive()
    current_x_value = approximate_result

    for _ in range(number_of_iteratioins):
        fx = arithmetic_tree_root.evaluate(current_x_value)
        derivative_fx = derivative_of_root.evaluate(current_x_value)

        if abs(fx) < result_tolerance:
            return current_x_value

        if abs(derivative_fx) < numerical_zero_tolerance:
            return None

        current_x_value = current_x_value - (fx / derivative_fx)

    return current_x_value


def main() -> None:
    print(process_expression_to_postfix(process_expression(process_equation(load_input()))))
    return None


if __name__ == "__main__":
    main()


