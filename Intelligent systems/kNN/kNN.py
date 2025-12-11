import random
import math

# 1. Зареждане на данните
def load_iris(filename):
    data = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue 
            parts = line.split(",")
            features = [float(x) for x in parts[:4]]
            label = parts[4]
            data.append((features, label))
    return data

# 2. Разделяне на данните на train/test
def train_test_split(data, train_ratio=0.8):
    data_shuffled = data[:]
    random.shuffle(data_shuffled)

    n_train = int(len(data_shuffled) * train_ratio)
    train = data_shuffled[:n_train]
    test = data_shuffled[n_train:]
    return train, test

# 3. Намиране на средно и стандартно отклонение по всяка характеристика (само върху train)
def compute_mean_std(train):
    num_features = len(train[0][0])
    means = [0.0] * num_features
    stds = [0.0] * num_features

    n = len(train)
    for features, label in train:
        for j in range(num_features):
            means[j] += features[j]
    for j in range(num_features):
        means[j] /= n

    for features, label in train:
        for j in range(num_features):
            diff = features[j] - means[j]
            stds[j] += diff * diff

    for j in range(num_features):
        stds[j] = math.sqrt(stds[j] / n)
        if stds[j] == 0:
            stds[j] = 1.0  

    return means, stds

# 4. Нормализация: (x - mean) / std
def normalize_dataset(dataset, means, stds):
    normalized = []
    for features, label in dataset:
        new_features = []
        for j in range(len(features)):
            x = (features[j] - means[j]) / stds[j]
            new_features.append(x)
        normalized.append((new_features, label))
    return normalized

# 5. Евклидово разстояние между две точки (списък от числа)
def euclidean_distance(x, y):
    s = 0.0
    for j in range(len(x)):
        diff = x[j] - y[j]
        s += diff * diff
    return math.sqrt(s)

# 6. kNN предсказване за една точка
def knn_predict(train, query_features, k):
    distances = []  
    for features, label in train:
        d = euclidean_distance(features, query_features)
        distances.append((d, label))

    distances.sort(key=lambda x: x[0])

    k_nearest = distances[:k]

    votes = {}
    for d, label in k_nearest:
        if label not in votes:
            votes[label] = 0
        votes[label] += 1

    best_label = None
    best_count = -1
    for label, count in votes.items():
        if count > best_count:
            best_count = count
            best_label = label

    return best_label

# 7. Точност: колко процента правилни предсказания
def accuracy(train, dataset, k):
    correct = 0
    total = len(dataset)
    for features, label in dataset:
        pred = knn_predict(train, features, k)
        if pred == label:
            correct += 1
    return correct / total

# 8. 10-fold cross-validatio
def cross_validation_10(train, k):
    n = len(train)
    indices = list(range(n))
    random.shuffle(indices)

    folds = []
    fold_size = n // 10
    start = 0
    for i in range(9):
        end = start + fold_size
        folds.append(indices[start:end])
        start = end
    folds.append(indices[start:])

    fold_accuracies = []

    for fold_idx in range(10):
        val_indices = folds[fold_idx]
        train_indices = []
        for i in range(10):
            if i == fold_idx:
                continue
            train_indices.extend(folds[i])

        fold_train = [train[i] for i in train_indices]
        fold_val = [train[i] for i in val_indices]

        acc = accuracy(fold_train, fold_val, k)
        fold_accuracies.append(acc)

    avg_acc = sum(fold_accuracies) / len(fold_accuracies)

    var = 0.0
    for acc in fold_accuracies:
        diff = acc - avg_acc
        var += diff * diff
    var /= len(fold_accuracies)
    std_dev = math.sqrt(var)

    return fold_accuracies, avg_acc, std_dev

# 9. Главна функция
def main():
    random.seed(42)  

    k = int(input().strip()) 

    data = load_iris("iris/iris.data")
    train, test = train_test_split(data, train_ratio=0.8)

    means, stds = compute_mean_std(train)
    train_norm = normalize_dataset(train, means, stds)
    test_norm = normalize_dataset(test, means, stds)


    train_acc = accuracy(train_norm, train_norm, k)


    fold_accs, avg_acc, std_dev = cross_validation_10(train_norm, k)


    test_acc = accuracy(train_norm, test_norm, k)

    print("1. Train Set Accuracy:")
    print("    Accuracy: {:.2f}%".format(train_acc * 100))
    print()
    print("2. 10-Fold Cross-Validation Results:")
    print()
    for i, acc in enumerate(fold_accs, start=1):
        print("    Accuracy Fold {}: {:.2f}%".format(i, acc * 100))
    print()
    print("    Average Accuracy: {:.2f}%".format(avg_acc * 100))
    print("    Standard Deviation: {:.2f}%".format(std_dev * 100))
    print()
    print("3. Test Set Accuracy:")
    print("    Accuracy: {:.2f}%".format(test_acc * 100))


if __name__ == "__main__":
    main()
