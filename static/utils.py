import bcrypt


def hash_password(password: str) -> str:
    password = password.encode()
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt).decode()


def validate_password(password: str, hashed_password: str) -> bool:
    password: bytes = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)