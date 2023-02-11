from typing import Dict
import traceback


class InvalidInputArgumentType(Exception):
    """
    Custom exception that can be leveraged for restricting  input arguments to certain types.
    use input_args_types for passing input argument to type mapping
    """

    def __init__(self, input_args_types: Dict[str, str]):
        self.input_args_types = input_args_types
        self.message = "One or more arguments has invalid type. Please refer below required types for all arguments: " \
                       f"{[k + ' is of type ' + self.input_args_types[k] for k in input_args_types]}"
        super().__init__(self.message)


if __name__ == '__main__':
    # sample use cases:
    try:
        raise InvalidInputArgumentType({'a': 'int', 'b': 'str'})
    except Exception as e:
        print(traceback.format_exception(e))
