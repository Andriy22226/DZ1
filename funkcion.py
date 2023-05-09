# from tools import *
import os
import sys
import shutil
from pathlib import Path
import Constants as CON


def normalize(adress: str, filename: str) -> None:
    find_kirilic = [x for x in CON.CIRILIC_SYMV if x in filename.lower()]
    name_cln = ""
    if len(find_kirilic) > 0:
        result = filename.translate(CON.TRANS)
        for el in result:
            if el.isalpha() or el.isalnum() or el == ".":
                name_cln += el
            if el in CON.OTHER:
                name_cln += el.replace(el, "_")
        oldname = os.path.join(adress, filename)
        newname = os.path.join(adress, name_cln)
        os.rename(oldname, newname)


    
def new_dir(path: Path, newDirName: str) -> Path:
   # creat new directory. Skips if directory exists.
    newDir = path / newDirName
    newDir.mkdir(exist_ok=True)
    return newDir


    
def get_all_items(path: Path):
    # Generator that yield items recursively from dirs and subdirs.
    for item in path.iterdir():
        if item.is_dir():
            yield from get_all_items(item)
        else:
            yield item

count_removed_dirs = 0

    
def remove_empty_dirs(path: str | Path) -> int:
    # Deletes empty dirs recursively. Returns integer number of removed dirs.
    
    global count_removed_dirs

    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            remove_empty_dirs(os.path.join(root, dir))
        if not dirs and not files:
            os.rmdir(root)  
            #  os.rmdir() removes only if dir is empty
            count_removed_dirs += 1

    return count_removed_dirs

def del_empty_dirs(adress: str) -> None:
    for dirs in os.listdir(adress):
        dir = os.path.join(adress, dirs)
        if os.path.isdir(dir):
            del_empty_dirs(dir)
            if not os.listdir(dir):
                os.rmdir(dir)



def move_to_folder(file: Path, localPath: Path) -> Path:
    # moves the file, if the name matches adds a suffix and creates a new path.
    max_attempts = 50
    suffix = 1

    local_file_path = localPath / file.name # If the file exists, prohibits overwhite
    while local_file_path.exists() and suffix <= max_attempts:
        suffix += 1
        local_file_path = localPath / f"{file.stem}_{suffix}{file.suffix}"

    if suffix > max_attempts:
        raise Exception(   
            "Could not move file, maximum number of attempts reached")

    file.rename(local_file_path)
    return local_file_path

def sort_dir(path: str | Path, unpackArch=True) -> tuple:
    file_formats = {
    'Audio': ['.mp3', '.wav', '.aac', '.wma'],
    'Video': ['.mp4', '.avi', '.mkv', '.wmv',],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp'],
    'Documents': ['.dot', '.odi', '.sxc', '.sxd', '.doc', '.txt'],
    'Archives': ['.zip', '.rar', '.tar.gz', '.7z']
    }
    log_list = []
    unpack_counter = 0
    path = Path(path)
    files = [file for file in get_all_items(path)]

    for file in files:
        for categ, formats in file_formats.items():
            if file.suffix.lower() in formats:

                if categ == "Archives" and unpackArch == True and file.suffix in {".zip", ".tar", ".gztar", ".bztar", ".xztar"}:
                    # Avoid backup archive if such was made
                    if file.stem == path.name + "_backup":
                        break
                    locat_to_unpack = new_dir(path, categ)
                    unpack_arch_and_remove(file, locat_to_unpack)
                    unpack_counter += 1
                    break
                else:
                    locat_dir = new_dir(path, categ)
                    new_file_path = move_to_folder(file, locat_dir)
                    log_list.append((file, new_file_path))
                    break

        else:
            locat_dir = new_dir(path, "Unknown")
            new_file_path = move_to_folder(file, locat_dir)
            log_list.append((file, new_file_path))

    return log_list, unpack_counter

def deep_folders(adress: str) -> None:
    for el in os.listdir(adress):
        way = os.path.join(adress, el)
        if os.path.isdir(way):
            files_in_way = os.listdir(way)
            for file in files_in_way:
                shutil.move(os.path.join(way, file), adress)
                del_empty_dirs(adress)
            if not os.path.isdir(adress):
                break
            else:
                deep_folders(adress)

def transfer_files(adress: str, folder_name: str, files: list) -> None:
    if folder_name not in adress:
        os.chdir(adress)
        os.mkdir(folder_name)
    if folder_name == "archives":
        to_unpack_folder = os.path.join(adress, folder_name)
        os.chdir(to_unpack_folder)
        for arch_name in files:
            name = arch_name.split(".")[0]
            os.mkdir(name)
            path_to_unpack = os.path.join(to_unpack_folder, name)
            file_for_unpack = os.path.join(adress, arch_name)
            try:
                shutil.unpack_archive(file_for_unpack, path_to_unpack)
                os.remove(file_for_unpack)
            except shutil.ReadError:
                all_err_arch = []
                error_name = os.path.split(file_for_unpack)
                all_err_arch.append(error_name[-1])
                del_empty_dirs(os.path.join(adress, "archives"))
                global all_resume
                all_resume += (
                    f"file {all_err_arch} has an archive extension, but is not an archive.\n"
                )
    if folder_name != "archives":
        file_locatination = os.path.join(adress, folder_name)
        for file in files:
            shutil.move(os.path.join(adress, file), file_locatination)

def unpack_arch_and_remove(file: Path, locat: Path):
    # Unpacks archive to the given dir and removes it after.
    locatDir = locat / file.stem
    shutil.unpack_archive(file, locatDir)
    file.unlink()


def main(path):
    normalize(path)
    sort_dir(path)
    remove_empty_dirs(path)


if __name__ == '__main__':
    try:
        path = rf"{sys.argv[1]}"
        try:
            main(path)
        except FileNotFoundError as e:
            print(f"Invalid path argument: {e}")
    except IndexError as err:
        print(f"At least 1 argument should be passed: {err}")
