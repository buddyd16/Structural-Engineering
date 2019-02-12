import itertools

def load_pattern(num_spans):
    test = []
    n = num_spans
    for r in range(n):
       for item in itertools.combinations(range(n), r):
           check = [1]*n
           for i in item:
               check[i] = 0
           test.append(check)
    return test
    

out = load_pattern(3)

n=20

pat1 = [1 for i in range(1,n+1)]
pat2 = [1 if i % 2 == 0 else 0 for i in range(1,n+1)]
pat3 = [0 if i % 2 == 0 else 1 for i in range(1,n+1)]

count = 0
pat4 = []
pat5 = []
pat6 = []
for i in range(1,n+1):
    
    if count<=1:
        if count == 0:
            pat4.append(1)
            pat5.append(0)
            pat6.append(1)
        else:
            pat4.append(1)
            pat5.append(1)
            pat6.append(0)
        count+=1
    else:
        pat4.append(0)
        pat5.append(1)
        pat6.append(1)
        count=0

patterns = [pat1,pat2,pat3,pat4,pat5,pat6]

patterns_trans = map(list, zip(*patterns))
    