"""
Test suite for Issue #2: BFS line-of-sight blocking fix
Tests that checkmate() correctly handles blocked sliding pieces
"""

import sys
sys.path.append('Back')
from checkmate import checkmate

def board_to_string(board):
    """Convert 2D list to string format expected by checkmate()"""
    return '\n'.join([''.join(row) for row in board])

def test_blocked_rook_vertical():
    """
    Test: Rook blocked vertically by a Pawn
    Board:
        . . . . . . . .
        . . . . . . . .
        R . . . . . . .  <- Rook at (2,0)
        . . . . . . . .
        P . . . . . . .  <- Pawn at (4,0) BETWEEN Rook and King
        . . . . . . . .
        . . . . . . . .
        K . . . . . . .  <- King at (7,0)
    
    Expected: King is NOT in check (Rook is blocked)
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['R', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['P', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['K', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == False, "Rook should be blocked by Pawn - King NOT in check"
    print("✓ Test passed: Blocked Rook (vertical)")

def test_unblocked_rook_vertical():
    """
    Test: Rook with clear path vertically
    Board:
        . . . . . . . .
        . . . . . . . .
        R . . . . . . .  <- Rook at (2,0) with clear path
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        K . . . . . . .  <- King at (7,0)
    
    Expected: King IS in check
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['R', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['K', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == True, "Rook has clear path - King in check"
    print("✓ Test passed: Unblocked Rook (vertical)")

def test_blocked_bishop_diagonal():
    """
    Test: Bishop blocked diagonally
    Board:
        . . . . . . . .
        . . . . . . . .
        . . B . . . . .  <- Bishop at (2,2)
        . . . . . . . .
        . . . . P . . .  <- Pawn at (4,4) blocks Bishop
        . . . . . . . .
        . . . . . . K .  <- King at (6,6)
        . . . . . . . .
    
    Expected: King is NOT in check (Bishop is blocked)
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'B', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'P', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', 'K', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == False, "Bishop should be blocked by Pawn - King NOT in check"
    print("✓ Test passed: Blocked Bishop (diagonal)")

def test_unblocked_bishop_diagonal():
    """
    Test: Bishop with clear diagonal path
    Board:
        . . . . . . . .
        . . . . . . . .
        . . B . . . . .  <- Bishop at (2,2) with clear path
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . K .  <- King at (6,6)
        . . . . . . . .
    
    Expected: King IS in check
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'B', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', 'K', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == True, "Bishop has clear path - King in check"
    print("✓ Test passed: Unblocked Bishop (diagonal)")

def test_blocked_queen_horizontal():
    """
    Test: Queen blocked horizontally
    Board:
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        Q . P . . . K .  <- Queen at (4,0), blocked by Pawn at (4,2), King at (4,6)
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
    
    Expected: King is NOT in check (Queen is blocked)
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['Q', '.', 'P', '.', '.', '.', 'K', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == False, "Queen should be blocked by Pawn - King NOT in check"
    print("✓ Test passed: Blocked Queen (horizontal)")

def test_unblocked_queen_horizontal():
    """
    Test: Queen with clear horizontal path
    Board:
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        Q . . . . . K .  <- Queen at (4,0), King at (4,6)
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
    
    Expected: King IS in check
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['Q', '.', '.', '.', '.', '.', 'K', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == True, "Queen has clear path - King in check"
    print("✓ Test passed: Unblocked Queen (horizontal)")

def test_pawn_attack_not_affected():
    """
    Test: Pawn attacks are NOT affected by blocking (one-square diagonal only)
    Board:
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . . . . .
        . . . . K . . .  <- King at (5,4)
        . . . P . . . .  <- Pawn at (6,3) - one row below King, one column left
        . . . . . . . .
    
    Expected: King IS in check (Pawn attack is one square diagonal, no blocking)
    """
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'K', '.', '.', '.'],
        ['.', '.', '.', 'P', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    result = checkmate(board_to_string(board))
    assert result == True, "Pawn attacks King directly (one square)"
    print("✓ Test passed: Pawn attack (no blocking needed)")

if __name__ == "__main__":
    print("\n=== Testing Issue #2: BFS line-of-sight blocking ===\n")
    
    test_blocked_rook_vertical()
    test_unblocked_rook_vertical()
    test_blocked_bishop_diagonal()
    test_unblocked_bishop_diagonal()
    test_blocked_queen_horizontal()
    test_unblocked_queen_horizontal()
    test_pawn_attack_not_affected()
    
    print("\n=== All tests passed! ===\n")
