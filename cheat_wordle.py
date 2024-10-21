import random
import nltk
import re
nltk.download('words')
from nltk.corpus import words

wordlist = [word for word in set(words.words()) if len(word) == 5 and word.isalpha()]
baseform = []
tags = ['NN', 'VB', 'JJ', 'RB']
for i in wordlist:
    pos = nltk.pos_tag([i])[0][1]
    if pos in tags:
        baseform.append(i.lower())
word = random.choice(tuple(set(baseform)))
n = 1
banned_letters = []
given_letters = []
correct_positions = {}
incorrect_positions = {}
print(f'Попытка {n}')
while True:
    user_word = input('Ваше слово: ')
    if user_word.isalpha() and len(user_word) == 5 and user_word.lower() in baseform:
        n += 1
        for i in range(len(user_word)):
            if user_word[i].lower() in word and user_word.lower() != word:
                given_letters.append(user_word[i])
                if user_word[i].lower() == word[i]:
                    print(f'{user_word[i]} стоит на правильном месте')
                    correct_positions[user_word[i]] = i+1
                else:
                    print(f'{user_word[i]} есть, но стоит не там')
                    if user_word[i] not in incorrect_positions:
                        incorrect_positions[user_word[i]] = [i+1]
                    else:
                        incorrect_positions[user_word[i]] += [i+1]
            elif user_word[i].lower() not in word and user_word.lower() != word:
                print(f'{user_word[i]} отсутствует в слове')
                banned_letters.append(user_word[i])
        if len(banned_letters) > 0:
            print(f'Список запрещенных букв: ', *set(banned_letters))
        if len(given_letters) > 0:
            print(f'Следующие слова должны содержать буквы: ', *set(given_letters))
        for key, value in correct_positions.items():
            print(f'{key} стоит на {value} месте')
        for key, value in incorrect_positions.items():
            print(f'{key} точно не стоит на', *value, 'месте')
        if user_word.lower() != word and n <= 6:
            print(f'Попытка {n}')
    if re.fullmatch(r'[A-Za-z]+', user_word):
        if len(user_word) > 5:
            print('Слово слишком длинное, попробуйте снова')
        elif len(user_word) < 5:
            print('Слово слишком короткое, попробуйте снова')
        elif user_word.lower() not in baseform:
            print('Такого слова не существует, попробуйте снова')
    elif not re.fullmatch(r'[A-Za-z]+', user_word):
        print('Недопустимый символ в слове, попробуйте снова')
    if user_word.lower() == word and n <= 7:
        print('Поздравляем, Вы выиграли!')
        break
    if n > 6:
        print(f'К сожалению, Вы проиграли. Загаданное слово: {word}')
        break

