import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import os
from datetime import datetime
import hashlib

stemmer = SnowballStemmer("english")
stop_words = set(stopwords.words('english'))
additional_stop_words = ['@', '.', ',', '”', '\'', '“', ';', ':', '-', "and"]
stop_words.update(additional_stop_words)

def clean_query(query):
    words = word_tokenize(query)
    stemmed_words = [stemmer.stem(word) for word in words]
    filtered_stem_words = [word.lower() for word in stemmed_words if word not in stop_words and word.isalnum()]
    return filtered_stem_words

def hash_to_bucket(word):
    hash_object = hashlib.sha256(word.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    return f'barrel_{hash_value % 4000}'

def search_inverted_indices(query, inverted_index_directory):
    print("\nstarting\n")


    # Initialize a set to store common URLs
    common_urls = set()
    all_urls=set()
    for word in query:
        # Determine the barrel for the word based on the first character
        barrel = hash_to_bucket(word)
        
        print(f"Loading file...{datetime.now()}\n")
        time=datetime.now()
        # Load the inverted index only if the barrel is relevant
        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)
                print(f"File loaded...time to load={datetime.now()-time}\n")
                time=datetime.now()
                # Check if the word is in the inverted index
                if word in inverted_index:
                    word_info = inverted_index[word]
                    # Extract URLs for the current word
                    urls = {entry['u'] for entry in word_info}
                    all_urls=all_urls.union(urls)
                    # If common_urls is empty, set it to the current URLs, else take the intersection
                    common_urls = common_urls.intersection(urls) if common_urls else urls
                print(f"time inside a barrel={datetime.now()-time}\n")
    un_common_urls=all_urls.difference(common_urls)
                
    
    return list(common_urls),list(un_common_urls)

# # Example usage
# inverted_index_directory = r'C:\Users\HP\Desktop\Data Structures\project\inverted_index'
# query = r'professor killed student in america street'
# time=datetime.now()
# cleaned_query = clean_query(query)
# result_urls = search_inverted_indices(cleaned_query, inverted_index_directory)
# print("\n".join(result_urls))
# print(f"\n\ntotal time={datetime.now()-time} ")

# Example usage
# inverted_index_directory = r'C:\Users\admin\Desktop\DSA\project\indices\inverted_index'
# query= input("Enter Query: ")
# time = datetime.now()
# cleaned_query = clean_query(query)
# common_result_urls,uncommon_result_urls = search_inverted_indices(cleaned_query, inverted_index_directory)

# url_list_path = r"C:\Users\admin\Desktop\DSA\project\indices\url_list.json"

# # Read the contents of the JSON file into a Python list
# try:
#     with open(url_list_path, "r") as json_file:
#         url_list_data = json.load(json_file)
# except FileNotFoundError:
#     # Handle the case when the file doesn't exist
#     url_list_data = []
#time=datetime.now()-time
#print(f"\n\ntotal time={datetime.now()-time}")
# Now, url_list_data contains the data loaded from the JSON file
# s=0
# print("\n!!COMMON URLS !!\n-------------\n")
# for doc in common_result_urls:
#     print(url_list_data[doc])
#     if s==50:
#         break
# print(f"\n\ntotal time={time}")
# print(f"\ntotal docs= {len(common_result_urls)}")

# print("\n!!UNCOMMON URLS !!\n-------------\n")
# for doc in uncommon_result_urls:
#     print(url_list_data[doc])
# print(f"\n\ntotal time={time}")
# print(f"\ntotal docs= {len(uncommon_result_urls)}")
