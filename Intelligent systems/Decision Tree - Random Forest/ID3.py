import math
import os
import random
from collections import deque


class Node:
    def __init__(self):
        self.value = None   
        self.next = None    
        self.childs = None  


class DecisionTreeClassifier:
    """Decision Tree Classifier using ID3 algorithm."""

    def __init__(self, X, feature_names, labels):
        self.X = X
        self.feature_names = feature_names
        self.labels = labels
        self.labelCategories = list(set(labels))
        self.labelCategoriesCount = [list(labels).count(x) for x in self.labelCategories]
        self.node = None
        self.entropy = self._get_entropy([x for x in range(len(self.labels))]) 

    def _get_entropy(self, x_ids):
        labels = [self.labels[i] for i in x_ids]
        label_count = [labels.count(x) for x in self.labelCategories]
        entropy = sum(
            [-count / len(x_ids) * math.log(count / len(x_ids), 2) if count else 0 for count in label_count]
        )
        return entropy

    def _get_information_gain(self, x_ids, feature_id):
        info_gain = self._get_entropy(x_ids)
        x_features = [self.X[x][feature_id] for x in x_ids]
        feature_vals = list(set(x_features))
        feature_vals_count = [x_features.count(x) for x in feature_vals]
        feature_vals_id = [
            [x_ids[i] for i, x in enumerate(x_features) if x == y]
            for y in feature_vals
        ]
        info_gain = info_gain - sum(
            [val_counts / len(x_ids) * self._get_entropy(val_ids)
             for val_counts, val_ids in zip(feature_vals_count, feature_vals_id)]
        )
        return info_gain

    def _get_feature_max_information_gain(self, x_ids, feature_ids):
        features_ig = [self._get_information_gain(x_ids, fid) for fid in feature_ids]
        max_id = feature_ids[features_ig.index(max(features_ig))]
        return self.feature_names[max_id], max_id

    def id3(self):
        x_ids = [x for x in range(len(self.X))]
        feature_ids = [x for x in range(len(self.feature_names))]
        self.node = self._id3_recv(x_ids, feature_ids, self.node)

    def _id3_recv(self, x_ids, feature_ids, node):
        if not node:
            node = Node()

        labels_in_features = [self.labels[x] for x in x_ids]

        if len(set(labels_in_features)) == 1:
            node.value = self.labels[x_ids[0]]
            return node

        if len(feature_ids) == 0:
            node.value = max(set(labels_in_features), key=labels_in_features.count)
            return node

        best_feature_name, best_feature_id = self._get_feature_max_information_gain(x_ids, feature_ids)
        node.value = best_feature_name
        node.childs = []

        feature_values = list(set([self.X[x][best_feature_id] for x in x_ids]))

        for value in feature_values:
            child = Node()
            child.value = value
            node.childs.append(child)

            child_x_ids = [x for x in x_ids if self.X[x][best_feature_id] == value]

            if not child_x_ids:
                child.next = max(set(labels_in_features), key=labels_in_features.count)
            else:
                new_feature_ids = feature_ids.copy()
                if best_feature_id in new_feature_ids:
                    new_feature_ids.pop(new_feature_ids.index(best_feature_id))
                child.next = self._id3_recv(child_x_ids, new_feature_ids, child.next)

        return node

    def predict_one(self, x_row):
        if not self.node:
            raise ValueError("Tree not built. Call id3() first.")

        node = self.node
        if node.childs is None and node.next is None and node.value in self.labelCategories:
            return node.value

        while True:
            if node.childs is None:
                return node.value if node.value in self.labelCategories else node.value

            feat_name = node.value
            feat_idx = self.feature_names.index(feat_name)
            v = x_row[feat_idx]

            matched = None
            for ch in node.childs:
                if ch.value == v:
                    matched = ch
                    break

            if matched is None:
                return max(set(self.labels), key=self.labels.count)
            
            if isinstance(matched.next, Node):
                node = matched.next
            else:
                return matched.next

    def predict(self, X_test):
        return [self.predict_one(row) for row in X_test]

    def printTree(self):
        if not self.node:
            return
        nodes = deque()
        nodes.append(self.node)
        while len(nodes) > 0:
            node = nodes.popleft()
            print(node.value)
            if node.childs:
                for child in node.childs:
                    print('({})'.format(child.value))
                    nodes.append(child.next)
            elif node.next:
                print(node.next)



def load_breast_cancer_data():
    candidates = [
        "./breast+cancer/breast-cancer.data",
        "/mnt/data/breast-cancer.data",
    ]
    path = None
    for p in candidates:
        if os.path.exists(p):
            path = p
            break
    if path is None:
        raise FileNotFoundError("Could not find breast-cancer.data in ./breast+cancer/ or /mnt/data/")

    feature_names = [
        "age",
        "menopause",
        "tumor-size",
        "inv-nodes",
        "node-caps",
        "deg-malig",
        "breast",
        "breast-quad",
        "irradiat",
    ]

    X, labels = [], []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split(",")]
            if len(parts) != 10:
                continue
            labels.append(parts[0])     
            X.append(parts[1:])        
    return X, feature_names, labels


def accuracy_score(y_true, y_pred):
    correct = sum(1 for a, b in zip(y_true, y_pred) if a == b)
    return correct / len(y_true) if y_true else 0.0


def stratified_split(X, y, test_ratio=0.2, seed=42):
    rnd = random.Random(seed)
    by_class = {}
    for i, cls in enumerate(y):
        by_class.setdefault(cls, []).append(i)

    train_idx, test_idx = [], []
    for cls, idxs in by_class.items():
        idxs = idxs.copy()
        rnd.shuffle(idxs)
        n_test = int(round(len(idxs) * test_ratio))
        test_idx.extend(idxs[:n_test])
        train_idx.extend(idxs[n_test:])

    rnd.shuffle(train_idx)
    rnd.shuffle(test_idx)

    X_train = [X[i] for i in train_idx]
    y_train = [y[i] for i in train_idx]
    X_test = [X[i] for i in test_idx]
    y_test = [y[i] for i in test_idx]
    return X_train, y_train, X_test, y_test


def stratified_kfold_indices(y, k=10, seed=42):
    rnd = random.Random(seed)
    by_class = {}
    for i, cls in enumerate(y):
        by_class.setdefault(cls, []).append(i)

    for cls in by_class:
        rnd.shuffle(by_class[cls])

    folds = [[] for _ in range(k)]
    for cls, idxs in by_class.items():
        for j, idx in enumerate(idxs):
            folds[j % k].append(idx)

    for f in folds:
        rnd.shuffle(f)
    return folds


def mean_std(values):
    if not values:
        return 0.0, 0.0
    m = sum(values) / len(values)
    var = sum((x - m) ** 2 for x in values) / len(values)
    return m, math.sqrt(var)


def read_input_spec():

    text = input().strip()
    if not text:
        raise ValueError("Empty input.")
    parts = text.split()
    mode = int(parts[0])
    letters = parts[1:]
    return mode, letters


def main():
    read_input_spec()

    X, feature_names, y = load_breast_cancer_data()

    X_train, y_train, X_test, y_test = stratified_split(X, y, test_ratio=0.2, seed=42)

    clf = DecisionTreeClassifier(X_train, feature_names, y_train)
    clf.id3()
    train_pred = clf.predict(X_train)
    train_acc = accuracy_score(y_train, train_pred)

    folds = stratified_kfold_indices(y_train, k=10, seed=42)
    cv_accs = []

    for i in range(10):
        val_idx = set(folds[i])
        tr_idx = [j for j in range(len(y_train)) if j not in val_idx]
        val_idx_list = list(val_idx)

        X_tr = [X_train[j] for j in tr_idx]
        y_tr = [y_train[j] for j in tr_idx]
        X_val = [X_train[j] for j in val_idx_list]
        y_val = [y_train[j] for j in val_idx_list]

        fold_clf = DecisionTreeClassifier(X_tr, feature_names, y_tr)
        fold_clf.id3()
        pred_val = fold_clf.predict(X_val)
        acc = accuracy_score(y_val, pred_val)
        cv_accs.append(acc)

    avg_acc, std_acc = mean_std(cv_accs)

    test_pred = clf.predict(X_test)
    test_acc = accuracy_score(y_test, test_pred)

    print("1. Train Set Accuracy:")
    print(f"    Accuracy: {train_acc * 100:.2f}%\n")

    print("10-Fold Cross-Validation Results:\n")
    for i, a in enumerate(cv_accs, 1):
        print(f"    Accuracy Fold {i}: {a * 100:.2f}%")
    print(f"\n    Average Accuracy: {avg_acc * 100:.2f}%")
    print(f"    Standard Deviation: {std_acc * 100:.2f}%\n")

    print("2. Test Set Accuracy:")
    print(f"    Accuracy: {test_acc * 100:.2f}%")


if __name__ == "__main__":
    main()
