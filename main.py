import math

from abc import ABC, abstractmethod
from typing import override

tuple_of_functions = ("exp", "log", "sin", "cos")


def load_input() -> str:
    """
    Load mathematical equation as an input.

    Arguments:

    Returns:
        str: The input as a string.
    """
    equation = input("Insert equation:")
    return equation


def process_equation(raw_equation: str) -> str:
    """
    Process the equation to a mathematical expression.

    Arguments:
        raw_equation (str): A mathematical equation as a string.

    Returns:
        str: A mathematical expression as a string.

    """
    print("Processing equation...")
    raw_equation = raw_equation.replace(" ", "")

    if "x" not in raw_equation:
        raise ValueError("Invalid format: Equation does not contain 'x'.")

    left_and_right_equation = raw_equation.split("=")

    if len(left_and_right_equation) != 2:
        raise ValueError("Invalid format: Equation must contain exactly one '=' sign.")

    for side in left_and_right_equation:
        if side == "":
            raise ValueError("Invalid format: The input is incomplete.")

    if left_and_right_equation[1] == "0":
        raw_expression = left_and_right_equation[0]
        return raw_expression

    else:
        raw_expression = left_and_right_equation[0] + f"-({left_and_right_equation[1]})"
        return raw_expression


def check_bracketing(raw_expression: str) -> bool:
    """
    The bracketing of a mathematical expression is correct.

    Arguments:
        raw_expression (str): A mathematical equation as a string.

    Returns:
        bool: The truth value to the statement of the function.
    """
    symbols = raw_expression.split()
    bracket_stack: list[str] = list()
    bracketing_is_valid = True

    for element in symbols:
        if element == "(":
            bracket_stack.append(element)
        elif element == ")":
            if len(bracket_stack) == 0 or bracket_stack.pop() != "(":
                bracketing_is_valid = False
                break

    if len(bracket_stack) != 0:
        bracketing_is_valid = False

    return bracketing_is_valid


def process_expression(raw_expression: str) -> list[str]:
    """
    Process the equation to a list of mathematical terms.

    Arguments:
        raw_expression (str): A mathematical equation as a string.

    Returns:
        list[str]: A sequence of mathematical terms the expression represents.
    """
    print("Processing expression...")
    global tuple_of_functions

    if not check_bracketing(raw_expression):
        raise ValueError("Invalid format: Bracketing is invalid.")

    expression: list[str] = list()
    raw_length = len(raw_expression)

    # Go through the whole raw_expression list and find mathematical expressions.
    i = 0
    while i < raw_length:
        character = raw_expression[i]

        # Find functions
        matched_function = False
        for function in tuple_of_functions:
            if raw_expression.startswith(function, i):
                expression.append(function)
                i += len(function)
                matched_function = True
                break
        if matched_function == True:
            continue

        # Find variables.
        if character.isalpha():
            starting_index = i
            while i < raw_length and raw_expression[i].isalpha():
                i += 1

            selected_term = raw_expression[starting_index:i]

            if (selected_term not in tuple_of_functions) and (selected_term != "x"):
                raise ValueError(f"Invalid format: Unknown term {selected_term}.")

            expression.append(selected_term)
            continue

        # Find constants.
        if character.isdigit() or character == ".":
            starting_index = i
            dot_count = 0
            while i < raw_length and (
                raw_expression[i].isdigit() or raw_expression[i] == "."
            ):
                if raw_expression[i] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise ValueError("Invalid format: Multiple decimal separators.")
                i += 1
            expression.append(raw_expression[starting_index:i])
            continue

        # Find operators.
        if character == "-":
            if not expression or expression[-1] == "(":
                expression.append("0")
            expression.append("-")
            i += 1
            continue

        if character == "+":
            if not expression or expression[-1] == "(":
                i += 1
                continue

        expression.append(character)
        i += 1

    operators = "+-*/^"
    for i in range(len(expression) - 1):
        if expression[i] in operators and expression[i + 1] in operators:
            raise ValueError("Invalid format: Oparator positioning.")
        if expression[i] == "(" and expression[i + 1] == ")":
            raise ValueError("Invalid format: Empty brackets.")

    return expression


def process_expression_to_postfix(expression: list[str]) -> list[str]:
    """
    Transforms a sequence of mathematical terms representing an expression
    into a sequence of mathematical terms representing an expresion in postfix.

    Arguments:
        expression (list[str]): A sequence of mathematical terms the expression represents.

    Returns:
        A sequence of mathematical terms representing an expresion in postfix.
    """
    print("Transforming expression to postfix...")
    global tuple_of_functions
    priority_dictionary = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    postfix_expression: list[str] = list()
    operator_stack: list[str] = list()

    for term in expression:
        if (
            term.isdigit()
            or ("." in term)
            or (term.isalpha() and term not in tuple_of_functions)
        ):
            postfix_expression.append(term)

        elif term in tuple_of_functions:
            operator_stack.append(term)

        elif term in priority_dictionary:
            while (
                len(operator_stack) > 0
                and operator_stack[-1] != "("
                and (
                    operator_stack[-1] in tuple_of_functions
                    or priority_dictionary.get(operator_stack[-1], 0)
                    >= priority_dictionary[term]
                )
            ):
                postfix_expression.append(operator_stack.pop())
            operator_stack.append(term)

        elif term == "(":
            operator_stack.append(term)

        elif term == ")":
            while len(operator_stack) > 0 and operator_stack[-1] != "(":
                postfix_expression.append(operator_stack.pop())
            if len(operator_stack) > 0 and operator_stack[-1] == "(":
                _ = operator_stack.pop()
            if len(operator_stack) > 0 and operator_stack[-1] in tuple_of_functions:
                postfix_expression.append(operator_stack.pop())

    while len(operator_stack) > 0:
        postfix_expression.append(operator_stack.pop())

    return postfix_expression


class node(ABC):
    """A class representing a mathematical term."""
    @abstractmethod
    def evaluate(self: "node", value_of_x: float) -> float:
        """A placeholder for the function 'evaluate'."""
        raise NotImplementedError

    @abstractmethod
    def derive(self: "node") -> "node":
        """A placeholder for the function 'derive'."""
        raise NotImplementedError

    @abstractmethod
    def simplify(self: "node") -> "node":
        """A placeholder for the function 'simplify'."""
        return self


class constant_node(node):
    """A class representing a constant mathematical term."""
    def __init__(self: "constant_node", value: float) -> None:
        """
        Initialize a constant_node.

        Arguments:
            value (float): The value of the constant.

        Returns:
        """
        self.value: float = value
        return None

    @override
    def evaluate(self: "constant_node", value_of_x: float) -> float:
        """
        Evaluating a constant term.

        Arguments:
            value_of_x (float): Value of the variable.

        Returns:
            float: Let f: x |-> c. Then f(x) = c for any x.
        """
        return self.value

    @override
    def derive(self: "constant_node") -> "constant_node":
        """
        Derive a constant term.

        Arguments:

        Returns:
            constant_node: Let f: x |-> c. Then f'(x) = 0 for any x.
        """
        return constant_node(0.0)

    @override
    def simplify(self: "node") -> "node":
        """
        Simplify a constant term.

        Arguments:

        Returns:
            self: Can not simplify a constant term.
        """
        return self


class variable_node(node):
    """A class representing a variable."""
    @override
    def evaluate(self: "variable_node", value_of_x: float) -> float:
        """
        Evaluating a variable.

        Arguments:
            value_of_x (float): Value of the variable.

        Returns:
            float: Let f: x |-> x. Then f(x) = x for any x.
        """
        return value_of_x

    @override
    def derive(self: "variable_node") -> constant_node:
        """
        Derive a variable.

        Arguments:

        Returns:
            constant_node: Let f: x |-> x. Then f'(x) = 1 for any x.
        """
        return constant_node(1)

    @override
    def simplify(self: "node") -> "node":
        """
        Simplify a variable.

        Arguments:

        Returns:
            self: Can not simplify a variable.
        """
        return self


class operation_node(node):
    """A class representing an operation."""
    def __init__(
        self: "operation_node", operation: str, left: node, right: node
    ) -> None:
        """
        Initialize an operation_node.

        Arguments:
            operation (str): The operation this node represents.
            left (node): An operand left of the operator.
            right (node): An operand right of the operator.

        Returns:
        """
        self.operation: str = operation
        self.left: node = left
        self.right: node = right
        return None

    @override
    def evaluate(self: "operation_node", value_of_x: float) -> float:
        """
        Evaluating an operation.

        Arguments:
            value_of_x (float): Value of the variable.

        Returns:
            float: Let f: x |-> g(x) (+-/*^) h(x), where g and h are functions of x.
                   Returns f(value_of_x).
        """
        left_value = self.left.evaluate(value_of_x)
        right_value = self.right.evaluate(value_of_x)

        if self.operation == "+":
            return left_value + right_value
        elif self.operation == "-":
            return left_value - right_value
        elif self.operation == "*":
            return left_value * right_value
        elif self.operation == "/":
            return left_value / right_value
        else:
            return math.pow(left_value, right_value)

    @override
    def derive(self: "operation_node") -> "operation_node":
        """
        Derivative of an operation.

        Arguments:

        Returns:
            operation_node: Let f: x |-> g(x) (+-/*^) h(x), where g and h are functions of x.
                   Returns f'(x).
        """
        if self.operation == "+":
            return operation_node("+", self.left.derive(), self.right.derive())
        elif self.operation == "-":
            return operation_node("-", self.left.derive(), self.right.derive())
        elif self.operation == "*":
            left_term = operation_node("*", self.left.derive(), self.right)
            right_term = operation_node("*", self.left, self.right.derive())
            return operation_node("+", left_term, right_term)
        elif self.operation == "/":
            left_term = operation_node("*", self.left.derive(), self.right)
            right_term = operation_node("*", self.left, self.right.derive())
            numerator = operation_node("-", left_term, right_term)
            denominator = operation_node("^", self.right, constant_node(2))
            return operation_node("/", numerator, denominator)
        else:
            new_exponent = operation_node("-", self.right, constant_node(1))
            power_rule = operation_node(
                "*", self.right, operation_node("^", self.left, new_exponent)
            )
            return operation_node("*", power_rule, self.left.derive())

    @override
    def simplify(self: "operation_node") -> node:
        """
        Simplify an operation.

        Arguments:

        Returns:
            node: Trivial simplification of the operation.
        """
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        left_value = self.left.value if isinstance(self.left, constant_node) else None
        right_value = (
            self.right.value if isinstance(self.right, constant_node) else None
        )

        if self.operation == "+":
            if left_value == 0:
                return self.right
            if right_value == 0:
                return self.left
        elif self.operation == "-":
            if right_value == 0:
                return self.left
        elif self.operation == "*":
            if left_value == 0 or right_value == 0:
                return constant_node(0)
            if left_value == 1:
                return self.right
            if right_value == 1:
                return self.left
        elif self.operation == "^":
            if right_value == 1:
                return self.left
            if right_value == 0:
                return constant_node(1)

        return self


class function_node(node):
    """A class representing a function."""
    def __init__(self: "function_node", function_name: str, argument: node) -> None:
        """
        Initialize a function_node.

        Arguments:
            function_name (str): The function this node represents.
            argument (node): An argument of the function this node represents.

        Returns:
        """
        self.function_name: str = function_name
        self.argument: node = argument
        return None

    @override
    def evaluate(self: "function_node", value_of_x: float) -> float:
        """
        Evaluating a function.

        Arguments:
            value_of_x (float): Value of the variable.

        Returns:
            float: Let f: x |-> (function_name)(x).
            Returns f(argument(value_of_x)).
        """
        value = self.argument.evaluate(value_of_x)

        if self.function_name == "sin":
            return math.sin(value)
        elif self.function_name == "cos":
            return math.cos(value)
        elif self.function_name == "exp":
            return math.exp(value)
        else:
            return math.log(value)

    @override
    def derive(self: "function_node") -> operation_node:
        """
        Derivative of a function.

        Arguments:

        Returns:
            operation_node: Let f: x |-> (function_name)(x).
            Returns f'((argument)(x))*(argument)'(x).
        """
        derivative_of_argument = self.argument.derive()

        if self.function_name == "sin":
            outer_function = function_node("cos", self.argument)
            return operation_node("*", outer_function, derivative_of_argument)
        elif self.function_name == "cos":
            outer_function = operation_node(
                "-", constant_node(0), function_node("sin", self.argument)
            )
            return operation_node("*", outer_function, derivative_of_argument)
        elif self.function_name == "exp":
            return operation_node(
                "*", function_node("exp", self.argument), derivative_of_argument
            )
        else:
            outer_function = operation_node("/", constant_node(1), self.argument)
            return operation_node("*", outer_function, derivative_of_argument)

    @override
    def simplify(self: "function_node") -> node:
        """
        Simplify a function.

        Arguments:

        Returns:
            node: Transforms a function_node to constant_node.
        """
        self.argument = self.argument.simplify()
        if isinstance(self.argument, constant_node):
            return constant_node(self.evaluate(0))
        return self


class binarytree:
    """ A binary tree class."""
    def __init__(self: "binarytree") -> None:
        """
        Initialize a binarytree.

        Arguments:

        Returns:
        """
        self.root: node | None = None
        return None


def build_arithmetic_tree_from_expression(postfix_expression: list[str]) -> binarytree:
    """
    Transform a postfix sequence of mathematical terms into an arithmetic tree.

    Arguments:
        postfix_expression (list[str]): A postfix sequence of mathematical terms representing
                                        an expression.

    Returns:
        binarytree: Arithmetic tree representing a mathematical expression.
    """
    print("Building arithmetic tree...")
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
    result_tolerance: float = 1e-7,
    numerical_zero_tolerance: float = 1e-12,
    number_of_iterations: int = 50,
) -> float | None:
    """
    Applies Newton's method to find the root of a mathematical expression.
    User inputs an initial guess and iteratively which is refined using the function's
    derivative to find where the expression evaluates to zero.

    Arguments:
        expression_tree (binarytree): The binary tree representing the parsed mathematical expression.
        result_tolerance (float): The acceptable absolute error for the function's calculated root.
        numerical_zero_tolerance (float): The threshold below which the derivative is considered zero.
        number_of_iterations (int): The maximum number of iterative refinement steps allowed.

    Returns:
        float: The approximated root of the arithmetic tree representing an expression.
        None: If the derivative evaluates to zero, a math domain error occurs, division by
            zero is encountered, or the solution is not found within the tolerance.
    """

    print("Applying Newtons method...")
    arithmetic_tree_root = expression_tree.root

    while True:
        raw_guess = input("Insert approximate result of the equation: ")
        raw_guess = raw_guess.replace(",", ".")
        try:
            approximate_result = float(raw_guess)
            break
        except ValueError:
            print("Invalid input. Enter a valid numerical value.")

    if arithmetic_tree_root is None:
        return approximate_result
    else:
        derivative_of_root = arithmetic_tree_root.derive()

    current_x_value = approximate_result

    for iteration in range(number_of_iterations):
        try:
            fx = arithmetic_tree_root.evaluate(current_x_value)
            derivative_fx = derivative_of_root.evaluate(current_x_value)

            if abs(derivative_fx) < numerical_zero_tolerance:
                print("Solution was not found in the given tolerance interval.")
                return None

            if abs(fx) < result_tolerance:
                print(f"Solution in tolerance interval was reached.")
                print(f"x = {current_x_value}")
                print(f"Number of iterations: {iteration}")
                return current_x_value

            current_x_value = current_x_value - (fx / derivative_fx)

        except ValueError:
            print("Value Error: Left the domain of the function.")
            return None
        except ZeroDivisionError:
            print("ZeroDivisionError: Division by zero encountered.")
            return None

    return current_x_value


def main() -> None:
    """Code pipeline."""
    raw_equation = load_input()
    raw_expression = process_equation(raw_equation)
    expression = process_expression(raw_expression)
    expression_in_postfix = process_expression_to_postfix(expression)
    arithmetic_tree = build_arithmetic_tree_from_expression(expression_in_postfix)
    _ = newton_method(arithmetic_tree)
    return None


if __name__ == "__main__":
    main()

