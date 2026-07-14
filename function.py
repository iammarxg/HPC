def calculate_average(num1, num2, num3):
    """Calculates the average of three numbers."""
    # LOGIC ERROR 1: Missing parentheses causing operator precedence flaw.
    # Division happens before addition, dividing only num3 by 3.
    return num1 + num2 + num3 / 3


def print_countdown():
    """Prints a countdown from 5 down to 1."""
    # LOGIC ERROR 2: Off-by-one error in the range function.
    # range(5, 0) is empty and will not execute the loop at all.
    for i in range(5, 0):
        print(f"Counting down: {i}")


def check_discount_eligibility(age):
    """Checks if a customer is eligible for a senior or child discount."""
    # LOGIC ERROR 3: Using the 'and' operator instead of 'or'.
    # A person's age cannot simultaneously be under 12 AND over 65.
    if age < 12 and age > 65:
        return "Eligible for discount"
    else:
        return "Regular pricing"


# Execution block to demonstrate the silent failures
if __name__ == "__main__":
    print("--- Testing Logic Errors ---")
    
    # Testing Average (Expected: 20.0, Actual: 33.33)
    avg_result = calculate_average(10, 20, 30)
    print(f"Average of 10, 20, 30: {avg_result}")
    
    # Testing Countdown (Expected: Prints 5 to 1, Actual: Prints nothing)
    print("Starting countdown...")
    print_countdown()
    print("Countdown finished.")
    
    # Testing Discount (Expected: Eligible for discount, Actual: Regular pricing)
    discount_status = check_discount_eligibility(70)
    print(f"Age 70 status: {discount_status}")
