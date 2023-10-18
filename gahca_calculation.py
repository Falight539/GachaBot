import numpy as np

def prob_cal(begin_pull: int, up_pity: int, possible_pull: int):

    ans = None

    M = np.zeros((3001, 10, 2), dtype=np.float16)

    P_5 = np.zeros(91, dtype=np.float16)

    P_trans = np.zeros(91, dtype=np.float16)
    pity_pull = 90  
    base_P = 0.006
    change_pull = 73  
    state_P = 1

    for i in range(1, pity_pull+1):
        P_5[i] = base_P
        if i > change_pull:
            P_5[i] = base_P + base_P*10*(i-change_pull)
        P_5[pity_pull] = 1
        P_trans[i] = state_P * P_5[i]
        state_P = state_P * (1-P_5[i])

    if up_pity:
        M[0][0][0] = 1
    else:
        M[0][0][1] = 1
    fix_const = 1-sum(P_trans[1:begin_pull+1])  

    for i in range(1, 1+pity_pull*2*7):
        for j in range(0, 7+1):
            for pull in range(1, 1 + pity_pull):
                last_5_star = i - pull
                if last_5_star < 0:
                    continue
                P_trans_now = P_trans[pull]
                if last_5_star == 0:
                    if pull <= begin_pull:
                        continue
                    else:
                        P_trans_now = P_trans[pull] / fix_const
                M[i][j][0] += 0.5 * M[last_5_star][j][1] * P_trans_now
                if j != 0:
                    M[i][j][1] += M[last_5_star][j - 1][0] * P_trans_now + 0.5 * M[last_5_star][j - 1][1] * P_trans_now

    for j in range(1, 8):
        P_full_constellation = M[:, j, 1]
        max_p = 0
        P_sum = np.zeros(1500, dtype=np.float16)
        Expectation = 0
        for i in range(1, 1+pity_pull*2*7):
            if P_full_constellation[i] > max_p:
                max_p = P_full_constellation[i]
            Expectation += i * P_full_constellation[i]
            P_sum[i] = P_sum[i-1] + P_full_constellation[i]
        ans = P_sum if j == 1 else ans

    print(f"Your Probability to gain atleast one Rate UP is {int(ans[possible_pull]*100)}%")
    return int(ans[possible_pull]*100)