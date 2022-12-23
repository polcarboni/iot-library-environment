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
