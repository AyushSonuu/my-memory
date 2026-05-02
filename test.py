height = [4,2,3]



n = len(height)
i = 0
j = 1
s = 0
while True:
    if i == n or j == n:
        break

    if height[i] > height[j]:
        j += 1

    else:
        s = s + (min(height[i], height[j])* (j-1-i)) - sum(height[i+1:j])
        print("i: ", i, "j: ", j, "s: ", s," sum(height[i+1:j]): ", sum(height[i+1:j]), "min(height[i], height[j]): ", min(height[i], height[j]), (min(height[i], height[j])* (j-1-i)))
        print(height[i+1:j])
        i = j
        j = i+1
    
    if j == n:
        i +=1
        j = i+1
print(s)