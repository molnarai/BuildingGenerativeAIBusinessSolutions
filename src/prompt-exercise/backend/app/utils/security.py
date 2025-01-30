from passlib.context import CryptContext
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from ldap3 import Server, Connection, ALL, Tls
import ssl
from ldap3.core.exceptions import LDAPBindError
import os
from typing import Dict
import socket

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def ldap_verify_user(username: str, password: str) -> bool:
    """
    Authenticate a user against a self-hosted LDAP server.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """
    # Initialize the LDAP server
    ldap_server_url = os.getenv("LDAP_SERVER_URI")
    base_dn = os.getenv("LDAP_BASE_DN")
    assert ldap_server_url is not None, "LDAP_SERVER_URI environment variable is not set"
    assert base_dn is not None, "LDAP_BASE_DN environment variable is not set"
    users_dn = f"ou=Users,{base_dn}"  
    user_dn = f"uid={username},{users_dn}" 
    
    # Optional: Configure TLS for secure connection
    tls_configuration = Tls(validate=ssl.CERT_NONE)  # Adjust validation as needed

    try:
        # Initialize the LDAP server
        server = Server(ldap_server_url, get_info=ALL) ## , use_ssl=True, tls=tls_configuration)

        # Attempt to bind (authenticate) with provided credentials
        with Connection(server, user=user_dn, password=password, auto_bind=True) as conn:
            print(f"Authentication successful for user: {username}")
            # for j, entry in enumerate(conn.entries):
            #     print(f"Entry: {entry}")
            return True

    except LDAPBindError as e:
        print(f"Authentication failed for user: {username}. Error: {e}")
        # return {"error": "Authentication failed"}
        return False
    

def extract_ldap_user_info(entry) -> dict:
    """
    Extract relevant fields from an LDAP entry object
    
    Args:
        entry: ldap3.abstract.entry.Entry object
    
    Returns:
        dict: Dictionary containing user information
    """
    user_info = {}
    
    # List of attributes to extract if they exist
    attributes = [
        'givenName',
        'sn',  # surname
        'cn',  # common name
        'uid',
        'mail',
        'uidNumber',
        'gidNumber',
        'memberOf',
        'gecos',  # display name
    ]
    
    for attr in attributes:
        try:
            if hasattr(entry, attr):
                # Handle multi-valued attributes (like memberOf)
                if isinstance(entry[attr].value, list):
                    user_info[attr] = entry[attr].values
                else:
                    user_info[attr] = entry[attr].value
        except (AttributeError, KeyError):
            continue

    # Clean up the memberOf groups to just get the group names
    if 'memberOf' in user_info:
        user_info['groups'] = [
            group.split(',')[0].split('=')[1] 
            for group in user_info['memberOf']
        ]

    return {
        "first_name": user_info.get('givenName'),
        "last_name": user_info.get('sn'),
        "display_name": user_info.get('gecos'),
        "email": user_info.get('mail'),
        "uid": user_info.get('uidNumber'),
        "gid": user_info.get('gidNumber'),
        "groups": user_info.get('groups', [])
    }


def ldap_search_user(username: str, password: str) -> Dict:
    ldap_server_url = os.getenv("LDAP_SERVER_URI")
    host = "10.230.100.236"
    port = 389
    if test_tcp_connection(host, port):
        print("**** Connection established ***")
    else:
        print(f"**** Unable to connect to LDAP server at {host}:{port} ****")
        return None

    base_dn = os.getenv("LDAP_BASE_DN")
    assert ldap_server_url is not None, "LDAP_SERVER_URI environment variable is not set"
    assert base_dn is not None, "LDAP_BASE_DN environment variable is not set"
    users_dn = f"ou=Users,{base_dn}"  
    user_dn = f"uid={username},{users_dn}"

    try:
        server = Server(ldap_server_url, get_info=ALL)

        with Connection(server, user=user_dn, password=password, auto_bind=True) as conn:
            search_filter = f"(uid={username})"
            conn.search(
                search_base=base_dn,
                search_filter=search_filter,
                attributes=['*']  # Request all attributes
            )

            if conn.entries:
                user_entry = conn.entries[0]
                return extract_ldap_user_info(user_entry)
            
            print(f"No entries found for username: {username}")
            return None

    except LDAPBindError as e:
        print(f"Authentication failed for user: {username}. Error: {e}")
        return None


def test_tcp_connection(hostname, port):
    """
    Establish a TCP connection to the given hostname or IP address on the specified port.

    Args:
        hostname (str): The hostname or IP address to connect to.
        port (int): The port number to connect to.

    Returns:
        bool: True if the connection is successful, False otherwise.
    """

    # Create a socket object
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set a timeout of 1 second for the connection attempt
    sock.settimeout(1)

    try:
        # Attempt to connect to the host on the specified port
        sock.connect((hostname, port))
        
        # If we reach this point, it means the connection was successful
        return True

    except socket.timeout:
        # If a timeout occurs, it means the connection attempt took too long (i.e., failed)
        return False

    except ConnectionRefusedError:
        # If a ConnectionRefusedError occurs, it means the host refused our connection request
        return False

    finally:
        # Regardless of whether an exception was raised or not, close the socket to free up resources
        sock.close()