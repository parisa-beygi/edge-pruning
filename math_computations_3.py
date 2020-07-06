
def find_combinations(n):
  a = {}
  a[0] = [[]]
  a[1] = [[1]]

  for i in range(2, n + 1):
    a[i] = []
    for k in range(1, i + 1):
      for e in a[i - k]:
        if e:
          if k >= e[-1]:
            a[i].append(e + [k])
        else:
          a[i].append([k])

  
  print (a)
  return a[n]
  # print (set(frozenset(i) for i in a[n]))

print (find_combinations(5))

  