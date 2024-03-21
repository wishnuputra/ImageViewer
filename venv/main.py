todos = []

while True:
    user_action = input("Type add, show, or exit: ")

    match user_action:
        case 'add':
            todo = input("Enter a todo: ")
            todos.append(todo)
        case 'show':
            [print(todo) for todo in todos]
        case 'exit':
            break
        case _:
            print("Not a valid input, please type again!!!")

print("Bye")