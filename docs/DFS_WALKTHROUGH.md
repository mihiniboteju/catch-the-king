# DFS Flow: Step-by-Step Walkthrough

## Example Scenario

Let's trace how `dfs_search()` finds a solution to place pieces on a board to put a King in check.

### Initial Setup
```
Board Size: 4x4 (simplified for clarity)
King Position: (3, 3) - bottom-right corner
Available Pieces: {'R': 1, 'P': 1}  # 1 Rook, 1 Pawn
Initial Board:
. . . .
. . . .
. . . .
. . . K
```

### Goal
Place the Rook and Pawn somewhere on the empty squares to create a board where the King is in check.

---

## Step-by-Step Execution

### **Step 1: Initial Call**
```python
dfs_search(initial_state, king_pos=(3,3), find_solution=True, solution=[])
```

**State:**
- Board: all empty except King at (3,3)
- Remaining pieces: {'R': 1, 'P': 1}
- Solution path: []

**Action:**
1. Convert board to string (with King placed): 
   ```
   "....\n....\n....\n...K"
   ```
2. Call `checkmate(board_str)` → Returns `False` (no pieces attacking yet)
3. Check if pieces remain → Yes, we have R=1, P=1
4. Get empty squares → [(0,0), (0,1), (0,2), (0,3), (1,0), ..., (3,2)] (15 squares)
5. Start iterating: Try placing each piece at each empty square

---

### **Step 2: Try First Placement - Rook at (0,0)**
```python
# Recursive call
dfs_search(new_state, king_pos=(3,3), find_solution=True, solution=[('R', 0, 0)])
```

**State:**
- Board:
  ```
  R . . .
  . . . .
  . . . .
  . . . K
  ```
- Remaining pieces: {'R': 0, 'P': 1}
- Solution path: [('R', 0, 0)]

**Action:**
1. Board string: `"R...\n....\n....\n...K"`
2. Call `checkmate(board_str)` → Returns `False` (Rook at (0,0) doesn't attack King at (3,3))
3. Still have pieces (P=1), continue searching
4. Get empty squares (14 remaining)
5. Try placing Pawn...

---

### **Step 3: Try Second Placement - Pawn at (0,1)**
```python
# Recursive call (depth 2)
dfs_search(new_state, king_pos=(3,3), find_solution=True, solution=[('R', 0, 0), ('P', 0, 1)])
```

**State:**
- Board:
  ```
  R P . .
  . . . .
  . . . .
  . . . K
  ```
- Remaining pieces: {'R': 0, 'P': 0}
- Solution path: [('R', 0, 0), ('P', 0, 1)]

**Action:**
1. Board string: `"RP..\n....\n....\n...K"`
2. Call `checkmate(board_str)` → Returns `False` (neither piece attacks King)
3. Check remaining pieces → All are 0
4. Return `[]` (no solution found with this combination)

**Backtrack:** Return to Step 2, try next Pawn position

---

### **Step 4: Try Pawn at (0,2)** *(continuing backtrack)*
Same as Step 3, but Pawn at (0,2). Still doesn't create check → Return `[]`, backtrack again.

---

### **Step 5: Try Pawn at (2,3)** *(many iterations later)*
```python
dfs_search(new_state, king_pos=(3,3), find_solution=True, solution=[('R', 0, 0), ('P', 2, 3)])
```

**State:**
- Board:
  ```
  R . . .
  . . . .
  . . . P
  . . . K
  ```
- Remaining pieces: {'R': 0, 'P': 0}
- Solution path: [('R', 0, 0), ('P', 2, 3)]

**Action:**
1. Board string: `"R...\n....\n...P\n...K"`
2. Call `checkmate(board_str)` → Returns `False` (Pawn at (2,3) above King at (3,3), but pawn only attacks diagonally down-left/down-right, not directly below)
3. No pieces remain → Return `[]`

**Backtrack:** Continue trying other combinations...

---

### **Step N: Try Rook at (3,0)** *(backtracked to Step 1)*

After exhausting Rook at (0,0), DFS backtracks all the way to Step 1 and tries next position...

```python
dfs_search(new_state, king_pos=(3,3), find_solution=True, solution=[('R', 3, 0)])
```

**State:**
- Board:
  ```
  . . . .
  . . . .
  . . . .
  R . . K
  ```
- Remaining pieces: {'R': 0, 'P': 1}
- Solution path: [('R', 3, 0)]

**Action:**
1. Board string: `"....\n....\n....\nR..K"`
2. Call `checkmate(board_str)` → Returns `True`! 
   - Rook at (3,0) and King at (3,3) are on the same row
   - Rook has clear horizontal path to King
   - King is in check!

---

### **Step N+1: SOLUTION FOUND! 🎯**

**Return path:** `[('R', 3, 0)]`

The recursion unwinds, returning the solution path up through all the recursive calls back to the original caller.

---

## Key Observations

### 1. **Depth-First Exploration**
- DFS explores placements in depth-first order
- It tries placing all pieces before checking the next first-placement position
- Example order: R@(0,0)→P@(0,0)❌, R@(0,0)→P@(0,1)❌, ..., R@(0,0)→P@(3,2)❌, then backtracks to try R@(0,1)...

### 2. **Early Termination**
- As soon as `checkmate()` returns `True`, DFS returns the solution immediately
- No need to explore remaining branches
- In our example, placing just the Rook at (3,0) was enough - didn't need to place the Pawn!

### 3. **Backtracking**
- When a branch fails (no check found), DFS returns `[]` or `False`
- Caller receives this, tries next piece/position combination
- This creates the depth-first tree traversal

### 4. **State Space**
For our 4×4 example with 2 pieces:
- First piece: 15 empty positions
- Second piece: 14 remaining positions
- Total combinations: 15 × 14 = 210 possible states
- DFS explores these in depth-first order until finding a solution

### 5. **Solution Path Construction**
- `solution` parameter accumulates placements: `[('R', 3, 0)]`
- Each recursive call adds its placement: `solution + [(piece, row, col)]`
- When goal found, this path is returned up the call stack

---

## Visual Call Tree (Simplified)

```
dfs_search(empty_board, [])
├─ place R at (0,0) → dfs_search([('R',0,0)])
│  ├─ place P at (0,1) → checkmate? No → return []
│  ├─ place P at (0,2) → checkmate? No → return []
│  ├─ ...
│  └─ place P at (3,2) → checkmate? No → return []
├─ place R at (0,1) → dfs_search([('R',0,1)])
│  └─ (similar exploration...)
├─ ...
└─ place R at (3,0) → dfs_search([('R',3,0)])
   └─ checkmate? YES! ✓
      └─ return [('R', 3, 0)]  ← SOLUTION FOUND
```

---

## Code Flow Diagram

```
START: dfs_search(state, king_pos, find_solution=True, solution=[])
  │
  ├─→ board_str = board_to_string(state.board, king_pos)
  │
  ├─→ if checkmate(board_str):
  │     YES → return solution  ← GOAL REACHED
  │     NO  → continue
  │
  ├─→ if no remaining pieces:
  │     return []  ← DEAD END
  │
  ├─→ for each empty_square in board:
  │     for each piece with count > 0:
  │       │
  │       ├─→ new_state = place_piece(state, piece, row, col)
  │       │
  │       ├─→ new_solution = solution + [(piece, row, col)]
  │       │
  │       ├─→ result = dfs_search(new_state, king_pos, True, new_solution)  ← RECURSE
  │       │
  │       └─→ if result not empty:
  │             return result  ← SOLUTION FOUND IN SUBTREE
  │
  └─→ return []  ← NO SOLUTION IN ANY BRANCH
```

---

## Performance Characteristics

### Time Complexity
- **Worst case:** O(b^d) where:
  - b = branching factor ≈ (empty_squares × piece_types)
  - d = depth = number of pieces to place
- **Our example:** ~15 × 2 branching, depth 2 → up to 210 states

### Space Complexity
- **Stack depth:** O(d) - maximum recursion depth equals number of pieces
- **State storage:** O(d) - solution path grows with depth

### When DFS Works Well
✅ Small number of pieces
✅ Solutions exist early in search tree
✅ Board has many constraints (few legal moves)

### When DFS Struggles
❌ Many pieces to place (large depth)
❌ Large boards (high branching factor)
❌ Solution requires specific ordering deep in tree
❌ Many equivalent states (no visited tracking)

---

## Comparison: DFS vs A* in solver.py

| Aspect | DFS | A* (astar_search) |
|--------|-----|-------------------|
| **Strategy** | Depth-first exploration | Best-first (guided by heuristic) |
| **Visited tracking** | None (explores duplicate states) | Yes (visited set of board strings) |
| **Ordering** | Arbitrary (loop order) | Priority queue by f = g + h |
| **Early exit** | First solution found | First solution found |
| **Memory** | O(depth) stack | O(visited states) heap + set |
| **Best for** | Small search spaces | Guided search with good heuristic |

---

## Suggested Improvements

1. **Add visited tracking to DFS:**
   ```python
   visited = set()
   board_key = board_to_string(state.board, king_pos)
   if board_key in visited:
       return []
   visited.add(board_key)
   ```

2. **Move ordering heuristic:**
   Place pieces closer to king first, or try attacking pieces (R, Q) before non-attacking (P).

3. **Iterative deepening:**
   Try DFS with max_depth=1, then 2, then 3... to find shortest solutions.

4. **Memoization:**
   Cache results for (board_state, remaining_pieces) → solution.

---

## Summary

DFS explores the placement space by:
1. **Trying one placement** (e.g., Rook at some position)
2. **Recursing** to place remaining pieces
3. **Checking goal** at each level (is King in check?)
4. **Backtracking** when branch fails
5. **Returning immediately** when solution found

It's simple and complete (will find a solution if one exists), but can be slow for large search spaces due to exploring many redundant paths.
