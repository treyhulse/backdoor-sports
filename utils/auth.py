def authenticate_user(username, password, db):
    user = db['accounts'].find_one({"username": username})
    if user and user['password'] == password:  # Use hashed passwords in production
        return user
    return None

def get_user_permissions(user, db):
    role = db['roles'].find_one({"role": user['role']})
    if role:
        permissions = db['permissions'].find_one({"role_id": role['_id']})
        return permissions['permissions'] if permissions else []
    return []

def check_permission(user, required_permission, db):
    user_permissions = get_user_permissions(user, db)
    return required_permission in user_permissions
