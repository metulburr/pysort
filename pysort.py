"""
Various sorting algorithms implemented in python.
This is purely an academic excercise as no sorting implementation written
in python will possibly out perform the builtin implementation of timsort.
Even so, writing algorithms such as these is very helpful in understanding
time complexity and algorithm design.

For an overview of sorting algorithms please see the Wikipedia page:
    http://en.wikipedia.org/wiki/Sorting_algorithm

Free for all purposes.  No warranty expressed or implied.

-Written by Sean J McKiernan
"""

import sys
import random


if sys.version_info[0] < 3:
    range = xrange


#Bubble sorts.
def bubble_naive(sequence):
    """
    http://en.wikipedia.org/wiki/Bubble_sort

    A standard bubble sort implementation with no optimizations.
    Very bad and very slow.

    Inplace: Yes
    Time complexity: always O(n^2)
    """
    length = len(sequence)-1
    for _ in range(length):
        for i in range(length):
            if sequence[i] > sequence[i+1]:
                sequence[i],sequence[i+1] = sequence[i+1],sequence[i]


def bubble_optimized(sequence):
    """
    Performs much better than the naive implementation by itterating through
    one less item in the inner loop each time through the outer loop.

    Inplace: Yes
    Time complexity: always O(n^2)
    """
    for passes in range(len(sequence)-1, 0, -1):
        for i in range(passes):
            if sequence[i] > sequence[i+1]:
                sequence[i], sequence[i+1] = sequence[i+1], sequence[i]


def bubble_optimized_with_flag(sequence):
    """
    Performs negligibly worse than the bubble_optimized when the list is
    completely shuffled, but much better on lists that are almost sorted.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    for passes in range(len(sequence)-1, 0, -1):
        changed = False
        for i in range(passes):
            if sequence[i] > sequence[i+1]:
                sequence[i], sequence[i+1] = sequence[i+1], sequence[i]
                changed = True
        if not changed:
            break


def bubble_final_position(sequence):
    """
    Performs negligibly worse than the bubble_optimized when the list is
    completely shuffled, but much better on lists that are almost sorted.
    This implementation takes advantage of the fact that quite often multiple
    items find themselves in their final position after an iteration.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    swap_point = len(sequence)
    while swap_point:
        new_swap = 0
        for i in range(1, swap_point):
            if sequence[i-1] > sequence[i]:
                sequence[i-1], sequence[i] = sequence[i], sequence[i-1]
                new_swap = i
        swap_point = new_swap


#Insertion sorts.
def insertion(sequence):
    """
    http://en.wikipedia.org/wiki/Insertion_sort

    Basic insertion sort. Still worst of O(n^2) but much faster than other
    algorithms of the same time complexity like bubble sort.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    for i in range(1,len(sequence)):
        while i>0 and sequence[i]<sequence[i-1]:
            sequence[i], sequence[i-1] = sequence[i-1], sequence[i]
            i -= 1


def insertion_optimized(sequence):
    """
    Improves performance by reducing the number of swaps required.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    for i,val in enumerate(sequence):
        while i>0 and val<sequence[i-1]:
            sequence[i] = sequence[i-1]
            i -= 1
        sequence[i] = val


def insertion_optimized_alt(sequence):
    """
    Significantly faster than insertion_optimized on a shuffled list.
    Slightly slower on an already sorted list.

    Inplace: Yes
    Time complexity: best O(n), avg and worst O(n^2)
    """
    j = 0
    for i,val in enumerate(sequence):
        for j in range(i,-1,-1):
            if j>0 and val<sequence[j-1]:
                sequence[j] = sequence[j-1]
            else:
                break
        sequence[j] = val


#Quick sorts.
def quick_random(sequence):
    """
    http://en.wikipedia.org/wiki/Quicksort

    Quick sort with random pivot selection.  Far superior to insertion and
    bubble sort in general cases, but quite a bit worse in cases where the list
    is already sorted.

    Inplace: No
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    length = len(sequence)
    if length < 2:
        return sequence
    pivot = sequence.pop(random.randrange(length))
    above = []
    below = []
    for item in sequence:
        if item > pivot:
            above.append(item)
        else:
            below.append(item)
    return quick_random(below)+[pivot]+quick_random(above)


def quick_median(sequence):
    """
    Quick sort with median-of-3 pivot selection.
    Not much noticable difference over random pivot selection.

    Inplace: No
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    length = len(sequence)
    if length < 2:
        return sequence
    pivot_index = median_of_three(sequence, 0, length-1)
    pivot = sequence.pop(pivot_index)
    above = []
    below = []
    for item in sequence:
        if item > pivot:
            above.append(item)
        else:
            below.append(item)
    return quick_median(below)+[pivot]+quick_median(above)


def quick_inplace_random(sequence, left=0, right=None):
    """
    In-place quicksort with random pivot selection.
    See the helper function partition() below.

    Inplace: Yes
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    if right is None:
        right = len(sequence)-1
    if left < right:
        pivot_ind = random.randint(left,right)
        pivot_new_ind = partition(sequence, left, right, pivot_ind)
        quick_inplace_random(sequence, left, pivot_new_ind-1)
        quick_inplace_random(sequence, pivot_new_ind+1, right)


def quick_inplace_median(sequence, left=0, right=None):
    """
    In-place quicksort with median-of-3 pivot selection.
    See the helper function partition() below.

    Inplace: Yes
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    if right is None:
        right = len(sequence)-1
    if left < right:
        pivot_ind = median_of_three(sequence, left, right)
        pivot_new_ind = partition(sequence, left, right, pivot_ind)
        quick_inplace_median(sequence, left, pivot_new_ind-1)
        quick_inplace_median(sequence, pivot_new_ind+1, right)


def quick_inplace_repeat(sequence, low=0, high=None):
    """
    In-place quicksort with median-of-3 pivot selection.
    Uses an optimization specifically for lists that contain repeated elements.
    With the other methods a list of all the same item automatically causes
    worst O(n^2) performance.  Here we avoid this at the cost of slightly
    longer average times.

    See the helper function partition_repeat() below.

    Inplace: Yes
    Time complexity: best O(n), avg O(nlogn), worst O(n^2)
    """
    if high is None:
        high = len(sequence)-1
    if low < high:
        pivot_ind = median_of_three(sequence, low, high)
        left, right = partition_repeat(sequence, low, high, pivot_ind)
        quick_inplace_repeat(sequence, low, left)
        quick_inplace_repeat(sequence, right, high)


def partition(sequence, left, right, pivot_ind):
    """This is the key to the in-place quicksort."""
    pivot = sequence[pivot_ind]
    sequence[pivot_ind], sequence[right] = sequence[right], sequence[pivot_ind]
    index = left
    for i in range(left,right):
        if sequence[i] <= pivot:
            sequence[i], sequence[index] = sequence[index], sequence[i]
            index += 1
    sequence[index], sequence[right] = sequence[right], sequence[index]
    return index


def partition_repeat(sequence, left, right, pivot_ind):
    """
    Partitioner that allows quicksort to avoid worst case performance on a
    list that contains numerous repeated elements.
    """
    pivot = sequence[pivot_ind]
    index = left
    for i in range(left, right+1):
        if sequence[i] < pivot:
            sequence[i], sequence[index] = sequence[index], sequence[i]
            index += 1
    left = index
    for i in range(left, right+1):
        if sequence[i] == pivot:
            sequence[i], sequence[index] = sequence[index], sequence[i]
            index += 1
    return left, index


def median_of_three(sequence, left, right):
    """
    Find the index (with respect to sequence) of the median of three values.
    """
    mid = (left+right)//2
    if sequence[left] > sequence[mid]:
        if sequence[mid] > sequence[right]:
            return mid
        elif sequence[left] > sequence[right]:
            return right
        return left
    elif sequence[left] > sequence[right]:
        return left
    elif sequence[mid] > sequence[right]:
        return right
    return mid


#Merge sorts.
def merge_sort(sequence):
    """
    http://en.wikipedia.org/wiki/Merge_sort

    A basic implementation of merge sort.  Despite enjoying a lower worst
    case time complexity, quick sort often outperforms merg sort in practical
    cases.

    Uses the helper function merge() below.

    Inplace: No
    Time complexity: all O(nlogn)
    """
    length = len(sequence)
    if length < 2:
        return sequence
    middle = length//2
    left = merge_sort(sequence[:middle])
    right = merge_sort(sequence[middle:])
    return merge(left, right)


def merge(left, right):
    """Merges the values in left and right in the correct order."""
    new = []
    left_index, right_index = 0, 0
    len_left, len_right = len(left), len(right)
    while left_index < len_left and right_index < len_right:
        if left[left_index] <= right[right_index]:
            new.append(left[left_index])
            left_index += 1
        else:
            new.append(right[right_index])
            right_index += 1
    new += left[left_index:]
    new += right[right_index:]
    return new


#Heap sorts.
def heap_sort(sequence):
    """
    http://en.wikipedia.org/wiki/Heapsort

    A basic implementation of heap sort.  As with merge sort, heap sort is
    also often out performed by quick sort in practical cases.

    Uses helper functions heapify() and sift_down()

    Inplace: Yes
    Time complexity: all O(nlogn)
    """
    highest_index = len(sequence)-1
    heapify(sequence, highest_index)
    for end in range(highest_index, 0, -1):
        sequence[end], sequence[0] = sequence[0], sequence[end]
        sift_down(sequence, 0, end-1)


def heapify(sequence, highest_index):
    """Take a sequence and put it in heap order.  Operates inplace."""
    first = (highest_index-1)//2
    for start in range(first, -1, -1):
        sift_down(sequence, start, highest_index)


def sift_down(sequence, start, end):
    """Change position of item in list until it is correctly placed in heap."""
    root = start
    while root*2+1 <= end:
        child = root*2+1
        swap = root
        if sequence[swap] < sequence[child]:
            swap = child
        if child+1 <= end and sequence[swap] < sequence[child+1]:
            swap = child+1
        if swap != root:
            sequence[root], sequence[swap] = sequence[swap], sequence[root]
            root = swap
        else:
            break


#Inefficient/novelty sorts.
def bogo(sequence):
    """
    http://en.wikipedia.org/wiki/Bogosort

    Check if the list is in order; if it is not, shuffle the list.
    Not intended to be a realistic method of sorting.

    This algorithm is so bad that a list of even 10 elements can take
    more than 15 seconds to sort (as such it is not included in the
    algorithms automatically tested in test_sorts.py).

    Inplace: Yes
    Time complexity: O(n*n!)
    """
    while any(sequence[i]>sequence[i+1] for i in range(len(sequence)-1)):
        random.shuffle(sequence)
    return sequence
