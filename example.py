import re
import sys

class Example():
    def __init__(self, data):

        self.text = None
        self.english = None
        self.source = None
        self.type = None

        for i, item in enumerate(data):
            key, value = item
            if key == "ex":
                self.text = value
            elif key == "eng":
                self.english = value
            elif key == "src":
                self.source = value
            else:
                raise ValueError(f"Unexpected data: {key}, {value}")
