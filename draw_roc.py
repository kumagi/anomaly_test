# -*- coding: utf-8 -*-

import jubatus
from jubatus.common import Datum
import json
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt

labels = None
scores = None
with open("result.json", "r") as f:
    value = (json.loads(f.read()))
    labels = np.array(value["labels"])
    scores = np.array(value["scores"])


for i in range(len(scores)):
    if np.isinf(scores[i]):
        scores[i] = 10000000

fpr, tpr, thresholds = metrics.roc_curve(labels, scores, pos_label=1)
auc = metrics.auc(fpr, tpr)

plt.figure()
