#include <iostream>
#include <vector>
#include <cstdlib> 
#include <ctime>    


const int MAX_N = 51;

void generate_board(int n, std::vector<int>& board)
{
    for (int row = 0; row < n; ++row)
        board[row] = std::rand() % n;
}


bool check_is_possible(int n)
{
    if (n == 2 || n == 3)
    {
        std::cout << "Not possible with n = " << n << '\n';
        return false;
    }
    return true;
}


void print_pos(const std::vector<int>& board)
{
    
    for (int i = 0; i < board.size(); ++i)
    {
        std::cout << board[i] << " ";
    }
    std::cout << '\n';
}

void print_board(const std::vector<int>& board) 
{
    int n = board.size();
    if (n >= MAX_N)
    {
        std::cout << "Board too large to display (" << n << "x" << n << ")\n";
        return;
    }

    for (int row = 0; row < n; ++row) {
        for (int col = 0; col < n; ++col)
        {
            if (board[col] == row)
                std::cout << "* ";
            else
                std::cout << "_ ";
        }
        std::cout << "\n";
    }
}

bool check_diagonal(const std::vector<int>& board)
{
    int n = board.size();
    for (int i = 0; i < n - 1; ++i)
    {
        for (int j = i + 1; j < n; ++j)
        {
            int row_diff = std::abs(i - j);
            int col_diff = std::abs(board[i] - board[j]);
            if (row_diff == col_diff)
                return false;
        }
    }
    return true; 
}

bool check_col(const std::vector<int>& board)
{
    int n = board.size();
    for (int i = 0; i < n - 1; ++i)
    {
        for (int j = i + 1; j < n; ++j)
        {
            if (board[i] == board[j])
                return false;
        }
    }
    return true;
}

int conflicts_for(const std::vector<int>& board, int row, int col) {
    int n = board.size();
    int conflicts = 0;

    for (int r = 0; r < n; ++r)
    {
        if (r == row)
            continue;

        int c = board[r];

        if (c == col)
        { 
            conflicts++;
            continue;
        }

        if (std::abs(r - row) == std::abs(c - col))
            conflicts++;
    }
    return conflicts;
}


static inline void collect_conflicted_rows(const std::vector<int>& board, std::vector<int>& out_rows)
{
    out_rows.clear();
    int n = board.size();

    for (int row = 0; row < n; ++row)
    {
        if (conflicts_for(board, row, board[row]) > 0)
            out_rows.push_back(row);
    }
}


int pick_best_col_random_tiebreak(const std::vector<int>& costs) {
    int n = costs.size();
    int best = costs[0];
    for (int c = 1; c < n; ++c) 
        best = std::min(best, costs[c]);

    std::vector<int> bucket;
    for (int c = 0; c < n; ++c)
        if (costs[c] == best) bucket.push_back(c);

    int idx = std::rand() % (int)bucket.size();
    return bucket[idx];
}


bool min_conflicts(std::vector<int>& board, int max_steps = 50000) {
    int n = board.size();
    if (n == 0)
        return true;

    std::vector<int> conflicted_rows;
    conflicted_rows.reserve(n);

    for (int step = 0; step < max_steps; ++step) {

        collect_conflicted_rows(board, conflicted_rows);
        if (conflicted_rows.empty()) return true;


        int row = conflicted_rows[std::rand() % (int)conflicted_rows.size()];


        std::vector<int> costs(n);
        for (int col = 0; col < n; ++col)
            costs[col] = conflicts_for(board, row, col);

        int best_col = pick_best_col_random_tiebreak(costs);

  
        board[row] = best_col;
    }

    return false; 
}


void print_final(std::vector<int>& board)
{
    int n = board.size();
    if (!check_is_possible(n))
        return;
    generate_board(n, board);
    std::cout << "\nFirst Positions:\n";
    print_pos(board);
    std::cout << "\nFirst board:\n";
    print_board(board);
    min_conflicts(board);
    std::cout << "\n\n\nFinal Positions (After Min-Conflicts):\n";
    print_board(board);
    std::cout << "\nFinal board(After Min-Conflicts):\n";
    print_pos(board);
}

int main()
{
    int n = 0;
    std::cin >> n;
    std::vector<int> board(n);
    print_final(board);
}


