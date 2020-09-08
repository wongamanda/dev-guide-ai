# Prolog - Auto Generated #
import os, uuid, matplotlib
matplotlib.use('Agg')
# import matplotlib.pyplot
import pandas as pd
import numpy as np
import ast

os.chdir(u'C:/Users/amawong/PythonEditorWrapper_71b15c21-6320-4615-8579-68002cd1e932')
dataset = pd.read_csv('input_df_423750c9-fd50-42ce-89b6-1d3a966b419c.csv')

# matplotlib.pyplot.figure(figsize=(5.55555555555556,4.16666666666667), dpi=72)
# matplotlib.pyplot.show = lambda args=None,kw=None: matplotlib.pyplot.savefig(str(uuid.uuid1()))
# Original Script. Please update your script content here and once completed copy below section back to the original editing window #
# The following code to create a dataframe and remove duplicated rows is always executed and acts as a preamble for your script: 


def get_unique_key_phrases(theme_list):
    theme_list = list(theme_list)[0]
    reduced = set(theme_list)
    phrase_occurences = {}
    copy = theme_list
    
    for key_phrase in reduced:
        phrase_occurences[key_phrase] = 0
        while key_phrase in copy:
            phrase_occurences[key_phrase] += 1
            copy.remove(key_phrase)
    phrase_occurences = sorted(phrase_occurences.items(), key=lambda x:x[1], reverse=True)
    phrase_occurences = np.array(phrase_occurences)
    phrase_occurences = pd.DataFrame(phrase_occurences, columns=["Key Phrase", "Count"])
    return phrase_occurences


if __name__ == "__main__":
    try:
        dataset = pd.DataFrame(dataset, columns=['Key Phrases', 'Theme'])

        dataset['Key Phrases'] = dataset['Key Phrases'].str.strip()

        df = dataset.groupby('Theme')['Key Phrases'].apply(list).reset_index()

        new_phrase_column = []

        for phrase_list in df.loc[:, 'Key Phrases']:
            flat_row = [inner for item in phrase_list for inner in ast.literal_eval(item)]
            new_phrase_column.append(flat_row)
        df['Key Phrases'] = new_phrase_column

        speed_list = df.loc[(df["Theme"] == 'speed'), 'Key Phrases'].values
        price_list = df.loc[(df["Theme"] == 'price'), 'Key Phrases'].values
        features_list = df.loc[(df["Theme"] == 'features'), 'Key Phrases'].values
        reliability_list = df.loc[(df["Theme"] == 'reliability'), 'Key Phrases'].values
        services_list = df.loc[(df["Theme"] == 'services'), 'Key Phrases'].values
        design_list = df.loc[(df["Theme"] == 'design'), 'Key Phrases'].values
        security_list = df.loc[(df["Theme"] == 'security'), 'Key Phrases'].values
        other_list = df.loc[(df["Theme"] == 'other'), 'Key Phrases'].values

        print("Printing SPEED", "\n", get_unique_key_phrases(speed_list))
        print("Printing PRICE", "\n", get_unique_key_phrases(price_list))
        print("Printing FEATURES", "\n", get_unique_key_phrases(features_list))
        print("Printing RELIABILITY", "\n", get_unique_key_phrases(reliability_list))
        print("Printing SERVICES", "\n", get_unique_key_phrases(services_list))
        print("Printing DESIGN", "\n", get_unique_key_phrases(design_list))
        print("Printing SECURITY", "\n", get_unique_key_phrases(security_list))
        print("Printing OTHER", "\n", get_unique_key_phrases(other_list))

    
    except Exception as ex:
        print(ex)





# Epilog - Auto Generated #
os.chdir(u'C:/Users/amawong/PythonEditorWrapper_71b15c21-6320-4615-8579-68002cd1e932')
