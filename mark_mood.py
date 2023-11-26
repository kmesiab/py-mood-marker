"""Module for Py-Mood-Marker application.

This module contains functions and logic to analyze sentiments and emotions from text data.
It includes capabilities to read data, process and analyze it for sentiment and emotional content,
and output the results with enhanced metadata.
"""
import json
import multiprocessing
import sys
import time

import contractions
from nrclex import NRCLex
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

MIN_WORD_COUNT = 5
OUTPUT_FILE_NAME = "mood-marked.json"
INPUT_FILE_NAME = "data.json"


def expand_contractions(json_line):
    """Expand contractions in the text of a JSON line.

    Args:
        json_line (dict): A JSON object containing the text to be processed.

    Returns:
        dict: The JSON object with expanded contractions in the text.
    """
    json_line['text'] = contractions.fix(json_line['text'])
    return json_line


def get_emotion(json_line):
    """Analyze and add emotion scores to a JSON line.

    Args:
        json_line (dict): A JSON object containing the text to be analyzed.

    Returns:
        dict: The JSON object with added emotion scores.
    """
    emotion_analysis = NRCLex(json_line['text'])
    sorted_emotion_score_values = sorted(
        emotion_analysis.raw_emotion_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    # Simplified way to convert sorted_emotion_score_values to a dictionary
    sorted_emotions_dict = dict(sorted_emotion_score_values)
    json_line['emotion_scores'] = sorted_emotions_dict

    return json_line


def get_vader_emotion(json_line):
    """Analyze text sentiment using VADER and add the scores to a JSON line.

    Args:
        json_line (dict): A JSON object containing the text to be analyzed.

    Returns:
        dict: The JSON object with VADER sentiment scores.
    """
    analyzer = SentimentIntensityAnalyzer()
    varder_scores = analyzer.polarity_scores(json_line['text'])
    json_line['vader_emotion_scores'] = varder_scores
    return json_line


def process_line(json_line):
    """Process a line of JSON to analyze sentiment and emotions.

    Args:
        json_line (str): A string representation of a JSON object.

    Returns:
        dict or None: The processed JSON object, or None if processing fails.
    """
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

    if word_count < MIN_WORD_COUNT:
        return json_row

    json_row = get_emotion(json_row)
    json_row = get_vader_emotion(json_row)
    json_row = expand_contractions(json_row)

    return json_row


def save_to_file(json_lines):
    """Save the processed JSON lines to a file.

    Args:
        json_lines (list): A list of processed JSON objects.
    """
    with open(OUTPUT_FILE_NAME, 'w', encoding='UTF-8') as outfile:
        json.dump(json_lines, outfile)


if __name__ == '__main__':

    start_time = time.time()

    # Read the input file
    try:
        with open(INPUT_FILE_NAME, 'r', encoding='UTF-8') as file:
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
