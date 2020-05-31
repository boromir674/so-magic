import pandas as pd

# __all__ = []

def split_attributes(dataframe):
    """Return the categorical and numerical columns/attributes of the given dataframe"""
    _ = dataframe._get_numeric_data().columns.values
    return list(set(dataframe.columns) - set(_)), _

def missing_values(dataframe):
    return {k: v for k, v in dataframe.isnull().sum().to_dict().items() if v != 0}

# train_data.describe(include=['O'])

def drop_columns(dataframe, *columns):
    """Call this method to remove given columns for the given dataframe and get a new dataframe reference"""
    return dataframe.drop([*columns], axis=1)

def add_column(dataframe, name, values):
    """Call this method to add a new column with the given values and get a new dataframe reference"""
    return dataframe.assign(**{name: values})
########
def bin_column(column_ref, nb_bins):
    return pd.cut(column_ref, nb_bins)

def qbin_column(column_ref, nb_bins):
    return pd.qcut(column_ref, nb_bins)

def string_map(column_ref, strings, target_form):
    """Call this method to replace values found in 'strings' list with the target form, given a column (ie Series) reference and return the reference"""
    return column_ref.replace(strings, target_form)
####
def add_bin_for_continuous(dataframe, column, new_column, nb_bins):
    return add_column(dataframe, new_column, list(bin_column(dataframe[column], nb_bins)))

def add_reg(dataframe, name, regex, target):
    """Call this method to add a new column by applying a regex extractor to an existing column and get a new dataframe reference"""
    return add_column(dataframe, name, list(dataframe[target].str.extract(regex, expand=False)))

def map_replace_string(dataframe, column, norm):  #, strings_data, target_forms):
    """Call this method to replace strings with normalized form, given the input mapping
    Example input:
    norm = {
    'Rare': ['Lady', 'Countess','Capt', 'Col', 'Don', 'Dr', 'Major', 'Rev', 'Sir', 'Jonkheer', 'Dona'],
    'Miss': ['Mlle', 'Ms'],
    'Mrs': ['Mme']
    }
    """
    for k, v in norm.items():
        dataframe[column] = string_map(dataframe[column], v, k)
    # c = list(reversed([list(_) for _ in zip(*list(norm.items()))]))
    # for strings, target in zip(strings_data, target_forms):
    #     dataframe[column] = string_map(dataframe[column], strings, target)
    return dataframe


###############################
def df_map(a_callable, dataframes, *args, **kwargs):
    return [a_callable(x, *args, **kwargs) for x in dataframes]
#########################

# # DROP 'Ticket' and 'Cabin' columns
# train_data, test_data = df_map(drop_columns, [train_data, test_data], 'Ticket', 'Cabin')

def complete_categorical_with_most_freq(dataframe, column):
    return dataframe.assign(**{column: dataframe[column].fillna(dataframe[column].dropna().mode()[0])})

def complete_numerical_with_median(dataframe, column):
    return dataframe.assign(**{column: dataframe[column].fillna(dataframe[column].dropna().median())})

from itertools import product
from functools import reduce

class MedianFiller:
    def __call__(self, dataframe, column, columns):
        """
        Call this method to fill missing values in a dataframe's column according to the medians computed on correlated columns\n
        :param str dataframe:
        :param str column: column with missing values
        :param list columns: correlated columns
        :return: a dataframe reference with the column completed
        """
        for vector in product(*[list(dataframe[c].unique()) for c in columns]):
            self._set_value(dataframe, column, self._condition(dataframe, columns, vector))
        return dataframe.assign(**{column: dataframe[column].astype(int)})

    def _set_value(self, dataframe, column, condition):
        dataframe.loc[(dataframe[column].isnull()) & condition, column] = self._convert(
            dataframe[condition][column].dropna().median())

    def _condition(self, dataframe, columns, values_vector):
        return reduce(lambda i, j: i & j, [dataframe[c] == values_vector[e] for e, c in enumerate(columns)])

    def _convert(self, value):
        return value



def create_column(dataframe, name, a_callable):
    return dataframe.assign(**{name: a_callable(dataframe)})

# # CREATE 5 BINS for 'Age' column (discreetize) and add a column in 'train' data
# train_data = train_data.assign(**{'AgeBand': pd.cut(train_data.Age.astype(int), 5)})


def add_qbin(dataframe, target, nb_bins, destination):
    """Call this function to create a column (with 'destination' name) of quantisized bins of the continuous variable given in the target column"""
    return dataframe.assign(**{destination: pd.qcut(dataframe[target], nb_bins)})


def binned_indices(values, left_boundaries):
    """Call this function to get an array of indices the given values belong based on the input boundaries.\n
        If values in `x` are beyond the bounds of `left_boundaries`, 0 or ``len(left_boundaries)`` is returned as appropriate."""
    return np.digitize(values, left_boundaries)


def _map(intervals_list):
    """Call this function to get a dictionary mapping Interval objects to numerical codes (0, 1, ..).
        Assumes that the input Intervals list is sorted"""
    return {(interval_obj): index for index, interval_obj in enumerate(intervals_list)}


## operations for dfs with constructed bins/bands
def encode_bands(dataframe, target_column, intervals_list, destination_column):
    """Call this function to get a dictionary mapping Interval objects to numerical codes (0, 1, ..).
        Assumes that the input Intervals list is sorted"""
    return dataframe.assign(**{destination_column: dataframe[target_column].map(_map(intervals_list)).astype(int)})


def encode_bands_many(dataframe, targets, intervals_lists, destinations):
    """"""
    return dataframe.assign(**{dest_c: dataframe[target_c].map(_map(intervals_list)).astype(int)
                               for target_c, intervals_list, dest_c in zip(targets, intervals_lists, destinations)})


def encode_continuous(dataframe, target_column, intervals_list, destination_column):
    return dataframe.assign(
        **{destination_column: binned_indices(dataframe[target_column], iter(x.left for x in intervals_list)) - 1})


def encode_continuous_many(dataframe, targets, intervals_lists, destinations):
    return dataframe.assign(**{dest_c: binned_indices(dataframe[target_c], [x.left for x in intervals_list]) - 1
                               for target_c, intervals_list, dest_c in zip(targets, intervals_lists, destinations)})


def _op_gen(dataframe, columns, band_str='Band', post_str='_Code'):
#     interval_lists = [sorted(dataframe[c+band_str].unique()) for c in columns]
#     coded = ['{}{}'.format(c, post_str) for c in columns]
    _ = [list(_) for _ in zip(*list([(sorted(dataframe[c+band_str].unique()), '{}{}'.format(c, post_str)) for c in columns]))]
    yield lambda x: encode_bands_many(x, [c+band_str for c in columns], _[0], _[1])
    while 1:
        yield lambda x: encode_continuous_many(x, columns, _[0], _[1])


#### CONSTANTS #####
POST_STR = '_Code'  # postfix string for encoded variables
BAND_STR = 'Band'

#### SETTINGS ###
# PICK columns with categorical variables to encode with sklearn LabelEncoder
TO_ENCODE_WITH_SKLEARN = ['Embarked', 'Sex', 'Title']

TO_ENCODE_WITH_INTERVALS = ['Age', 'Fare']



def label_encode(dataframe, columns, encode_callback, code_str='_Code'):
    return dataframe.assign(**{c+code_str: encode_callback(dataframe[c]) for c in columns})

#                                [train_data, test_data],
#                                ['Embarked', 'Sex', 'Title'],
#                                LabelEncoder().fit_transform)  # encodes categorical objects into indices starting from 0


# ENCODE 'Age' and 'Fare' by creating the 'Age_code' and 'Fare_Code' coluns in 'train_data' and 'test_data'
# train_data, test_data = encode_bands([train_data, test_data], TO_ENCODE_WITH_INTERVALS, bin_str=BAND_STR, post=POST_STR)
#
# op_gen = _op_gen(train_data, ['Age', 'Fare'], band_str='Band', post_str='_Code')
# train_data, test_data = [next(op_gen)(df) for df in [train_data, test_data]]




#### SELECTION
#
# #define y variable aka target/outcome
# Target = ['Survived']
#
# # FEATURE SLECTION
# # define variables (original and encoded)
# feature_titles = ['Sex','Pclass', 'Embarked', 'Title','SibSp', 'Parch', 'Age', 'Fare', 'FamilySize', 'IsAlone'] #pretty name/values for charts
# feature_names = ['Sex_Code','Pclass', 'Embarked_Code', 'Title_Code','SibSp', 'Parch', 'Age', 'Fare'] #coded for algorithm calculation
# # data1_xy =  Target + data1_x
# # print('Original X Y: ', data1_xy, '\n')
#
#
# #define x variables for original w/bin variables to remove continuous variables
# data1_x_bin = ['Sex_Code','Pclass', 'Embarked_Code', 'Title_Code', 'FamilySize', 'Age_Code', 'Fare_Code']
# # data1_xy_bin = Target + data1_x_bin
# # print('Bin X Y: ', data1_xy_bin, '\n')
#
#
# #define x and y variables for dummy variables original
# data1_dummy = pd.get_dummies(train_data[feature_titles])
# data1_x_dummy = data1_dummy.columns.tolist()
# # data1_xy_dummy = Target + data1_x_dummy
# # print('Dummy X Y: ', data1_xy_dummy, '\n')
#
#
# # SELECT variables
# numerical_feats = ['Pclass', 'Fare_Code', 'Age_Code', 'FamilySize']  # ordering makes sence: eg: class_1 < class_2,
# binary_feats = ['Sex_Code', 'IsAlone']
# categorical_feats = ['Embarked']
#
# assert all(all(x in train_dataframe.columns for x in y) for y in [numerical_feats, binary_feats, categorical_feats])
#
# # convert eg column "color" that takes {'white', 'black'} as values to
# # 2 columns: 'color_white' and 'color_black' (that take 0 or 1)
# pd.get_dummies(train_data[categorical_feats]).head()
#
#
# X_train = pd.concat([train_data[numerical_feats + binary_feats], pd.get_dummies(train_data[categorical_feats])], axis=1)
# X_test = pd.concat([test_data[numerical_feats + binary_feats], pd.get_dummies(test_data[categorical_feats])], axis=1)
# X_train.head()
#
#
# X_train = pd.concat([train_data[numerical_feats + binary_feats], pd.get_dummies(train_data[categorical_feats])], axis=1)
# X_test = pd.concat([test_data[numerical_feats + binary_feats], pd.get_dummies(test_data[categorical_feats])], axis=1)
# X_train.head()


def get_df_from_json(cls, json_path):
    return pd.read_json(path_or_buf=json_path)

def from_csv(file_path):
    return pd.read_csv(file_path)
