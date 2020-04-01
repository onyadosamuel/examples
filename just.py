import random # import the random class

dic = {50:'A',55:'B',57:'C',58:'D',60:'E'} # has distances as the key and the towns as the values
num = [50,55,57,58,60] # a list that contains the distances of the cities

store = [] # this is a list that store the sum of numbers more than 174
while len(store) < 3: # while loop to find the three distances
    numbers = random.choices(num,k=3) 
    a = sum(numbers)
    if a > 174:
        print('.................')
        say = 'You can go to to cities {} , {} and {}'.format(dic[numbers[0]],dic[numbers[1]],dic[numbers[2]])
        print(say)
        print('.................')

        store.append(a)
    else:
        continue

print('This is the store of distances',store)
print('The maximum distance among the three distances ',max(store))
