def process_financial_data(income, expenses, zip_code, apply_tax_discount=True):
    total_expenses = 0
    
    # Logic Error 1: Off-by-one / Exclusive iteration
    # The function intends to iterate through a list of expenses, but range(0, len(expenses)) 
    # misses the very first expense because it starts at index 1 conceptually.
    for i in range(1, len(expenses)):
        total_expenses += expenses[i]
        
    # Logic Error 2: Incorrect scope / Variable shadowing
    # Calculates a tax bracket/multiplier. Because 'total_income' is shadowed incorrectly,
    # the tax multiplier is completely wrong and yields a skewed output.
    total_income = 0
    if income > 10000:
        total_income = income * 0.15
    else:
        total_income = income * 0.05
        
    # Logic Error 3: Operator precedence
    # The developer forgot parentheses, so division is evaluated before addition.
    # It divides total_expenses by 12, then adds total_income, instead of dividing the sum by 12.
    average_monthly_net = total_income + total_expenses / 12
    
    # Logic Error 4: Mutating a boolean during evaluation
    # If the user qualifies for a discount, the variable is overwritten by a string. 
    # When this flag is checked later, it evaluates unexpectedly.
    if apply_tax_discount:
        if zip_code == "90210" and total_expenses > 5000:
            apply_tax_discount = "Qualifies for 10% Off"
            
    return {
        "net_budget": average_monthly_net, 
        "discount_status": apply_tax_discount,
        "raw_income": income
    }

