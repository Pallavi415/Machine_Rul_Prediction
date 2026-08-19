# Preparing the training data

import pandas as pd


def load_training_data(path):
    columns = (
        ["unit_id", "cycle"]
        + [f"setting_{i}" for i in range(1, 4)]
        + [f"sensor_{i}" for i in range(1, 22)]
    )

    df = pd.read_csv(
        path,
        sep=r"\s+",
        header=None,
        names=columns
    )

    # Creating the RUL target

    max_cycle = df.groupby("unit_id")["cycle"].transform("max")
    df["RUL"] = max_cycle - df["cycle"]

    return df


def remove_constant_features(df):
    # Finding constant features

    constant_columns = df.columns[df.nunique() == 1]

    # Removing constant features

    df = df.drop(columns=constant_columns)

    return df, constant_columns