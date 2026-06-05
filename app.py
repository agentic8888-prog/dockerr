from agent import run_agent

print("File Agent Started")

while True:

    user_input = input("\nYou: ")

    if user_input.lower() == "exit":
        break

    response = run_agent(user_input)

    print("\nAgent:")
    print(response)
    