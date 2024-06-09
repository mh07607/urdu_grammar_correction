import argparse
import warnings
from collections import Counter
from contextlib import ExitStack
from typing import IO, Tuple, Dict
from more_itertools import flatten
#from stanfordnlp.pipeline.doc import Document
import os

#import sys
#sys.path.append("/home/mh07607/Documents/hindi_grammar_correction/Colab Notebooks/errant/errant")

from errant.errant.annotator import Annotator

warnings.simplefilter("ignore", UserWarning)


def main():
    # Parse command line args
    args = parse_args()
    print("Loading resources...")
    # Load Errantsrc/ATen/native/TensorAdvancedIndexing.cpp:573:
    # UserWarning: masked_fill_ received a mask with dtype torch.uint8, this behavior is
    # now deprecated,please use a mask with dtype torch.bool instead.

    annotator = Annotator()

    # Counter Storing all the error types for a histogram
    error_count = Counter()

    print("Processing parallel files...")
    # Process an arbitrary number of files line by line simultaneously. Python 3.3+
    # See https://tinyurl.com/y4cj4gth
    with ExitStack() as stack:
        files = [stack.enter_context(open(i)) for i in [args.orig] + args.cor]
        out_files = {}

        # For each group of lines from the files process them together and output result to m2
        for lines in zip(*files):
            docs = tuple(annotator.parse(line, args.tok) for line in lines)
            process_sentences(docs[0], docs[1:], error_count, out_files, args, annotator, )
        for out_file in out_files:
            list(map(lambda file:file.close(),out_files[out_file]))

    # Save error counts to file
    with open('error_file', 'w') as error_file:
        for key in error_count:
            error_file.write(str(key) + '\t' + str(error_count[key]))


# Process each group of sentences, and write to the m2 file
def process_sentences(orig, cors, error_count: Counter, out_m2: Dict[str, IO],
                      args: argparse.Namespace,
                      annotator: Annotator):
    # Write orig to the output m2 file
    temp1 = []
    for sent in orig.sentences:
        for word in sent.words:
            temp1.append(word)

    # Loop through the corrected texts
    for cor_id, cor in enumerate(cors):
        # Align the texts and extract and classify the edits
        edits = annotator.annotate(orig, cor, args.lev, args.merge)
        for edit in edits:
            error_count[edit.type] += 1
            file_name = edit.type.replace(":", "_")
            if file_name not in out_m2:
                os.makedirs(os.path.join("test_out",file_name),exist_ok=True)
                file_path=os.path.join(os.path.join("test_out",file_name),file_name)
                out_m2[file_name] = open(file_path+ ".m2", 'w'),open(file_path+ ".src", 'w'),open(file_path+ ".trg", 'w')
            outfile = out_m2[file_name]
            outfile[0].write(" ".join(["S"] + [token.text for token in temp1]) + "\n")
            outfile[0].write(edit.to_m2(cor_id) + "\n")
            outfile[0].write("\n")
            src,trg=edit.to_srctrg()
            outfile[1].write(src+'\n')
            outfile[2].write(trg+'\n')

# Parse command line args
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Align parallel text files and extract and classify the edits.\n",
        formatter_class=argparse.RawTextHelpFormatter,
        usage="%(prog)s [-h] [options] -orig ORIG -cor COR [COR ...] -out OUT")
    parser.add_argument(
        "-orig",
        help="The path to the original text file.",
        required=True)
    parser.add_argument(
        "-cor",
        help="The paths to >= 1 corrected text files.",
        nargs="+",
        default=[],
        required=True)
    parser.add_argument(
        "-tok",
        help="Word tokenise the text using spacy (default: False).",
        action="store_true")
    parser.add_argument(
        "-lev",
        help="Align using standard Levenshtein (default: False).",
        action="store_true")

    parser.add_argument(
        "-merge",
        help="Choose a merging strategy for automatic alignment.\n"
             "rules: Use a rule-based merging strategy (default)\n"
             "all-split: Merge nothing: MSSDI -> M, S, S, D, I\n"
             "all-merge: Merge adjacent non-matches: MSSDI -> M, SSDI\n"
             "all-equal: Merge adjacent same-type non-matches: MSSDI -> M, SS, D, I",
        choices=["rules", "all-split", "all-merge", "all-equal"],
        default="rules")
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    main()
