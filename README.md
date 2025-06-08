# 🔐 Password Hashing with Passlib

This project uses [Passlib](https://passlib.readthedocs.io/en/stable/) for secure password hashing.

## ✅ Configuration

We use `CryptContext` with the `bcrypt` hashing scheme:

```bash
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

## 🔍 About `deprecated="auto"`

- Automatically marks all schemes **except the first one** in the list as deprecated.
- Ensures new passwords are hashed with the **preferred algorithm** (`bcrypt` in this case).
- Still allows verification of passwords hashed with older (deprecated) algorithms.
- Helps in **migrating users to stronger password hashes over time**.

## ♻️ Optional Password Rehashing on Login

You can automatically upgrade old password hashes during user login:

```bash
if pwd_context.verify(plain_password, hashed_password) and pwd_context.needs_update(hashed_password):
    new_hash = pwd_context.hash(plain_password)
    # Save `new_hash` to the database
```