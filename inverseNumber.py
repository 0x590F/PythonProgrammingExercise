def inverse_number(string):
    'input a number which is string than,you will get the inverse number'
    ans = 0
    for i in range(len(string)):
        for j in range(i):
            if string[j] > string[i]:
                ans += 1
    return ans
 
print(inverse_number(input("Please input the number: ")))
