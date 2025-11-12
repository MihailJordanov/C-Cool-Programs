#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <iomanip>



struct Point
{
    std::string name;
    double x;
    double y;
};

#include <vector>
#include <algorithm>
#include <random>

std::vector<int> generateRandomPermutation(int n) {
    std::vector<int> perm(n);
    for (int i = 0; i < n; ++i)
        perm[i] = i;

    static std::random_device rd;
    static std::mt19937 gen(rd());

    std::shuffle(perm.begin(), perm.end(), gen);
    return perm;
}

void printArray(std::vector<int> arr)
{
    int n = arr.size();
    for (int i = 0; i < n; ++i)
        std::cout << arr[i] << ' ';
    std::cout << " - ";
}


double euclid(const Point& a, const Point& b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    return sqrt(dx * dx + dy * dy);
}

void makeAllEdges(const std::vector<Point>& points, std::vector<std::vector<double>>& dist, int n)
{
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            double d = euclid(points[i], points[j]);
            dist[i][j] = d;
            dist[j][i] = d;
        }
    }
}

double findPath(const std::vector<std::vector<double>>& dist, const std::vector<int>& pop, int n)
{
    double path = 0;
    for (int i = 0; i < n - 1; ++i)
        path += dist[pop[i]][pop[i + 1]];
    return path;
}

std::vector<double> computeFitnessScaled(const std::vector<double>& paths) {
    const double eps = 1e-9;
    double mx = *std::max_element(paths.begin(), paths.end());
    std::vector<double> fit(paths.size());
    for (size_t i = 0; i < paths.size(); ++i)
        fit[i] = (mx - paths[i]) + eps; 
    return fit;
}

static std::mt19937& rng() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    return gen;
}


int selectTournament(const std::vector<double>& paths, int k = 3) {
    std::uniform_int_distribution<int> uni(0, (int)paths.size() - 1);
    int best = uni(rng());
    for (int i = 1; i < k; ++i) {
        int cand = uni(rng());
        if (paths[cand] < paths[best]) best = cand;
    }
    return best;
}

std::vector<int> orderCrossover(const std::vector<int>& p1, const std::vector<int>& p2) {
    int n = p1.size();
    std::vector<int> child(n, -1);
    std::uniform_int_distribution<int> cut(0, n - 1);
    int a = cut(rng()), b = cut(rng());
    if (a > b) std::swap(a, b);

    for (int i = a; i <= b; ++i)
        child[i] = p1[i];

    int pos = (b + 1) % n;
    for (int i = 0; i < n; ++i) {
        int candidate = p2[(b + 1 + i) % n];
        if (std::find(child.begin(), child.end(), candidate) == child.end()) {
            child[pos] = candidate;
            pos = (pos + 1) % n;
        }
    }
    return child;
}

void mutate(std::vector<int>& route, double prob = 0.05) {
    std::uniform_real_distribution<double> chance(0.0, 1.0);
    if (chance(rng()) < prob) {
        std::uniform_int_distribution<int> pick(0, route.size() - 1);
        int i = pick(rng());
        int j = pick(rng());
        std::swap(route[i], route[j]);
    }
}

void printPointsNames(std::vector<int>& arr, std::vector<Point>& points, int n)
{
    for (int i = 0; i < n; ++i)
    {
        std::cout << points[arr[i]].name;
        if (i != n-1)
            std::cout << " -> ";
    }
    std::cout << '\n';
}

void geneticAlgorithm(const std::vector<std::vector<double>>& dist, std::vector<Point>& points, int n)
{
    int population_max = std::max(80, std::min(4 * n, 300));
    int generations = 100;

    // initialisation population
    std::vector<std::vector<int>> population(population_max);
    for (int i = 0; i < population_max; ++i)
        population[i] = generateRandomPermutation(n);

    std::vector<double> paths(population_max);

    for (int gen = 0; gen < generations; ++gen)
    {
        // find paths
        for (int i = 0; i < population_max; ++i)
            paths[i] = findPath(dist, population[i], n);

        // find best
        int elite_idx = (int)std::distance(paths.begin(),
            std::min_element(paths.begin(), paths.end()));
        auto elite = population[elite_idx];
        double bestLen = paths[elite_idx];

        // fitness
        auto fitness = computeFitnessScaled(paths);

        // new population
        std::vector<std::vector<int>> next_pop;
        next_pop.reserve(population_max);

        // save best
        next_pop.push_back(elite);

        // Selection
        while ((int)next_pop.size() < population_max)
        {
            int p1 = selectTournament(paths, 3);
            int p2 = selectTournament(paths, 3);
            while (p2 == p1)
                p2 = selectTournament(paths, 3);

            // Cross-over
            auto child1 = orderCrossover(population[p1], population[p2]);
            auto child2 = orderCrossover(population[p2], population[p1]);

            // Mutation
            mutate(child1, 0.05);
            mutate(child2, 0.05);

            next_pop.push_back(child1);
            if ((int)next_pop.size() < population_max)
                next_pop.push_back(child2);
        }

        population.swap(next_pop);

        // print best 
        if (gen == 0 || gen == generations - 1 || gen % (generations / 10) == 0) {
            //std::cout << std::fixed << std::setprecision(4)
            //    << "Generation " << gen << " | Best path length: " << bestLen << "\n";
            std::cout << bestLen << '\n';
        }
    }

    for (int i = 0; i < population_max; ++i)
        paths[i] = findPath(dist, population[i], n);

    int best_idx = (int)std::distance(paths.begin(),
        std::min_element(paths.begin(), paths.end()));

    std::cout << "\nBest route found:\n";
    printPointsNames(population[best_idx], points, n);
    std::cout << "\nLength: " << std::fixed << std::setprecision(4);
    std::cout << paths[best_idx] << "\n";

}

int main()
{
    std::string dataset;
    int n = 0;
    std::cin >> dataset;
    std::cin >> n;

    std::vector<Point> points(n);
    std::vector<std::vector<double>> dist(n, std::vector<double>(n, 0.0));


    for (int i = 0; i < n; ++i) {
        std::cin >> points[i].name >> points[i].x >> points[i].y;  
    }


    makeAllEdges(points, dist, n);

    //std::cout << std::fixed << std::setprecision(3);
    //for (int i = 0; i < n; ++i) {
    //    for (int j = 0; j < n; ++j)
    //        std::cout << dist[i][j] << " ";
    //    std::cout << "\n";
    //}

    geneticAlgorithm(dist, points, n);
}
    