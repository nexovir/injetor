import colorama, time, subprocess, requests , argparse, os
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import pyfiglet

banner = pyfiglet.figlet_format("Injector")
parser = argparse.ArgumentParser(description='Injector - Smart parameter injection tool')

# --- Input Group ---
input_group = parser.add_argument_group('Input Options')
input_group.add_argument('-l', '--urlspath', help='Path to file containing list of target URLs for Injection.', required=True)
input_group.add_argument('-w', '--wordlist',    help='Path to a file containing parameters to fuzz for reflection',required=False)
input_group.add_argument('-p', '--parameter', help='Comma-separated parameter to test for reflection (default: "nexovir")', default='nexovir', required=False)

# --- Modes ---
notif_group = parser.add_argument_group('Mode')
notif_group.add_argument('-vm' , '--valuemode' ,help='How to apply valuemode: {"append" , "replace"} (default \"append\")',choices=['append', 'replace'],default='append',required=False)
notif_group.add_argument('-gm', '--generatemode',help='Control how parameters are generated: {"root", "ignore", "combine", "all"} (default: "all")',choices=['root', 'ignore', 'combine', 'all'],default='all',required=False)

# --- Configurations ---
notif_group = parser.add_argument_group('Configurations')
input_group.add_argument('-c', '--chunk', help='Number of URLs to process per batch (default: 25)',type=int,  default=25, required=False)

# --- Notification & Logging Group ---
notif_group = parser.add_argument_group('Notification & Logging')
notif_group.add_argument('-s', '--silent', help='Disable prints output to the command line (default False)', action='store_true', default=False, required=False)

# --- Output ---
notif_group = parser.add_argument_group('Outputs')
notif_group.add_argument('-o', '--output', help='Path to file where discovered URLs should be saved', required=False)


args = parser.parse_args()

#Input & Group
urls_path = args.urlspath
wordlist = args.wordlist
parameter = args.parameter

#Mode
value_mode = args.valuemode
generate_mode = args.generatemode

#Configuration
chunk = args.chunk

#Notification
silent = args.silent

print(banner) if not silent else None


def read_write_list(list_data: list, file: str, type: str):

    objects = []
    
    if type == "read" or type == 'r':
        with open(file, 'r') as f:
            objects = list(set(line.strip() for line in f.read().splitlines() if line.strip()))
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



def injector (urls : list , generate_mode : str , value_mode : str , parameter : str , wordlist_parameters : list , chunk : int) -> list:
    all_urls = []
    def value_mode_generate(url, parameter , value_mode):
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

    def append_parameter(urls, parameter, wordlist_parameters, chunk):
        urls_generated = []
        for url in urls:
            for i in range(0, len(wordlist_parameters), chunk):

                chunk_params = wordlist_parameters[i:i + chunk]

                query_string = '&'.join([f"{p}={parameter}" for p in chunk_params])

                if '?' in url:
                    full_url = f"{url}&{query_string}"
                else:
                    full_url = f"{url}?{query_string}"

                urls_generated.append(full_url)
                
        return urls_generated


    def root_mode(urls , parameter, wordlist_parameters, chunk):
        valid_urls = []
        for url in urls:
            base_url = url.split('?')[0]
            if base_url not in valid_urls:
                valid_urls.append(base_url)

        urls_generated = append_parameter(valid_urls, parameter, wordlist_parameters, chunk)
        all_urls.extend(urls_generated)

    def ignore_mode (urls , value_mode , parameter):
        urls_generated = append_parameter(urls, parameter, wordlist_parameters, chunk)
        all_urls.extend(urls_generated)

    def combine_mode (urls , value_mode , parameter):
        for url in urls :
            if '?' in url:
                urls_generated = value_mode_generate(url , parameter , value_mode)
                all_urls.extend(urls_generated)


    if generate_mode == 'combine':
        combine_mode(urls , value_mode , parameter)

    elif generate_mode == 'root':
        root_mode(urls , parameter , wordlist_parameters , chunk)

    elif generate_mode == 'ignore':
        ignore_mode(urls , value_mode , parameter)

    else:
        combine_mode(urls , value_mode , parameter)
        root_mode(urls , parameter , wordlist_parameters , chunk)
        ignore_mode(urls , value_mode , parameter)
    return all_urls


try:
    all_parameters = []
    urls = read_write_list("", urls_path, 'r')
    wordlist_parameters = read_write_list("", wordlist, 'r') if wordlist else []
    all_urls = injector(urls , generate_mode , value_mode , parameter , wordlist_parameters , chunk)    
    for url in all_urls :
        print(url)
        
except Exception as e:
    print(
        f"An error occurred: {str(e)}",
    )