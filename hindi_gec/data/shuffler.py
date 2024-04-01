import random

def shuffle_src_trg(src, trg):
    src_sentences = []
    trg_sentences = []

    with open(src, 'r', encoding='utf-8') as src_file:
        src_sentences = src_file.readlines()

    with open(trg, 'r', encoding='utf-8') as trg_file:
        trg_sentences = trg_file.readlines()

    combined_data = list(zip(src_sentences, trg_sentences))
    random.shuffle(combined_data)

    shuffled_src, shuffled_trg = zip(*combined_data)

    with open(src+'.shuffled', 'w',encoding='utf-8', newline='') as src_shuffled_file:
        src_shuffled_file.writelines(shuffled_src)

    with open(trg+'.shuffled', 'w',encoding='utf-8', newline='') as trg_shuffled_file:
        trg_shuffled_file.writelines(shuffled_trg)


shuffle_src_trg('urwiki.extracted.clean.src', 'urwiki.extracted.clean.trg')