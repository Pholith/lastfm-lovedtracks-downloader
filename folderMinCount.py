import os
import shutil
import sys

def find_loved_tracks_folder():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    for folder in os.listdir(script_dir):
        if  folder.endswith("lovedtracks") and os.path.isdir(os.path.join(script_dir, folder)):
            return os.path.join(script_dir, folder)
    return None


def reorganize_files(minimum_file_count: int):

    root_folder = find_loved_tracks_folder()
    if not root_folder:
        print("Folder 'lovedTracks' not found.")
        return

    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        
        if os.path.isdir(folder_path):
            files = os.listdir(folder_path)
            
            if len(files) < minimum_file_count:
                file_path = os.path.join(folder_path, files[0])
                destination_path = os.path.join(root_folder, files[0])
                
                shutil.move(file_path, destination_path)
                os.rmdir(folder_path)
                print(f"Folder removed: {files[0]}")

minimumFileCountBeforeErase : int= 2
if len(sys.argv) > 0:
    minimumFileCountBeforeErase = sys.argv[1]

reorganize_files()
