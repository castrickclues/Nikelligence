import requests
import json
import argparse

def email_lookup(email, token, json_file=None):

    if not token:
        with open('token.txt', 'r') as f:
            token = f.read().strip()
            if not token:
                print('[!] JWT token not found in token.txt. Please refer to the README.md for instructions on how to obtain the token or enter it manually via -t')
                return


    URL = f"https://api.nike.com/usersearch/search/v2?searchstring={email}"
    HEADERS = {
        "User-Agent": "NRC/4.36.0 (prod; 1711163123; Android 11.1.0; samsung SM-G781B)",
        "Appid": "com.nike.sport.running.droid",
        "Authorization": f'Bearer {token}'
    }

    response = requests.get(URL, headers=HEADERS, timeout=10)

    if response.status_code == 401:
        print('[!] Expired/Invalid Token')
        return
    elif response.status_code != 200:
        print('[!] Error: ', response.status_code)
        print('[!] Response: ', response.text)
        return

    try:
        objects = response.json().get('objects')

        if not objects:
            print('[!] No results found')
            return
        else:
            data = objects[0]

        if data.get('email').lower() != email.lower():
            return None

        id = data.get('upmId')
        firstname = data.get('firstName')
        lastname = data.get('lastName')
        username = data.get('displayName')
        hometown = data.get('hometown')
        visibility = data.get('visibility')
        avatar = data.get('imageUrl')

        info = {
            "id": id,
            "avatar": avatar,
            "username": username,
            "first_name": firstname,
            "last_name": lastname,
            "location": hometown,
            "visibility": visibility
        }

        info = {k: v for k, v in info.items() if v is not None and v != '' and v != 0}

        print("\n[*] Result")
        print("-" * 50)
        if id:
            print(f'{"ID:":<15}{id}')
        if username:
            print(f'{"Username:":<15}{username}')
        if avatar:
            print(f'{"Avatar:":<15}{avatar}')
        if firstname:
            print(f'{"First Name:":<15}{firstname}')
        if lastname:
            print(f'{"Last Name:":<15}{lastname}')
        if hometown:
            print(f'{"Location:":<15}{hometown}')
        if visibility:
            print(f'{"Visibility:":<15}{visibility}')
        print("\n")

        if json_file:
            with open(f'{json_file}.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(info, indent=4))
            print(f'\n[+] Results exported to {json_file}.json\n')

    except Exception as e:
        print(f'\n[!] Error: {e}\n')
        return None

def name_filter(input, firstname, lastname):
    input = input.lower()
    input_parts = input.split(' ')

    if len(input_parts) == 1:
        return True

    input_firstname = input_parts[0]
    input_lastname = input_parts[1]

    firstname = firstname.lower()
    lastname = lastname.lower()

    if (input_firstname == firstname and input_lastname == lastname) or (input_lastname == firstname and input_firstname == lastname):
        return True

    return False

def email_filter(input, email):
    first_name_only = False

    input = input.lower()
    input_parts = input.split(' ')

    if len(input_parts) == 1:
        first_name_only = True

    email = email.lower()

    if first_name_only:
        if input in email:
            return True
    else:
        firstname = input_parts[0]
        lastname = input_parts[1]

        if (firstname in email) and (lastname in email):
            return True

    return False

def email_domain_filter(email, domain):
    email = email.lower()
    domain = domain.lower()

    email_domain = email.split('@')[1]
    if email_domain == domain:
        return True

    return False

def name_lookup(full_name, token, email_only_mode=False, name_strict_mode=False, email_strict_mode=False, email_domain=None, json_file=None):

    if not token:
        with open('token.txt', 'r') as f:
            token = f.read().strip()
            if not token:
                print('[!] JWT token not found in token.txt. Please refer to the README.md for instructions on how to obtain the token or enter it manually via -t')
                return


    URL = f"https://api.nike.com/usersearch/search/v2?searchstring={full_name}"
    HEADERS = {
        "User-Agent": "NRC/4.36.0 (prod; 1711163123; Android 11.1.0; samsung SM-G781B)",
        "Appid": "com.nike.sport.running.droid",
        "Authorization": f'Bearer {token}'
    }

    response = requests.get(URL, headers=HEADERS, timeout=10)

    if response.status_code == 401:
        print('[!] Expired/Invalid Token')
        return
    elif response.status_code != 200:
        print('[!] Error: ', response.status_code)
        print('[!] Response: ', response.text)
        return

    try:
        objects = response.json().get('objects')

        if not objects:
            print('[!] No results found')
            return
        else:
            data = objects

        total_results = len(data)
        print(f'\n[+] Found {total_results} results\n')

        results = []
        filtered_results = 0

        for account in data:
            id = account.get('upmId')
            firstname = account.get('firstName')
            lastname = account.get('lastName')
            username = account.get('displayName')
            hometown = account.get('hometown')
            visibility = account.get('visibility')
            avatar = account.get('imageUrl')
            email = account.get('email')

            if email_only_mode and not email:
                filtered_results += 1
                continue
            if name_strict_mode and not name_filter(full_name, firstname, lastname):
                filtered_results += 1
                continue
            if email_strict_mode and email and not email_filter(full_name, email):
                filtered_results += 1
                continue
            if email_domain and email and not email_domain_filter(email, email_domain):
                filtered_results += 1
                continue

            info = {
                "email": email,
                "id": id,
                "avatar": avatar,
                "username": username,
                "first_name": firstname,
                "last_name": lastname,
                "location": hometown,
                "visibility": visibility
            }
            info = {k: v for k, v in info.items() if v is not None and v != '' and v != 0}
            results.append(info)

            print("-" * 50)
            if email:
                print(f'{"Email:":<15}{email}')
            if id:
                print(f'{"ID:":<15}{id}')
            if username:
                print(f'{"Username:":<15}{username}')
            if avatar:
                print(f'{"Avatar:":<15}{avatar}')
            if firstname:
                print(f'{"First Name:":<15}{firstname}')
            if lastname:
                print(f'{"Last Name:":<15}{lastname}')
            if hometown:
                print(f'{"Location:":<15}{hometown}')
            if visibility:
                print(f'{"Visibility:":<15}{visibility}')
            print("\n")

        if filtered_results:
            print(f'[+] Filtered {filtered_results} results due to strict mode enabled\n')

        if json_file:
            with open(f'{json_file}.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(results, indent=4))
            print(f'\n[+] Results exported to {json_file}.json\n')


    except Exception as e:
        print(f'\n[!] Error: {e}\n')
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Look up an email address or a name on Nike Run Club - by @castrickclues -')
    parser.add_argument('-e', '--email', help='Email to lookup. Example: "johndoe@gmail.com"')
    parser.add_argument('-n', '--name', help='Name to lookup. Example: "John Doe"')
    parser.add_argument('-t', '--token',help='Provide the JWT token manually. Example: eyJ..')
    parser.add_argument('-eD','--email-domain', help='Filter results by email domain. Example: "gmail.com" [Name lookup only]')
    parser.add_argument('-eO','--email-only', action='store_true', help='Show only results that have an email [Name lookup only]')
    parser.add_argument('-nS','--name-strict', action='store_true', help='Show only results that match the full name strictly (Works with fullnames only) [Name lookup only]')
    parser.add_argument('-eS','--email-strict', action='store_true', help='Show only results that contains the full name in the email username part [Name lookup only]')
    parser.add_argument('--json', help='Export results to a JSON file.')

    args = parser.parse_args()

    if not args.email and not args.name:
        parser.error('Either --email or --name must be specified.')

    if args.email:
        email_lookup(args.email, args.token, args.json)
    else:
        name_lookup(args.name, args.token, args.email_only, args.name_strict, args.email_strict, args.email_domain, args.json)
