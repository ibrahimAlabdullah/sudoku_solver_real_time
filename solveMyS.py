import math

def is_solved(l):
    for x, i in enumerate(l):
        for y, j in enumerate(i):
            if j == 0:
                # Incomplete
                return None
            for p in range(9):
                if p != x and j == l[p][y]:
                    # Error
                    #print('horizontal issue detected!', (x, y))
                    return False
                if p != y and j == l[x][p]:
                    # Error
                    #print('vertical issue detected!', (x, y))
                    return False
            i_n, j_n = get_box_start_coordinate(x, y)
            for (i, j) in [(i, j) for p in range(i_n, i_n + 3) for q in range(j_n, j_n + 3)
                           if (p, q) != (x, y) and j == l[p][q]]:
                    # Error
                #print('box issue detected!', (x, y))
                return False
    # Solved
    return True


def is_valid(l):
    for x, i in enumerate(l):
        for y, j in enumerate(i):
            if j != 0:
                for p in range(9):
                    if p != x and j == l[p][y]:
                        # Error
                        #print('horizontal issue detected!', (x, y))
                        return False
                    if p != y and j == l[x][p]:
                        # Error
                        #print('vertical issue detected!', (x, y))
                        return False
                i_n, j_n = get_box_start_coordinate(x, y)
                for (i, j) in [(i, j) for p in range(i_n, i_n + 3) for q in range(j_n, j_n + 3)
                               if (p, q) != (x, y) and j == l[p][q]]:
                        # Error
                    #print('box issue detected!', (x, y))
                    return False
    # Solved
    return True


def get_box_start_coordinate(x, y):
    return 3 * int(math.floor(x/3)), 3 * int(math.floor(y/3))


def get_horizontal(x, y, l):
    return [l[x][i] for i in range(9) if l[x][i] > 0]


def get_vertical(x, y, l):
    return [l[i][y] for i in range(9) if l[i][y] > 0]


def get_box(x, y, l):
    existing = []
    i_n, j_n = get_box_start_coordinate(x, y)
    for (i, j) in [(i, j) for i in range(i_n, i_n + 3) for j in range(j_n, j_n + 3)]:
        existing.append(l[i][j]) if l[i][j] > 0 else None
    return existing


def detect_and_simplify_double_pairs(l, pl):
    for (i, j) in [(i, j) for i in range(9) for j in range(9) if len(pl[i][j]) == 2]:
        temp_pair = pl[i][j]
        for p in (p for p in range(j+1, 9) if len(pl[i][p]) == 2 and len(set(pl[i][p]) & set(temp_pair)) == 2):
            for q in (q for q in range(9) if q != j and q != p):
                pl[i][q] = list(set(pl[i][q]) - set(temp_pair))
                if len(pl[i][q]) == 1:
                    l[i][q] = pl[i][q].pop()
                    return True
        for p in (p for p in range(i+1, 9) if len(pl[p][j]) == 2 and len(set(pl[p][j]) & set(temp_pair)) == 2):
            for q in (q for q in range(9) if q != i and p != q):
                pl[q][j] = list(set(pl[q][j]) - set(temp_pair))
                if len(pl[q][j]) == 1:
                    l[q][j] = pl[q][j].pop()
                    return True
        i_n, j_n = get_box_start_coordinate(i, j)
        for (a, b) in [(a, b) for a in range(i_n, i_n+3) for b in range(j_n, j_n+3)
                       if (a, b) != (i, j) and len(pl[a][b]) == 2 and len(set(pl[a][b]) & set(temp_pair)) == 2]:
            for (c, d) in [(c, d) for c in range(i_n, i_n+3) for d in range(j_n, j_n+3)
                           if (c, d) != (a, b) and (c, d) != (i, j)]:
                pl[c][d] = list(set(pl[c][d]) - set(temp_pair))
                if len(pl[c][d]) == 1:
                    l[c][d] = pl[c][d].pop()
                    return True
    return False


def update_unique_horizontal(x, y, l, pl):
    tl = pl[x][y]
    for i in (i for i in range(9) if i != y):
        tl = list(set(tl) - set(pl[x][i]))
    if len(tl) == 1:
        l[x][y] = tl.pop()
        return True
    return False


def update_unique_vertical(x, y, l, pl):
    tl = pl[x][y]
    for i in (i for i in range(9) if i != x):
        tl = list(set(tl) - set(pl[i][y]))
    if len(tl) == 1:
        l[x][y] = tl.pop()
        return True
    return False


def update_unique_box(x, y, l, pl):
    tl = pl[x][y]
    i_n, j_n = get_box_start_coordinate(x, y)
    for (i, j) in [(i, j) for i in range(i_n, i_n+3) for j in range(j_n, j_n+3) if (i, j) != (x, y)]:
        tl = list(set(tl) - set(pl[i][j]))
    if len(tl) == 1:
        l[x][y] = tl.pop()
        return True
    return False


def find_and_place_possibles(l):
    while True:
        pl = populate_possibles(l)
        if pl != False:
            return pl


def populate_possibles(l):
    pl = [[[]for j in i] for i in l]
    for (i, j) in [(i, j) for i in range(9) for j in range(9) if l[i][j] == 0]:
        p = list(set(range(1, 10)) - set(get_horizontal(i, j, l) + get_vertical(i, j, l) + get_box(i, j, l)))
        if len(p) == 1:
            l[i][j] = p.pop()
            return False
        else:
            pl[i][j] = p
    return pl


def find_and_remove_uniques(l, pl):
    for (i, j) in [(i, j) for i in range(9) for j in range(9) if l[i][j] == 0]:
        if update_unique_horizontal(i, j, l, pl) == True:
            return True
        if update_unique_vertical(i, j, l, pl) == True:
            return True
        if update_unique_box(i, j, l, pl) == True:
            return True
    return False


def try_with_possibilities(l):
    while True:
        improv = False
        pl = find_and_place_possibles(l)
        if detect_and_simplify_double_pairs(l, pl) == True:
            continue
        if find_and_remove_uniques(l, pl) == True:
            continue
        if improv == False:
            break
    return pl


def get_first_conflict(pl):
    for (x, y) in [(x, y) for x, i in enumerate(pl) for y, j in enumerate(i) if len(j) > 0]:
        return (x, y)


def get_deep_copy(l):
    new_list = [i[:] for i in l]
    return new_list


def run_assumption(l, pl):
    try:
        c = get_first_conflict(pl)
        fl = pl[c[0]][c[1]]
        # print('Assumption Index : ', c)
        # print('Assumption List: ',  fl)
    except:
        return False
    for i in fl:
        new_list = get_deep_copy(l)
        new_list[c[0]][c[1]] = i
        new_pl = try_with_possibilities(new_list)
        is_done = is_solved(new_list)
        if is_done == True:
            l = new_list
            return new_list
        else:
            new_list = run_assumption(new_list, new_pl)
            if new_list != False and is_solved(new_list) == True:
                return new_list
    return False
