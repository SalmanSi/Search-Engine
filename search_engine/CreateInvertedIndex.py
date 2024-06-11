import json
import os
from collections import defaultdict
import timeit
import hashlib

def hash_to_barrel(word):
    hash_object = hashlib.sha256(word.encode())
    hash_value = int(hash_object.hexdigest(), 16)
    return f'barrel_{hash_value % 4000}'

def update_inverted_indices(forward_index_directory, inverted_index_directory):
    inverted_indices = {f'barrel_{i}': defaultdict(list) for i in range(4000)}

    forward_index_files = [f for f in os.listdir(forward_index_directory) if f.endswith('.json')]

    # Load existing inverted indices
    for inverted_index_file in os.listdir(inverted_index_directory):
        inverted_index_path = os.path.join(inverted_index_directory, inverted_index_file)
        with open(inverted_index_path, 'r') as json_file:
            existing_inverted_index = json.load(json_file)
            barrel_name = inverted_index_file.replace('inverted_index_', '').replace('.json', '')
            inverted_indices[barrel_name] = existing_inverted_index

    # Iterating through each forward index file
    for forward_index_file in forward_index_files:
        forward_index_file_path = os.path.join(forward_index_directory, forward_index_file)

        with open(forward_index_file_path, 'r') as json_file:
            forward_index_data = json.load(json_file)

        # Iterating through each article in the forward index
        for article in forward_index_data:
            words_info = article['w']

            # Go through each word in the article
            for word, info in words_info.items():
                barrel = hash_to_barrel(word)
                try:
                    # Check if the word already exists in the inverted index for the current barrel
                    existing_entries = inverted_indices[barrel][word]

                    # If the word exists, append information to the existing list
                    if existing_entries:
                        existing_entries.append({
                            'u': article['u'],  # You can include the URL here if needed
                            'f': info['f'],
                            'p': info['p']
                        })
                    else:
                        # If the word doesn't exist, create a new entry
                        inverted_indices[barrel][word].append({
                            'u': article['u'],
                            'f': info['f'],
                            'p': info['p']
                        })
                except KeyError:
                    print(f"KeyError: {barrel}")

    # Save the updated inverted indices
    for barrel, inverted_index in inverted_indices.items():
        inverted_index_path = os.path.join(inverted_index_directory, f'inverted_index_{barrel}.json')
        
        # Measure the time it takes to dump the JSON data
        start_time = timeit.default_timer()
        with open(inverted_index_path, 'w') as json_file:
            json.dump(inverted_index, json_file)
        elapsed_time = timeit.default_timer() - start_time
        print(f"Dumping took approximately {elapsed_time} seconds.\n")

# input and output paths specified 
#forward_index_directory = r'C:\Users\admin\Desktop\DSA\project\indices\forward_index'
#inverted_index_directory = r'C:\Users\admin\Desktop\DSA\project\indices\inverted_index'

# function to create/update inverted index called
#update_inverted_indices(forward_index_directory, inverted_index_directory)
