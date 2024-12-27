def test_input(user_input):
    # Business logic to check for the word "Friday"
    if "Friday" in user_input:
        return f"Hello! You said: {user_input}"
    else:
        return "No trigger word detected."