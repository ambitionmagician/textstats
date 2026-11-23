#!/usr/bin/env python3
import argparse
import sys
import json
import re
from collections import Counter

STOPWORDS = {
    'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
    'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'shall', 'can', 'need', 'dare', 'ought',
    'used', 'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
    'she', 'we', 'they', 'what', 'which', 'who', 'whom', 'when', 'where',
    'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
    'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
    'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there', 'then',
    'once', 'if', 'because', 'until', 'while', 'about', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'between', 'under', 'again',
    'further', 'any', 'up', 'down', 'out', 'over', 'under'
}

def count_syllables(word):
    word = word.lower()
    vowels = 'aeiouy'
    syllable_count = 0
    prev_was_vowel = False
    
    for char in word:
        is_vowel = char in vowels
        if is_vowel and not prev_was_vowel:
            syllable_count += 1
        prev_was_vowel = is_vowel
    
    if word.endswith('e') and syllable_count > 1:
        syllable_count -= 1
    
    return max(1, syllable_count)

def analyze_text(text):
    chars = len(text)
    lines = text.count('\n') + 1 if text else 0
    paragraphs = len(re.split(r'\n\s*\n', text.strip())) if text.strip() else 0
    
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = len(sentences)
    
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    word_count = len(words)
    
    avg_words_per_sentence = word_count / sentence_count if sentence_count > 0 else 0.0
    avg_word_length = sum(len(w) for w in words) / word_count if word_count > 0 else 0.0
    
    total_syllables = sum(count_syllables(w) for w in words)
    reading_time = word_count / 200.0
    
    if sentence_count > 0 and word_count > 0:
        flesch = 206.835 - 1.015 * (word_count / sentence_count) - 84.6 * (total_syllables / word_count)
    else:
        flesch = 0.0
    
    word_freq = Counter()
    for word in words:
        lower_word = word.lower()
        if lower_word not in STOPWORDS:
            word_freq[lower_word] += 1
    
    return {
        'characters': chars,
        'words': word_count,
        'sentences': sentence_count,
        'paragraphs': paragraphs,
        'lines': lines,
        'avg_words_per_sentence': avg_words_per_sentence,
        'avg_word_length': avg_word_length,
        'reading_time': reading_time,
        'flesch_score': flesch,
        'word_freq': word_freq
    }

def main():
    parser = argparse.ArgumentParser(
        description='Analyze text statistics for a given file or stdin.',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        'file',
        help='Path to text file, or "-" to read from stdin'
    )
    parser.add_argument(
        '--top',
        type=int,
        metavar='N',
        help='Show top N most frequent words'
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results in JSON format'
    )
    
    args = parser.parse_args()
    
    try:
        if args.file == '-':
            text = sys.stdin.read()
        else:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.file}' not found", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied for file '{args.file}'", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)
    
    stats = analyze_text(text)
    
    if args.json:
        output = {
            'characters': stats['characters'],
            'words': stats['words'],
            'sentences': stats['sentences'],
            'paragraphs': stats['paragraphs'],
            'lines': stats['lines'],
            'avg_words_per_sentence': stats['avg_words_per_sentence'],
            'avg_word_length': stats['avg_word_length'],
            'reading_time': stats['reading_time'],
            'flesch_score': stats['flesch_score']
        }
        if args.top and stats['word_freq']:
            output['top_words'] = stats['word_freq'].most_common(args.top)
        print(json.dumps(output, indent=2))
    else:
        print(f"Characters: {stats['characters']}")
        print(f"Words: {stats['words']}")
        print(f"Sentences: {stats['sentences']}")
        print(f"Paragraphs: {stats['paragraphs']}")
        print(f"Lines: {stats['lines']}")
        print(f"Average words per sentence: {stats['avg_words_per_sentence']:.2f}")
        print(f"Average word length: {stats['avg_word_length']:.2f}")
        print(f"Estimated reading time: {stats['reading_time']:.2f} minutes")
        print(f"Flesch reading-ease score: {stats['flesch_score']:.2f}")
        
        if args.top and stats['word_freq']:
            print(f"\nTop {args.top} most frequent words:")
            for word, count in stats['word_freq'].most_common(args.top):
                print(f"  {word}: {count}")

if __name__ == '__main__':
    main()
