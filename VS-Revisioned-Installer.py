import sys
from time import sleep
import base64
from winreg import OpenKey, HKEY_CURRENT_USER, QueryValueEx, CloseKey
import requests
import zipfile
from tqdm import tqdm
from shutil import copy2, rmtree
from os import makedirs, walk, rmdir, remove, getenv, getcwd, system, path, listdir
from re import search, findall


directory = getcwd()


def find_game_path(game_name):
    drives = ['A:\\', 'B:\\', 'C:\\', 'D:\\', 'E:\\', 'F:\\', 'G:\\', 'H:\\', 'I:\\', 'J:\\', 'K:\\', 'L:\\', 'M:\\', 'N:\\', 'O:\\', 'P:\\', 'Q:\\', 'R:\\', 'S:\\', 'T:\\', 'U:\\', 'V:\\', 'W:\\', 'X:\\', 'Y:\\', 'Z:\\']

    for drive in drives:
        try:
            root_dirs = listdir(drive)
            for root_dir in root_dirs:
                candidate_path = path.join(drive, root_dir, "steamapps", "common", game_name)
                if path.exists(candidate_path):
                    return candidate_path.replace('/', '\\')
        except (PermissionError, FileNotFoundError):
            # Ignore any permission or file not found errors and continue to the next drive
            pass
    
    return None

game_name = "VampireSlayerTheResurrection"
game_path = find_game_path(game_name)

if game_path:
    print("Game installation path:", game_path)
    pak_path = path.join(game_path.strip(), "ISZ", "Content")
    exe_path = path.join(game_path.strip(), "ISZ", "Binaries", "Win64")


if game_path == None:
    def get_steam_game_path(game_name):
        try:
            steam_key = OpenKey(HKEY_CURRENT_USER, r"Software\Valve\Steam")
            steam_install_path = QueryValueEx(steam_key, "SteamPath")[0]
            game_vdf_path = path.join(steam_install_path, "steamapps", "appmanifest_{}.acf".format(game_name))
        
            with open(game_vdf_path, 'r') as f:
                content = f.read()

            start_index = content.find('"installdir"') + 13
            end_index = content.find('"', start_index)
            game_install_dir = content[start_index:end_index]
            game_path = path.join(steam_install_path, "steamapps", "common", game_install_dir)
        
            return game_path.replace('/', '\\')  # Replace forward slashes with backslashes

        except FileNotFoundError:
            return None

    game_name = "2188960"  # AppID

    game_path = get_steam_game_path(game_name)

    if game_path:
        print("Game installation path:", game_path)
        pak_path = path.join(game_path.strip(), "VampireSlayerTheResurrection", "ISZ", "Content")
        exe_path = path.join(game_path.strip(), "VampireSlayerTheResurrection", "ISZ", "Binaries", "Win64")
    
    if game_path == None:
        print("Unable To Find Vampire Slayer: The Resurrection Installation Path.")
        print("When Providing Directory please Inlcude the Folder 'VampireSlayerTheResurrection'.")
        game_path = input("Please Type Installation Path: ")

        if "\\VampireSlayerTheResurrection" in game_path:
            pak_path = path.join(game_path.strip(), "ISZ", "Content")
            exe_path = path.join(game_path.strip(), "ISZ", "Binaries", "Win64")
        else:
            print("Not A Valid Directory. Please Re-Input the Install Directory. Or Reinstall the Game.")
            sleep(3)
            system('clear')
            get_steam_game_path()


def get_steam32_id():
    try:
        # Read the Steam configuration file
        with open(r"C:\Program Files (x86)\Steam\config\config.vdf", "r") as file:
            content = file.read()
        
        # Use regular expressions to extract the Steam64 ID
        match = search(r'"SteamID"\s+"(\d+)"', content)
        if match:
            steam64_id = match.group(1)
            steam32_id = steam64_to_steam32(steam64_id)
            return steam32_id
        
        return None
        
    except Exception as e:
        return None

def steam64_to_steam32(steam64_id):
    steam32_id = int(steam64_id) - 76561197960265728
    return steam32_id

# Call the function to retrieve the Steam32 ID
steam32_id = get_steam32_id()

if steam32_id:
    print(" ")
else:
    if path.exists("Windows\\sysWOW64"):
        print("Steam32 ID Doesn't Exist. Assumption of Pirated or Cracked Copy.")
        print("If you think this is an Error, or Are getting this Message Wrongfully.")
        print("Please report it here: 'https://github.com/ISZ-Hacker-Organization/VS-Revisioned-Installer/issues' Thank You.")
        sleep(9)
        exit()
    else:
        print("Operating System Isn't Windows-NT or 9X. Mod is Uncompatible with Linux and Unix Systems.")
        sleep(4)
        exit()





def read_numerical_digits():
    try:
        # Get the local AppData directory
        appdata_dir = getenv('LOCALAPPDATA')

        # Construct the full file path
        file_path = path.join(appdata_dir, 'VS', 'Saved', 'SaveGames', 'steam_autocloud.vdf')

        with open(file_path, "r") as file:
            lines = file.readlines()

        # Extract numerical digits from the third line using regular expressions
        third_line = lines[2].strip()  # Access the third line and remove leading/trailing whitespaces
        digits = findall(r'\d+', third_line)

        # Combine the digits into a single string
        result = ''.join(digits)

        result = int(result)

        return result

    except Exception as e:
        print("Error reading SteamAppID digits:", e)
        return None

# Call the function to read numerical digits
numerical_digits = read_numerical_digits()

var_steamid = steam32_id + 76561197960265728 

if numerical_digits:
    if numerical_digits == steam32_id:
        print(f"Verification Passed Successfully '{numerical_digits} = {var_steamid}'.")
        print(" ")
    else:
        print("Unable To Verify Legitimate Copy.")
        print("If you think this is an Error, or Are getting this Message Wrongfully.")
        print("Please report it here: 'https://github.com/ISZ-Hacker-Organization/VS-Revisioned-Installer/issues' Thank You.")
        sleep(9)




url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/Single_Player.zip'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('SinglePlayerMod.zip', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()




url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/0xDBA2149AE61C394EEACE1D4CC8C9F9767C74D2401A7DFA29C5923AEDEC11ED49.key.txt'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('0xDBA2149AE61C394EEACE1D4CC8C9F9767C74D2401A7DFA29C5923AEDEC11ED49', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()


url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/server_c.txt'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('server_c', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()


url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/dxgi.dll'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('dxgi.dll', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()

url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/ISZ-Win64-Shipping-Patch.I2plg'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('ISZ-Win64-Shipping.exe', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()

url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/UnrealModUnlocker.dll'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('UnrealModUnlocker.dll', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()

url = 'https://github.com/Cracko298/VS-Revisioned/releases/download/v0.1-alpha-1/_mod.dll'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('_mod.dll', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()


url = 'https://github.com/Cracko298/VS-Revisioned-Files/releases/download/v0.1-alpha-1/ISZ-Win64-Shipping.profile'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('ISZ-Win64-Shipping.profile', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()


url = 'https://github.com/Cracko298/VS-Revisioned-Files/releases/download/v0.1-alpha-1/ModLoaderInfo.ini'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('ModLoaderInfo.ini', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()



url = 'https://github.com/Cracko298/VS-Revisioned-Files/releases/download/v0.1-alpha-1/UnrealEngineModLoader.dll'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('UnrealEngineModLoader.dll', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()



url = 'https://github.com/Cracko298/VS-Revisioned-Files/releases/download/v0.1-alpha-1/xinput1_3.dll'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('xinput1_3.dll', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()

url = 'https://github.com/Cracko298/VS-Revisioned-Files/releases/download/v0.1-alpha-1/UnrealModUnlocker-Settings.ini'

response = requests.get(url, stream=True)
total_size = int(response.headers.get('content-length', 0))

# Create a tqdm instance with the total file size
progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

# Download the file in chunks and update the progress bar
with open('UnrealModUnlocker-Settings.ini', 'wb') as file:
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            file.write(chunk)
            progress_bar.update(len(chunk))

# Close the progress bar
progress_bar.close()





print("Download(s) complete.")

print(" ")

import zipfile
from tqdm import tqdm

zip_path = 'SinglePlayerMod.zip'
extract_path = directory

try:
    # Get the total number of files in the zip archive
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        total_files = len(zip_ref.infolist())

    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all contents to the specified path
        extracted_files = []
        with tqdm(total=total_files, unit='file') as pbar:
            for file in zip_ref.infolist():
                zip_ref.extract(file, extract_path)
                extracted_files.append(file.filename)
                pbar.update(1)

    print("Extraction(s) complete.")
except zipfile.BadZipFile:
    print("Error: The specified file is not a valid ZIP archive.")
except FileNotFoundError:
    print(f"Error: File '{zip_path}' not found.")

remove(zip_path)
print(f"Pak File Directory: {pak_path}.")
print(f"Exe File Directory: {exe_path}.")

sleep(1.5)

plugin_path = path.join(exe_path,"UnrealModPlugins")
profile_path = path.join(plugin_path, "Profiles")

print(" ")
print(f"Installing Patch Into: {exe_path}.")
makedirs(plugin_path, exist_ok=True)
makedirs(profile_path, exist_ok=True)

file_list = [
    ("_mod.dll", path.join(plugin_path, path.basename("_mod.dll"))),
    ("UnrealModUnlocker.dll", path.join(plugin_path, path.basename("UnrealModUnlocker.dll"))),

    ("xinput1_3.dll", path.join(plugin_path, path.basename("xinput1_3.dll"))),
    ("UnrealEngineModLoader.dll", path.join(plugin_path, path.basename("UnrealEngineModLoader.dll"))),

    ("ISZ-Win64-Shipping.profile", path.join(profile_path, path.basename("ISZ-Win64-Shipping.profile"))),
    ("ModLoaderInfo.ini", path.join(plugin_path, path.basename("ModLoaderInfo.ini"))),
    
    ("0xDBA2149AE61C394EEACE1D4CC8C9F9767C74D2401A7DFA29C5923AEDEC11ED49", path.join(exe_path, path.basename("0xDBA2149AE61C394EEACE1D4CC8C9F9767C74D2401A7DFA29C5923AEDEC11ED49"))),
    ("UnrealModUnlocker-Settings.ini", path.join(exe_path, path.basename("UnrealModUnlocker-Settings.ini"))),
    ("dxgi.dll", path.join(exe_path, path.basename("dxgi.dll"))),
    ("server_c", path.join(exe_path, path.basename("server_c"))),
    ("ISZ-Win64-Shipping.exe", path.join(exe_path, path.basename("ISZ-Win64-Shipping.exe")))
]

for source_file, destination_file in tqdm(file_list, desc="Copying Patch Files", unit="file"):
    copy2(source_file, destination_file)

mod_files = path.join(directory, "Single_Player")

sleep(1)
print(" ")
print(f"Installing Mod Into: {pak_path}.")

file_list = []

for root, dirs, files in walk(mod_files):
    for file in files:
        source_file = path.join(root, file)
        relative_path = path.relpath(source_file, mod_files)
        destination_file = path.join(pak_path, relative_path)
        file_list.append((source_file, destination_file))

for source_file, destination_file in tqdm(file_list, desc="Copying Mod Files", unit="file"):
    makedirs(path.dirname(destination_file), exist_ok=True)
    copy2(source_file, destination_file)

sleep(1)
print(" ")
print(f"Removing Temp Files.")



file_paths = [
    path.join(directory, "_mod.dll"),
    path.join(directory, "UnrealModUnlocker.dll"),
    path.join(directory, "0xDBA2149AE61C394EEACE1D4CC8C9F9767C74D2401A7DFA29C5923AEDEC11ED49"),
    path.join(directory, "dxgi.dll"),
    path.join(directory, "server_c"),
    path.join(directory, "ISZ-Win64-Shipping.exe"),
    path.join(directory, "UnrealModUnlocker-Settings.ini"),
    path.join(directory, "ISZ-Win64-Shipping.profile"),
    path.join(directory, "ModLoaderInfo.ini"),
    path.join(directory, "UnrealEngineModLoader.dll"),
    path.join(directory, "xinput1_3.dll"),
]

for file_path in tqdm(file_paths, desc="Removing files", unit="file"):
    if path.isfile(file_path):
        remove(file_path)




if path.exists(mod_files):
    with tqdm(total=sum([len(files) for _, _, files in walk(mod_files)]), desc="Deleting Temp Directory", unit="file") as pbar:
        try:
            rmtree(mod_files)
            pbar.update(81)
        except Exception as e:
            pbar.update(0)
        pbar.close()


print(" ")
print("Installed 'VS: Revisioned' Successfully.")
print("Closing Window in '5' Seconds.")
sleep(5)