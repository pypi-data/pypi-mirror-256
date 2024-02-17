
# PyFraction

PyFraction is a Python package that introduces a new data type for Fraction operations. This package aims to provide a convenient and efficient way to work with fractions in Python applications.

## Features

* Custom Fraction data type for precise fraction arithmetic.
* Support for basic arithmetic operations such as addition, subtraction, multiplication, and division.
* Simplification of fractions to their lowest terms.
* Comparison operations for fractions. (In Progress)
* Conversion utilities to convert fractions to other data types. (In Progress)


## Installation
You can install PyFraction using pip:

```pip install pyfraction ```

## Usage

Here's a quick example demonstrating the usage of PyFraction:

```python
# Your Python code goes here
from pyfraction import Fraction

# Create fractions
frac1 = Fraction(3, 4)
frac2 = Fraction(2, 5)

# Perform arithmetic operations
result_addition = frac1 + frac2
result_subtraction = frac1 - frac2
result_multiplication = frac1 * frac2
result_division = frac1 / frac2


# Output results
print("Addition:", result_addition)
print("Subtraction:", result_subtraction)
print("Multiplication:", result_multiplication)
print("Division:", result_division)

```

## Contributing

We welcome contributions from the community! If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request on GitHub.

## License
See the [LICENSE](licence.txt) file for details.

## Acknowledgments
Inspiration for this project came from the need for a simple and efficient way to work with fractions in Python.
Special thanks to contributors who helped improve and maintain this package.