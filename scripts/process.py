"""

./process.py --operation sent --lang <iso code> --input <input path> --output <output_path>

"""

import os
import sys
import argparse
from pathlib import Path

from webcorpus.processors.arts import ArtsProcessor
from webcorpus.processors.sent import SentProcessor
from webcorpus.processors.topic import TopicProcessor
from webcorpus.processors.paragraph import ParagraphProcessor


parser = argparse.ArgumentParser()
parser.add_argument("--operation", type=str)
parser.add_argument("--lang", type=str)
parser.add_argument("--input", type=str)
parser.add_argument("--output", type=str)

args = parser.parse_args()

if args.operation == 'extract_arts':
    proc = ArtsProcessor(args.lang, args.input, args.output) 
    proc.run()
elif args.operation == 'extract_sents':
    proc = SentProcessor(args.lang, args.input, args.output) 
    proc.run()
elif args.operation == 'extract_genres':
    proc = TopicProcessor(args.lang, args.input, args.output) 
    proc.run()
elif args.operation == 'extract_paragraphs':
    proc = ParagraphProcessor(args.lang, args.input, args.output) 
    proc.run()
else:
    print('Invalid operation')
