from os import system as syst
import sys
import requests

def gdrive_linux(link, name):
  if name == "":
    print("ERROR - You haven't specified file name")
    sys.exit(0)

  FILEID = f'https://docs.google.com/uc?export=download&id={link}'
  FILENAME = name
  syst(f'wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate {FILEID} -O- | sed -rn \'s/.*confirm=([0-9A-Za-z_]+).*/\1\n/p\')&id={link}" -O {FILENAME} && rm -rf /tmp/cookies.txt')

def gdrive(id, destination):
    def get_confirm_token(response):
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return value

        return None

    def save_response_content(response, destination):
        CHUNK_SIZE = 32768

        with open(destination, "wb") as f:
            for chunk in response.iter_content(CHUNK_SIZE):
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)