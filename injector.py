import colorama, time, subprocess, requests , argparse, os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


parser = argparse.ArgumentParser(description='Injector - Smart parameter injection tool')

# --- Input Group ---
input_group = parser.add_argument_group('Input Options')
input_group.add_argument('-l', '--urlspath', help='Path to file containing list of target URLs for Injection.', required=True)
input_group.add_argument('-w', '--wordlist',    help='Path to a file containing parameters to fuzz for reflection',required=False)

# --- Modes ---
notif_group = parser.add_argument_group('Mode')
notif_group.add_argument('-vm' , '--valuemode' ,help='How to apply valuemode: {"append" , "replace"} (default \"append\")',choices=['append', 'replace'],default='append',required=False)
notif_group.add_argument('-gm', '--generatemode',help='Control how parameters are generated: {"root", "ignore", "combine", "all"} (default: "all")',choices=['root', 'ignore', 'combine', 'all'],default='all',required=False)

# --- Configurations ---
notif_group = parser.add_argument_group('Configurations')
input_group.add_argument('-c', '--chunk', help='Number of URLs to process per batch (default: 25)', default=25, required=False)

# --- Notification & Logging Group ---
notif_group = parser.add_argument_group('Notification & Logging')
notif_group.add_argument('-s', '--silent', help='Disable prints output to the command line (default False)', action='store_true', default=False, required=False)

# --- Output ---
notif_group = parser.add_argument_group('Outputs')
notif_group.add_argument('-o', '--output', help='Path to file where discovered URLs should be saved', required=False)


args = parser.parse_args()

#Input & Group
urls_path = args.urlspath
parameter = args.parameter

#Mode
value_mode = args.valuemode
generate_mode = args.generatemode

#Configuration
chunk = args.chunk

#Notification
silent = args.silent



def sendmessage(message: str, telegram: bool = False, colour: str = "YELLOW", logger: bool = True , silent : bool = False):
    color = getattr(colorama.Fore, colour, colorama.Fore.YELLOW)
    if not silent:
        print(color + message + colorama.Style.RESET_ALL)
    time_string = time.strftime("%d/%m/%Y, %H:%M:%S", time.localtime())
    if logger:
        with open('logger.txt', 'a') as file:
            file.write(message + ' -> ' + time_string + '\n')

    if telegram:
        token_bot = {YOUR_TOKEN_BOT} 
        chat_id = "5028701156"
        url = f"https://api.telegram.org/bot{token_bot}/sendMessage"
        payload = {'chat_id': chat_id, 'text': message}
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Telegram message failed: {e}")



def read_write_list(list_data: list, file: str, type: str):

    objects = []
    
    if type == "read" or type == 'r':
        with open(file, 'r') as f:
            objects = set(f.read().splitlines())
        return objects
    
    elif type == "write" or type == 'w': 
        with open(file, 'w') as f:
            for item in set(list_data):
                f.write(item.strip() + '\n')


    elif type == "append" or type == 'a':
        try:
            with open(file, 'r') as f:
                existing_items = set(f.read().splitlines())
        except FileNotFoundError:
            existing_items = set()
        
        with open(file, 'a') as f:
            for item in set(list_data):
                if item.strip() and item not in existing_items:
                    f.write(item.strip() + '\n')



def injector (urls : list , generate_mode : str , value_mode : str , parameter : str) -> list:

    def append_mode(url, parameter , value_mode):
        urls_generated = []
        parsed = urlparse(url)
        query_pairs = parse_qsl(parsed.query, keep_blank_values=True)
        for i in range(len(query_pairs)):
            modified_pairs = query_pairs.copy()
            key, value = modified_pairs[i]
            modified_pairs[i] = (key, value + parameter) if value_mode == 'append' else (key, parameter)
            new_query = urlencode(modified_pairs)
            new_url = urlunparse(parsed._replace(query=new_query))
            urls_generated.append(new_url)

        return urls_generated


    def normal_mode (urls , value_mode , parameter):
        pass
    def ignore_mode (urls , value_mode , parameter):
        pass

    def combine_mode (urls , value_mode , parameter):
        for url in urls :
            if '?' in url:
                urls_generated = append_mode(url , parameter , value_mode)
                

    if generate_mode == 'combine':
        combine_mode(urls , value_mode , parameter)
    elif generate_mode == 'normal':
        pass
    elif generate_mode == 'ignore':
        pass


try:
    all_parameters = []
    urls = read_write_list("", urls_path, 'r')
    injector(urls , generate_mode , value_mode , parameter)
    # light_reflector(urls)

except Exception as e:
    sendmessage(
        f"An error occurred: {str(e)}",
        telegram=notification,
        colour="RED",
        logger=logger,
        silent=silent
    )