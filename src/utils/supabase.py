import urllib


def generate_supabase_conection_string(base_string, supabase_password, username=None):
    base_string = base_string.replace("[YOUR-PASSWORD]", urllib.parse.quote(supabase_password))

    if username:
        base_string = base_string.replace("[YOUR-USERNAME]", urllib.parse.quote(username))

    return base_string.strip()
