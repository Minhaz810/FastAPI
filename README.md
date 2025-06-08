## 🧭 Built In Utiliy for FastAPI auth

Instead of usinng pydantic schema to retrieve user's credentials, we can use fastapi security

# 📘 FastAPI OAuth2 + JWT Authentication Flow

This document explains how the authentication flow works in a FastAPI app using `Depends`, OAuth2, and JWTs.

---

## 🔁 Overview

The app uses:

- `OAuth2PasswordBearer` to extract the Bearer token from requests.
- A `get_current_user()` dependency to validate the JWT token.
- `Depends()` to inject dependencies automatically into routes.

---

## 📍 Route Handler

```python
@router.get("/")
def get_all_posts(
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user)
):
    posts = db.query(models.Post).all()
    return {"data": posts}
```

1. Depends(get_db): Injects a database session.
2. Depends(get_current_user): Extracts and validates the JWT token, returning the user ID.

## 🔐 OAuth2 Password Bearer
```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
```
1. FastAPI expects the token in the Authorization: Bearer <token> header.
2. It extracts the token, but does not validate it.

## 🧾 get_current_user Function
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    return verify_access_token(token, credentials_exceptions)
```

1. Receives the token from oauth2_scheme.
2. Defines a standard 403 Forbidden error if the token is invalid.
3. Calls verify_access_token() to decode and validate the token.

## 🧠 verify_access_token Function
```python
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: int = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data
```
1. Decodes the token using SECRET_KEY and ALGORITHM.
2. Extracts user_id from the payload.
3. If missing or invalid, raises the HTTPException.
4. Wraps the user ID in a TokenData schema and returns it.

## ✅ What Depends() Does
__Depends() tells FastAPI:__

“Call this function first, and inject its return value into the route or another function.”

When you write this:
```python
def get_current_user(token: str = Depends(oauth2_scheme)):
```
1. Sees Depends(oauth2_scheme).
2. Calls the oauth2_scheme function (which extracts the token from the header).
3. Passes the result (the token string) as the token argument to get_current_user.