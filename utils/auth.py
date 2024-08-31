# utils/auth.py

def authenticate_user(username, password, db):
    """
    Authenticate a user by checking if the username and password match an entry in the database.
    
    Parameters:
    - username: The username provided by the user.
    - password: The password provided by the user.
    - db: The MongoDB database connection.

    Returns:
    - user: The user document if authentication is successful, None otherwise.
    """
    user = db['accounts'].find_one({"username": username})
    if user and user['password'] == password:  # Ideally, use hashed password comparison
        return user
    return None

def get_user_permissions(user, db):
    """
    Retrieve the permissions associated with a user's role.
    
    Parameters:
    - user: The user document.
    - db: The MongoDB database connection.

    Returns:
    - permissions: A list of permissions associated with the user's role.
    """
    # Fetch the role document
    role = db['roles'].find_one({"role": user['role']})
    
    if role:
        # Fetch the permissions document
        permissions = db['permissions'].find_one({"role_id": role['_id']})
        
        if permissions:
            return permissions['permissions']
        else:
            return []
    else:
        return []

def check_permission(user, required_permission, db):
    """
    Check if a user has a specific permission.
    
    Parameters:
    - user: The user document.
    - required_permission: The permission to check.
    - db: The MongoDB database connection.

    Returns:
    - bool: True if the user has the required permission, False otherwise.
    """
    user_permissions = get_user_permissions(user, db)
    return required_permission in user_permissions
