#!/usr/bin/env python3
"""
Test suite for Issue #1: A* line-of-sight blocking
Verifies that checkmate_astar correctly handles blocked sliding pieces.
"""

import sys
sys.path.insert(0, 'Back')
from checkmate import checkmate_astar

def test_blocked_rook_vertical():
    """Rook blocked by Pawn on same column"""
    print("Test 1: Blocked Rook (vertical)")
    board = """
K . . . . . . .
P . . . . . . .
R . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0)")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_blocked_rook_horizontal():
    """Rook blocked by Pawn on same row"""
    print("Test 2: Blocked Rook (horizontal)")
    board = """
K P R . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0)")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_unblocked_rook():
    """Rook with clear path to King"""
    print("Test 3: Unblocked Rook")
    board = """
K . . R . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (True, threat > 0)")
    assert result[0] == True and result[1] > 0, f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_blocked_bishop_diagonal():
    """Bishop blocked by Pawn on diagonal"""
    print("Test 4: Blocked Bishop (diagonal)")
    board = """
K . . . . . . .
. P . . . . . .
. . B . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0)")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_unblocked_bishop():
    """Bishop with clear diagonal path to King"""
    print("Test 5: Unblocked Bishop")
    board = """
K . . . . . . .
. . . . . . . .
. . B . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (True, threat > 0)")
    assert result[0] == True and result[1] > 0, f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_blocked_queen_vertical():
    """Queen blocked vertically"""
    print("Test 6: Blocked Queen (vertical)")
    board = """
K . . . . . . .
P . . . . . . .
Q . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0)")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_blocked_queen_diagonal():
    """Queen blocked on diagonal"""
    print("Test 7: Blocked Queen (diagonal)")
    board = """
K . . . . . . .
. P . . . . . .
. . Q . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0)")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_unblocked_queen():
    """Queen with clear path to King"""
    print("Test 8: Unblocked Queen (horizontal)")
    board = """
K . . Q . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (True, threat > 0)")
    assert result[0] == True and result[1] > 0, f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_pawn_not_affected():
    """Pawn attacks are not affected by blocking (no path checking)"""
    print("Test 9: Pawn attack (no blocking check needed)")
    board = """
K . . . . . . .
P . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0) - Pawn not in attack position")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")
    
    print("Test 10: Pawn in attack position")
    board = """
. K . . . . . .
P . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (True, threat > 0)")
    assert result[0] == True and result[1] > 0, f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_multiple_blockers():
    """Multiple pieces blocking the path"""
    print("Test 11: Multiple blockers")
    board = """
K . . . . . . .
P . . . . . . .
P . . . . . . .
R . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (False, 0)")
    assert result == (False, 0), f"Failed! Got {result}"
    print("  ✓ PASSED\n")

def test_edge_case_adjacent_piece():
    """Piece immediately adjacent to King (no cells in between)"""
    print("Test 12: Adjacent Rook (no cells to block)")
    board = """
K R . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
"""
    result = checkmate_astar(board)
    print(f"  Result: {result}")
    print(f"  Expected: (True, threat > 0)")
    assert result[0] == True and result[1] > 0, f"Failed! Got {result}"
    print("  ✓ PASSED\n")

if __name__ == "__main__":
    print("=" * 60)
    print("Testing Issue #1: A* Line-of-Sight Blocking")
    print("=" * 60 + "\n")
    
    try:
        test_blocked_rook_vertical()
        test_blocked_rook_horizontal()
        test_unblocked_rook()
        test_blocked_bishop_diagonal()
        test_unblocked_bishop()
        test_blocked_queen_vertical()
        test_blocked_queen_diagonal()
        test_unblocked_queen()
        test_pawn_not_affected()
        test_multiple_blockers()
        test_edge_case_adjacent_piece()
        
        print("=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print("\n" + "=" * 60)
        print(f"✗ TEST FAILED: {e}")
        print("=" * 60)
        sys.exit(1)
