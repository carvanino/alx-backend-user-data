def pascal_triangle(n):
    array = []
    arr = []
    if n <= 0:
        return array
    for row in range(n):
        print('ROW', row)
        if row == 0:
            array.append(1)
        #if row > 0:
            #array.insert(row, 1)
        for col in range(row):
            #arr = []
            # arr = [1, 2, 1]
            # arr = array.copy() # Both old and new array have the same value at this point
            #arr = [*array]
            print('Test', arr)
            if col > 0:
                new = arr[col-1] + arr[col]
                array.insert(col, new) # update array using old array value
                # array = [1, 3, 2, 1]
                print('Array after insert =', array)
                #array = [*arr]
                #arr = array.copy()
            if row < 2 and col == row - 1:
                array.append(1)
            #arr[col+1] = arr[col] + arr[col+1]
            #array = [*array, *arr]
            arr = array.copy() # Both old and new array have the same value at this point
        print(array)

