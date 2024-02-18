import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from upgini.errors import ValidationError
from upgini.metadata import SYSTEM_RECORD_ID, TARGET, ModelTaskType
from upgini.resource_bundle import bundle
from upgini.utils.target_utils import balance_undersample, define_task


def test_invalid_target():
    y = pd.Series(["", "", ""])
    with pytest.raises(ValidationError, match=bundle.get("empty_target")):
        define_task(y)

    y = pd.Series([np.nan, np.inf, -np.inf])
    with pytest.raises(ValidationError, match=bundle.get("empty_target")):
        define_task(y)

    y = pd.Series([1, 1, 1, 1, 1])
    with pytest.raises(ValidationError, match=bundle.get("dataset_constant_target")):
        define_task(y)


def test_define_binary_task_type():
    y = pd.Series([0, 1, 0, 1, 0, 1])
    assert define_task(y, False) == ModelTaskType.BINARY
    assert define_task(y, True) == ModelTaskType.BINARY

    y = pd.Series(["a", "b", "a", "b", "a"])
    assert define_task(y, False) == ModelTaskType.BINARY
    assert define_task(y, True) == ModelTaskType.BINARY


def test_define_multiclass_task_type():
    y = pd.Series(range(1, 51))
    assert define_task(y, False) == ModelTaskType.MULTICLASS
    assert define_task(y, True) == ModelTaskType.MULTICLASS

    y = pd.Series([float(x) for x in range(1, 51)])
    assert define_task(y, False) == ModelTaskType.MULTICLASS
    assert define_task(y, True) == ModelTaskType.MULTICLASS

    y = pd.Series(range(0, 50))
    assert define_task(y, False) == ModelTaskType.MULTICLASS
    assert define_task(y, True) == ModelTaskType.MULTICLASS

    y = pd.Series(["a", "b", "c", "b", "a"])
    assert define_task(y, False) == ModelTaskType.MULTICLASS
    assert define_task(y, True) == ModelTaskType.MULTICLASS

    y = pd.Series(["0", "1", "2", "3", "a"])
    assert define_task(y, False) == ModelTaskType.MULTICLASS
    assert define_task(y, True) == ModelTaskType.MULTICLASS

    y = pd.Series([0.0, 3.0, 5.0, 0.0, 5.0, 0.0, 3.0, 0.0, 5.0, 0.0, 5.0, 0.0, 3.0, 0.0, 3.0, 5.0, 3.0])
    assert define_task(y, False) == ModelTaskType.MULTICLASS


def test_define_regression_task_type():
    y = pd.Series([0.0, 3.0, 5.0, 0.0, 5.0, 0.0, 3.0, 0.0, 5.0, 0.0, 5.0, 0.0, 3.0, 0.0, 3.0, 5.0, 3.0])
    assert define_task(y, True) == ModelTaskType.REGRESSION

    y = pd.Series([0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.5])
    assert define_task(y, False) == ModelTaskType.REGRESSION
    assert define_task(y, True) == ModelTaskType.REGRESSION

    y = pd.Series([0, 1, 2, 3, 4, 5, 6, 8])
    assert define_task(y, False) == ModelTaskType.REGRESSION
    assert define_task(y, True) == ModelTaskType.REGRESSION

    y = pd.Series([0.0, 3.0, 5.0, 0.0, 5.0, 0.0, 3.0])
    assert define_task(y, False) == ModelTaskType.REGRESSION
    assert define_task(y, True) == ModelTaskType.REGRESSION


def test_balance_undersampling_binary():
    df = pd.DataFrame({SYSTEM_RECORD_ID: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], TARGET: [0, 1, 0, 0, 0, 0, 0, 0, 0, 0]})
    balanced_df = balance_undersample(
        df, TARGET, ModelTaskType.BINARY, 42, imbalance_threshold=0.1, min_sample_threshold=2
    )
    print(balanced_df)
    expected_df = pd.DataFrame({
        SYSTEM_RECORD_ID: [1, 2, 3, 7, 9, 10],
        TARGET: [0, 1, 0, 0, 0, 0]
    })
    assert_frame_equal(balanced_df.sort_values(by=SYSTEM_RECORD_ID).reset_index(drop=True), expected_df)

    balanced_df = balance_undersample(
        df, TARGET, ModelTaskType.BINARY, 42, imbalance_threshold=0.1, min_sample_threshold=8
    )
    print(balanced_df)
    expected_df = pd.DataFrame({
        SYSTEM_RECORD_ID: [1, 2, 3, 4, 6, 7, 9, 10],
        TARGET: [0, 1, 0, 0, 0, 0, 0, 0]
    })
    assert_frame_equal(balanced_df.sort_values(by=SYSTEM_RECORD_ID).reset_index(drop=True), expected_df)

    df = pd.DataFrame({"system_record_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], TARGET: [0, 1, 0, 0, 0, 0, 0, 0, 1, 0]})
    balanced_df = balance_undersample(
        df, "target", ModelTaskType.BINARY, 42, imbalance_threshold=0.1, min_sample_threshold=4
    )
    print(balanced_df)
    assert_frame_equal(balanced_df, df)

    # TODO check another imbalance threshold


def test_balance_undersaampling_multiclass():
    df = pd.DataFrame({
        SYSTEM_RECORD_ID: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        TARGET: ["a", "b", "b", "c", "c", "c", "b", "c", "c", "c"]
    })

    balanced_df = balance_undersample(
        df, TARGET, ModelTaskType.MULTICLASS, 42, imbalance_threshold=0.1, min_sample_threshold=10
    )
    print(balanced_df)

    expected_df = pd.DataFrame({
        SYSTEM_RECORD_ID: [1, 2, 3, 5, 10],
        TARGET: ["a", "b", "b", "c", "c"]
    })
    assert_frame_equal(balanced_df.sort_values(by=SYSTEM_RECORD_ID).reset_index(drop=True), expected_df)
