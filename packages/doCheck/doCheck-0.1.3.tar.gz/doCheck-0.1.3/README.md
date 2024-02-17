# doCheck

## Introduction

`doCheck` is an open-source type checking module written in Python, released under the Mulan Permissive Software License v2 (MulanPSL-2.0). This module provides a set of reusable Checker classes for validating properties and conditions of different types of values.

## Installation

```bash
pip install doCheck
```

## Features

- Provides various logical operator overload methods such as intersection, union, complement, negation, etc., for composing complex data validation rules.
- Includes `LiteralChecker` (also known as `EnumChecker`) to check if a value is in a predefined list.
- `TypeChecker` is used to validate if a value belongs to a specific collection of data types.
- `RangeChecker` supports conditional checks within a numeric range and allows customization of interval closure.
- Additionally, `CallableChecker` and `RegexChecker` are provided to check if a value is a callable object and if a string matches a regular expression, respectively.

## Usage Example

```python
import doCheck as dc

# Create checker instances
is_integer = dc.TypeChecker(int)
is_even = dc.RangeChecker(0, float('inf'), leftClosed=True, step=2)
is_valid_name = dc.RegexChecker(r'^[A-Za-z]+\s[A-Za-z]+$')

# Apply checkers
print(is_integer.check(42))  # Output: True
print(is_even.check(10))     # Output: True
print(is_valid_name.check("John Doe"))  # Output: True
```

## License

doCheck module is licensed under the Mulan Permissive Software License v2.0. For more information about this license, please visit: [https://opensource.org/license/mulanpsl-2-0/](https://opensource.org/license/mulanpsl-2-0/)

| [![Github](https://img.shields.io/badge/GitHub-black?logo=github)](https://github.com/kuankuan2007/do-check) | [![gitee](https://img.shields.io/badge/Gitee-rgb(199%2C29%2C35)?logo=gitee)](https://gitee.com/kuankuan2007/do-check) | [![Static Badge](https://img.shields.io/badge/Gitab-rgb(226%2C67%2C41)?logo=gitlab)](https://gitlab.com/kuankuan2007/do-check) |

Note: To use this module, make sure to import it correctly and comply with the relevant open-source license terms.
