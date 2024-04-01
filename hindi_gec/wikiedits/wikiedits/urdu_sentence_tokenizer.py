import string

class UrduSentenceTokenizer:
    LANGUAGES = ('urdu',)
    NUMBERS = '٠١٢٣٤٥٦٧٨٩' + string.digits
    URDU_BASE = 'آ ا ب پ ت ٹ ث ج چ ح خ د ڈ ذ ر ڑ ز ژ س ش ص ض ط ظ ع غ ف ق ک گ ل م ن ں و ہ ی ے ئ ؤ ۃ ھ'\
           + NUMBERS \
           + '\u200d\xa0\u200c'
    
    URDU = URDU_BASE
    NON_URDU = string.ascii_letters + "*&^@#:<>/+=-_}{[]%$~"
    SENTENCE_END = "۔؟؛\n"
    ALLOWED_PUNCTUATION = ",()" + '"'
    ALLOWED_WHITESPACE = ' '
    URDU = set(URDU + SENTENCE_END + ALLOWED_WHITESPACE + ALLOWED_PUNCTUATION)
    #REGULARIZE_TABLE = str.maketrans("|ا\t", "۔  ")
    SENTENCE_END_TABLE = str.maketrans(SENTENCE_END, '.' * len(SENTENCE_END))

    def line_to_sentence(self, line):
        pos = 0
        old_pos = 0
        while pos < len(line):
            new_pos = min(filter(lambda x: x != -1, (line.find(end, pos) for end in self.SENTENCE_END)),
                          default=len(line) - 1) + 1
            yield line[old_pos:new_pos]
            pos = new_pos
            old_pos = new_pos

    def tokenize(self, text, min_tok=6, max_tok=27, max_non_urdu=.2, ret_blank=False):
        #text = text.translate(self.REGULARIZE_TABLE)

        non_urdu_chars = ''.join(set(text) - self.URDU)
        if non_urdu_chars:
            text = text.translate(str.maketrans(non_urdu_chars, '&' * len(non_urdu_chars)))

        for sentence in self.line_to_sentence(text):
            for punct in self.SENTENCE_END + self.ALLOWED_PUNCTUATION:
                sentence = sentence.replace(punct, " " + punct + " ")
            non_urdu_ratio = sentence.count('&') / (len(sentence) + 1)
            sentence = sentence.replace('&', ' ')
            sentence = " ".join(sentence.split())
            sentence = sentence.replace("( )", " ").split()
            len_sent = len(sentence)
            if min_tok <= len_sent < max_tok and non_urdu_ratio < max_non_urdu:
                sentence = " ".join(sentence).strip()
                if sentence[-1] not in self.SENTENCE_END:
                    sentence += " ۔"
                yield sentence.translate(self.SENTENCE_END_TABLE)
            elif ret_blank:
                yield ""

if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Tokenize and Sentence Tokenize Urdu text")
    parser.add_argument("input_file", default=None, nargs="?", help="input filename")
    parser.add_argument(
        "--min_tok",
        default=6,
        type=int,
        nargs="?",
        help="minimum tokens (words) for a valid sentence",
    )
    parser.add_argument(
        "--max_tok",
        default=27,
        type=int,
        nargs="?",
        help="max tokens (words) for a valid sentence",
    )
    parser.add_argument(
        "--max_non_urdu",
        default=.2,
        type=float,
        nargs="?",
        help="max non Urdu percentage for a valid sentence",
    )
    args = parser.parse_args()
    tokenizer = UrduSentenceTokenizer()
    input_file = open(args.input_file) if args.input_file else sys.stdin
    for inp_line in input_file:
        if inp_line.isspace():
            continue
        for sent in tokenizer.tokenize(inp_line,
                                       min_tok=args.min_tok,
                                       max_tok=args.max_tok,
                                       max_non_urdu=args.max_non_urdu
                                       ):
            print(sent)
