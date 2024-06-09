import random
import os
import numpy as np
from errors import word_error
import csv

MAX_SENTENCE_LENGTH = 26
MIN_SENTENCE_LENGTH = 4

def generate_number_of_errors():
    probability = random.randint(0, 100)
    if(probability > 80):
        return 3
    elif(probability > 50):
        return 2
    else:
        return 1

def generate_error(sentence: str):
    num_errors = generate_number_of_errors()

    indices = np.arange(len(list(word_error.keys())))
    np.random.shuffle(indices)

    for i in indices:
        word_to_replace = list(word_error.keys())[i]
        if(word_to_replace in sentence):
            sentence = sentence.replace(word_to_replace, word_error[word_to_replace])
            num_errors-=1
            if(num_errors == 0):
                break
    
    return sentence



def generate_data(file_content):
    csv_filename = 'output.csv'

    with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)

        sentences = file_content.split(u'۔')
        # Write data to the CSV file
        for sentence in sentences:
            # checking if sentence has length between range
            num_words = len(sentence.split(' '))
            if(num_words < MIN_SENTENCE_LENGTH or num_words > MAX_SENTENCE_LENGTH):
                continue

            cleaned_sentence = sentence.strip()+u"۔"
            if len(cleaned_sentence) > 2:
                incorrect_sentence = generate_error(cleaned_sentence)
                csv_writer.writerow([incorrect_sentence, cleaned_sentence])

#data_folder = "urdu_children_stories"