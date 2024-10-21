import random
import re
import nltk
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
print(f'Попытка {n}')
while True:
    user_word = input('Ваше слово: ')
    if user_word.isalpha() and len(user_word) == 5 and user_word.lower() in baseform:
        n += 1
        for i in range(len(user_word)):
            if user_word[i].lower() in word and user_word.lower() != word:
                if user_word[i].lower() == word[i]:
                    print(f'{user_word[i]} стоит на правильном месте')
                else:
                    print(f'{user_word[i]} есть, но стоит не там')
            elif user_word[i].lower() not in word and user_word.lower() != word:
                print(f'{user_word[i]} отсутствует в слове')
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

