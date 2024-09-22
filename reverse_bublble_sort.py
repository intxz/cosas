import time
import random

arr = random.sample(range(21), 4)
print(f"Original array: {arr}")

def reverse_bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(0, len(arr)-i-1):
            print(f"Sorting the array: {arr}", end="\r")
            time.sleep(1)
            if arr[j] < arr[j+1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

sorted_arr = reverse_bubble_sort(arr)
print(f"Sorted array: {sorted_arr}")