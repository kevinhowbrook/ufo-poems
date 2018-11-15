import sqlite3
import math
from datetime import datetime
import time
import ftfy
from random import randint

def removeNonAscii(s): return "".join(filter(lambda x: ord(x) < 128, s))


def get_data():
    conn = sqlite3.connect('database/database.db')
    cur = conn.cursor()
    with conn:
        data = cur.execute(
            'SELECT original_id, title, detailedDescription, city, region, \
             country, latitude, longitude, shape, submitted FROM sightings \
             ORDER BY submitted desc').fetchall()
        return data


data = get_data()[:4000]
word_counter = 0

def get_random_puctuation(input):
    # don't run all the time, otherwise it looks hard to read
    if randint(1, 20) % randint(1, 20):
        return input
    if randint(1, 20) % 2:
        output = '<i>' + input + '</i>'
    else:
        output = '<strong>' + input + '</strong>'

    return output


def get_random_spaces(input):
    # don't run all the time, otherwise it looks hard to read
    if randint(1, 20) % randint(1, 20):
        return input
    spaces = ''
    for v in range(randint(0, 4)):
        spaces += ' '
    output = input + spaces
    return output


def get_random_breaks(input):
    if randint(0, 200) % 2:
        return input
    breaks = ''
    for v in range(randint(0, 3)):
        breaks += '<br>'
    output = input + breaks
    return output



# poems
with open('ufo_poems.md', 'w') as f:
    poems = []
    for item in data:

        if item[1] is '':
            continue

        # title
        title = ftfy.fix_text(str(item[1]))
        # Randomly space and position words
        title = title.split()

        poem = []  # Will hold our poem
        for word in title:
            word_counter += 1
            _word = []
            for letter in word:
                _word.append(get_random_spaces(letter))
            _word = ''.join(_word)

            _word = get_random_breaks(_word)
            _word = get_random_puctuation(_word)

            poem.append(_word)

        poems.append(poem)

    # wrap each poem in a <p> tag for formatting
    for i, v in enumerate(poems):
        # also randomly join words or space them
        sep = ''
        number = randint(0, 200)
        if number % 2 or number % 3 or number % 4:
            sep = ' '

        poems[i] = '<p>' + sep.join(v) + '</p> \n\n --- \n\n '

    poems = ' '.join(poems)
    f.write(poems)
    print(word_counter)



# Whole novel writer

# word_counter = 0
# with open('ufo_novel.md', 'w') as f:
#     for item in data:
#         # must have a title and desc,
#         # use or len(item[2]) < 150 for long descriptions,
#         # otherwise # it's a boring read

#         if item[1] is '' and item[2] is '':
#             continue

#         # title
#         title = ftfy.fix_text(str(item[1]))
#         f.write('## ' + title + '\n\n')
#         # Submitted
#         if(item[9]):
#             when = time.mktime(datetime.strptime(
#                 item[9], "%Y-%m-%dT%H:%M:%SZ").timetuple())
#             time_reported = datetime.utcfromtimestamp(
#                 when).strftime('%a %d %B %Y - %H:%M:%S')
#             f.write('### ' + time_reported + '\n\n')

#         # desctiption, needs some cleaning
#         desc = str(item[2])
#         desc = desc.replace('~', '')
#         desc = '. '.join(
#             map(lambda desc: desc.strip().capitalize(), desc.split('.')))
#         desc = '! '.join(
#             map(lambda desc: desc.strip().capitalize(), desc.split('!')))
#         desc = ftfy.fix_text(desc)

#         f.write(desc + '\n')

#         # Increment the word counter
#         word_counter += len(desc.split())

#         f.write('\n\n')
