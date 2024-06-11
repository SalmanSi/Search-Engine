import os
import json
from json.decoder import JSONDecodeError



#creates url_list json file if it does not exist
def create_url_file(url_file_name):
    
    if os.path.exists(url_file_name):
        print("\nFile already exists\n")
        with open(url_file_name,'r') as url_in:
            # try to load data    
            content=url_in.read(2)
        if not content:
            # if file empty, add an empty array
            print("file was empty\n")
            with open(url_file_name,'w') as url_in:
                json.dump([],url_in)
    else:
        with open(url_file_name,'w') as url_list:
            print("\nfile created\n")
            json.dump([],url_list)  

def dump_url_data(data,url_file_name):
    
    #create file if does not exist
    create_url_file(url_file_name)

    with open(url_file_name,'r') as url_in:
        #load old urls list
        old_list=json.load(url_in)
        #print(f"old_list: {old_list}\n")
        # add the new urls
        old_list+=data
        #print(f"New list {old_list}\n")
        # save the updated list
        with open(url_file_name,'w') as url_out:
            json.dump(old_list,url_out)
            print("new urls added")


def get_url_id(url_file_name):
    create_url_file(url_file_name)
    with open(url_file_name,'r') as url_out:
        content=json.load(url_out)
        return(len(content))