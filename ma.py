from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import send2trash
local_folder = input('Enter the name of the folder: ')
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

folder_name = 'gdrive_folder'
limit = 45
os.chdir(local_folder)
folder_num = 1
count_limit = 0
start = True
folder_links_dict = {}
for file in os.listdir():
    count_limit += 1
    if start:
        folder1 = drive.CreateFile(
            {'title': folder_name + f'_{folder_num}', 'mimeType': 'application/vnd.google-apps.folder'})
        folder1.Upload()
        folder1.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        folder_links_dict[folder1['title']] = folder1['alternateLink']
        start = False

    if count_limit > limit:
        count_limit = 1
        folder_num += 1
        folder1 = drive.CreateFile({'title': folder_name + f'_{folder_num}', 'mimeType': 'application/vnd.google-apps.folder'})
        folder1.Upload()
        folder1.InsertPermission({
            'type': 'anyone',
            'value': 'anyone',
            'role': 'reader'})
        folder_links_dict[folder1['title']] = folder1['alternateLink']

    file1 = drive.CreateFile({'title': file, 'parents': [{'id': folder1['id'], 'kind': 'drive#fileLink'}]})
    print(f'>>Uploading to {folder1["title"]}\\{file1["title"]}')
    file1.SetContentFile(file)
    file1.Upload()
    file1 = None
    send2trash.send2trash(file)
print(folder_links_dict)
os.chdir('..')
with open('folder_links.txt', 'w') as f:
    outp = ''
    for key in folder_links_dict:
        outp += f'{key} : {folder_links_dict[key]}\n'
    f.write(outp)
print('>>folder links written to folder_links.txt')
