
'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math

def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    sum_of_squares = 0.0
    for x in vec:
        sum_of_squares += vec[x] * vec[x]

    return math.sqrt(sum_of_squares)

def cosine_similarity(vec1, vec2):
    top = 0
    bottom = 1
    b = 0
    c = 0
    for a in vec1.keys():
        if a in vec2.keys():
            top += vec1[a] * vec2[a]
    for a in vec1.values():
        b += a **2
    for a in vec2.values():
        c += a **2
    bottom = (bottom * b * c)**(.5)
    return top/bottom

def build_semantic_descriptors(sentences):
    returned = {}
    for a in range(len(sentences)):
        prev_keys = []
        for b in range(len(sentences[a])):
            if sentences[a][b] not in returned.keys():
                returned[sentences[a][b]] = {}
            prev_words = []
            for c in range(len(sentences[a])):
                if sentences[a][c] != sentences[a][b] and sentences[a][c] not in prev_words and sentences[a][b] not in prev_keys:
                    prev_words.append(sentences[a][c])
                    if sentences[a][c] not in returned[sentences[a][b]].keys():
                        returned[sentences[a][b]][sentences[a][c]] = 1
                    else:
                        returned[sentences[a][b]][sentences[a][c]] +=1
            prev_keys.append(sentences[a][b])
    return returned

def build_semantic_descriptors_x(oldy, sentences):
    for a in range(len(sentences)):
        prev_keys = []
        for b in range(len(sentences[a])):
            if sentences[a][b] not in oldy.keys():
                oldy[sentences[a][b]] = {}
            prev_words = []
            for c in range(len(sentences[a])):
                if sentences[a][c] != sentences[a][b] and sentences[a][c] not in prev_words and sentences[a][b] not in prev_keys:
                    prev_words.append(sentences[a][c])
                    if sentences[a][c] not in oldy[sentences[a][b]].keys():
                        oldy[sentences[a][b]][sentences[a][c]] = 1
                    else:
                        oldy[sentences[a][b]][sentences[a][c]] +=1
            prev_keys.append(sentences[a][b])

def build_semantic_descriptors_from_files(filenames):
    right = {}
    for a in range(len(filenames)):
        file = open(filenames[a], "r", encoding="latin1")
        data = file.read().replace('\n', ' ').strip().lower()
        data = data.replace(",","").replace("--"," ") .replace("-"," ").replace(":","").replace(";","")
        data = data.replace("!", ".").replace("?",".").split(".")
        data = [x for x in data if x != '']
        for a in range(len(data)):
            data[a] = data[a].split(" ")
            data[a] = [x for x in data[a] if x != '']
        build_semantic_descriptors_x(right, data)
    return right

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    similarity = -10
    saved = ""
    for a in choices:
        if semantic_descriptors.get(word, -1) == -1 or semantic_descriptors.get(a, -1) == -1:
            if similarity < -1:
                similarity = -1
                saved = a
        elif similarity_fn(semantic_descriptors[a], semantic_descriptors[word]) > similarity:
            similarity = similarity_fn(semantic_descriptors[a], semantic_descriptors[word])
            saved = a
    return saved


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    correct = 0
    total = 0
    file = open(filename, "r")
    data = file.read().strip().split("\n")
    data = [x for x in data if x != '']

    for a in range(len(data)):
        data[a] = data[a].split(" ")
        data[a] = [x for x in data[a] if x != '']

        word = data[a][0]
        choices = data[a][2:]
        shit = most_similar_word(word, choices, semantic_descriptors, similarity_fn)
        total += 1
        print (shit)
        print (data[a][1])
        if shit == data[a][1]:
            correct +=1
    return correct/total * 100
"""
sem_descriptors = build_semantic_descriptors_from_files(["wp.txt", "sw.txt"])
res = run_similarity_test("test.txt", sem_descriptors, cosine_similarity)
print(res, "of the guesses were correct")
"""