#! /usr/bin/env python3
"""
Simple script for downloading MagPi magazine
python3 magpi.py <issuenr>
python3 magpi.py <start-issuenr> <end-issuenr>
"""
import os
import requests
import sys
import pathlib

one_issue = 2
multi_issues = 3
num_args = len(sys.argv)
if num_args < 2:
    exit("Specify issue(s) to download")
if num_args > 3:
    exit("Can only specify one issue or an start and end issue")

start = None
if num_args >= one_issue:
    try:
        start = int(sys.argv[1])
    except ValueError as ve:
        print(f"Specify a number, not '{sys.argv[1]}'")
        exit()

end = None
if num_args == multi_issues:
    try:
        end = int(sys.argv[2])
    except ValueError as ve:
        print(f"Specify a number, not '{sys.argv[2]}'")
        exit()
    except IndexError as ve:
        print("\nNot spesified ending nr. Will just download one issue\n")

if not start:
    print("\nStrange things\n")
    exit()

if not end:
    end = start

if end:
    if start > end:
        start, end = end, start

for nr in range(start, end+1):
    if nr < 10:
        nr = "0" + str(nr)
    else:
        nr = str(nr)
    dl_url = f"https://magpi.raspberrypi.org/issues/{nr}/pdf/download"
             
    web = requests.get(dl_url)
    web_content = str(web.content)
    web_content = web_content.split('<')
    download_link = ""
    for i in web_content:
        if 'href="/downloads/' in i and ".pdf" in i:
            dl_string = i.split('href="')[1]
            dl_string = dl_string.split('">')[0]
            download_link = "https://magpi.raspberrypi.org" + dl_string
        if download_link:
            break

    if download_link:
        dl_path = f"/Users/{os.getlogin()}/Documents/Magazines/MagPi/MagPi{nr}.pdf"
        if os.path.exists(dl_path):
            print(f"MagPi{nr}.pdf already downloaded")
        else:
            f_path = os.path.dirname(dl_path)
            pathlib.Path(f_path).mkdir(parents=True, exist_ok=True)
            print(f"Downloading Magpi{nr} - {download_link}")
            myfile = requests.get(download_link)
            print(f"Saving Magpi{nr} - {dl_path}")
            open(dl_path, 'wb').write(myfile.content)
    else:
        print(f"Found no download link to Magpi issue {nr}")
