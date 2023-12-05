def create_board():
    input1 = input("Enter Board size (NxN): ")
    size = int(input1)
    print("Board Size " + input1 + " x " + input1)

    global max_index, row, col, min_index
    row, col = 0, 0
    min_index = 0
    max_index = size - 1

    array = [[0 for i in range(size)] for k in range(size)]
    return array

def move_left():
    global row
    row = row - 1
    if (row < min_index):
        row = max_index

def move_right():
    global row
    row = row + 1
    if (row > max_index):
        row = min_index

def move_up():
    global col
    col = col - 1
    if (col < min_index):
        col = max_index

def move_down():
    global col
    col = col + 1
    if (col > max_index):
        col = min_index

def clear():
    global array
    for i in range(len(array)):
        for k in range(len(array)):
            array[i][k] = "-"
            
        

def main():
    global array
    array = create_board()
    x = 0
    
    for r in array:
            for element in r:
                print(element, end=" ")
            print()
    
    while True:
        x = 0
        direction = input("Enter direction [L(eft), R(ight), U(p), D(own), C(lear), exit]: ")
        if direction == "L":
            move_left()
        elif direction == "R":
            move_right()
        elif direction == "U":
            move_up()
        elif direction == "D":
            move_down()
        elif direction == "C":
            clear()
            x = 1
        elif direction == "exit":
            print("Thank you for sketching!")
            return
                
        if(x != 1):
            array[col][row] = "x" 
        
        for r in array:
            for element in r:
                print(element, end=" ")
            print()
            
main()
