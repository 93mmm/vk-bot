from dataclasses import dataclass
from datetime import datetime


@dataclass
class ExceptionData:
    def __init__(self, ex, **variables):
        self.ex = ex
        self.variables = variables

    def __str__(self):
        message = f"Thrown exception: {repr(self.ex)}\nVariables:\n"
        for key, value in self.variables.items():
            message += f"{key} = {value}\n"
        return message + "\n"
