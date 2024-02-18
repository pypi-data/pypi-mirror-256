import numpy as np
from sklearn.linear_model import LogisticRegression

from quapy.method.aggregative import CC, PCC, ACC, PACC
from quapy.benchmarking._base import MethodDescriptor

lr_hyper = {'C': np.logspace(-3, 3, 7), 'class_weight': ['balanced', None]}

wrap_cls_params = lambda params: {'classifier__' + key: val for key, val in params.items()}

cc = MethodDescriptor(
    id='CC',
    name='CC(LR)',
    instance=CC(LogisticRegression()),
    hyperparams=wrap_cls_params(lr_hyper)
)

pcc = MethodDescriptor(
    id='PCC',
    name='PCC(LR)',
    instance=PCC(LogisticRegression()),
    hyperparams=wrap_cls_params(lr_hyper)
)

acc = MethodDescriptor(
    id='ACC',
    name='ACC(LR)',
    instance=ACC(LogisticRegression()),
    hyperparams=wrap_cls_params(lr_hyper)
)

pacc = MethodDescriptor(
    id='PACC',
    name='PACC(LR)',
    instance=PACC(LogisticRegression()),
    hyperparams=wrap_cls_params(lr_hyper)
)