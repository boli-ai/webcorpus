"""
Copyright © Sumanth Doddapaneni 2022, all rights reserved.

Create a paragraph file from an article corpus

"""
from tqdm import tqdm
from ..corpus import NewsCorpus, FileCorpus
from ..language import code2script, in_script


class ParagraphProcessor:

    def __init__(self, lang, input_path, output_path):
        self.lang = lang
        self.script = code2script(lang)
        self.input_corpus = NewsCorpus(lang, input_path)
        self.output_corpus = FileCorpus(lang, output_path)

    def check_paragraph(self, paragraph):
        """
        * Check paragraphs that contain one or more words not in the
          desired language
        * Check short paragraphs
        """

        # check threshold again
        if len(paragraph) < 10:
            return False
        cval = map(lambda c: in_script(c, self.script) or c.isdigit(), paragraph)
        if sum(cval) >= 0.9 * len(paragraph):
            return True
        return False

    def run(self):
        """
        Create a paragraph file from an article corpus
        """
        for article in tqdm(self.input_corpus.all_instances()):
            content = article['body']
            content = content.replace(u'\xa0', u' ')
            content = content.replace('\\n', '\n')

            paragraphs = []

            for para in content.split('\n'):
                if self.check_paragraph(para):
                    paragraphs.append(para)

            for para in paragraphs:
                self.output_corpus.add_instance(para)
        self.output_corpus.flush()