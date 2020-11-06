def validate_email(email):
    """
    Checks if email matches requirements.

    Parameters:
    email (str): email address string

    Returns:
    bool : Success
    """
    if len(email) >= 5 and '@' in email and '.' in email:
        return check_valid_chars(email)
    else:
        return False


def validate_password(password):
    """
    Checks if password matches requirements.

    Parameters:
    password (str): password string

    Returns:
    bool : Success
    """
    if len(password) >= 2:
        return check_valid_chars(password)
    else:
        return False


def validate_username(username):
    """
    Checks if username matches requirements.

    Parameters:
    username (str): username string

    Returns:
    bool : Success
    """
    if len(username) >= 2:
        return check_valid_chars(username)
    else:
        return False


def check_valid_chars(word):
    """
    Checks if word contains invalid characters.

    Parameters:
    word (str): word string

    Returns:
    bool : Success
    """
    for c in word:
        if ord(c) < 33 and ord(c) > 126:
            return False
    return True
