import pandas as pd
import nltk as nl
import re
import string


def load_kcb_faqs_data(filepath):
    df_data = pd.read_excel(filepath)
    print(df_data.head())
    print(df_data.tail())
    print(df_data.info())
    print(f'Columns available {df_data.columns}')
    print(f'Unique classifications available {df_data.intent.unique().tolist()}')
    return df_data


def clean_text(text):
    '''Make text lowercase, remove text in square brackets,remove links,remove punctuation
    and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


def generate_ngrams(text, ngrams_count):
    text = str(text).split()
    return list(nl.ngrams(text, ngrams_count))


def extra_intent_text_and_bi_grams(df_data):
    # clean data
    df_data = df_data[df_data.text.notna()]
    df_data.text = df_data['text'].apply(clean_text)
    intent_classes = df_data.intent.unique().tolist()
    classes_data = []
    for intent_group in intent_classes:
        intent_group_data = df_data.loc[df_data['intent'] == intent_group]
        intent_group_text = ''
        for index, row in intent_group_data.iterrows():
            intent_group_text = intent_group_text + ' ' + row.text
        intent_group_dict = {'intent_group': intent_group,
                             'intent_group_text': intent_group_text,
                             'intent_group_bi_grams': generate_ngrams(intent_group_text, 2)}
        classes_data.append(intent_group_dict)
    return classes_data


def classify_using_bi_grams_computation(text, classes_data):
    bi_input = list(nl.ngrams(clean_text(text).split(), 2))
    intent_classification = []
    for intent_group_dict_item in classes_data:
        for input_tag in bi_input:
            x = 1
            try:
                x *= intent_group_dict_item['intent_group_bi_grams'].count(input_tag) / \
                    intent_group_dict_item['intent_group_text'].count(input_tag[0])
            except:
                x = 0.00
        intent_classification_item = {'intent': intent_group_dict_item['intent_group'], 'probability': x}
        intent_classification.append(intent_classification_item)
    return intent_classification


if __name__ == '__main__':
    kcb_faqs_data = load_kcb_faqs_data('data/KCB FAQs.xlsx')
    intent_classes_data = extra_intent_text_and_bi_grams(kcb_faqs_data)
    input_text = input("Enter your KCB question: ")
    print(classify_using_bi_grams_computation(input_text, intent_classes_data))

