from flask import Flask, jsonify, redirect, request
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)


"""
---------------------------------------- FUNCTIONS ----------------------------------------
"""


def extract_token(url):
    match = re.search(r'&x=([a-f0-9]+)', url)
    if match:
        return match.group(1)
    return None


def extract_download_link(html):
    soup = BeautifulSoup(html, 'html.parser')
    download_button = soup.find('div', class_='downloadButton')
    if download_button:
        link = download_button.find('a')['href']
        return link
    return None


"""
---------------------------------------- ROUTES ----------------------------------------
"""


# when someone goes to /versions, run this function
@app.route('/versions', methods=['GET'])
def get_versions():
    url = 'https://optifine.net/downloads'  # cloudflare
    response = requests.get(url)
    html = response.content  # get the html

    soup = BeautifulSoup(html, 'html.parser')  # parse the html
    mirror_links = []  # create an empty list

    for link in soup.find_all('a', href=lambda href: href and "optifine.net/adloadx" in href):
        href = link['href']
        if "adfoc.us/" not in href:
            mirror_links.append(href)  # add the download url to the list

    return jsonify({'mirror_links': mirror_links})  # return the list as json


@app.route('/dl', methods=['GET'])
def download_version():
    adloadx_link = request.args.get('link')
    if adloadx_link:
        response = requests.get(adloadx_link)
        download_link = extract_download_link(response.content)
        return redirect(f"https://optifine.net/{download_link}")

    return jsonify({'error': 'Invalid adloadx link'})


# auto run the app
if __name__ == '__main__':
    app.run()
