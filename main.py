# AviOS: This is where AviOS starts. Light intro, tone, art/visual
# Will adjust intro text later maybe with stylings
# Greet the user when AviOS(software) launches

print("AviOS is starting up. Let's build something real.")

# Show the main menu so the user can pick what they want to do
print("\nWhat do you want to do?")
print("1. Tasks")
print("2. Habits")
print("3. Expenses")

# Wait for the user to type a number and store it
choice = input("\nPick a number: ")

# Respond based on what they picked
# will later replace these with real features
if choice == "1":
    print("Opening Tasks...")
elif choice == "2":
    print("Opening Habits...")
elif choice == "3":
    print("Opening Expenses...")
else:
    print("That's not a valid option. Try 1, 2 or 3.")