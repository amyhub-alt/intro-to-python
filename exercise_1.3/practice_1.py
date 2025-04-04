first_value = int(input("Enter first number: "))
second_value = int(input("Enter second number: "))
select_operator = str(input("Choose + or -."))

if select_operator == "+":
    result = first_value + second_value
    print("Result:", result)

elif select_operator == "-":
    result = first_value - second_value
    print("Result:", result)

else:
    print("unknown operator")