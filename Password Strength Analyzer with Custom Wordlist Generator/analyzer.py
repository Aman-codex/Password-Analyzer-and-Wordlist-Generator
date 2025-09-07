
from math import log2
from zxcvbn import zxcvbn

def entropy_estimate(password):
    
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32 
    if pool == 0:
        return 0.0
    return round(len(password) * log2(pool), 2)

def assess_password(password):
    
    score = zxcvbn(password)
    ent = entropy_estimate(password)
    result = {
        'zxcvbn_score': score['score'],  # 0-4
        'zxcvbn_feedback': score.get('feedback', {}),
        'estimated_entropy_bits': ent,
        'crack_time_display': score.get('crack_times_display', {}),
    }
    return result
