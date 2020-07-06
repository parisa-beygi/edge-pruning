
import math

def get_divisor_pairs(k):
  sqr = int(math.sqrt(k))
  l = list()

  for i in range(1, sqr + 1):
    if k % i ==0:
      l.append((i, k//i))
  return l



# Python3 program to find out all 
# combinations of positive  
# numbers that add upto given number 
  
# arr - array to store the combination 
# index - next location in array 
# num - given number 
# reducedNum - reduced number  
def findCombinationsUtil(list_of_combinations, arr, index, num, 
                              reducedNum, count): 
  
    # Base condition 
    if (reducedNum < 0): 
        return; 
  
    # If combination is  
    # found, print it 
    if (reducedNum == 0): 
        l = []
        for i in range(index): 
            # print(arr[i], end = " "); 
            l.append(arr[i])
        # print("");

        list_of_combinations.append(l) 
        return; 

    # The number of numbers exceed the required number of numbers
    if index == count:
      return

    # Find the previous number stored in arr[].  
    # It helps in maintaining increasing order 
    prev = reducedNum if(index == 0) else arr[index - 1]; 
  
    # note loop starts from previous  
    # number i.e. at array location 
    # index - 1 
    for k in reversed(range(1, prev + 1)): 
          
        # next element of array is k 
        arr[index] = k; 
  
        # call recursively with 
        # reduced number 
        findCombinationsUtil(list_of_combinations, arr, index + 1, num,  
                                 reducedNum - k, count); 
  
# Function to find out all  
# combinations of positive numbers  
# that add upto given number. 
# It uses findCombinationsUtil()  
def findCombinations(n): 
      
    # array to store the combinations 
    # It can contain max n elements 
    arr = [0] * n; 
    list_of_combinations = list()
    # find all combinations 
    findCombinationsUtil(list_of_combinations, arr, 0, n, n, 10)
    # print (list_of_combinations)
    return list_of_combinations
  
# Driver code 
n = 5; 
print (findCombinations(n))
  
# This code is contributed by mits 

# print (get_divisor_pairs(1))