import json
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
import hashlib
import os
from datetime import datetime 
import math

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




def load_inverted_index(inverted_index_directory, barrel):
    inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
    with open(inverted_index_path, 'r') as json_file:
        return json.load(json_file)
    
    
def calculate_tf_idf(inverted_index_directory, query):
    # Step 1: Calculate TF for each word in the query for each URL
    tf_scores = {}
    for word in query:
        
        # print("printing the word")
        # print(word)
        # input("Press Enter to continue...")
        # print("proceded with word", word)
        barrel = hash_to_bucket(word)
        inverted_index=load_inverted_index(inverted_index_directory,barrel)

        if word in inverted_index:
            for entry in inverted_index[word]:
                url = entry['u']
                frequency = entry['f']
                if url not in tf_scores:
                    tf_scores[url] = {}
                tf_scores[url][word] = frequency

    # Step 2: Calculate IDF for each word
    idf_scores = {}
    total_documents = 150000
    for word in query:
        # print("printing the word")
        # print(word)
        # input("Press Enter to continue...")
        # print("proceded with word", word)
        barrel = hash_to_bucket(word)
        inverted_index=load_inverted_index(inverted_index_directory,barrel)

        if word in inverted_index:
            documents_containing_word = len(inverted_index[word])
            idf_scores[word] = math.log(total_documents / (1 + documents_containing_word))

    # Step 3: Calculate TF-IDF scores for each URL
    tf_idf_scores = {}
    for url, tf_values in tf_scores.items():
        score = 0
        for word, tf in tf_values.items():
            if word in idf_scores:
                score += tf * idf_scores[word]
        tf_idf_scores[url] = score

    # Step 4: Sort URLs based on their TF-IDF scores
    sorted_urls = sorted(tf_idf_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_urls

def search_inverted_indices(query, inverted_index_directory):
    # Initialize a dictionary to store URLs and their frequencies

    url_frequencies = {}
    common_urls=set()
    all_urls=set()
    # Initialize a dictionary to store positions for each URL
    url_positions = {}

    for word in query:
        # Determine the barrel for the word based on the first character
        # print(word)
        

        
        barrel = hash_to_bucket(word)
        # print(barrel)
        # Load the inverted index only if the barrel is relevant
        if barrel != 'other_barrel':
            inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
            with open(inverted_index_path, 'r') as json_file:
                inverted_index = json.load(json_file)

                # Check if the word is in the inverted index
                if word in inverted_index:
                    word_info = inverted_index[word]
                    # Extract URLs for the current word
                    urls = {entry['u'] for entry in word_info}
                    all_urls=all_urls.union(urls)
                    # If common_urls is empty, set it to the current URLs, else take the intersection
                    common_urls = common_urls.intersection(urls) if common_urls else urls
    return all_urls


#query= input("Enter Query: ")
time=datetime.now()
inverted_index_directory = r'C:\Users\admin\Desktop\3rd Semester\DSA\project\indices\inverted_index'
# cleaned_query=clean_query(query)
# common_urls = search_inverted_indices(cleaned_query, inverted_index_directory)
# result = calculate_tf_idf(inverted_index_directory, cleaned_query)
# 

# url_list_path = r"C:\Users\admin\Desktop\DSA\project\indices\url_list.json"

# # Read the contents of the JSON file into a Python list
# try:
#     with open(url_list_path, "r") as json_file:
#         url_list_data = json.load(json_file)
# except FileNotFoundError:
#     # Handle the case when the file doesn't exist
#     url_list_data = []

# Now, url_list_data contains the data loaded from the JSON file

# Print URLs with their TF-IDF scores in sorted order
# s=0
# print("printing the common urls")
# for url, score in result:
#     if(s==50):
#         break
#     if(url in common_urls):
#         print(f"URL: {url_list_data[url]}")#\tScore: {score}")
#         s+=1
# print(f"\n\ntotal time={datetime.now()-time}\nTotal docs={s}")

