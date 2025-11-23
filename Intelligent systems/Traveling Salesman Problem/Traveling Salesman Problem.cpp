#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <iomanip>
#include <algorithm>
#include <random>
#include <chrono>


struct Point
{
    std::string name;
    double x;
    double y;
};


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



static std::mt19937& rng() {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    return gen;
}


int selectTournamentPaths(const std::vector<double>& paths, int k = 3) {
    if (paths.empty()) return 0;

    std::uniform_int_distribution<int> uni(0, (int)paths.size() - 1);


    int best = uni(rng());

    for (int i = 1; i < k; ++i) {
        int cand = uni(rng());
        if (paths[cand] < paths[best])  
            best = cand;
    }

    return best;
}


void mutateReverse(std::vector<int>& route, double prob = 0.05) {
    int n = route.size();
    if (n < 4) return;

    std::uniform_real_distribution<double> chance(0.0, 1.0);
    if (chance(rng()) < prob) {

        std::uniform_int_distribution<int> pick(0, n - 1);

        int i = pick(rng());
        int j = pick(rng());

        if (i > j) std::swap(i, j);

        if (j - i < 2) return;

        std::reverse(route.begin() + i, route.begin() + j + 1);
    }
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


void printPointsNames(std::vector<int>& arr, std::vector<Point>& points, int n)
{
    for (int i = 0; i < n; ++i)
    {
        std::cout << points[arr[i]].name;
        if (i != n - 1)
            std::cout << " -> ";
    }
    std::cout << '\n';
}

void geneticAlgorithm(const std::vector<std::vector<double>>& dist, std::vector<Point>& points, int n)
{
    int population_max = 700;
    int generations = 500;

    // initialisation population
    std::vector<std::vector<int>> population(population_max);
    for (int i = 0; i < population_max; ++i)
        population[i] = generateRandomPermutation(n);

    std::vector<double> paths(population_max);

    // --- adaptive mutation ---
    double mutationProb = 0.05;                 
    double globalBestLen = std::numeric_limits<double>::infinity();
    int generationsSinceImprovement = 0;
    const double eps = 1e-9;

    for (int gen = 0; gen < generations; ++gen)
    {
        // 1) find paths
        for (int i = 0; i < population_max; ++i)
            paths[i] = findPath(dist, population[i], n);

        // 2) find best
        int elite_idx = (int)std::distance(paths.begin(), std::min_element(paths.begin(), paths.end()));
        auto elite = population[elite_idx];
        double bestLen = paths[elite_idx];

        // update global for mutatae up prob
        if (bestLen + eps < globalBestLen) {
            globalBestLen = bestLen;
            generationsSinceImprovement = 0;   
        }
        else {
            generationsSinceImprovement++;
        }


        // new population
        std::vector<std::vector<int>> next_pop;
        next_pop.reserve(population_max);

        // save best 
        next_pop.push_back(elite);

        // Selection + crossover + mutation
        while ((int)next_pop.size() < population_max)
        {
            int p1 = selectTournamentPaths(paths, 4);
            int p2 = selectTournamentPaths(paths, 4);
            while (p2 == p1)
                p2 = selectTournamentPaths(paths, 4);

            // ==== MAKE 4 CHILDREN ====
            auto child1 = orderCrossover(population[p1], population[p2]);
            auto child2 = orderCrossover(population[p2], population[p1]);
            auto child3 = orderCrossover(population[p1], population[p2]);
            auto child4 = orderCrossover(population[p2], population[p1]);

            // ==== MUTATION (reverse) ====
            mutateReverse(child1, mutationProb);
            mutateReverse(child2, mutationProb);
            mutateReverse(child3, mutationProb);
            mutateReverse(child4, mutationProb);

            // ==== ADD TO NEXT POPULATION ====
            next_pop.push_back(child1);
            if ((int)next_pop.size() < population_max) next_pop.push_back(child2);
            if ((int)next_pop.size() < population_max) next_pop.push_back(child3);
            if ((int)next_pop.size() < population_max) next_pop.push_back(child4);
        }

        population.swap(next_pop);

        // print best 
        if (gen == 0 || gen == generations - 1 || gen % (generations / 10) == 0) {
            std::cout << std::fixed << std::setprecision(15)
                << bestLen << '\n';
        }

        if (gen > 0 && gen % 10 == 0 && generationsSinceImprovement >= 10) {
            mutationProb += 0.05;                 
            if (mutationProb > 0.95) mutationProb = 0.95;  
        }
    }


    for (int i = 0; i < population_max; ++i)
        paths[i] = findPath(dist, population[i], n);

    int best_idx = (int)std::distance(
        paths.begin(),
        std::min_element(paths.begin(), paths.end())
    );

    std::cout << std::fixed << std::setprecision(15);
    printPointsNames(population[best_idx], points, n);
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


    for (int i = 0; i < n; ++i)
        std::cin >> points[i].name >> points[i].x >> points[i].y;

    makeAllEdges(points, dist, n);
    geneticAlgorithm(dist, points, n);
}
