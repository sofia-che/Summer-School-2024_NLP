import pandas as pd
import pymorphy2
import re
positive = ['хороший', 'хорошо', 'спасибо', 'радостный', 'радостно', 'радость', 'радовать', 'вкусный', 'вкусно',
            'забавный', 'забавно', 'забава', 'милый', 'мило', 'уютный', 'уют', 'уютно', 'веселый', 'весёлый', 'весело',
            'веселье', 'мелодичный', 'мелодично', 'прекрасный', 'прекрасно', 'свободный', 'свобода', 'свободно',
            'ласковый', 'ласково', 'впечатляющий', 'впечатляюще', 'талантливый', 'талант', 'талантливо', 'красивый',
            'красота', 'красиво']
negative = ['ненавистный', 'ненавистно', 'ненависть', 'безответственный', 'безответственно', 'безответственность',
            'дикий', 'дико', 'дикость', 'наказание', 'жестокость', 'жестокий', 'жестоко', 'убийство', 'убивать', 'убить',
            'убийца', 'ужасный', 'ужасно', 'ужас' 'беда', 'страшный', 'виновный', 'вина', 'варварство', 'грустный',
            'грустно', 'грусть', 'печальный', 'печально', 'печаль', 'плохой', 'плохо', 'фейк']
morph = pymorphy2.MorphAnalyzer()
lst_df = [pd.read_excel('tweeter_dub1.xlsx'), pd.read_excel('tweeter_dub2.xlsx')]


def lemmatize(text):
    tokens = re.split(r'\W+', text)
    lemmas = [morph.parse(token)[0].normal_form for token in tokens if token]
    return ' '.join(lemmas)


def calculate_sent(text):
    sent = 0
    tokens = re.split(r'\W+', text)
    for token in tokens:
        if token in positive:
            sent += 1
        elif token in negative:
            sent -= 1
    return sent


mean_values = {}
mean_by_date = []

for i in range(len(lst_df)):
    lst_df[i]['lemmatized'] = lst_df[i]['текст поста'].apply(lemmatize)
    lst_df[i]['sent_value'] = lst_df[i]['lemmatized'].apply(calculate_sent)
    mean_date = lst_df[i].groupby('дата поста')['sent_value'].mean().reset_index()
    mean_type = lst_df[i].groupby('Вид автора поста')['sent_value'].mean().reset_index()
    mean_values[i+1] = lst_df[i]['sent_value'].mean()
    if lst_df[i]['sent_value'].mean() == min(mean_values.values()):
        for date, value in lst_df[i].groupby('дата поста'):
            if value['sent_value'].mean() > 0:
                mean_by_date.append(date)
    with pd.ExcelWriter(f'tweets_dub_analyzed{i+1}.xlsx', engine='openpyxl') as w:
        lst_df[i].to_excel(w, sheet_name='general_info', index=False)
        mean_date.to_excel(w, sheet_name='mean_by_date', index=False)
        mean_type.to_excel(w, sheet_name='mean_by_type', index=False)

df1 = pd.read_excel('tweets_dub_analyzed1.xlsx', sheet_name='mean_by_type')
df2 = pd.read_excel('tweets_dub_analyzed2.xlsx', sheet_name='mean_by_type')
author_types1 = df1.loc[df1['sent_value'].idxmax()]['Вид автора поста']
author_types2 = df2.loc[df2['sent_value'].idxmax()]['Вид автора поста']
print(f'В среднем твиты добрее на дубе {max(mean_values, key=mean_values.get)}')
print(f'Количество дней, в которые посты на менее добром дубе были в среднем добрее (больше нуля): {len(mean_by_date)}')
print(f'Самый добрый на первом дубе - {author_types1} (значение {df1["sent_value"].max()}), на втором - {author_types2} (значение {df2["sent_value"].max()})')
new_df = pd.DataFrame()
new_df['Вид автора поста'] = df1['Вид автора поста']
new_df['sent_value_x'] = df1['sent_value']
new_df['sent_value_y'] = df2['sent_value']
new_df['sent_value_total'] = new_df[['sent_value_x', 'sent_value_y']].mean(axis=1)
author_types_total = new_df.loc[new_df['sent_value_total'].idxmax()]['Вид автора поста']
print(f'Самый добрый на обоих дубах - {author_types_total} (значение {new_df["sent_value_total"].max()})')
