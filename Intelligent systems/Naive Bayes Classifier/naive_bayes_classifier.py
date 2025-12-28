import pandas as pd
import numpy as np
from collections import Counter
from math import log
import os


DATA_DIR = "./congressional+voting+records"
DATA_FILE = "house-votes-84.data"

ATTRIBUTES = [f"a{i}" for i in range(1, 17)]
COLUMNS = ["class"] + ATTRIBUTES

def load_data():
    path = os.path.join(DATA_DIR, DATA_FILE)

    if not os.path.exists(path):
        raise FileNotFoundError(f"No file: {path}")

    df = pd.read_csv(path, header=None, names=COLUMNS)
    return df


def preprocess(df, mode):
    df = df.copy()

    if mode == 0:
        return df

    elif mode == 1:
        for cls in df["class"].unique():
            cls_df = df[df["class"] == cls]
            for attr in ATTRIBUTES:
                mode_val = cls_df[cls_df[attr] != "?"][attr].mode()
                if not mode_val.empty:
                    df.loc[(df["class"] == cls) & (df[attr] == "?"), attr] = mode_val[0]
        return df
    else:
        raise ValueError("Must be between 0 and 1")

def stratified_split(df, test_size=0.2):
    train, test = [], []

    for cls in df["class"].unique():
        cls_data = df[df["class"] == cls].sample(frac=1, random_state=42)
        split = int(len(cls_data) * (1 - test_size))
        train.append(cls_data.iloc[:split])
        test.append(cls_data.iloc[split:])

    return pd.concat(train), pd.concat(test)


class NaiveBayes:
    def __init__(self, laplace_lambda=1.0):
        self.lmbd = laplace_lambda
        self.class_probs = {}
        self.feature_probs = {}
        self.classes = []

    def fit(self, df):
        self.classes = df["class"].unique()
        total = len(df)

        for cls in self.classes:
            cls_df = df[df["class"] == cls]
            self.class_probs[cls] = log(len(cls_df) / total)
            self.feature_probs[cls] = {}

            for attr in ATTRIBUTES:
                values = df[attr].unique()
                counts = Counter(cls_df[attr])

                self.feature_probs[cls][attr] = {}
                for val in values:
                    num = counts.get(val, 0) + self.lmbd
                    den = len(cls_df) + self.lmbd * len(values)
                    self.feature_probs[cls][attr][val] = log(num / den)

    def predict(self, X):
        preds = []
        for _, row in X.iterrows():
            scores = {}
            for cls in self.classes:
                score = self.class_probs[cls]
                for attr in ATTRIBUTES:
                    score += self.feature_probs[cls][attr].get(row[attr], log(1e-9))
                scores[cls] = score
            preds.append(max(scores, key=scores.get))
        return preds


def accuracy(y_true, y_pred):
    return np.mean(np.array(y_true) == np.array(y_pred))


def cross_validation(df, k=10, lmbd=1.0):
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    folds = np.array_split(df, k)
    accs = []

    for i in range(k):
        test = folds[i]
        train = pd.concat(folds[:i] + folds[i+1:])
        nb = NaiveBayes(lmbd)
        nb.fit(train)
        preds = nb.predict(test)
        accs.append(accuracy(test["class"], preds))

    return accs

def main():
    mode = int(input().strip())  
    df = load_data()
    df = preprocess(df, mode)

    train_df, test_df = stratified_split(df)


    nb = NaiveBayes(laplace_lambda=1.0)
    nb.fit(train_df)

    train_preds = nb.predict(train_df)
    train_acc = accuracy(train_df["class"], train_preds)


    cv_accs = cross_validation(train_df, k=10, lmbd=1.0)

    test_preds = nb.predict(test_df)
    test_acc = accuracy(test_df["class"], test_preds)


    print("1. Train Set Accuracy:")
    print(f"    Accuracy: {train_acc * 100:.2f}%\n")

    print("10-Fold Cross-Validation Results:\n")
    for i, acc in enumerate(cv_accs):
        print(f"    Accuracy Fold {i+1}: {acc * 100:.2f}%")

    print(f"\n    Average Accuracy: {np.mean(cv_accs) * 100:.2f}%")
    print(f"    Standard Deviation: {np.std(cv_accs) * 100:.2f}%\n")

    print("2. Test Set Accuracy:")
    print(f"    Accuracy: {test_acc * 100:.2f}%")

if __name__ == "__main__":
    main()
