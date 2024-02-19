from turtle import *

# Constants for size 1
height1 = 100
width1 = 50
Vheading1 = 75.96376
Vheight1 = 103.07764
Xheading1 = 63.43497
Xheight1 = 111.80338

# Constants for size 2
height2 = 50
width2 = 25
Vheading2 = 75.96376
Vheight2 = 51.53882
Xheading2 = 63.43497
Xheight2 = 55.9017

def guideline(height, width):
    penup()
    setheading(0)
    pensize(3)
    backward(width)
    pendown()
    forward(width)
    pensize(1)

def topline(height, width):
    penup()
    setheading(90)
    forward(height * 0.1)
    guideline(height, width)
    setheading(-90)
    penup()
    forward(height * 0.1)

# Draw letter I 1
def I(height, width):
    setheading(0)
    forward(width)
    pendown()
    guideline(height, width)
    pendown()
    backward(width/2)
    right(90)
    forward(height)
    left(90)
    forward(width/2)
    guideline(height, width)
    penup()
    left(90)
    forward(height)
    right(90)

# Draw letter V 5
def V(heading, sidelength, height, width):
    setheading(-heading)
    pendown()
    forward(sidelength)
    setheading(0)
    forward(width/2)
    guideline(height, width)
    backward(width/2)
    setheading(heading)
    forward(sidelength)
    guideline(height, width)
    penup()
    pensize(1)

# Draw letter X 10
def X(heading, sidelength, height, width):
    setheading(-heading)
    pendown()
    forward(sidelength)
    guideline(height, width)
    setheading(-heading)
    backward(sidelength/2)
    setheading(heading)
    backward(sidelength/2)
    forward(sidelength)
    guideline(height, width)
    penup()

# Draw letter L 50
def L(height, width):
    Lwidth = width * 0.9
    Lheight = height * 0.9
    setheading(0)
    forward(width)
    guideline(height, width)
    pendown()
    backward(Lwidth)
    setheading(-90)
    forward(Lheight)
    setheading(0)
    forward(Lwidth)
    penup()
    setheading(-90)
    forward(height * 0.1)
    guideline(height, width)
    penup()
    setheading(90)
    forward(height)

# Draw letter C 100
def C(height, width):
    penup()
    setheading(0)
    forward(width)
    guideline(height, width)
    penup()
    right(90)
    forward(height)
    guideline(height, width)
    setheading(180)
    pendown()
    circle(-height // 2, 180)
    setheading(0)

# Draw letter D 500
def D(height, width):
    setheading(-90)
    pendown()
    forward(height)
    left(90)
    forward(width)
    guideline(height, width)
    backward(width)
    circle(height // 2, 180)
    setheading(0)
    forward(width)
    guideline(height, width)
    penup()

# Draw letter M 1,000
def M(heading, sidelength, height, width):
    penup()
    setheading(-90)
    pendown()
    forward(height/2)
    left(90)
    forward(10)
    backward(10)
    right(90)
    forward(height/2)
    backward(height)
    setheading(0)
    V(heading, sidelength, height, width)
    pendown()
    setheading(-90)
    forward(height/2)
    right(90)
    forward(10)
    backward(10)
    left(90)
    forward(height/2)
    backward(height)
    penup()

# Draw letter V with topline 5,000
def W(heading, sidelength, height, width):
    M(heading, sidelength, height, width)
    topline(height, width)

# Draw letter X with topline 10,000
def K(heading, sidelength, height, width):
    X(heading, sidelength, height, width)
    penup()
    topline(height, width)

# Draw letter L with topline 50,000
def J(height, width):
    L(height, width)
    topline(height, width)

# Draw letter C with topline 100,000
def O(height, width):
    C(height, width)
    topline(height, width)

# Draw letter D with topline 500,000
def B(height, width):
    D(height, width)
    topline(height, width)

# Draw letter M with topline 1,000,000
def N(heading, sidelength, height, width):
    M(heading, sidelength, height, width)
    topline(height, width)

# This function moves the turtle to a specific position
def tp(x, y):
    penup()
    goto(x, y)
    pendown()

# Convert integer to Roman numeral
def int_to_roman(num):
    # Define the values and corresponding Roman numerals
    values = [1000000, 900000, 500000, 400000, 100000, 90000, 50000, 40000, 10000, 9000, 5000, 4000, 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['N', 'ON', 'B', 'OB', 'O', 'KO', 'J', 'KJ', 'K', 'MK', 'W', 'MW', 'M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']

    result = ''  # Initialize an empty string to store the Roman numeral

    # Iterate through the values and numerals
    for i in range(len(values)):
        # Calculate how many times the current numeral needs to be added
        count = num // values[i]

        # Add the current numeral repeated 'count' times to the result
        result += numerals[i] * count

        # Update 'num' using the modulus to get the remainder
        num %= values[i]

    # Return the final Roman numeral representation
    return result

# Draw Roman numeral based on size
def draw_roman_numeral(numeral, size, x, y):
    tp(x, y)

    heading, side_length, height, width = (Vheading1, Vheight1, height1, width1) if size == 1 else (Vheading2, Vheight2, height2, width2)

    draw_function = {
        'N': lambda: N(heading, side_length, height, width),
        'B': lambda: B(height, width),
        'O': lambda: O(height, width),
        'J': lambda: J(height, width),
        'K': lambda: K(Xheading1, Xheight1, height1, width1) if size == 1 else K(Xheading2, Xheight2, height2, width2),
        'W': lambda: W(Vheading1, Vheight1, height1, width1) if size == 1 else W(Vheading2, Vheight2, height2, width2),
        'M': lambda: M(Vheading1, Vheight1, height1, width1) if size == 1 else M(Vheading2, Vheight2, height2, width2),
        'D': lambda: D(height, width),
        'C': lambda: C(height, width),
        'L': lambda: L(height, width),
        'X': lambda: X(Xheading1, Xheight1, height1, width1) if size == 1 else X(Xheading2, Xheight2, height2, width2),
        'V': lambda: V(Vheading1, Vheight1, height1, width1) if size == 1 else V(Vheading2, Vheight2, height2, width2),
        'I': lambda: I(height, width)
    }

    for letter in numeral:
        draw_function.get(letter, lambda: None)()

# Draw Roman numeral rows based on size and length
def draw_rows(numeral, size):
    length = len(numeral)

    if size == 1 and length > 24:
        print("Numeral was too large to display as size 1")
        return

    # Number of rows calculation
    rows = (length - 1) // 16 + 1

    # Draw each row based on the number of rows
    for row in range(rows):
        x_coordinate = -200
        y_coordinate = 190 - row * 76
        draw_roman_numeral(numeral[row * 16:(row + 1) * 16], size, x_coordinate, y_coordinate)

# Main drawing function to convert integers into drawn Roman Numerals
def draw():
    usernum = int(input("Enter a number: "))
    numeral = int_to_roman(usernum)
    print("Numeral length:", len(numeral))
    draw_rows(numeral, 1)

# This allows the user to choose what numerals to draw, in what order and which size they want
def roman_chooser():
    print("Numeral Options: I, V, X, L, C, D, M, W, K, J, O, B, N")
    print("***Note*** From W on, the numerals are not actually the letters that will be drawn")
    numeral = input("Enter a Roman numeral: ")
    size = int(input("Enter numeral size (1 or 2): "))
    draw_rows(numeral, size)

# Convert Roman numeral to integer (not drawn)
def roman_to_int(roman):
    # Define the values and corresponding Roman numerals
    values = [1000000, 900000, 500000, 400000, 100000, 90000, 50000, 40000, 10000, 9000, 5000, 4000, 1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    numerals = ['N', 'ON', 'B', 'OB', 'O', 'KO', 'J', 'KJ', 'K', 'MK', 'W', 'MW', 'M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V', 'IV', 'I']

    total = 0
    prev_value = 0

    # Iterate through the Roman numeral string in reverse
    for numeral in reversed(roman):
        current_value = values[numerals.index(numeral)]

        # If the current value is less than the previous, subtract it
        if current_value < prev_value:
            total -= current_value
        else:
            total += current_value

        # Update the previous value for the next iteration
        prev_value = current_value

    print(total)

# Main program

def roman_main():
    speed(0)
    choice = input("drw, r-i, chs: ")
    if choice == "drw":
        draw()
    elif choice == "r-i":
        inRom = input("Input a Roman Numeral: ")
        roman_to_int(inRom)
    elif choice == "chs":
        roman_chooser()
    else:
        print("Input not accepted")
    done()