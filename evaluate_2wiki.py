import re
import string
from collections import Counter
from typing import Tuple, List, Any, Dict
import json


def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction: str, ground_truth: str):
    normalized_prediction = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)

    ZERO_METRIC = (0, 0, 0)

    if normalized_prediction in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC
    if normalized_ground_truth in ['yes', 'no', 'noanswer'] and normalized_prediction != normalized_ground_truth:
        return ZERO_METRIC

    prediction_tokens = normalized_prediction.split()
    ground_truth_tokens = normalized_ground_truth.split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return ZERO_METRIC
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1, precision, recall


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def eval_answer(qa):
    prediction, gold = qa['predict'], qa['a']
    em = exact_match_score(prediction, gold)
    f1, prec, recall = f1_score(prediction, gold)
    return em, f1 #, prec, recall




with open("output/output_2wiki_SiReRAG_gpt4o_temp0.json") as fp:
    qa_pairs = json.load(fp)
    em = 0.
    f1 = 0.
    for idx, qa in enumerate(qa_pairs):
        em_s, f1_s = eval_answer(qa)
        # print(idx, em_s, f1_s)
        em += em_s
        f1 += f1_s
    print(em, f1)

