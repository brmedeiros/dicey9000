#!/usr/bin/python3

def login_token(login_info):
    try:
        token_input = open(login_info, 'rU')
        token = token_input.read().replace('\n', '')
    except FileNotFoundError:
        token = login_info
    return token

if __name__ == '__main__':
    main()
