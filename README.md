# NELA GT-22 Search Engine

## Description
This project is a search engine built on the NELA GT-22 dataset. It parses articles to create forward and inverted indices after preprocessing, such as removing stop words. The data is then organized into barrels for efficient retrieval, achieving search times of around 150 ms. The project supports dynamic article addition and searching functionalities, and is implemented using Django and NLTK.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Features](#features)


## Installation

### Prerequisites
- Python 3.8 or higher
- Django 3.x or higher
- NLTK

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/nela-gt22-search-engine.git
   cd nela-gt22-search-engine
2. Downlaod the dataset: https://arxiv.org/abs/2203.05659
3. Install Django and NLTK
4. Give path to dataset
5. Run the server: python manage.py runserver

## Usage

Enter queries in the search bar and retreive the results

## Features
1. **Efficient Retrieval:** Achieve search results in about 150 ms through optimized indexing and data storage mechanisms.
2. **Dynamic Article Addition:** Easily add new articles to the search engine without downtime, using the Django admin interface or API endpoints.
3. **Comprehensive Preprocessing:** Articles undergo preprocessing including tokenization, stop word removal, and other cleaning steps using NLTK to enhance search accuracy.
4. **Forward and Inverted Indexing:** Utilizes both forward and inverted indices to ensure quick and relevant search results.
5. **Barrel Storage:** Organizes indexed terms into barrels for efficient search operations, balancing speed and storage.
6. **Django Framework:** Built using Django, ensuring a robust and scalable web application structure.
7. **NLTK Integration:** Leverages the power of NLTK for natural language processing tasks such as tokenization and stop word removal.
8. **User-Friendly Interface:** Provides a clean and intuitive user interface for easy searching and article management.
9. **Scalability:** Designed to handle large datasets and support future expansions and enhancements.
