# Description

Nikelligence is a tool allowing you to look up an email address or a name on Nike Run Club (NRC) fitness app.
##### Using this tool to search for a name will typically return results that include users' email addresses. We've added filtering utilities to help refine these results.

## Prerequisites

- Python 3.x
- `requests` library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/castrickclues/Nikelligence.git
    cd Nikelligence
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
## Obtaining your JWT token
For this tool to work, it needs a JWT token for authentication.

#### Follow these steps to get yours:

1 - Visit [Nike](https://www.nike.com/) website

2 - Create an account

3 - While being logged in, open your browser DevTools (F12) then go to the *Network* tab

4 - In the Filter search bar, search for `api.nike.com`

5 - Pick any matching request and in the *Headers* tab look for *Request Headers*

6 - Copy the `Authorization` header value without the `Bearer ` part, it starts with `eyJ...`

7 - Put it in `token.txt` or provide it manually via `-t`



## Usage

### Searching by Email

To search for a user by their email address, use the `-e` or `--email` flag followed by the email address. This will retrieve user information associated with the provided email.

```bash
python nikelligence.py -e "johndoe@gmail.com"
```

### Searching by Name

To search for a user by their name, use the -n or --name flag followed by the full name enclosed in double quotes. This method retrieves accounts matching the provided full name. While it's possible to search by first or last name alone, using the full name ensures more accurate results.

```bash
python nikelligence.py -n "John Doe"
```

#### Additional Filters (Name Lookup Only)

`-eO`, `--email-only`: Show only results that have an email (since some results may not contain an email)

`-nS`, `--name-strict`: Show only results that match the full name strictly (works with fullnames only)

`-eS`, `--email-strict`: Show only results that contains the full name in the email username part

`-eD`, `--email-domain`: Filter results by email domain. Example: "gmail.com"


##### Example

```bash
python nikelligence.py -n "John Doe" -eO -nS -eS -eD "gmail.com"
```


## Disclaimer 

This tool is provided for educational purposes only. The use of this tool is at your own risk. We do not take responsibility for any misuse or illegal activities conducted with this tool. It is intended to be used responsibly and ethically for legitimate purposes
