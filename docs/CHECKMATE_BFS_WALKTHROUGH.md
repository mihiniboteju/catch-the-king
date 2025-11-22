# BFS in checkmate(): Concise Walkthrough

## Purpose
The `checkmate()` function uses **Breadth-First Search (BFS)** to detect if the King is under attack by exploring the board layer by layer from the King's position.

---

## Example Scenario

### Board Setup
```
Board: 8x8
. . . . . . . .   Row 0
. . B . . . . .   Row 1 ← Bishop at (1,2)
. . . . . . . .   Row 2
. . . . . . . .   Row 3
. . . . K . . R   Row 4 ← King at (4,4), Rook at (4,7)
. . . . . . . .   Row 5
. . . P . . . .   Row 6 ← Pawn at (6,3)
. . . . . . . .   Row 7
```

**Enemies:**
- Rook at (4,7) - same row as King
- Bishop at (1,2) - on diagonal with King
- Pawn at (6,3) - not in attack position

---

## How BFS Works

### Core Idea
BFS expands from the King's position **level by level** (like ripples in water), checking each cell to see if it contains an attacking piece.

### Algorithm Steps

**1. Initialize Queue**
```python
from collections import deque

queue = deque([(ky, kx)])  # Start at King position (4,4)
visited = set()
visited.add((ky, kx))
```

**2. BFS Loop**
```python
while queue:
    y, x = queue.popleft()  # Process cells in FIFO order
    
    # Check all 8 directions from current cell
    for dy, dx in [(-1,0), (1,0), (0,-1), (0,1), 
                   (-1,-1), (-1,1), (1,-1), (1,1)]:
        ny, nx = y + dy, x + dx
        
        if valid and not visited:
            visited.add((ny, nx))
            piece = board[ny][nx]
            
            # If enemy piece found, check if it attacks King
            if piece in ('Q', 'R', 'B', 'P'):
                if is_piece_attacking_king(piece, (ny, nx), (ky, kx), board):
                    return True  # King in check!
            
            # Add empty cells to queue for further exploration
            if piece == '.':
                queue.append((ny, nx))

return False  # No attacking pieces found
```

---

## Step-by-Step Trace

### Level 0: Start at King (4,4)
```
Queue: [(4,4)]
Visited: {(4,4)}
```

### Level 1: Explore 8 Neighbors
```
Process (4,4) → Check neighbors:
  (3,4), (5,4), (4,3), (4,5), (3,3), (3,5), (5,3), (5,5)

Pieces found:
  (4,5) = '.' → Add to queue
  (4,3) = '.' → Add to queue
  (3,4) = '.' → Add to queue
  ... all empty → Add to queue

Queue: [(4,5), (4,3), (3,4), (5,4), (3,3), (3,5), (5,3), (5,5)]
Visited: {(4,4) + all 8 neighbors}
```

### Level 2: Process (4,5)
```
Dequeue (4,5)
Check neighbors: (3,5), (5,5), (4,4)✗visited, (4,6), ...

(4,6) = '.' → Add to queue
(3,5) already visited ✗
... continue

Queue: [(4,3), (3,4), (5,4), ..., (4,6)]
```

### Level 3: Process (4,6)
```
Eventually dequeue (4,6)
Check neighbor (4,7):

(4,7) = 'R'  ← Rook found!

Check if Rook attacks King:
  is_piece_attacking_king('R', (4,7), (4,4), board)
  - Same row? YES (4 == 4) ✓
  - Clear path from (4,7) to (4,4)?
    Check cells: (4,6), (4,5) → Both empty ✓
  
  → Rook ATTACKS King!

return True  ← KING IN CHECK!
```

---

## Visual BFS Expansion

```
Level-by-level expansion (numbers show BFS level):

. . . . . . . .
. . B . . . . .
. . . 3 3 3 3 .
. . 3 2 2 2 2 3
. . 3 2 1 1 1 2 R  ← Rook found at level 3
. . 3 2 1 1 1 2
. . . 3 2 2 2 3
. . . . 3 3 3 .

Expansion order:
Level 0: King (4,4)
Level 1: 8 neighbors around King
Level 2: All cells 2 steps away
Level 3: Rook at (4,7) found ✓
```

---

## Why BFS (Not DFS)?

| Aspect | BFS | DFS |
|--------|-----|-----|
| **Exploration** | Layer by layer | Depth first |
| **Find nearest** | ✓ Always finds closest | ✗ May find farther first |
| **Order** | FIFO (queue) | LIFO (stack) |
| **Use case** | Shortest path, nearest target | Exhaustive search |

For detecting check, BFS finds the **closest attacking piece** naturally!

---

## Key Function: `is_piece_attacking_king()`

This shared function checks if a piece attacks the King:

```python
def is_piece_attacking_king(piece, piece_pos, king_pos, board):
    py, px = piece_pos
    ky, kx = king_pos
    
    # Pawn: diagonal attack
    if piece == 'P':
        return (py == ky + 1 and abs(px - kx) == 1)
    
    # Rook: horizontal/vertical with clear path
    if piece == 'R':
        if (py == ky or px == kx):
            return has_clear_path(board, py, px, ky, kx)
        return False
    
    # Bishop: diagonal with clear path
    if piece == 'B':
        if abs(py - ky) == abs(px - kx):
            return has_clear_path(board, py, px, ky, kx)
        return False
    
    # Queen: combines Rook + Bishop
    if piece == 'Q':
        if (py == ky or px == kx or abs(py - ky) == abs(px - kx)):
            return has_clear_path(board, py, px, ky, kx)
        return False
```

**Key:** Uses `has_clear_path()` to check for blocking pieces (Issue #2 fix!)

---

## Complete Example Output

### Example 1: Rook Attacks
```
Board: K . . R

BFS expansion:
  Level 0: K
  Level 1: cells around K
  Level 2: cells 2 away
  Level 3: Rook found → Attacks? YES ✓

Result: True
```

### Example 2: Blocked Rook
```
Board: K . P . R

BFS expansion:
  Level 0: K
  Level 1: empty cells
  Level 2: Pawn found → Attacks? NO (not in position)
  Level 3: Rook found → Attacks? NO ✗ (Pawn blocks path)

Result: False
```

### Example 3: No Threats
```
Board: K . . .
       . . . .
       . . . R  ← Not aligned

BFS explores entire board → No attacks found

Result: False
```

---

## Performance

**Time Complexity:** O(n) where n = board size
- BFS visits each cell at most once
- Early termination when attack found

**Space Complexity:** O(n)
- Queue stores unprocessed cells
- Visited set stores seen cells

**Average Case:** Much faster than O(n) due to early termination!

---

## BFS vs A* in checkmate.py

| Feature | BFS (checkmate) | A* (checkmate_astar) |
|---------|-----------------|----------------------|
| **Algorithm** | Breadth-First | A* with heuristic |
| **Priority** | None (FIFO) | f = g + h |
| **Finds** | Any attacking piece | Closest attacking piece |
| **Return** | True/False | (True/False, threat_level) |
| **Efficiency** | Good | Better (guided search) |

**When to use:**
- `checkmate()`: Simple check detection
- `checkmate_astar()`: Need threat level (distance-based score)

---

## Summary

BFS in `checkmate()`:
1. **Starts** at King position
2. **Expands** level by level (8 directions)
3. **Checks** each enemy piece for attack
4. **Uses** `is_piece_attacking_king()` with line-of-sight
5. **Returns** `True` immediately when attack found
6. **Returns** `False` if no attacks after full exploration

**Simple, efficient, and naturally finds nearest threats!** 🎯
