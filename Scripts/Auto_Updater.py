import requests
import shutil
import os

def download_file_from_google_drive( destination):
    URL = "https://www.googleapis.com/drive/v3/files/1oNHvtQ9ASsnH3ycjbKQlnnn-XNEvjtGH"

    session = requests.Session()

    response = session.get(URL, params = { 'alt' : 'media' , 'key': "AIzaSyBqT7OwhNEk9v1zZCiwykfgcvnlXSprxW8", 'confirm': 1 }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = {'alt' : 'media' , 'key': "AIzaSyBqT7OwhNEk9v1zZCiwykfgcvnlXSprxW8", 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb+") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                print('working')
                f.write(chunk)

if __name__ == "__main__":
    file_id = 'TAKE ID FROM SHAREABLE LINK'
    shutil.rmtree('extracts',ignore_errors=True)
    os.mkdir('extracts')
    destination = './extracts/temp.rar'
    download_file_from_google_drive(destination)
    shutil.unpack_archive(filename='./extracts/temp.rar',extract_dir="./extracts",format="zip")
    print("Hello")
    input()
    shutil.rmtree('extracts',ignore_errors=True)
    