from .utils import generate_words, gen_values


class StrainLexicon(object):

    def __init__(self):
        self.id2word = {}
        self.word2id = {}
        self._next_id = 0

    def munch(self, text, normalizer='lemmatize'):
        for w in generate_words(text, normalize=normalizer):
            self._add_word(w)

    def _add_word(self, token):
        if token not in self.id2word:
            self.id2word[self._next_id] = token
            self.word2id[token] = self._next_id
            self._next_id += 1

    def __len__(self):
        return self._next_id


class FeatureComputer:

    def __init__(self, strain_dataset):
        """
        :type strain_dataset: strain_dataset.StrainDataset
        """
        self._dt = strain_dataset
        self.feat_defs = [get_encoding_type(feat_name) + '#' + feat_name for feat_name in self._dt.generate_variables()]

        self.variable2extractor = {'type': type_f,
                                   'name': name_f,
                                   'effects': effects_f,
                                   'medical': medical_f,
                                   'negatives': negatives_f,
                                   'flavors': flavors_f,
                                   'difficulty': difficulty_f,
                                   'height': height_f,
                                   'yield': yield_f,
                                   'flowering': flowering_f,
                                   'stretch': stretch_f,
                                   }

    def encode(self, encoder_type, strain, feat_type):
        """Call this method to """
        extractor = self.variable2extractor[feat_type]
        if encoder_type == 'binary-1':
            v = [0.0] * (self._dt.get_nb_values(feat_type) - 1)
            for value in gen_values(extractor(strain)):
                if self._dt.field2id[feat_type][value] > 0:
                    v[get_id_reporter(self._dt, feat_type)(value) - 1] = 1.0
        else:
            v = [0.0] * self._dt.get_nb_values(feat_type)
            if encoder_type == 'binary-on-off':
                for value in gen_values(extractor(strain)):
                    v[get_id_reporter(self._dt, feat_type)(value)] = 1.0
            elif encoder_type == 'set-real-value':
                for key, value in gen_values(extractor(strain)):
                    v[get_id_reporter(self._dt, feat_type)(key)] = value / float(100)
        return v

    def get_basic_feature_representation(self, strain):
        """Call this method to get encoded feature vectors for each datapoint.\n
        :param str strain:
        """
        rep = []
        for feat_def in self.feat_defs:
            enc_type, feat_type = feat_def.split('#')
            re = self.encode(enc_type, strain, feat_type)
            rep += re
        # assert len(rep) == sum(len(self._dt.value_sets[var]) for var in
        #                      self._dt.generate_variables()), "len of binary vector: {}, sum of value_sets sizes: {}".format(
        #     len(rep), sum(len(self._dt.value_sets[var]) for var in self._dt.generate_variables()))
        return rep


# define encoding for variables
# encoding type -> variable features
enctype2features = {
    'binary-1': [],
    'binary-on-off': [
        'type',
        'flavors',
        'difficulty',
        'yield',
        'flowering',
        'height',
        'stretch',
        # 'name'
    ],
    'set-real-value': [
        'effects',
        'medical',
        'negatives'
    ],
}
def get_encoding_type(feat_name):
    for enc_type, list_of_feats in enctype2features.items():
        if feat_name in list_of_feats:
            return enc_type


def get_id_reporter(weedata, variable):
    return lambda x: weedata.field2id[variable][x]


def type_f(item):
    return str(item['type'])


def name_f(item):
    return item['name']


def effects_f(item):
    return item['effects']


def medical_f(item):
    return item['medical']


def negatives_f(item):
    return item['negatives']


def flavors_f(item):
    return item['flavors']


def parents_f(item):
    return item['parents']


def difficulty_f(item):
    return str(item['grow_info']['difficulty'])


def height_f(item):
    return str(item['grow_info']['height'])


def yield_f(item):
    return str(item['grow_info']['yield'])


def flowering_f(item):
    return str(item['grow_info']['flowering'])


def stretch_f(item):
    return str(item['grow_info']['stretch'])
