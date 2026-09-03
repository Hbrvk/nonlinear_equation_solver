# nonlinear_equation_solver

This program computes roots for nonlinear equations based on a required initial
starting point.

## Format of input

- A nonlinear equation, where the viable functions are log, exp, sin, cos.
- There has to be a star (*) operator in between coefficients and variables.
- The hat (^) operator is used only for constant exponents,
exp(.) for exponents containing variables.
- Noting your variable "x" is the only acceptable way.
- All spaces in the input are ignored.
- There is a required initial numerical starting point.

### Correct examples

- sin( x ) = 0, x_0 = 3
- exp(sin(x))=1, x_0 = 0.5
- 2.5*(-x)^3 = 1, x_0 = 0

### Incorrect examples

- 3 = x - 1 = 2, x_0 = 0
- 3*-x = 0, x_0 = 1
- 3^x = 1, x_0 = 0.5
