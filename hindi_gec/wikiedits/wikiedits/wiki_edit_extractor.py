# -*- coding: utf-8 -*-

import logging

from more_itertools import pairwise

from wikiedits.edit_extractor import EditExtractor
from wikiedits.wiki.wiki_dump_parser import WikiDumpParser

log = logging.getLogger(__name__)


from wikiedits.wiki import VANDALISM_REGEXES
class WikiEditExtractor:

    def __init__(self, filename, **kwargs):
        self.dump = WikiDumpParser(filename)
        self.vandalism_regex = VANDALISM_REGEXES[kwargs['lang']]
        self.extractor = EditExtractor(**kwargs)

    def extract_edits(self, continue_index=0):
        n_edits = 0
        revs = enumerate(self.revision_pair())
        while True:
            try:
                (index, (old_text, new_text, meta)) = next(revs)
                if index % 5000 == 0:
                    log.info(f"Processed Revisions: {index}")
                if index < continue_index:
                    continue
                if new_text and old_text:
                    edits = self.extractor.extract_edits(old_text, new_text)
                    if edits:
                        n_edits += len(edits)
                        if n_edits % 500 == 0:
                            log.info(f"Processed Edits: {n_edits}")
                        yield edits, meta
            except StopIteration:
                log.info("Finished")
                break
            except (KeyboardInterrupt) as e:
                log.info(e)

    def revision_pair(self):
        for old_rev, new_rev in self.adjacent_revisions():
            meta = new_rev.copy()
            meta.pop('text')
            yield old_rev['text'], new_rev['text'], meta

    def adjacent_revisions(self):
        dmp_itr = self.dump.clean_rev_iter()
        for old_rev, new_rev in pairwise(dmp_itr):
            if new_rev.get('comment', '') is not None and self.vandalism_regex.search(
                    new_rev.get('comment', '')) is not None:
                continue
            yield old_rev, new_rev
