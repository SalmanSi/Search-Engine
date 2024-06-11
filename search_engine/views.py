from django.shortcuts import render
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect
from django.db import connection
from django.utils import timezone
from django.http import HttpResponse
import json
import os
# Create your views here.

from .ranking import clean_query, calculate_tf_idf, search_inverted_indices
from .createForwardIndex import Create_Forward_Index
from .filing import get_url_id,dump_url_data
from .CreateInvertedIndex import update_inverted_indices
#from .query import search_inverted_indices
inverted_index_directory = r'C:\Users\admin\Desktop\3rd Semester\DSA\project\indices\inverted_index'
#path of file to store url list
url_list_path = r"C:\Users\admin\Desktop\3rd Semester\DSA\project\indices\url_list.json"





#with ranking

def search_view(request):
    if request.method == "POST":
        # Call relevant functions
        query = request.POST["query"]
        cleaned_query = clean_query(query)
        common_urls = search_inverted_indices(cleaned_query, inverted_index_directory)
        result = calculate_tf_idf(inverted_index_directory, cleaned_query)
        print(cleaned_query)
        # Read the contents of the JSON file into a Python list
        try:
            with open(url_list_path, "r") as json_file:
                url_list_data = json.load(json_file)
        except FileNotFoundError:
            # Handle the case when the file doesn't exist
            url_list_data = []

        # Extract URLs with their TF-IDF scores in sorted order
        urls_with_scores = []
        s = 0
        for url_id, score in result:
            if s == 50:
                break
            if url_id in common_urls and url_id < len(url_list_data):
                url = url_list_data[url_id]  # Get the URL from the url_list_data
                urls_with_scores.append({'url': url, 'score': score})
                s += 1
        print (f"S==={s}")
        # Pass the URLs with scores as context to the template
        context = {'urls_with_scores': urls_with_scores}

        return render(request, "search_engine/home.html", context)

    return render(request, "search_engine/home.html")

#without ranking:
# def search_view(request):
#     if request.method == "POST":
#         # Call relevant functions
#         query = request.POST["query"]
#         cleaned_query = clean_query(query)
#         common_result_urls, uncommon_result_urls = search_inverted_indices(cleaned_query, inverted_index_directory)

#         # Read the contents of the JSON file into a Python list
#         try:
#             with open(url_list_path, "r") as json_file:
#                 url_list_data = json.load(json_file)
#         except FileNotFoundError:
#             # Handle the case when the file doesn't exist
#             url_list_data = []

#         s = 0
#         all_urls = []
#         for doc in common_result_urls:
#             if s == 50:  # Adjust the limit if needed
#                 break
#             else:
#                 all_urls.append({'url': url_list_data[doc], 'score': 0})  # Update with actual score
#                 s += 1
#         print(all_urls)
#         return render(request, "search_engine/home.html", {'urls_with_scores': all_urls})

#     return render(request, "search_engine/home.html")

def add_content_view(request):
    if request.method == 'POST':
        input_file = request.FILES.get('jsonFile')
        # create forward index
        if input_file:
            # Get file details
            file_name = input_file.name
            file_content_type = input_file.content_type
            file_size = input_file.size

            # Specify the directory where you want to save the file
            save_directory = r'C:\Users\admin\Desktop\dynamic_addition'

            # Create the directory if it doesn't exist
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            # Construct the file path
            file_path = os.path.join(save_directory, file_name)

            # Save the file to the specified directory
            with open(file_path, 'wb') as destination:
                for chunk in input_file.chunks():
                    destination.write(chunk)

            # path to directory in which forward_index is saved
            forward_index_directory=r'C:\Users\admin\Desktop\dynamic_addition\forward_index'
            # output prefix
            output_prefix='forward_index_combined_1.0'

            #path to input directory containing newsdata
            input_file_path = file_path
            Create_Forward_Index(input_file_path,forward_index_directory)
            
            
            #create inverted index

            # input and output paths specified 
            inverted_index_directory = r'C:\Users\admin\Desktop\3rd Semester\DSA\project\indices\inverted_index'

            # function to create/update inverted index called
            update_inverted_indices(forward_index_directory, inverted_index_directory)

            print("data added")
            return render(request, "search_engine/home.html")


    return render(request,"search_engine/add_content.html")