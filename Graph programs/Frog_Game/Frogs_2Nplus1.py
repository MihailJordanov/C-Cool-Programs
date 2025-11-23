from typing import List, Tuple, Dict, Optional

def generate_start(n: int) -> str:
    return ">" * n + "_" + "<" * n

def generate_goal(n: int) -> str:
    return "<" * n + "_" + ">" * n


def no_inner_pair(s_after: List[str], pos: int, ch: str) -> bool:
    m = len(s_after)
    if ch == '>':
        if pos + 1 < m and s_after[pos + 1] == '>':
            return all(c == '>' for c in s_after[pos + 1:])
    elif ch == '<':
        if pos - 1 >= 0 and s_after[pos - 1] == '<':
            return all(c == '<' for c in s_after[:pos])
    return True

def neighbors_with_hole(state: str, index: int) -> List[Tuple[str, int]]:
    s = list(state)
    m = len(s)
    out: List[Tuple[str, int]] = []

    if index >= 1 and s[index-1] == '>':
        t = s.copy()
        t[index], t[index-1] = t[index-1], t[index]
        if no_inner_pair(t, index, '>'):
            out.append(("".join(t), index - 1))

    if index >= 2 and s[index-2] == '>' and s[index-1] == '<':
        t = s.copy()
        t[index], t[index-2] = t[index-2], t[index]

        if no_inner_pair(t, index, '>'):
            out.append(("".join(t), index - 2))

    if index + 2 < m and s[index+1] == '>' and s[index+2] == '<':
        t = s.copy()
        t[index], t[index+2] = t[index+2], t[index]
        if no_inner_pair(t, index, '<'):
            out.append(("".join(t), index + 2))

    if index + 1 < m and s[index+1] == '<':
        t = s.copy()
        t[index], t[index+1] = t[index+1], t[index]
        if no_inner_pair(t, index, '<'):
            out.append(("".join(t), index + 1))

    return out


def dfs_path_simple_hole(start: str, goal: str, _ind : int) -> List[str]:
    if start == goal:
        return [start]

    index = _ind               
    stack: List[Tuple[str, int]] = [(start, index)]
    parent: Dict[str, Optional[str]] = {start: None}
    visited = {start}

    while stack:
        cur, hole_index = stack.pop()
        if cur == goal:
            path: List[str] = []
            x: Optional[str] = cur
            while x is not None:
                path.append(x)
                x = parent[x]
            path.reverse()
            return path

        for nxt, hole_ind in neighbors_with_hole(cur, hole_index):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = cur
                stack.append((nxt, hole_ind))

    return []

def main():
    n = int(input().strip())
    start = generate_start(n)
    goal = generate_goal(n)
    path = dfs_path_simple_hole(start, goal, n)
    for state in path:
        print(state)

if __name__ == "__main__":
    main()
