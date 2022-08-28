l = int(input("Enter Length: "))
list = []
print("Enter Elements:")
for i in range(0,l):
    list.append(int(input()))

a = int(input("Element to be searched: "))
low = 0
high = l-1
mid = (low+high)//2

while low<=high:
    if list[mid]==a:
        break
    elif list[mid]<a:
        low = mid+1
    else:
        high = low-1
    mid = (low+high)//2

if low<=high:
    print("element found at position: ", mid+1)
else:
    print("Element not found")