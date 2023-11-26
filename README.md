# Py-Mood-Marker 📊

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/kmesiab/py-mood-marker/blob/main/LICENSE)
[![GitHub issues](https://img.shields.io/github/issues/kmesiab/py-mood-marker)](https://github.com/kmesiab/py-mood-marker/issues)
[![GitHub stars](https://img.shields.io/github/stars/kmesiab/py-mood-marker)](https://github.com/kmesiab/py-mood-marker/stargazers)
![Lint Status](https://github.com/kmesiab/py-mood-marker/actions/workflows/pylint.yml/badge.svg)

## Overview 🚀
Py-Mood-Marker is a Python application designed to analyze conversational data, focusing on extracting sentiments and emotions from text. It reads data from a JSON file, processes each entry to determine the sentiment, emotional content, and overall intensity of sentiments, and outputs enhanced data with these additional metadata.

## Key Features 🌟
- **Sentiment Analysis**: Utilizes VADER (Valence Aware Dictionary and sEntiment Reasoner) to determine the overall sentiment intensity of the text.
- **Emotion Analysis**: Identifies various emotions present in the text using NRCLex.
- **Contraction Expansion**: Expands contracted forms (e.g., "I'm" to "I am") in the text for better analysis.

## Installation 📦
Before running the application, ensure you have the following Python packages installed:
- contractions
- NRCLex
- vaderSentiment

You can install these packages using pip:

```ssh
pip install contractions nrclex vaderSentiment
```

## Usage 📝
1. Place your JSON data file in the same directory as the script. The data file should be named `data.json`.
2. Run the script by executing the following command

```shell
python mark_mood.py
```

The script will process the data, perform sentiment and emotion analysis using VADER and NRCLex, expand contractions, and print the enhanced data to the console.

## Data File

The input data file should be in the following format:

```json
{"role": "caller", "text": "in what way what do you mean ?"}
{"role": "rep", "text": "It just not telling you the truth..."}
{"role": "rep", "text": "actually told me that ..."}
{"role": "rep", "text": "probably started..."}
```

This format consists of JSON objects with two key-value pairs: "role" and "text." 
The "role" indicates the speaker's role, and the "text" contains the spoken text.

The output format, after processing, will look like this:

```json
{
  "role": "caller",
  "text": "is well because again it is still fresh...",
  "vader_emotion_scores": {
    "neg": 0.1,
    "neu": 0.8,
    "pos": 0.1,
    "compound": 0.2
  },
  "emotion_scores": {
    "joy": 3,
    "positive": 3
  }
}
```

In the output, the "role" and "text" remain the same, but additional metadata is added:

## Metadata Explanation 📋
- `vader_emotion_scores`: A dictionary containing sentiment scores (negative, neutral, positive, and compound) from VADER analysis.
- `emotion_scores`: A dictionary containing emotion scores based on NRCLex analysis.

## Contributing 🤝
Contributions are welcome! Feel free to open issues or submit pull requests.

## License 📄
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
