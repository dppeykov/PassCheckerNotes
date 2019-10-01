import requests
import hashlib
import sys

def request_api_data(query_char):

    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching from the API: {res.status_code}. Check the API and try again!')
    return res

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0
    

def pwned_api_check(password):
    # Check the password if it exists in the API responce
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_chars, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_chars)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} found {count} times. You should probably change your password!')
        else:
            print(f'{password} was not found. It is a good password and you can continue to use it!')
    return 'Done!'
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


