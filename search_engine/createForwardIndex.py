#nltk used for tokenization,stemming and frequency distribution 
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from nltk.stem import SnowballStemmer
from nltk.corpus import stopwords
from json.decoder import JSONDecodeError
import sys
sys.path.append(r"C:\Users\admin\Desktop\3rd Semester\DSA\project")  # Adjust the relative path as needed
# json module to work with json files
import json 

# os module to work with the file system
import os
from .filing import get_url_id,dump_url_data




# Function to create forward index
# Arguments:
# input_directory - Directory containing newsdata in json files
# output_directory - Directory in which forward index is saved
# output_prefix - foward_index files created with this prefix
# batch_size - maximum number of articles allowed to be saved in a single forward_index json file 
url_list_path = r"C:\Users\admin\Desktop\3rd Semester\DSA\project\indices\url_list.json"
batch_count = 0 #counts number of batches 


def Create_Forward_Index(input_file_path,output_directory,output_prefix='forward_index', batch_size=10000):
    
    count =0#counts total number of documents processed
    batch_count =0#counts number of batches 
    doc_id=get_url_id(url_list_path)
    # list initialized to hold forward index entries
    forward_index_list = [] 

    #list for storing urls
    url_list=[]

    # English stemmer initialized
    stemmer = SnowballStemmer("english")  

    # some stop words are added and saved in a set (as they allow faster memberhsip tests) 
    stop_words = set(stopwords.words('english'))
    additional_stop_words = ['@', '.', ',', '”', '\'', '“', ';', ':', '-', "and"]
    stop_words.update(additional_stop_words)

    # news articles loaded in articles variable
    with open(input_file_path, 'r') as inputFile:
        articles = json.load(inputFile)

        # loop to iterate through all articles in the input file
        for article in articles:

            # content and title of each article is tokenized and saved in words list
            words = word_tokenize(article['content'])
            title = word_tokenize(article['title'])
            words.extend(title)
            
            # each word in the words list is reduced to its base form and saved in list 
            stemmed_words = [stemmer.stem(word) for word in words]
            # words converted to lower case and saved if they are not stop words and are alpha numeric
            filtered_stem_words = [word.lower() for word in stemmed_words if word not in stop_words and word.isalnum()]
            #frequency distribution of words created 
            freq_dist = FreqDist(filtered_stem_words)

            # Increase frequency of title words (helps in ranking algorithm later)
            for word in title:
                freq_dist[word.lower()] += 10
            
            # dictioray to store forward index entry of a single article
            # url id saved (serves as doc id as its unique)
            # empty dictionary for word (to store position and frequency)
            url_list.append(article['url'])
            forward_index = {"u": doc_id, "w": {}}
            doc_id+=1

            #loops thtough each word in the filtered stem words
            #if word is not in the dictionary, add its frequency and position
            #if word is already in the dictionary,just append its postion 
            #as a result of this loop, a dictoinary for one article is created
            for position, word in enumerate(filtered_stem_words):
                if word in forward_index["w"]:
                    forward_index["w"][word]["p"].append(position)
                else:
                    forward_index["w"][word] = {"f": freq_dist[word], "p": [position]}

            #append this forward_index dict to fowrard_index list
            forward_index_list.append(forward_index)
            #counts and prints articles process
            count += 1#counts docs
            print(f"\ndocs processed: {count}\n")

            # if 10000 aritcles processed, create a json file using the prfix and batch count
            # dump the list of dictionaries in that file
            if count % batch_size == 0:
                print(f"10k done\n")
                batch_count += 1
                output_file = os.path.join(output_directory, f"{output_prefix}_{batch_count}.json")
                with open(output_file, 'w') as json_file:
                    json.dump(forward_index_list, json_file)
                forward_index_list = [] #list reset for next batch

        # if some newsdata file didnt had 10k articles,
        # dump it's forward index in the same way as above   
        if forward_index_list:
            batch_count += 1
            output_file = os.path.join(output_directory, f"{output_prefix}_{batch_count}.json")
            with open(output_file, 'w') as json_file:
                json.dump(forward_index_list, json_file)


     # Write the updated data back to the JSON file
    dump_url_data(url_list,url_list_path)
        






    