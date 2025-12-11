#include <iostream>
#include <vector>
#include <string>
#include <math.h>

char player = 'X', opponent = 'O';

struct Table
{
    std::vector<std::vector<char>> arr{ {0,0,0}, {0,0,0}, {0,0,0} };

    void setOnPos(char c, int row, int cow)
    {
        if (c != 'X' && c != 'O')
        {
            std::cout << "Not correct input charater!\n";
            return;
        }
        if ((row > 3 || row < 1) || (cow > 3 || cow < 1))
        {
            std::cout << "Not correct positions to play on\n!";
            return;
        }

        int row_i = row - 1;
        int cow_i = cow - 1;

        if (arr[row_i][cow_i] != 0)
        {
            std::cout << "This position is already filled!\n";
            return;
        }

        arr[row_i][cow_i] = c;
    }

    char isWin() const
    {
        for (int r = 0; r < 3; r++)
            if (arr[r][0] != 0 && arr[r][0] == arr[r][1] && arr[r][1] == arr[r][2])
                return arr[r][0];

        for (int c = 0; c < 3; c++)
            if (arr[0][c] != 0 && arr[0][c] == arr[1][c] && arr[1][c] == arr[2][c])
                return arr[0][c];

        if (arr[0][0] != 0 && arr[0][0] == arr[1][1] && arr[1][1] == arr[2][2])
            return arr[0][0];

        if (arr[0][2] != 0 && arr[0][2] == arr[1][1] && arr[1][1] == arr[2][0])
            return arr[0][2];

        return 0;
    }

    int evaluate() const
    {
        char winner = isWin();

        if (winner == opponent)
            return 10;   
        if (winner == player)
            return -10;   

        return 0;  
    }

    bool isMoveLeft() const
    {
        for (int i = 0; i < 3; i++)
            for (int j = 0; j < 3; j++)
                if (arr[i][j] == 0)
                    return true;
        return false;
    }

    void printTable() const
    {
        for (int r = 0; r < 3; r++)
        {
            std::cout << "+---+---+---+\n";
            std::cout << "|";

            for (int c = 0; c < 3; c++)
            {
                char ch = arr[r][c];
                if (ch == 0) ch = '_';

                std::cout << " " << ch << " |";
            }

            std::cout << "\n";
        }
        std::cout << "+---+---+---+\n";
    }

};

struct Move
{
    int row = 0;
    int cow = 0;
};

int minMax(Table& t, int depth, bool isMax, int alpha, int beta)
{
    int score = t.evaluate();

    if (score == 10)       
        return score - depth;  
    if (score == -10)    
        return score + depth;

    if (!t.isMoveLeft())
        return 0;

    if (isMax)
    {
        int best = INT_MIN;

        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                if (t.arr[i][j] == 0)
                {
                    t.arr[i][j] = opponent;

                    int val = minMax(t, depth + 1, false, alpha, beta);
                    best = std::max(best, val);

                    t.arr[i][j] = 0;

                    alpha = std::max(alpha, best);
                    if (beta <= alpha)
                        return best;
                }
            }
        }

        return best;
    }
    else
    {
        int best = INT_MAX;

        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                if (t.arr[i][j] == 0)
                {
                    t.arr[i][j] = player;

                    int val = minMax(t, depth + 1, true, alpha, beta);
                    best = std::min(best, val);

                    t.arr[i][j] = 0;

                    beta = std::min(beta, best);
                    if (beta <= alpha)
                        return best;
                }
            }
        }

        return best;
    }
}

Move findBestMove(Table& t)
{
    int bestVal = -1000;
    Move bestMove;
    bestMove.row = -1;
    bestMove.cow = -1;


    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            if (t.arr[i][j] == 0)
            {
                t.arr[i][j] = opponent;

                int moveVal = minMax(t, 0, false, INT_MIN, INT_MAX);

                t.arr[i][j] = 0;

                if (moveVal > bestVal)
                {
                    bestMove.row = i;
                    bestMove.cow = j;
                    bestVal = moveVal;
                }
            }
        }
    }

    return bestMove;
}

void AIplay(Table& t)
{
    if (!t.isMoveLeft() || t.isWin())
        return; 

    Move bestMove = findBestMove(t);

    if (bestMove.row == -1 || bestMove.cow == -1)
        return; 

    t.arr[bestMove.row][bestMove.cow] = opponent;
    std::cout << "AI plays...\n";
    t.printTable();
}

void printGameResult(const Table& t)
{
    char winner = t.isWin();

    if (winner)
        std::cout << "WINNER: " << winner << '\n';
    else
        std::cout << "DRAW\n";

}

void game()
{
    std::string first;
    std::string human;
    char firstC = 0;
    char humanC = 0;

    std::cin >> first >> firstC;
    std::cin >> human >> humanC;

    if (firstC != 'X' && firstC != 'O')
    {
        std::cout << "Not correct input First!\n";
        return;
    }

    if (humanC != 'X' && humanC != 'O')
    {
        std::cout << "Not correct input Human!\n";
        return;
    }

    player = humanC;
    opponent = (player == 'X' ? 'O' : 'X');

    int row = 0, col = 0;
    Table t;

    if (player == firstC)
    {
        std::cout << "Enter Row and Col: ";
        std::cin >> row >> col;
        t.setOnPos(player, row, col);
        t.printTable();
    }

    AIplay(t);

    while (true)
    {
        if (t.isWin() || !t.isMoveLeft())
        {
            printGameResult(t);
            break;
        }

        std::cout << "Enter Row and Col: ";
        std::cin >> row >> col;
        t.setOnPos(player, row, col);
        t.printTable();

        if (t.isWin() || !t.isMoveLeft())
        {
            printGameResult(t);
            break;
        }

        AIplay(t);

        if (t.isWin() || !t.isMoveLeft())
        {
            printGameResult(t);
            break;
        }
    }
}

void judge()
{
    std::string turnWord;
    char turnC;

    std::cin >> turnWord >> turnC;
    if (turnWord != "TURN" || (turnC != 'X' && turnC != 'O'))
    {
        std::cout << "-1\n"; 
        return;
    }

    opponent = turnC;                     
    player = (turnC == 'X' ? 'O' : 'X'); 

    Table t;

    std::string line;
    std::getline(std::cin, line); 


    for (int r = 0; r < 3; ++r)
    {
        std::getline(std::cin, line);


        std::getline(std::cin, line);

        auto getCell = [](char ch) -> char
        {
            return (ch == '_' ? 0 : ch);
        };

        t.arr[r][0] = getCell(line[2]);
        t.arr[r][1] = getCell(line[6]);
        t.arr[r][2] = getCell(line[10]);
    }


    std::getline(std::cin, line);


    if (t.isWin() || !t.isMoveLeft())
    {
        std::cout << -1 << '\n';
        return;
    }


    Move bestMove = findBestMove(t);

    if (bestMove.row == -1 || bestMove.cow == -1)
    {
        std::cout << -1 << '\n';
        return;
    }

    std::cout << (bestMove.row + 1) << " " << (bestMove.cow + 1) << '\n';
}


int main()
{
    std::string mode;
    std::cin >> mode;
    if (mode == "GAME")
    {
        game();
    }
    else if (mode == "JUDGE")
    {
        judge();
    }
    else
    {
        std::cout << "Not correct game mode\n!";
        return -1; 
    }
}
