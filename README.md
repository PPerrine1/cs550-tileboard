# (A01) TileBoard Assignment

Complete class TileBoard in file boardtypes.py for representing n-puzzles.  
It should be derived from class Board (provided) and should support the following interface:

	- TileBoard(n, force_state=None) –   Creates an n-puzzle of size n.  Example TileBoard(8) creates the 8-puzzle shown below.  You can force a specific configuration using the force_state argument and a list or tuple, e.g. (8,None,5,4,7,2,3,1) for the puzzle on the next page. This can be helpful for testing by letting you create easily solvable puzzles, e.g. (1,2,None,4,5,3,7,8,6) is solvable in two moves. If force_state is not specified, create a random board.
	
Your puzzle must be solvable. Method TileBoard.solvable takes a list or tuple of tiles (like force_state) and checks whether or not the puzzle can be solved.  For random puzzles, reshuffle until you get a solveable puzzle.  When the puzzle is forced to a specific configuration using force_state, throw a ValueError if the puzzle is not solvable.

	- Operator == to check if two tile boards are in the same state.  Use method __eq__(other_obj) to overload the equality operator.
	- state_tuple() - Flatten the list of list representation of the board provided by the parent class and cast it to a tuple.  e.g. [[1,2,3],[4,None,5],[6,7,8]] becomes (1,2,3,4,None,5,6,7,8)
	- get_actions() – Return list of possible moves.  It is easier to think of the blank space as being moved rather than specifying which numbered tiles can be moved.  We will return this as a list of lists where each sublist is a[row_delta,col_delta] list specifying the offset of the space from its current position relative to the current row and column.   Values of the deltas can be -1, 0, or 1 indicating that the space should be moved:  left, no move, or right and up, no move, or down.

Concrete examples for the puzzle at right where space can be moved to the left,right, or down: [ [0,-1], [0,1], [1,0] ]. 

	- move(offset) – Given a valid action of the rom [row_delta, col_delta], return a new TileBoard that represents the state after the move.Example:  action [0,-1] would move the space zero rows and one column to the left, exchanging the blank and 8.
	
Hint:  To maintain multiple versions of the board in a later assignment involving search, it is important that you not just modify the lists.  As Python objects contain pointers to the list, changing the lists in the current object would also change the lists in any other object that was created from this one.  There are many ways that you could prevent this, but one of the easiest ways to clone an object is to use the copy module’s deepcopy method:  newboard = copy.deepcopy(self)  # Create a deep copy of the object  # make modifications to newboard.
	
	- solved() – Return True if the puzzle is in a goal state (the blank must be in thecenter of an odd sized puzzle.  You may define it as you wish for even sized puzzles). 
	
The portions of the program that you need to modify are either marked as “todo:” or raise a NotImplementedError.  A driver function (driver.py) is provided . It should print a board and allow you to play an 8 puzzle.

Some general hints:

	- The random module has a method shuffle that can be used to permute a list.  This is useful for randomizing the initial state.
	- If you need math functions (e.g. sqrt), they are in Python’s math module.
	- Use tuples for hashing!
	
A zip archive with skeleton code and modules driver and basic_search.board are provided for you.  They are available on Blackboard.  You should not modify any files other than tielboard.py.
