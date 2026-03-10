"""
Utility functions for the AI Content Generator
Includes word counting, file operations, and text processing
"""

import pandas as pd
import numpy as np
from datetime import datetime
import os


def count_words(text):
    """
    Counts the number of words in a given text string.
    
    Args:
        text (str): The input text to count words from
        
    Returns:
        int: Number of words in the text
    """
    if not text:
        return 0
    return len(text.split())


def count_characters(text):
    """
    Counts the number of characters in a text string.
    
    Args:
        text (str): The input text to count characters from
        
    Returns:
        int: Number of characters (excluding spaces)
    """
    if not text:
        return 0
    return len(text.replace(" ", ""))


def save_text_to_file(text, filename=None):
    """
    Saves generated text to a .txt file.
    
    Args:
        text (str): The content to save
        filename (str, optional): Name of the output file. 
                                 If None, generates a timestamp-based name
        
    Returns:
        str: Path to the saved file
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"article_{timestamp}.txt"
    
    # Create outputs directory if it doesn't exist
    os.makedirs("outputs", exist_ok=True)
    
    filepath = os.path.join("outputs", filename)
    
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)
        return filepath
    except IOError as e:
        print(f"Error saving file: {e}")
        return None


def calculate_reading_time(text, words_per_minute=200):
    """
    Calculates estimated reading time for the text.
    
    Args:
        text (str): The input text
        words_per_minute (int): Average reading speed (default: 200 WPM)
        
    Returns:
        dict: Contains minutes and seconds for reading time
    """
    word_count = count_words(text)
    total_seconds = (word_count / words_per_minute) * 60
    
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)
    
    return {
        "minutes": minutes,
        "seconds": seconds,
        "total_seconds": total_seconds
    }


def format_reading_time(reading_time_dict):
    """
    Formats reading time for display.
    
    Args:
        reading_time_dict (dict): Output from calculate_reading_time()
        
    Returns:
        str: Formatted reading time string
    """
    minutes = reading_time_dict["minutes"]
    seconds = reading_time_dict["seconds"]
    
    if minutes == 0:
        return f"{seconds} seconds"
    elif seconds == 0:
        return f"{minutes} minute{'s' if minutes > 1 else ''}"
    else:
        return f"{minutes} min {seconds} sec"


def summarize_content(text, num_sentences=3):
    """
    Simple extractive summarization (returns first N sentences).
    
    Args:
        text (str): The input text to summarize
        num_sentences (int): Number of sentences to include in summary
        
    Returns:
        str: Summarized text
    """
    sentences = text.split('.')
    summary = '.'.join(sentences[:num_sentences])
    return summary.strip() + '.' if summary else text


def validate_input(topic, keywords):
    """
    Validates user input before generating content.
    
    Args:
        topic (str): Blog topic
        keywords (str): Keywords string
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if not topic or not topic.strip():
        return False, "Topic cannot be empty"
    
    if not keywords or not keywords.strip():
        return False, "Keywords cannot be empty"
    
    if len(topic) < 3:
        return False, "Topic must be at least 3 characters long"
    
    if len(keywords) < 3:
        return False, "Keywords must be at least 3 characters long"
    
    return True, ""