import json
import multiprocessing
import sys

import nltk
import contractions

from nrclex import NRCLex

from textblob import TextBlob
from textblob.en.sentiments import NaiveBayesAnalyzer

try:
    nltk.download('movie_reviews')
except Exception as e:
    print(f"An error occurred: {e}")
    print("Could not download the required NLTK data. Exiting the program.")
    sys.exit(1)

try:
    nltk.download('punkt')
except Exception as e:
    print(f"An error occurred: {e}")
    print("Could not download the required NLTK data. Exiting the program.")
    sys.exit(1)

csv_contents = open('data.json', 'r').read()
rows = csv_contents.split('\n')

annotated_rows = []
output_file_name = "mood-marked.json"


def get_sentiment(json_line):
    text_blob = TextBlob(json_line['text'], analyzer=NaiveBayesAnalyzer())
    json_line['classification'] = text_blob.sentiment.classification
    json_line['p_pos'] = text_blob.sentiment.p_pos * 100
    json_line['p_neg'] = text_blob.sentiment.p_neg * 100
    json_line['polarity'] = text_blob.polarity.real
    json_line['subjectivity'] = text_blob.subjectivity.real
    return json_line


def expand_contractions(json_line):
    json_line['text'] = contractions.fix(json_line['text'])
    return json_line


def get_emotion(json_line):
    emotion_analysis = NRCLex(json_line['text'])
    sorted_emotion_score_values = sorted(emotion_analysis.raw_emotion_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_emotions_dict = {k: v for k, v in sorted_emotion_score_values}
    json_line['emotion_scores'] = sorted_emotions_dict

    return json_line


def process_line(json_line):
    if json_line == '':
        return json_line

    """ parse this row into a json object """
    json_row = json.loads(json_line)

    if 'text' not in json_row and not json_row['text']:
        return json_line

    print(f"Analyzing sentence: {json_row['text']}")

    """ get the sentiment of this row """
    print("Analyzing sentiment...")
    json_row = get_sentiment(json_row)

    """ expand the contractions """
    print("Analyzing emotion...")
    json_row = get_emotion(json_row)

    """ expand the contractions """
    print("Expanding contractions...")
    json_row = expand_contractions(json_row)

    return json_row


def save_to_file(json_lines):
    with open(output_file_name, 'w') as outfile:
        json.dump(json_lines, outfile)


if __name__ == '__main__':

    """ Thread pool for the main app """
    pool = multiprocessing.Pool()
    results = pool.map(process_line, rows[1:])

    """ Main program loop """
    for result in results:
        annotated_rows.append(result)

    pool.close()
    pool.join()

    """ Save the results to a file"""
    save_to_file(annotated_rows)
