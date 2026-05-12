"""Gym challenge starter: convert kilograms to pounds.

Instructions for Oscar:

1. Read the instructions and do not change the text comments.
2. Create the function `convert_kg_to_lb(kg_value)`.
3. In `main()`, ask the user for a weight in kilograms.
4. Convert the input to a number and call `convert_kg_to_lb`.
5. Print the result in pounds with a clear message.
6. Handle invalid input by showing a friendly error.

Example output:
    Enter weight in kg: 75
    75.00 kg = 165.35 lb
"""

CONVERSION_FACTOR = 2.20462


def convert_kg_to_lb(kg_value):
    """Convert kilograms to pounds."""
    # TODO: return the converted value in pounds
    user_input = input("Please enter a weight in kilograms: ").strip()


def main():
    print("Gym unit converter: kilograms to pounds")
    # TODO: ask the user for a weight in kilograms
    user_input = input("Please enter a weight in kilograms: ").strip()
    # TODO: convert the input to float
    try:
        kg = float(user_input)
    # TODO: handle invalid values with a friendly message
    except ValueError:
        print("Please enter a valid number for kilograms!")
        return
    # TODO: call convert_kg_to_lb and print the result
    lbs = convert_kg_to_lb(kg)
    print(f"{kg} kg is {lbs:.2f} lb.")


if __name__ == "__main__":
    main()
