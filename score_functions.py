def noise_score(n0, n1, n2, n3):
    ntot = n0 + n1 + n2 + n3
    score = 10

    if n1/ntot > 0.5:
        score = score - 2
        if n1/ntot > 0.6:
            score = score - 1
    
    if n2/ntot > 0.2:
        score = score - 2
        if n2/ntot > 0.4:
            score = score -2
    
    if n3 > 2:
        score = score - 2
        if n3 > 4:
            score = score -2

    if score < 0:
        score = 0
    
    return score


def temp_hum_score(temp, hum):

    t1 = 17 - 0.1*hum
    t2 = 23 - 0.4*hum
    t3 = 26 - 0.5*hum
    t4 = 31 - 0.5*hum
    score = 2

    if temp <= t4:
        score = score - 1
        if temp <= t3:
            score = score - 1
            if temp <= t2:
                score = score - 1
                if temp <= t1:
                    score = score - 1
    
    return score
