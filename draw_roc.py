# -*- coding: utf-8 -*-

import jubatus
from jubatus.common import Datum
import json
import numpy as np
import pylab as pl
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
roc_auc = metrics.auc(fpr, tpr)

plt.figure()
pl.clf()
pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
pl.plot([0, 1], [0, 1], 'k--')
pl.xlim([0.0, 1.0])
pl.ylim([0.0, 1.0])
pl.xlabel('False Positive Rate')
pl.ylabel('True Positive Rate')
pl.title('Receiver Operating Characteristic')
pl.legend(loc="lower right")
pl.savefig("roc.png")
pl.show()
