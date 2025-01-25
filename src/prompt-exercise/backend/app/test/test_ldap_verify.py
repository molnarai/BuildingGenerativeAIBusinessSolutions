#!/usr/bin/env python3

# import unittest
import os
import sys
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(ROOT_DIR))
# print(sys.path)

import getpass
import os

from utils.security import ldap_verify_user, ldap_search_user

if __name__ == '__main__':
    
    os.environ['LDAP_SERVER_URI'] = 'ldap://10.230.100.236'
    os.environ['LDAP_BASE_DN'] = 'dc=insight,dc=gsu,dc=edu'

    username = input('Username: ')
    password = getpass.getpass('Password: ')

    # Check if the user exists in LDAP
    user_exists = ldap_verify_user(username, password)
    print(f"User {username} exists in LDAP: {user_exists}")
    user_info = ldap_search_user(username, password)
    print(f"User {username} info: {user_info}")

    

