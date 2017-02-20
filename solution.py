assignments = []
rows = 'ABCDEFGHI'
cols = '123456789'


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins_column(box,values,unsolved_values):
    digits = values[box]
    local_peer = False
    for peer in column_peers[box]:
        if (peer in unsolved_values and  values[peer] == values[box]):
            local_peer = True
    if local_peer == True:
        for peer in column_peers[box]:
            if values[peer] == digits:
                assign_value(values,peer,digits)
            else:
                for digit in digits:
                    assign_value(values,peer,values[peer].replace(digit,''))

def naked_twins_row(box,values,unsolved_values):
    digits = values[box]
    local_peer = False
    for peer in row_peers[box]:
        if (peer in unsolved_values and  values[peer] == values[box]):
            local_peer = True
    if local_peer == True:
        for peer in row_peers[box]:
            if values[peer] == digits:
                assign_value(values,peer,digits)
            else:
                for digit in digits:
                    assign_value(values,peer,values[peer].replace(digit,''))

def naked_twins_square(box,values,unsolved_values):
    digits = values[box]
    local_peer = False
    for peer in square_peers[box]:
        if (peer in unsolved_values and  values[peer] == values[box]):
            local_peer = True
    if local_peer == True:
        for peer in square_peers[box]:
            if values[peer] == digits:
                assign_value(values,peer,digits)
            else:
                for digit in digits:
                    assign_value(values,peer,values[peer].replace(digit,''))
def naked_twins_helper(box,values,unsolved_values,type_peers):
    digits = values[box]
    local_peer = False
    for peer in type_peers[box]:
        if (peer in unsolved_values and  values[peer] == values[box]):
            local_peer = True
    if local_peer == True:
        for peer in type_peers[box]:
            if values[peer] == digits:
                assign_value(values,peer,digits)
            else:
                for digit in digits:
                    assign_value(values,peer,values[peer].replace(digit,''))
def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    unsolved_values = [box for box in values.keys() if len(values[box]) == 2]
    for box in unsolved_values:

        naked_twins_helper(box,values,unsolved_values,row_peers)
        naked_twins_helper(box,values,unsolved_values,column_peers)
        naked_twins_helper(box,values,unsolved_values,square_peers)

    return values

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    values = []
    all_digits = '123456789'
    for c in grid:
        if c == '.':
            values.append(all_digits)
        elif c in all_digits:
            values.append(c)
    assert len(values) == 81
    return dict(zip(boxes, values))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            assign_value(values,peer,values[peer].replace(digit,''))
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        values = eliminate(values)
        # Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """


    values = grid_values(grid)
    values = naked_twins(values)

    return search(values)

boxes = cross(rows, cols)
diagonal_unit_left_to_right = [[a[0]+a[1] for a in zip(rows,cols)]]
diagonal_unit_right_to_left = [[a[0]+a[1] for a in zip(rows,cols[::-1])]]
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units + diagonal_unit_left_to_right + diagonal_unit_right_to_left
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

row_units_dict = dict((s, [u for u in row_units if s in u]) for s in boxes)
row_peers = dict((s, set(sum(row_units_dict[s],[]))-set([s])) for s in boxes)

column_units_dict = dict((s, [u for u in column_units if s in u]) for s in boxes)
column_peers = dict((s, set(sum(column_units_dict[s],[]))-set([s])) for s in boxes)

square_units_dict = dict((s, [u for u in square_units if s in u]) for s in boxes)
square_peers = dict((s, set(sum(square_units_dict[s],[]))-set([s])) for s in boxes)




if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'


    display(solve(diag_sudoku_grid))
    # try:
    #     from visualize import visualize_assignments
    #     visualize_assignments(assignments)
    #
    # except SystemExit:
    #     pass
    # except:
    #     print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
