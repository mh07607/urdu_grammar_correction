import string


class IndicSentenceTokenizer:
    LANGUAGES = ('hindi',)
    NUMBERS = '०१२३४५६७८९' + string.digits
    INDIC = 'ऀँंःऄअआइईउऊऋऌऍऎएऐऑऒओऔकखगघङचछजझञटठडढणतथदधनऩपफबभमयरऱलळऴवशषसहऺऻ़ऽािीुूृॄॅॆेैॉॊोौ्ॎॏॐ॓॔ॕॖॗक़ख़ग़ज़ड़ढ़फ़य़ॠॡॢॣ' \
            + NUMBERS \
            + '\u200d\xa0\u200c'
    NON_INDIC = string.ascii_letters + "*&^@#:<>/+=-_}{[]%$~"
    SENTENCE_END = "۔!?;\n"
    ALLOWED_PUNCTUATION = ",()" + '"'
    ALLOWED_WHITESPACE = ' '
    INDIC = set(INDIC + SENTENCE_END + ALLOWED_WHITESPACE + ALLOWED_PUNCTUATION)
    REGULARIZE_TABLE = str.maketrans("|ا॥\t", "।।। ")
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

    def tokenize(self, text, min_tok=6, max_tok=27, max_non_indic=.2, ret_blank=False):
        text = text.translate(self.REGULARIZE_TABLE)

        non_indic_chars = ''.join(set(text) - self.INDIC)
        if non_indic_chars:
            text = text.translate(str.maketrans(non_indic_chars, '&' * len(non_indic_chars)))

        for sentence in self.line_to_sentence(text):
            for punct in self.SENTENCE_END + self.ALLOWED_PUNCTUATION:
                sentence = sentence.replace(punct, " " + punct + " ")
            non_indic_ratio = sentence.count('&') / (len(sentence) + 1)
            sentence = sentence.replace('&', ' ')
            sentence = " ".join(sentence.split())
            sentence = sentence.replace("( )", " ").split()
            len_sent = len(sentence)
            if min_tok <= len_sent < max_tok and non_indic_ratio < max_non_indic:
                sentence = " ".join(sentence).strip()
                if sentence[-1] not in self.SENTENCE_END:
                    sentence += " ।"
                yield sentence.translate(self.SENTENCE_END_TABLE)
            elif ret_blank:
                yield ""


if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Tokenize and Sentence Tokenize Indian text")
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
        "--max_non_indic",
        default=.2,
        type=float,
        nargs="?",
        help="max non indic percentage a valid sentence",
    )
    args = parser.parse_args()
    tokenizer = IndicSentenceTokenizer()
    input_file = open(args.input_file) if args.input_file else sys.stdin
    for inp_line in input_file:
        if inp_line.isspace():
            continue
        for sent in tokenizer.tokenize(inp_line,
                                       min_tok=args.min_tok,
                                       max_tok=args.max_tok,
                                       max_non_indic=args.max_non_indic
                                       ):
            print(sent)
