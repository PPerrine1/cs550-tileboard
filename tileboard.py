# Authors: Nicole Miller and Patrick Perrine
# CS 550, Section 1, Dr. Marie Roch
# Submitted on 02/10/2020

import random
import copy
import math

from basicsearch_lib.board import Board

class TileBoard(Board):
    def __init__(self, n, multiple_solutions=False, force_state=None,
                 verbose=False):
        """"TileBoard(n, multiple_solutions
        Create a tile board for an n puzzle.
        
        If multipleSolutions are true, the solution need not
        have the space in the center.  This defaults to False but
        is automatically set to True when there is no middle square 
        
        force_state can be used to initialize an n puzzle to a desired
        configuration.  No error checking is done.  It is specified as
        a list with n+1 elements in it, 1:n and None in the desired order.

        verbose is a boolean for turning on debugging
        """

        self.verbose = verbose  # not debug state, up to you to use it

        self.boardsize = int(math.sqrt(n + 1))
        if math.sqrt(n + 1) != self.boardsize:
            raise ValueError("Bad board size\n" +
                             "Must be one less than an odd perfect square 8, 24, ...")

        # initialize parent
        super().__init__(self.boardsize, self.boardsize)

        ## Compute solution states
        # Set self.goals to a list of solution tuples
        # If multiple_solutions is true, None can be anywhere:
        # [(None,1,2,3,...), (1,None,2,3,...), (1,2,None,3,...)]
        # Otherwise, must be the last square:  [(1,2,3,...,None)]

        # Initialize solution state list
        self.goals = []

        if multiple_solutions:
            # Generate all possible solution tuples
            for x in range(1, n + 1):
                sol = []
                for y in range(1, n + 1):
                    if x == y:
                        # Place None in the appropriate slot per solution
                        sol.append(None)
                    sol.append(y)
                # Append solutions to self.goals
                self.goals.append(tuple(sol))
        else:
            # Generate solution tuple where None is in the last square
            sol = list(range(1, n + 1))
            sol.append(None)
            self.goals.append(tuple(sol))

        ## Determine initial state and make sure that it is solvable

        # Temporary list to be assigned to the class board
        tmp_board = []

        if force_state:
            # Check if the forced state board is solvable
            if self.solvable(force_state):
                # If solvable, assign to temporary board
                tmp_board = force_state
            else:
                # If not solvable, raise exception and halt program
                raise ValueError("Board not solvable.")

        if not force_state:
            # Generate a list where None is in the last square, then shuffle randomly
            tmp_board = list(range(1, n + 1))
            tmp_board.append(None)
            random.shuffle(tmp_board)

        # If our random board is not solvable, then we re-shuffle until it is
        while not force_state and not self.solvable(tmp_board):
            random.shuffle(tmp_board)

        ## Populate the board using self.place and tmp_board

        for x in range(self.boardsize):
            for y in range(self.boardsize):
                # Pop each element from tmp_board and place into current board
                self.place(x, y, tmp_board.pop(0))

    def solvable(self, tiles, verbose=False):
        """solvable - Determines if a puzzle is solvable

            Given a list of tiles, determine if the N-puzzle is solvable.
            You do not need to know how to do this, but the calculation
            is based on the inversion order.

            for each number in the list of tiles,
               How many following numbers are less than that one
               e.g. [13, 10, 11, 6, 5, 7, 4, 8, 1, 12, 14, 9, 3, 15, 2, None]
               Example:  Files following 9:  [3, 15, 2, None]
               Two of these are smaller than 9, so the inversion order
                   for 9 is 2

            A puzzle's inversion order is the sum of the tile inversion
            orders.  For puzzles with even numbers of rows and columns,
            the row number on which the blank resides must be added.
            Note that we need not worry about 1 as there are
            no tiles smaller than one.

            See Wolfram Mathworld for further explanation:
                http://mathworld.wolfram.com/15Puzzle.html
            and http://www.cut-the-knot.org/pythagoras/fifteen.shtml

            This lets us know if a problem can be solved.  The inversion
            order modulo 2 is invariant across moves.  This means that
            when we make a legal move, the inversion order will always
            be even or odd.  The solution state always has an even
            inversion order, so any puzzle with an odd inversion
            number cannot be solved.
        """

        inversionorder = 0
        # Make life easy, remove None
        reduced = [t for t in tiles if t is not None]
        # Loop over all but last (no tile after it)
        for idx in range(len(reduced) - 1):
            value = reduced[idx]
            after = reduced[idx + 1:]  # Remaining tiles
            smaller = [x for x in after if x < value]
            numtiles = len(smaller)
            inversionorder = inversionorder + numtiles
            if verbose:
                print("idx {} value {} tail {} #smaller {} sum: {}".format(
                    idx, value, after, numtiles, inversionorder))

        # Even number of rows must take the blank position into account
        if self.get_rows() % 2 == 0:
            if verbose:
                print("Even # rows, adding for position of blank")
            inversionorder = inversionorder + \
                             math.floor(tiles.index(None) / self.boardsize) + 1

        solvable = inversionorder % 2 == 0  # Solvable if even
        return solvable

    def __hash__(self):
        """__hash__ - Hash the board state"""

        # Convert state to a tuple and hash
        return hash(self.state_tuple())

    def __eq__(self, other):
        """__eq__ - Check if objects equal:  a == b"""

        ## Determine if two board configurations are equivalent

        # Checks if board sizes are equivalent
        if self.get_rows() == other.get_rows():
            if self.get_cols() == other.get_cols():
                # Iterates through each board, checking each element
                for x in range(self.boardsize):
                    for y in range(self.boardsize):
                        # If there's a mismatch, break loop and return False
                        if self.get(x, y) != other.get(x, y):    
                            break
                        # If we've reached the final iteration, return True
                        if x == y and x == self.boardsize - 1:
                            return True
        return False

    def state_tuple(self):
        """state_tuple - Return board state as a single tuple"""

        # Initializae temporary list
        board_tuple = []

        # Use extend to add each element of the board to board_tuple
        for x in self.board: board_tuple.extend(x)

        # Return board_tuple as a tuple
        return tuple(board_tuple)

    def get_actions(self):
        """Return row column offsets of where the empty tile can be moved"""
        
        # Initialize list of move offsets
        # Up: [-1, 0], Down: [1, 0], Left: [0, -1], Right: [0, 1]
        poss_actions = [[-1, 0], [1, 0], [0, -1], [0, 1]]

        # Get index of empty tile using state_tuple function
        empty_tile_index = self.state_tuple().index(None)

        # Remove impossible move offsets based on empty tile position
        if (empty_tile_index % self.boardsize) == 0:
            # Tile is on the left, remove left offset
            poss_actions.remove([0, -1])
        if (empty_tile_index % self.boardsize) == self.boardsize - 1:
            # Tile is on the right, remove right offset
            poss_actions.remove([0, 1])
        if empty_tile_index < self.boardsize:
            # Tile is on the top, remove up offset
            poss_actions.remove([-1, 0])
        if empty_tile_index >= math.pow(self.boardsize, 2) - self.boardsize:
            # Tile is on the bottom, remove down offset
            poss_actions.remove([1, 0])
        
        # Return all possible actions based on empty tile
        return poss_actions

    def move(self, offset):
        """move - Move the empty space by [delta_row, delta_col] and return new board"""

        # Create a deep copy of the current board
        new_b = copy.deepcopy(self.board)

        # Search for empty tile's coordinates (NOT index) using the deep copy
        found = False
        for x in range(len(new_b)):
            for y in range(len(new_b[x])):
                if new_b[x][y] is None:
                    empty_t = [x, y]
                    found = True
                    break
            if found:
                break
        
        # Apply move offset accordingly
        if offset[0] != 0:
            # Move up or down
            new_b[empty_t[0]][empty_t[1]] = new_b[empty_t[0] + offset[0]][empty_t[1]]
            new_b[empty_t[0] + offset[0]][empty_t[1]] = None
        elif offset[1] != 0:
            # Move left or right
            new_b[empty_t[0]][empty_t[1]] = new_b[empty_t[0]][empty_t[1] + offset[1]]
            new_b[empty_t[0]][empty_t[1] + offset[1]] = None

        # Assign our shifted board as our current board
        self.board = new_b

    def solved(self):
        """solved - Is the puzzle solved?  Returns boolean"""

        # Iterates through possible solution set
        for x in range(len(self.goals)):
            # Checks if current state matches one of the solutions
            if self.state_tuple() == self.goals[x]:
                return True
        return False

        
