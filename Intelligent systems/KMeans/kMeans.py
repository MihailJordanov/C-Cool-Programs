import numpy as np
import matplotlib.pyplot as plt


def load_xy(path: str) -> np.ndarray:
    data = np.loadtxt(path, dtype=float)
    if data.ndim == 1:
        data = data.reshape(1, -1)
    if data.shape[1] != 2:
        raise ValueError(f"Expected 2 columns (x y), got {data.shape[1]}")
    return data


def wcss(X: np.ndarray, labels: np.ndarray, centroids: np.ndarray) -> float:
    s = 0.0
    for k in range(len(centroids)):
        pts = X[labels == k]
        if len(pts) == 0:
            continue
        diff = pts - centroids[k]
        s += float(np.sum(diff * diff))
    return s


def silhouette_score(X: np.ndarray, labels: np.ndarray) -> float:
    n = X.shape[0]
    uniq = np.unique(labels)
    if len(uniq) < 2:
        return -1.0

    D = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(axis=2))

    s_vals = np.zeros(n, dtype=float)
    for i in range(n):
        ci = labels[i]

        same = np.where(labels == ci)[0]
        if same.size <= 1:
            s_vals[i] = 0.0
            continue

        a = (np.sum(D[i, same]) - 0.0) / (same.size - 1)

        b = np.inf
        for c in uniq:
            if c == ci:
                continue
            other = np.where(labels == c)[0]
            if other.size == 0:
                continue
            b = min(b, float(np.mean(D[i, other])))

        s_vals[i] = (b - a) / max(a, b)

    return float(np.mean(s_vals))


def init_random(X: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    idx = rng.choice(X.shape[0], size=k, replace=False)
    return X[idx].copy()


def init_kmeans_pp(X: np.ndarray, k: int, rng: np.random.Generator) -> np.ndarray:
    n = X.shape[0]
    centroids = np.empty((k, X.shape[1]), dtype=float)

    centroids[0] = X[rng.integers(0, n)]

    d2 = ((X - centroids[0]) ** 2).sum(axis=1)

    for i in range(1, k):
        probs = d2 / np.sum(d2)
        chosen = rng.choice(n, p=probs)
        centroids[i] = X[chosen]
        new_d2 = ((X - centroids[i]) ** 2).sum(axis=1)
        d2 = np.minimum(d2, new_d2)

    return centroids


def kmeans_run(
    X: np.ndarray,
    k: int,
    init: str,
    seed: int,
    max_iters: int = 300,
    tol: float = 1e-6,
) -> tuple[np.ndarray, np.ndarray, int]:
    rng = np.random.default_rng(seed)

    if init == "random":
        centroids = init_random(X, k, rng)
    elif init == "kmeans++":
        centroids = init_kmeans_pp(X, k, rng)
    else:
        raise ValueError("init must be 'random' or 'kmeans++'")

    labels = np.zeros(X.shape[0], dtype=int)

    for it in range(max_iters):
        d2 = ((X[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
        new_labels = np.argmin(d2, axis=1)

        new_centroids = centroids.copy()
        for j in range(k):
            pts = X[new_labels == j]
            if len(pts) == 0:
                new_centroids[j] = X[rng.integers(0, X.shape[0])]
            else:
                new_centroids[j] = np.mean(pts, axis=0)

        shift = float(np.max(np.sqrt(((new_centroids - centroids) ** 2).sum(axis=1))))
        centroids = new_centroids
        labels = new_labels

        if shift < tol:
            return centroids, labels, it + 1

    return centroids, labels, max_iters


def score_solution(X, labels, centroids, metric_id: int) -> float:
    if metric_id == 1:
        return wcss(X, labels, centroids)
    elif metric_id == 2:
        return silhouette_score(X, labels)
    else:
        raise ValueError("metric must be 1 (WCSS) or 2 (Silhouette)")


def better(a: float, b: float, metric_id: int) -> bool:
    if metric_id == 1:     
        return a < b
    elif metric_id == 2:    
        return a > b
    else:
        raise ValueError("metric must be 1 or 2")


def kmeans_random_restart(
    X: np.ndarray,
    k: int,
    metric_id: int,
    n_init: int = 20,
    base_seed: int = 42,
) -> tuple[np.ndarray, np.ndarray, float, int]:
    best_centroids = None
    best_labels = None
    best_score = None
    best_iters = None

    for r in range(n_init):
        seed = base_seed + r * 997  
        centroids, labels, iters = kmeans_run(X, k, init="random", seed=seed)

        sc = score_solution(X, labels, centroids, metric_id)

        if best_score is None or better(sc, best_score, metric_id):
            best_score = sc
            best_centroids = centroids
            best_labels = labels
            best_iters = iters

    return best_centroids, best_labels, float(best_score), int(best_iters)

def save_centroids(path: str, centroids: np.ndarray) -> None:
    np.savetxt(path, centroids, fmt="%.6f")


def save_labels(path: str, labels: np.ndarray) -> None:
    np.savetxt(path, labels.astype(int), fmt="%d")


def plot_clusters(path_png: str, X: np.ndarray, labels: np.ndarray, centroids: np.ndarray, title: str) -> None:
    plt.figure()
    plt.scatter(X[:, 0], X[:, 1], c=labels, s=25)  
    plt.scatter(centroids[:, 0], centroids[:, 1], marker="x", s=150)
    plt.title(title)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.tight_layout()
    plt.savefig(path_png, dpi=160)
    plt.close()

def main():
    print("K-Means clustering")
    print("------------------")
    print("Input format:")
    print("<file> <algorithm> <metric> <k>")
    print("Example: unbalance.txt kmeans 1 8")
    print()

    user_input = input("Enter input: ").strip().split()

    if len(user_input) != 4:
        print("Wrong input format!")
        return

    file_path = user_input[0]
    algorithm = user_input[1].lower()
    metric_id = int(user_input[2])
    k = int(user_input[3])

    X = load_xy(file_path)

    if k <= 0 or k > len(X):
        print("Invalid number of clusters!")
        return

    if algorithm == "kmeans":
        centroids, labels, score, iters = kmeans_random_restart(
            X, k, metric_id=metric_id, n_init=20, base_seed=42
        )
        title = "kmeans with random restart"

    elif algorithm == "kmeans++":
        centroids, labels, iters = kmeans_run(
            X, k, init="kmeans++", seed=42
        )
        score = score_solution(X, labels, centroids, metric_id)
        title = "kmeans++"

    else:
        print("Unknown algorithm!")
        return

    save_centroids("centroids.txt", centroids)
    save_labels("labels.txt", labels)

    out_png = f"clusters_{algorithm}_m{metric_id}_k{k}.png"
    plot_clusters(out_png, X, labels, centroids, title)

    print()
    print("Finished!")
    print("Score:", score)
    print("Centroids saved to centroids.txt")
    print("Labels saved to labels.txt")
    print("Image saved to", out_png)

if __name__ == "__main__":
    main()

