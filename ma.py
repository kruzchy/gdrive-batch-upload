from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import send2trash

gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

local_folder = input('Enter the name of the folder: ')
os.chdir(local_folder)
file_links_dict = {}

folder1 = drive.CreateFile(
        {'title': local_folder, 'mimeType': 'application/vnd.google-apps.folder'})
folder1.Upload()

for file in os.listdir():
    file1 = drive.CreateFile({'title': file, 'parents': [{'id': folder1['id'], 'kind': 'drive#fileLink'}]})
    file1.SetContentFile(file)
    file1.Upload()
    file1.InsertPermission({
        'type': 'anyone',
        'value': 'anyone',
        'role': 'reader', })
    print(f'>>Uploading {folder1["title"]}\\{file1["title"]}')

    file_links_dict[file1['title']] = file1['alternateLink']
    file1 = None
    # send2trash.send2trash(file)
print(file_links_dict)
os.chdir('..')
with open('file_links.txt', 'w') as f:
    outp = ''
    for key in file_links_dict:
        outp += f'{key} :\n{file_links_dict[key]}\n\n'
    f.write(outp)
print('>>file links written to file_links.txt')
