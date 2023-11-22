import json
import multiprocessing
import sys
import time

import contractions
from nrclex import NRCLex
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

min_word_count = 5
output_file_name = "mood-marked.json"


def expand_contractions(json_line):
    json_line['text'] = contractions.fix(json_line['text'])
    return json_line


def get_emotion(json_line):
    emotion_analysis = NRCLex(json_line['text'])
    sorted_emotion_score_values = sorted(emotion_analysis.raw_emotion_scores.items(), key=lambda x: x[1], reverse=True)
    sorted_emotions_dict = {k: v for k, v in sorted_emotion_score_values}
    json_line['emotion_scores'] = sorted_emotions_dict

    return json_line


def get_vader_emotion(json_line):
    analyzer = SentimentIntensityAnalyzer()
    vs = analyzer.polarity_scores(json_line['text'])
    json_line['vader_emotion_scores'] = vs
    return json_line


# Function to process each line of JSON
def process_line(json_line):
    if not json_line.strip():
        return None

    try:
        json_row = json.loads(json_line)
    except json.JSONDecodeError:
        print(f"Error decoding JSON: {json_line}")
        return None

    if 'text' not in json_row or not json_row['text']:
        return None

    word_count = len(json_row['text'].split())

    if word_count < min_word_count:
        return json_row

    json_row = get_emotion(json_row)
    json_row = get_vader_emotion(json_row)
    json_row = expand_contractions(json_row)

    return json_row


def save_to_file(json_lines):
    with open(output_file_name, 'w') as outfile:
        json.dump(json_lines, outfile)


if __name__ == '__main__':

    start_time = time.time()

    # Read the input file
    try:
        with open('data.json', 'r') as file:
            csv_contents = file.read()
    except FileNotFoundError:
        print("Error: The file 'data.json' was not found.")
        sys.exit(1)
    except IOError:
        print("Error: An I/O error occurred while reading 'data.json'.")
        sys.exit(1)

    # Split the file content into rows
    rows = csv_contents.split('\n')
    annotated_rows = []

    # Process lines using a thread pool
    with multiprocessing.Pool(maxtasksperchild=10) as pool:
        results = pool.map(process_line, rows[1:])

    # Collect results
    for result in results:
        if result is not None:
            annotated_rows.append(result)

    # Save the results to a file
    save_to_file(annotated_rows)

    print(f"Finished processing {len(annotated_rows)} rows in {time.time() - start_time} seconds.")
