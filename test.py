height = [4,2,3]



n = len(height)
# i = 0
# j = 1
s = 0
# while True:
#     if i == n or j == n:
#         break

#     if height[i] > height[j]:
#         j += 1

#     else:
#         s = s + (min(height[i], height[j])* (j-1-i)) - sum(height[i+1:j])
#         print("i: ", i, "j: ", j, "s: ", s," sum(height[i+1:j]): ", sum(height[i+1:j]), "min(height[i], height[j]): ", min(height[i], height[j]), (min(height[i], height[j])* (j-1-i)))
#         print(height[i+1:j])
#         i = j
#         j = i+1
    
#     if j == n :
#         i +=1
#         j = i+1
# print(s)

for i in range(n):
    left_max = 0; right_max = 0

    for j in range(i+1):
        left_max = max(left_max, height[j])
    for j in range(i, n):
        right_max = max(right_max, height[j])
    
    s = s + (min(left_max, right_max) - height[i])

print(s)