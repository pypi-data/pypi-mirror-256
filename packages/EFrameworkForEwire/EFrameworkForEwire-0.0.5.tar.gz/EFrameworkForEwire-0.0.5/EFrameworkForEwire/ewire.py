class Calculator:
    """A simple calculator class."""

    def __init__(self):
        """Initialize the calculator."""
        pass

    def add(a, b):
        """Add two numbers."""
        return a + b

    def subtract(a, b):
        """Subtract one number from another."""
        return a - b

    def multiply(a, b):
        """Multiply two numbers."""
        return a * b

    def divide(a, b):
        """Divide one number by another."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b