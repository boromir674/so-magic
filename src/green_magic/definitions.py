import os
from collections import OrderedDict as od
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

field2empty_obj = od({
    'type': '',
    'name': '',
    'flavors': [],
    'effects': {},
    'medical': {},
    'negatives': {},
    'difficulty': '',
    'height': '',
    'yield': '',
    'flowering': '',
    'stretch': '',
    'parents': [],
    'description': '',
    'image_urls': ''
    }
)

all_vars = tuple(['_id'] + [_ for _ in field2empty_obj.keys()])

#### ENCODING SUPPORTED
#  * 'binary_on_off'
#  * 'binary-1'
#  * 'set-real-value'



#######################

grow_info = {
    'difficulty': ('Easy', 'Moderate', 'Difficult'),
    'height': ('< .75 m', '.76-2 m', '> 2 m'),
    'yield': ('40-99', '100-250', '251-500'),
    'flowering': ('7-9 wks', '10-12 wks', '> 12 wks'),
    'stretch': ('< 100%', '100-200%', '> 200%')
}

labeling = {
    'highness': {
        'yielding_vars': {
            'effects': ['Creative', 'Euphoric', 'Happy', ]
        }
    }

}

# 'Creative',
#   'Energetic',
#   'Euphoric',
#   'Focused',
#   'Giggly',
#   'Happy',
#   'Hungry',
#   'Relaxed',
#   'Sleepy',
#   'Talkative',
#   'Tingly',
#   'Uplifted'},
