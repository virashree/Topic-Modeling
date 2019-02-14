import gensim
import gensim.corpora as corpora


def iter_documents(top_file):
    """
    Generator: iterate over all relevant documents, yielding one
    document (=list of utf8 tokens) at a time.
    """
    documents = [line.split() for line in open(top_file).read().splitlines()]
    return documents


class TweetCorpus_byTweets:

    def __init__(self, top_dir):
        self.top_dir = top_dir
        self.docs = iter_documents(self.top_dir)
        self.id2word = gensim.corpora.Dictionary(self.docs)
        self.corpus = [self.id2word.doc2bow(text) for text in self.docs]

    def get_texts(self):
        for doc in iter(self.docs):
            yield doc

    def __len__(self):
        return len(self.docs)

    def __iter__(self):
        """
        Again, __iter__ is a generator => TxtSubdirsCorpus is a streamed iterable.
        """
        for doc in iter(self.get_texts()):
            # transform tokens (strings) into a sparse vector, one at a time
            yield self.id2word.doc2bow(doc)

    def store_corpus(self, corpus_filename):
        corpora.MmCorpus.serialize(corpus_filename, self.corpus)
        print("corpus saved")

    def store_dictionary(self, dictionary_filename):
        self.id2word.save(dictionary_filename)
        print("dictionary saved")

