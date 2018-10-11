import random
from functools import wraps
from dataset import data, extra_data

def only_active(func):
    @wraps(func)
    def wrapped(bot, update):
        # SO SLOWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW

        with open('state', 'rb') as f:
            if f.read()[0] == 65:
                return func(bot, update)


    return wrapped

def change_state(active):
    with open('state', 'wb') as f:

        if active:
            f.write(b'A')
        else:
            f.write(b'2')

def get_reply_data(question):
    question = question.lower()
    answers = []
    danger = 0

    def all(keyowrds, request):
        keywords_list = keyowrds.strip().split()
        total = 0
        for word in keywords_list:
            if word in request:
                print(word)
                total += 1

        if total / len(keywords_list) > 0.5:
            return total / len(keywords_list)

        return False

    def any(keyowrds, request):
        keywords_list = q.strip().split()
        total = 0
        for word in keywords_list:
            if word in question:
                total = 1
                break

        if total == 1:
            return True

        return False

    for q in data['all'].keys():
        result = all(q, question)
        if result:
            answers.append((data['all'][q], result))

    for q in data['any'].keys():
        result = any(q, question)
        if result:
            answers.append((data['any'][q], result))


    for q in data['qa'].keys():
        if all(q, question):
            current_data = data['qa'][q]
            return {
                'state': 2,
                'message': current_data[0],
                'extra': extra_data.index(current_data[1][0])
            }

    answer = sorted(answers, key=lambda x: x[1])[0][0]


    if not answers:
        return {
            'state': 0,
            'message': 'could not find answers to your question',
            'extra': '2' in answer
        }
    else:
        print(answers)
        return {
            'state': 1,
            'message': answer,
            'extra': '2' in answer
        }