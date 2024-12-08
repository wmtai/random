import sympy as sp
import copy
import numpy as np
import time


def amgm(expr):
    def enum_comb(local_rtn, cur, empty_idx, item):

        if empty_idx > item: return
        if item == -1:
            local_rtn.append(cur)
            return

        b = len(cur)
        start = max(empty_idx, 0)
        for i in range(start, b):
            new_cur = copy.deepcopy(cur)
            new_cur[i].append(item)
            new_idx = empty_idx - int(i == empty_idx)
            enum_comb(local_rtn, new_cur, new_idx, item - 1)

    def am_to_from_gm(terms, to_from):

        if to_from != sp.Add and to_from != sp.Mul: return None

        op_map = {sp.Add: 0,
                  sp.Mul: 1}

        rtn = []
        n = len(terms)
        for num_b in range(3, n + 2):
            all_comb = []
            cur = [[] for _ in range(num_b)]
            enum_comb(all_comb, cur, num_b - 2, n - 1)
            for comb in all_comb:
                new_args = []
                for b in range(num_b - 1):
                    single_term = op_map[to_from]
                    for i in comb[b]: single_term = to_from(*[single_term, terms[i]])
                    new_args.append(single_term)
                m = len(new_args)
                if to_from == sp.Add:
                    new_expr = m * sp.Pow(sp.Mul(*new_args), sp.Rational(1, m))
                    for i in comb[-1]: new_expr = to_from(*[new_expr, terms[i]])
                    rtn.append(new_expr)
                else:
                    new_expr = sp.Pow(sp.Rational(1, m) * sp.Add(*new_args), m)
                    for i in comb[-1]: new_expr = to_from(*[new_expr, terms[i]])
                    rtn.append(new_expr)
                    new_expr = sp.Rational(1, m) * sp.Add(*[sp.Pow(new_args[i], m) for i in range(m)])
                    for i in comb[-1]: new_expr = to_from(*[new_expr, terms[i]])
                    rtn.append(new_expr)

        return rtn

    def amgm_expr(expr, label):
        # print(expr,label)

        def f(term):
            if term.is_positive: return 1
            elif term.is_negative: return -1
            return 0

        if label == 0: return []
        t = type(expr)


        if t == sp.Add:
            rtn = []
            children = expr.args
            n = len(children)
            children_expr = dict()
            for i in range(n):
                child = children[i]
                children_expr[i] = amgm_expr(child, label)
            for i in range(n):
                m = len(children_expr[i])
                for j in range(m):
                    new_expr = children_expr[i][j]
                    for k in range(n):
                        if k == i: continue
                        new_expr += children[k]
                    rtn.append(new_expr)
            to_apply = []
            not_to_apply = []
            for i in range(n):
                child = children[i]
                if label == f(child):
                    to_apply.append(label * child)
                else:
                    not_to_apply.append(child)
            gm = am_to_from_gm(to_apply, sp.Add)
            for x in gm:
                temp = label * x
                rtn.append(sp.Add(*(not_to_apply + [temp])))

            # print(expr, rtn)
            return rtn


        if t == sp.Pow:
            power = expr.args[1]
            new_expr = expr.args[0]
            if power.is_positive:
                return [sp.Pow(x, power) for x in amgm_expr(new_expr, label)]
            elif power.is_negative:
                return [sp.Pow(x, power) for x in amgm_expr(new_expr, -label)]
            return []


        rtn = []
        prod = sp.fraction(expr)
        if type(prod[1])==sp.Mul and f(prod[0])*label==1:
            numer = amgm_expr(prod[1], -1)
            rtn += [prod[0] / y for y in numer ]
            # print(expr, rtn, numer)


        if t == sp.Mul:

            children = expr.args
            n = len(children)
            left_pos_neg = dict()
            right_pos_neg = dict()

            left_pos_neg[-1] = 1
            left_pos_neg[n] = 1
            right_pos_neg[-1] = 1
            right_pos_neg[n] = 1
            for i in range(n):left_pos_neg[i] = left_pos_neg[i - 1] * f(children[i])
            for i in range(n - 1, -1, -1): right_pos_neg[i] = right_pos_neg[i + 1] * f(children[i])
            children_expr = dict()
            for i in range(n):
                term_pos_neg = left_pos_neg[i - 1] * right_pos_neg[i + 1]
                children_expr[i] = amgm_expr(children[i], term_pos_neg * label)

            for i in range(n):
                m = len(children_expr[i])
                for j in range(m):
                    new_expr = children_expr[i][j]
                    for k in range(n):
                        if k == i: continue
                        new_expr *= children[k]
                    rtn.append(new_expr)
            # print(expr,rtn)
            pos_terms = [x for x in expr.args if f(x)==1]
            neg_terms = [x for x in expr.args if f(x)==-1]
            if (expr.is_positive and label == -1) or (expr.is_negative and label==1):
                rtn += [sp.Mul(*(neg_terms + [x])) for x in am_to_from_gm(pos_terms, sp.Mul)]
            # if expr.is_negative and label == 1:
            #     rtn += [sp.Mul(*(neg_terms + [x])) for x in am_to_from_gm(pos_terms, sp.Mul)]

            return list(set(rtn))

        return []

    t = type(expr)
    label=1
    if t==sp.Lt or t==sp.Le: label=1
    elif t==sp.Ge or t==sp.Gt: label=-1
    else: return [expr]

    left = expr.args[0]
    right = expr.args[1]
    rtn_left = [[l,right,t] for l in amgm_expr(left,label)]
    rtn_right = [[left,r,t] for r in amgm_expr(right,-label)]

    return rtn_left + rtn_right + [[left,right,t]]

    # terms=expr.args
    # print(am_to_from_gm(terms,type(expr)))
    # x, y, z, w = sp.symbols('x y z w', positive=True)
    # expr = (1 / (x + y)) * (1 / (x + z)) - x / (y + z)

    # print(sp.fraction(x**(-3)))
    # for x in amgm_expr(expr, 1): print(x)


# Define symbolic variables
x, y, z, w = sp.symbols('x y z w', positive=True)
expr = 1 < 1/(1+1/((x+y)*(z+w)))
# print(sp.fraction(expr.args[0])[1].args)
# amgm(expr)
for x in amgm(expr): print(x)

# print(sp.fraction(-1/(x+y)))