#include <iostream>
#include <string.h>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <queue>



void generateString(std::string& str, int n)
{
    str = "";
    for (int i = 0; i < n; ++i)
        str += 'L';

    str += '_';
    for (int i = 0; i < n; ++i)
        str += 'R';
}

void generateGoalString(std::string& str, int n)
{
    str = "";
    for (int i = 0; i < n; ++i)
        str += 'R';

    str += '_';
    for (int i = 0; i < n; ++i)
        str += 'L';
}


std::vector<std::string> bfs(std::unordered_map<std::string, std::vector<std::string>>& adj, std::string start_str, std::string goal_str)
{
    int n = adj.size();

    std::vector<std::string> res;
    std::queue<std::string> q;
    std::unordered_set<std::string> visited;
    std::unordered_map<std::string, std::string> parent;
    std::string str = start_str;

    visited.insert(str);
    q.push(str);

    while (!q.empty())
    {
        std::string cur = q.front();
        q.pop();
        res.push_back(cur);

        if (cur == goal_str)
        {
            res.clear();
            for (std::string x = goal_str;; x = parent[x])
            {
                res.push_back(x);
                if (x == start_str)
                    break;
            }
            std::reverse(res.begin(), res.end());
            return res;
        }

        auto it = adj.find(cur);
        if (it == adj.end()) continue;

        for (const std::string& x : it->second)
        {
            if (!visited.count(x))
            {
                visited.insert(x);
                parent[x] = cur;
                q.push(x);
            }
        }
    }

    return res;
}




void addEdges(std::unordered_map<std::string, std::vector<std::string>>& adj, std::string& str, std::unordered_set<std::string>& visited)
{
    if (visited.count(str)) return;
    visited.insert(str);

    std::string temp = str;
    // Left move
    for (int i = 0; i < str.size() - 1; ++i)
    {
        temp = str;
        if (str[i] == 'L' && str[i + 1] == '_')
        {
            temp[i] = '_';
            temp[i + 1] = 'L';
            adj[str].push_back(temp);
            //std::cout << str << " -> " << temp << '\n';
            addEdges(adj, temp, visited);
        }

        temp = str;
        if(i < (str.size() - 2) && str[i] == 'L' && str[i + 1] == 'R' && str[i + 2] == '_')
        {
            temp[i] = '_';
            temp[i + 2] = 'L';
            adj[str].push_back(temp);
            //std::cout << str << " -> " << temp << '\n';
            addEdges(adj, temp, visited);
        }
    }

 
    // Right move
    for (int i = 0; i < str.size() - 1; ++i)
    {
        temp = str;
        if (str[i] == '_' && str[i + 1] == 'R')
        {
            temp[i] = 'R';
            temp[i + 1] = '_';
            adj[str].push_back(temp);
            //std::cout << str << " -> " << temp << '\n';
            addEdges(adj, temp, visited);
        }

        temp = str;
        if (i < (str.size() - 2) && str[i] == '_' && str[i + 1] == 'L' && str[i + 2] == 'R')
        {
            temp[i] = 'R';
            temp[i + 2] = '_';
            adj[str].push_back(temp);
            //std::cout << str << " -> " << temp << '\n';
            addEdges(adj, temp, visited);
        }
    }
}


int main()
{
    std::cout << "Enter Number! How many frongs on one side?\n";
    int n = 0;
    std::cin >> n;
    std::string str;
    std::cout << "Starting Brindge:\n";
    generateString(str, n);
    std::cout << str << '\n';

    std::unordered_map<std::string, std::vector<std::string>> adj;
    std::unordered_set<std::string> visited;

    addEdges(adj, str, visited);

    std::string goal_str;
    generateGoalString(goal_str, n);

    std::vector<std::string> ans = bfs(adj, str, goal_str);

    for (std::string s : ans)
        std::cout << s << " ";
    std::cout << '\n';
}
