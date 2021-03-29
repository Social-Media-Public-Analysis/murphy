import numpy as np
import pandas as pd
from sklearn.feature_selection import SelectFwe, SelectPercentile, f_classif
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
from sklearn.svm import LinearSVC
from tpot.builtins import OneHotEncoder, StackingEstimator
from tpot.export_utils import set_param_recursive
from sklearn.preprocessing import FunctionTransformer
from copy import copy

# NOTE: Make sure that the outcome column is labeled 'target' in the data file
tpot_data = pd.read_csv('PATH/TO/DATA/FILE', sep='COLUMN_SEPARATOR', dtype=np.float64)
features = tpot_data.drop('target', axis=1)
training_features, testing_features, training_target, testing_target = \
            train_test_split(features, tpot_data['target'], random_state=42)

# Average CV score on the training set was: 0.3656802383316783
exported_pipeline = make_pipeline(
    make_union(
        make_pipeline(
            SelectFwe(score_func=f_classif, alpha=0.008),
            OneHotEncoder(minimum_fraction=0.1),
            SelectPercentile(score_func=f_classif, percentile=13)
        ),
        FunctionTransformer(copy)
    ),
    LinearSVC(C=0.1, dual=False, loss="squared_hinge", penalty="l2", tol=0.01)
)
# Fix random state for all the steps in exported pipeline
set_param_recursive(exported_pipeline.steps, 'random_state', 42)

exported_pipeline.fit(training_features, training_target)
results = exported_pipeline.predict(testing_features)
