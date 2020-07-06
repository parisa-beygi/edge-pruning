
class Combinations(object):

  def __init__(self, max_len, max_num):
    """Initialize the parameters of the Combinations."""
    self.a = {}
    self.a[0] = [[]]
    self.a[1] = [[1]]

    self.max_len = max_len
    self.max_num = max_num


  def get_dict(self):
    return self.a
  
  def get_last_index_computed(self):
    return max(self.a.items(), key = lambda x: x[0])[0]

  def split_range(self, k, m):
    return [i * k / m for i in range(m)]


  def process_comb_from(k1, k2):
    for k in range(k1, k2):
      
      for e in self.a[i - k][::-1]:
      
        if e:
          if len(e) >= self.max_len:
            continue
          if k >= e[-1]:
            self.a[i].append(e + [k])
        else:
          self.a[i].append([k])


  def find_combinations_dp(self, n):

    last_index = self.get_last_index_computed()

    if last_index == n:
      print ('HIT > Sum = {}'.format(n))
      return a[n]

    print ('MISS > Sum = {}, last index = {}'.format(n, last_index))

    for i in range(last_index + 1, n + 1):
      self.a[i] = []
      max_value = min(i, self.max_num) + 1
      for k in range(1, max_value):
        
        for e in self.a[i - k][::-1]:
        
          if e:
            if len(e) >= self.max_len:
              continue
            if k >= e[-1]:
              self.a[i].append(e + [k])
          else:
            self.a[i].append([k])

      # if max_value > 10:
      #   kk = self.split_range(max_value, 4)
      # else:
      #   kk = [1]
      # for j in range(len(kk) - 1):
      #   k1 = kk[j]
      #   k2 = kk[j + 1]
      #   self.process_comb_from(k1, k2)
        



    return self.a[n]

# c = Combinations(5, 25)
# print (c.find_combinations_dp(125))
# print (c.find_combinations_dp(126))

# print(c.get_dict())