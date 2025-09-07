import itertools
import re
from datetime import datetime

LEET_MAP = {
    'a': ['4', '@'],
    'b': ['8'],
    'e': ['3'],
    'i': ['1', '!'],
    'l': ['1', '|'],
    'o': ['0'],
    's': ['5', '$'],
    't': ['7'],
    'g': ['9']
}

COMMON_SUFFIXES = ['', '123', '1234', '2023', '2024', '!', '!!', '@', '#']
COMMON_PREFIXES = ['', '!', '@', '#']

def extract_years_from_date(token):
   
    years = set()
    m = re.search(r'(\d{4})', token)
    if m:
        years.add(m.group(1))
    
    m2 = re.search(r'(\d{2})\b', token)
    if m2:
        years.add('20' + m2.group(1))
    return years

def leet_variants(word, max_variants=50):
   
    variants = set()
    positions = []
    for i, ch in enumerate(word.lower()):
        if ch in LEET_MAP:
            positions.append((i, LEET_MAP[ch]))
    
    variants.add(word)
    for r in range(1, min(4, len(positions)+1)):
        for combo in itertools.combinations(positions, r):
            chars = list(word)
            for pos, subs in combo:
                chars[pos] = subs[0]  
            variants.add(''.join(chars))
            if len(variants) >= max_variants:
                return variants
    return variants

def case_variants(word):
    return {word, word.lower(), word.upper(), word.capitalize()}

def generate_candidates(hints, max_output=10000):
 
    seeds = set()
    
    for h in hints:
        parts = re.split(r'\W+', h)
        for p in parts:
            if p:
                seeds.add(p)

    
    years = set()
    for s in list(seeds):
        years |= extract_years_from_date(s)

    
    combos = set(seeds)
    for L in range(2, 4):
        for tup in itertools.permutations(seeds, L):
            combo = ''.join(tup)
            if len(combo) <= 30:
                combos.add(combo)
   
    candidates = set()
    for base in list(combos)[:2000]: 
        for c in case_variants(base):
            candidates.add(c)
            for l in leet_variants(c):
                candidates.add(l)
            candidates.add(c[::-1]) 
            for sfx in COMMON_SUFFIXES:
                candidates.add(c + sfx)
            for pfx in COMMON_PREFIXES:
                candidates.add(pfx + c)
        for y in years:
            candidates.add(base + y)
            candidates.add(y + base)

    
    filtered = {c for c in candidates if 4 <= len(c) <= 64}
  
    sorted_c = sorted(filtered, key=lambda x: (len(x), x))[:max_output]
    return sorted_c
