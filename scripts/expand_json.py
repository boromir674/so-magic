import json
import sys
import pandas as pd


# parse something like this (This should be one line. Here it is multi-line for showcasing purposes)
"""
{
 "name": "Mango Kush",
 "_id": "mango-kush", 
 "type": "hybrid",
 "effects": {"Relaxed": 84.9417839884954, "Uplifted": 69.0166321724966, "Euphoric": 73.7478616265042, "Giggly": 61.4963502820495, "Happy": 100.0},
 "medical": {"Lack of Appetite": 39.5724524662832, "Pain": 42.3843948614922, "Stress": 100.0, "Insomnia": 42.4187271741305, "Depression": 69.2028656456916},
 "negatives": {"Dizzy": 22.1503121602918, "Paranoid": 14.1867595722226, "Dry Eyes": 73.060705424837, "Headache": 16.3337649917133, "Dry Mouth": 100.0},
 "flavors": ["Mango", "Sweet", "Tropical"],
 "grow_info": {
    "difficulty": "Easy",
    "height": "< .75 m", 
    "yield": "251-500",
    "flowering": "7-9 wks",
    "stretch": "100-200%"},
 "parents": ["mango", "hindu-kush"],
 "description": "The Mango Kush marijuana strain tastes similar tothe actual mango fruit, with a distinct kush flavorand
                 hints of pine on the exhale. Itsbuds are covered with orange pistils and are described as very dense.
                 The plant has an average growth height of 4-5 feet. Flowering is 9-11 weeks and is a favorite with both
                  indoor and outdoor growers. The buds have thick shiny trichomes which are evident when the bud is broken
                   apart. The smell and taste are the same and described as mango and banana. THC content has been 
                   measured up to 16% and CBD at 0.3%."
 "image_urls": [],
 "image_paths": [], 
}
"""
# into this
"""
{
 "name": "Mango Kush",
 "_id": "mango-kush", 
 "type": "hybrid",
 
 "Relaxed": 84.9417839884954,
 "Uplifted": 69.0166321724966, 
 "Euphoric": 73.7478616265042,
 "Giggly": 61.4963502820495, 
 "Happy": 100.0,
 
 "Lack of Appetite": 39.5724524662832, 
 "Pain": 42.3843948614922,
 "Stress": 100.0,
 "Insomnia": 42.4187271741305,
 "Depression": 69.2028656456916,
 
 "Dizzy": 22.1503121602918,
 "Paranoid": 14.1867595722226,
 "Dry Eyes": 73.060705424837,
 "Headache": 16.3337649917133,
 "Dry Mouth": 100.0,
 
 "flavors": ["Mango", "Sweet", "Tropical"],
 
 "difficulty": "Easy",
 "height": "< .75 m", 
 "yield": "251-500",
 "flowering": "7-9 wks",
 "stretch": "100-200%",
 
 "parents": ["mango", "hindu-kush"],
 
 "description": "The Mango Kush marijuana strain tastes similar tothe actual mango fruit, with a distinct kush flavorand
                 hints of pine on the exhale. Itsbuds are covered with orange pistils and are described as very dense.
                 The plant has an average growth height of 4-5 feet. Flowering is 9-11 weeks and is a favorite with both
                  indoor and outdoor growers. The buds have thick shiny trichomes which are evident when the bud is broken
                   apart. The smell and taste are the same and described as mango and banana. THC content has been 
                   measured up to 16% and CBD at 0.3%."
 "image_urls": [],
 "image_paths": [], 
}
"""

TARGETS = ['effects', 'medical', 'negatives']
GROW_INFO_FIELD = 'grow_info'
GROW_INFO_FIELDS = ['difficulty', 'flowering', 'height', 'stretch', 'yield']

def main():
    # assumes one level of depth
    json_file = sys.argv[1]
    dest_file = sys.argv[2]
    df = pd.read_json(path_or_buf=json_file, lines=True)
    from functools import reduce
    for index, data in df.iterrows():
        assert all(x in data for x in TARGETS)
        assert all(type(data[x]) == dict for x in TARGETS)
        for el in TARGETS:
            _ = list(data[el].keys())
            if _ is None:
                print(_)
            # print(list(data[el].keys()))

        # assert all(bool(data[x]) for x in TARGETS)
        # print(r)
        # print(data['effects'])
        # print('----')
        # assert 'effects' in data
        # assert 'negatives' in data
        # assert 'medical' in data
        # assert all([t in r for t in TARGETS])
    # for en, i in enumerate(df['effects']):
    #     print(type(i))
    unique = {key: sorted(list(reduce(lambda i, j: set(list(i) + j), [list(data_dict.keys()) for data_dict in df[key]]))) for key in TARGETS}
              # sum([list(data_dict.keys()) for data_dict in df[key]])) for key in TARGETS}
    # unique = {key: set(sum([list(data_dict.keys()) for data_dict in df[key]])) for key in TARGETS}

    assert len(unique) == 3
    assert all(key in unique for key in TARGETS)
    print("Stats:\n{}".format('\n'.join([' ' + "'{}': [{}]".format(key, ', '.join(unique[key])) for key in TARGETS])))
    print
    print("Stats:\n{}".format('\n'.join([' ' + "'{}': #{}".format(key, len(unique[key])) for key in TARGETS])))

    # for key, discrete_values in unique.items():
    #     for inner_key in discrete_values:
    #         df = add_column(df, inner_key, [row[key].get(inner_key, '') for row in df.itterrows()])

    # for key, discrete_values in unique.items():
    #     df = add_columns(df, discrete_values, [[row[key].get(inner_key, '') for row in df.itterrows()] for inner_key in discrete_values])

    for key in TARGETS:
        discrete_values = sorted(list(unique[key]))
        df = add_columns(df, discrete_values, [list(df[key].apply(lambda x: x.get(inner_key, ''))) for inner_key in discrete_values])

    df = add_columns(df, GROW_INFO_FIELDS, [list(df[GROW_INFO_FIELD].apply(lambda x: x.get(inner_key, ''))) for inner_key in GROW_INFO_FIELDS])

    print(df.columns)
    for t in TARGETS:
        del df[t]
    del df[GROW_INFO_FIELD]
    # for i, row in df.iterrows():
    #     print(i)
    #     print(row)
    df.to_json(dest_file, orient='records', lines=True)

    dest_df = pd.read_json(path_or_buf=dest_file, lines=True)
    print(dest_df.columns)
    for i in dest_df['_id']:
        if 'mango' in i:
            print("'{}'".format(i))
    #     print(i)
    for id in df['_id']:
        if id not in set(list(dest_df['_id'])):
            print("ERROR", id)
            break

# def add_column(dataframe, name, values):
#     """Call this method to add a new column with the given values and get a new dataframe reference"""
#     return dataframe.assign(**{name: values})

def add_columns(dataframe, names, values_list):
    """Call this method to add a new column with the given values and get a new dataframe reference"""
    return dataframe.assign(**dict(zip(names, values_list)))


if __name__ == '__main__':
    main()