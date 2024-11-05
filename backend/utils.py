from constants import supabase


def create_user(email: str, password: str):
    response = supabase.auth.sign_up({
        "email": email, 
        "password": password
    })
    return response
