from ldap3 import Server, Connection, ALL, SUBTREE
from ldap3.core.exceptions import LDAPBindError

def ldap_search_user(username: str, password: str):
    """
    Connect to an LDAP server using root credentials, verify the user's password,
    and return user information if the password matches.

    Args:
        username (str): The username of the user to authenticate.
        password (str): The password of the user to authenticate.

    Returns:
        dict: A dictionary containing user information if authentication is successful.
        None: If authentication fails or the user is not found.
    """
    # LDAP server details
    ldap_server_url = "ldap://your-ldap-server.com"  # Replace with your LDAP server URL
    base_dn = "dc=example,dc=com"  # Replace with your base DN
    root_dn = "cn=admin,dc=example,dc=com"  # Replace with your root DN
    root_password = "rootpassword"  # Replace with your root password

    try:
        # Initialize the LDAP server
        server = Server(ldap_server_url, get_info=ALL)

        # Connect to the LDAP server using root credentials
        with Connection(server, user=root_dn, password=root_password, auto_bind=True) as conn:
            # Search for the user in the LDAP directory
            search_filter = f"(cn={username})"
            conn.search(
                search_base=base_dn,
                search_filter=search_filter,
                search_scope=SUBTREE,
                attributes=['givenName', 'sn', 'mail', 'uidNumber', 'gidNumber', 'memberOf']
            )

            if conn.entries:
                user_entry = conn.entries[0]  # Get the first matching entry
                user_dn = user_entry.entry_dn  # Get the distinguished name (DN) of the user

                # Attempt to bind with the user's credentials to verify the password
                try:
                    with Connection(server, user=user_dn, password=password, auto_bind=True):
                        # If bind is successful, return user information
                        user_info = {
                            "first_name": user_entry.givenName.value if hasattr(user_entry.givenName, 'value') else None,
                            "last_name": user_entry.sn.value if hasattr(user_entry.sn, 'value') else None,
                            "email": user_entry.mail.value if hasattr(user_entry.mail, 'value') else None,
                            "uid": user_entry.uidNumber.value if hasattr(user_entry.uidNumber, 'value') else None,
                            "gid": user_entry.gidNumber.value if hasattr(user_entry.gidNumber, 'value') else None,
                            "groups": [group.split(',')[0].split('=')[1] for group in user_entry.memberOf] if hasattr(user_entry.memberOf, 'values') else []
                        }
                        return user_info
                except LDAPBindError:
                    # Password does not match
                    return None

            # User not found
            return None

    except Exception as e:
        print(f"Error connecting to LDAP server: {e}")
        return None


# Example usage
if __name__ == "__main__":
    username = "testuser"
    password = "testpassword"
    result = ldap_search_user(username, password)
    if result:
        print("User authenticated successfully:")
        print(result)
    else:
        print("Authentication failed or user not found.")
