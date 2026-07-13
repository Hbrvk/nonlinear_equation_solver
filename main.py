import math

from abc import ABC, abstractmethod
from typing import override

"""
first run is assuming the input is correct and coefficients are whole
TODO:
fix the build tree function
do it in the syntax they use on the job - black?
print statement, co se prave vykonava
test edge cases
make it work on složené functions
test properly the 0 - x solution to sin(-x)
"""

tuple_of_functions = ('exp', 'log', 'sin', 'cos')

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
    global tuple_of_functions
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
    global tuple_of_functions
    priority_dictionary = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    postfix_expression: list[str] = list()
    operator_stack: list[str] = list()

    for term in expression:
        if term.isdigit() or (term.isalpha() and term not in tuple_of_functions):
            postfix_expression.append(term)

        elif term in tuple_of_functions:
            operator_stack.append(term)

        elif term in priority_dictionary:
            while len(operator_stack) > 0 and operator_stack[-1] != '(' and \
                  (operator_stack[-1] in tuple_of_functions or \
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
            if len(operator_stack) > 0 and operator_stack[-1] in tuple_of_functions:
                postfix_expression.append(operator_stack.pop())

    while len(operator_stack) > 0:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression

class node(ABC):
    @abstractmethod
    def evaluate(self: "node", value_of_x: float) -> float:
        raise NotImplementedError

    @abstractmethod
    def derive(self: "node") -> "node":
        raise NotImplementedError

    @abstractmethod
    def simplify(self: "node") -> "node":
        return self


class constant_node(node):
    def __init__(self: "constant_node", value: float) -> None:
        self.value: float = value
        return None

    @override
    def evaluate(self: "constant_node", value_of_x: float) -> float:
        return self.value

    @override
    def derive(self: "constant_node") -> "constant_node":
        return constant_node(0.0)

    @override
    def simplify(self: "node") -> "node":
        return self


class variable_node(node):
    @override
    def evaluate(self: "variable_node", value_of_x: float) -> float:
        return value_of_x

    @override
    def derive(self: "variable_node") -> constant_node:
        return constant_node(1)

    @override
    def simplify(self: "node") -> "node":
        return self


class operation_node(node):
    def __init__(self: "operation_node", operation: str, left: node, right: node) -> None:
        self.operation: str = operation
        self.left: node = left
        self.right: node = right
        return None

    @override
    def evaluate(self: "operation_node", value_of_x: float) -> float:
        left_value = self.left.evaluate(value_of_x)
        right_value = self.right.evaluate(value_of_x)

        if self.operation == '+': return left_value + right_value
        elif self.operation == '-': return left_value - right_value
        elif self.operation == '*': return left_value * right_value
        elif self.operation == '/': return left_value / right_value
        else: return math.pow(left_value, right_value)

    @override
    def derive(self: "operation_node") -> "operation_node":
        if self.operation == '+':
            return operation_node('+', self.left.derive(), self.right.derive())
        elif self.operation == '-':
            return operation_node('-', self.left.derive(), self.right.derive())
        elif self.operation == '*':
            part1 = operation_node('*', self.left.derive(), self.right)
            part2 = operation_node('*', self.left, self.right.derive())
            return operation_node('+', part1, part2)
        elif self.operation == '/':
            part1 = operation_node('*', self.left.derive(), self.right)
            part2 = operation_node('*', self.left, self.right.derive())
            numerator = operation_node('-', part1, part2)
            denominator = operation_node('^', self.right, constant_node(2))
            return operation_node('/', numerator, denominator)
        else:
            new_exp = operation_node('-', self.right, constant_node(1))
            power_rule = operation_node('*', self.right, operation_node('^', self.left, new_exp))
            return operation_node('*', power_rule, self.left.derive())

    @override
    def simplify(self: "operation_node") -> node:
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        left_value = self.left.value if isinstance(self.left, constant_node) else None
        right_value = self.right.value if isinstance(self.right, constant_node) else None

        if self.operation == '+':
            if left_value == 0: return self.right
            if right_value == 0: return self.left
        elif self.operation == '-':
            if right_value == 0: return self.left
        elif self.operation == '*':
            if left_value == 0 or right_value == 0: return constant_node(0)
            if left_value == 1: return self.right
            if right_value == 1: return self.left
        elif self.operation == '^':
            if right_value == 1: return self.left
            if right_value == 0: return constant_node(1)

        return self


class function_node(node):
    def __init__(self: "function_node", function_name: str, argument: node) -> None:
        self.funcion_name: str = function_name
        self.argument: node = argument
        return None

    @override
    def evaluate(self: "function_node", value_of_x: float) -> float:
        value = self.argument.evaluate(value_of_x)

        if self.funcion_name == 'sin': return math.sin(value)
        elif self.funcion_name == 'cos': return math.cos(value)
        elif self.funcion_name == 'exp': return math.exp(value)
        else: return math.log(value)

    @override
    def derive(self: "function_node") -> operation_node:
        derivative_of_argument = self.argument.derive()

        if self.funcion_name == 'sin':
            outer_function = function_node('cos', self.argument)
            return operation_node('*', outer_function, derivative_of_argument)
        elif self.funcion_name == 'cos':
            outer_function = operation_node('-', constant_node(0), function_node('sin', self.argument))
            return operation_node('*', outer_function, derivative_of_argument)
        elif self.funcion_name == 'exp':
            return operation_node('*', function_node('exp', self.argument), derivative_of_argument)
        else:
            outer_function = operation_node('/', constant_node(1), self.argument)
            return operation_node('*', outer_function, derivative_of_argument)

    @override
    def simplify(self: "function_node") -> node:
        self.argument = self.argument.simplify()
        if isinstance(self.argument, constant_node):
            return constant_node(self.evaluate(0))
        return self


class binarytree:
    def __init__(self: "binarytree") -> None:
        self.root: node | None = None
        return None


def build_arithmetic_tree_from_expression(postfix_expression: list[str]) -> binarytree:
    global tuple_of_functions
    helper_stack: list[node] = list()

    for term in postfix_expression:
        if term.replace(".", "").isdigit():
            helper_stack.append(constant_node(float(term)))
        elif term == "x":
            helper_stack.append(variable_node())
        elif term in tuple_of_functions:
            argument = helper_stack.pop()
            helper_stack.append(function_node(term, argument))
        else:
            right = helper_stack.pop()
            left = helper_stack.pop()
            helper_stack.append(operation_node(term, left, right))

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

    if arithmetic_tree_root is None:
        return approximate_result
    else:
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


