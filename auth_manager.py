login_status = {"is_logged_in": False, "attempts": 0}

# Reset the login attempts counter
def reset_attempts():
    login_status["attempts"] = 0

# Increment the login attempts counter
def increment_attempts():
    login_status["attempts"] += 1

# Check if the user is locked out due to failed attempts
def is_locked_out():
    return login_status["attempts"] >= 3

# Basic login mechanism for reauthorization
def login(user, password):
    if user == "admin" and password == "admin123":
        login_status["is_logged_in"] = True
        reset_attempts()
        return True
    return False
