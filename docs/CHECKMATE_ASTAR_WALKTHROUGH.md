# A* in checkmate_astar(): Concise Walkthrough

## Purpose

Uses **A* search** to:
1. Detect if King is in check
2. Calculate **threat level** (0-100) based on attacker's distance

**Key difference from solver A*:** Expands from King's position in **board space** to find nearest attacking piece (not placing pieces in state space).

---

## Example Setup

```
Board: 8x8
. B . . . . . .   Row 0
. . . . . . . .   Row 1
. . . P . . . .   Row 2
. . . . . . . .   Row 3
. . . . K . . R   Row 4 ← King (4,4), Rook (4,7)
. . . . . . . .   Row 5
. . . P . . . .   Row 6
. . . . . . . .   Row 7

Enemies:
- Rook at (4,7) - same row, 3 squares away
- Bishop at (1,1) - diagonal
- Pawn at (2,3) - not attacking
```

---

## Algorithm Steps

### 1. Setup
```python
# Find King and all enemy pieces
king_pos = (4, 4)
enemies = [(1,1,'B'), (2,3,'P'), (4,7,'R')]

# Heuristic: Euclidean distance to nearest enemy
def heuristic(y, x):
    return min(math.hypot(y - ey, x - ex) for ey, ex, _ in enemies)
```

### 2. Initialize A*
```python
# Priority queue: (f, g, position)
open_set = [(h(King), 0, King_pos)]  # f=2.24, g=0
visited = set()
```

### 3. A* Search Loop
```python
while open_set:
    f, g, (y, x) = heapq.heappop(open_set)
    
    if visited: continue
    visited.add((y, x))
    
    piece = board[y][x]
    
    # Check if enemy piece attacks King
    if piece in ('Q','R','B','P'):
        if is_piece_attacking_king(piece, (y,x), King_pos, board):
            min_distance = g
            break  # Attack found!
    
    # Expand to 8 neighbors
    for each neighbor (ny, nx):
        new_g = g + 1
        new_f = new_g + heuristic(ny, nx)
        heapq.heappush(open_set, (new_f, new_g, (ny, nx)))
```

### 4. Result
```python
# After finding Rook at distance g=3:
threat_level = max(0, 100 - 3 * 15) = 55
return (True, 55)
```

---

## Visual Search Expansion

```
A* expands from King, guided by heuristic toward enemies:

. B . . . . . .
. . . . . . . .
. . . P 2 2 2 .
. . . 2 1 1 1 2
. . . 2 1 K→1→1→R  ← Rook found at g=3
. . . 2 1 1 1 2
. . . . 2 2 2 .
. . . . . . . .

Numbers show g-value (steps from King)
Path to Rook: (4,4) → (4,5) → (4,6) → (4,7)
```

---

## Heuristic Function

```python
def heuristic(y, x):
    return min(math.hypot(y - ey, x - ex) for ey, ex, _ in enemies)
```

**Why Euclidean Distance?**
- **Admissible:** Never overestimates (A* finds optimal)
- **Guides search** toward nearest enemies first
- **Smooth gradient** for diagonal moves

**Example:**
```
From (4,4) to Rook (4,7):
h = √[(4-4)² + (4-7)²] = √9 = 3.0

From (4,5) to Rook (4,7):  
h = √[(4-4)² + (5-7)²] = √4 = 2.0  ← Closer, lower h
```

---

## Threat Level Formula

```python
threat_level = max(0, 100 - distance * 15)
```

| Distance | Calculation | Threat | Meaning |
|----------|-------------|--------|---------|
| 1 | 100 - 15 | **85** | Adjacent - Critical! |
| 2 | 100 - 30 | **70** | Very close |
| 3 | 100 - 45 | **55** | Close - Medium |
| 4 | 100 - 60 | **40** | Medium |
| 5 | 100 - 75 | **25** | Far |
| 7+ | 100 - 105+ | **0** | Very far (capped) |

**In our example:** Rook at distance 3 → Threat = 55

---

## Key Differences: Checkmate A* vs Solver A*

| Aspect | checkmate_astar() | solver astar_search() |
|--------|-------------------|----------------------|
| **Start** | King position | Empty board |
| **Goal** | Find attacking piece | Find checkmate state |
| **Space** | Board positions | Piece placement states |
| **g (cost)** | Steps from King | # pieces placed |
| **h (heuristic)** | Distance to enemy | Threat score (negative) |
| **Return** | (bool, threat_level) | Placement path |

---

## Performance

**Time Complexity:**
- Best: O(1) - Attacker adjacent
- Average: O(n) - n = squares in attack range
- Worst: O(n²) - Full board (no attack)

**Space Complexity:** O(n) for open_set and visited

**Why A* is Efficient:**
- Heuristic guides toward enemies
- Early termination when attack found
- Avoids exploring distant areas

---

## Summary

`checkmate_astar()` uses A* to:
1. **Expand** from King position outward
2. **Guided** by Euclidean distance to nearest enemy
3. **Check** each piece for attack capability
4. **Stop** when attacking piece found
5. **Return** (is_check, threat_level) based on distance

**Result:** Efficiently finds nearest attacker and scores threat by proximity! 🎯
