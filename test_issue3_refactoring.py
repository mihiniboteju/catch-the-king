"""
Test suite for Issue #3: Refactored shared functions
Tests the module-level helper functions
"""

import sys
sys.path.append('Back')
from checkmate import has_clear_path, is_piece_attacking_king, checkmate, checkmate_astar


# ============================================================================
# Test has_clear_path()
# ============================================================================

def test_has_clear_path_blocked_vertical():
    """Test vertical path with blocker"""
    board = [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['R', '.', '.', '.'],  # Rook at (2,0)
        ['.', '.', '.', '.'],
        ['P', '.', '.', '.'],  # Pawn at (4,0) blocks
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['K', '.', '.', '.']   # King at (7,0)
    ]
    
    assert has_clear_path(board, 2, 0, 7, 0) == False
    print("✓ Test passed: has_clear_path - blocked vertical")


def test_has_clear_path_clear_vertical():
    """Test vertical path without blocker"""
    board = [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['R', '.', '.', '.'],  # Rook at (2,0)
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['K', '.', '.', '.']   # King at (7,0)
    ]
    
    assert has_clear_path(board, 2, 0, 7, 0) == True
    print("✓ Test passed: has_clear_path - clear vertical")


def test_has_clear_path_blocked_horizontal():
    """Test horizontal path with blocker"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['Q', '.', 'P', '.', '.', '.', 'K', '.'],  # Q at (4,0), P blocks at (4,2), K at (4,6)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert has_clear_path(board, 4, 0, 4, 6) == False
    print("✓ Test passed: has_clear_path - blocked horizontal")


def test_has_clear_path_clear_horizontal():
    """Test horizontal path without blocker"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['Q', '.', '.', '.', '.', '.', 'K', '.'],  # Q at (4,0), K at (4,6)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert has_clear_path(board, 4, 0, 4, 6) == True
    print("✓ Test passed: has_clear_path - clear horizontal")


def test_has_clear_path_blocked_diagonal():
    """Test diagonal path with blocker"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'B', '.', '.', '.', '.', '.'],  # Bishop at (2,2)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'P', '.', '.', '.'],  # Pawn at (4,4) blocks
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', 'K', '.'],  # King at (6,6)
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert has_clear_path(board, 2, 2, 6, 6) == False
    print("✓ Test passed: has_clear_path - blocked diagonal")


def test_has_clear_path_clear_diagonal():
    """Test diagonal path without blocker"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'B', '.', '.', '.', '.', '.'],  # Bishop at (2,2)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', 'K', '.'],  # King at (6,6)
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert has_clear_path(board, 2, 2, 6, 6) == True
    print("✓ Test passed: has_clear_path - clear diagonal")


# ============================================================================
# Test is_piece_attacking_king()
# ============================================================================

def test_is_piece_attacking_king_pawn_attacking():
    """Test pawn attacking king"""
    board = [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.', 'K', '.', '.', '.'],  # King at (5,4)
        ['.', '.', '.', 'P', '.', '.', '.', '.'],  # Pawn at (6,3)
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert is_piece_attacking_king('P', (6, 3), (5, 4), board) == True
    print("✓ Test passed: is_piece_attacking_king - pawn attacking")


def test_is_piece_attacking_king_pawn_not_attacking():
    """Test pawn not attacking king"""
    board = [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.', 'K', '.', '.', '.'],  # King at (5,4)
        ['.', '.', 'P', '.', '.', '.', '.', '.'],  # Pawn at (6,2) - too far
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert is_piece_attacking_king('P', (6, 2), (5, 4), board) == False
    print("✓ Test passed: is_piece_attacking_king - pawn not attacking")


def test_is_piece_attacking_king_rook_blocked():
    """Test rook blocked by another piece"""
    board = [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['R', '.', '.', '.'],  # Rook at (2,0)
        ['.', '.', '.', '.'],
        ['P', '.', '.', '.'],  # Pawn at (4,0) blocks
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['K', '.', '.', '.']   # King at (7,0)
    ]
    
    assert is_piece_attacking_king('R', (2, 0), (7, 0), board) == False
    print("✓ Test passed: is_piece_attacking_king - rook blocked")


def test_is_piece_attacking_king_rook_attacking():
    """Test rook with clear path to king"""
    board = [
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['R', '.', '.', '.'],  # Rook at (2,0)
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['.', '.', '.', '.'],
        ['K', '.', '.', '.']   # King at (7,0)
    ]
    
    assert is_piece_attacking_king('R', (2, 0), (7, 0), board) == True
    print("✓ Test passed: is_piece_attacking_king - rook attacking")


def test_is_piece_attacking_king_bishop_blocked():
    """Test bishop blocked by another piece"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'B', '.', '.', '.', '.', '.'],  # Bishop at (2,2)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', 'P', '.', '.', '.'],  # Pawn at (4,4) blocks
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', 'K', '.'],  # King at (6,6)
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert is_piece_attacking_king('B', (2, 2), (6, 6), board) == False
    print("✓ Test passed: is_piece_attacking_king - bishop blocked")


def test_is_piece_attacking_king_bishop_attacking():
    """Test bishop with clear path to king"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', 'B', '.', '.', '.', '.', '.'],  # Bishop at (2,2)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', 'K', '.'],  # King at (6,6)
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert is_piece_attacking_king('B', (2, 2), (6, 6), board) == True
    print("✓ Test passed: is_piece_attacking_king - bishop attacking")


def test_is_piece_attacking_king_queen_blocked():
    """Test queen blocked by another piece"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['Q', '.', 'P', '.', '.', '.', 'K', '.'],  # Q at (4,0), P blocks at (4,2), K at (4,6)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert is_piece_attacking_king('Q', (4, 0), (4, 6), board) == False
    print("✓ Test passed: is_piece_attacking_king - queen blocked")


def test_is_piece_attacking_king_queen_attacking():
    """Test queen with clear path to king"""
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['Q', '.', '.', '.', '.', '.', 'K', '.'],  # Q at (4,0), K at (4,6)
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    
    assert is_piece_attacking_king('Q', (4, 0), (4, 6), board) == True
    print("✓ Test passed: is_piece_attacking_king - queen attacking")


def test_bfs_astar_consistency():
    """Test that BFS and A* give consistent in_check results"""
    test_boards = [
        # Unblocked Rook
        "........\n........\nR.......\n........\n........\n........\n........\nK.......",
        # Blocked Rook
        "........\n........\nR.......\n........\nP.......\n........\n........\nK.......",
        # Unblocked Bishop
        "........\n........\n..B.....\n........\n........\n........\n......K.\n........",
        # Blocked Bishop
        "........\n........\n..B.....\n........\n....P...\n........\n......K.\n........",
        # Pawn attack
        "........\n........\n........\n........\n........\n....K...\n...P....\n........",
    ]
    
    for i, board_str in enumerate(test_boards):
        bfs_check = checkmate(board_str)
        astar_check, _ = checkmate_astar(board_str)
        assert bfs_check == astar_check, f"Board {i+1}: BFS and A* should agree on check status"
    
    print("✓ Test passed: BFS and A* consistency")


if __name__ == "__main__":
    print("\n=== Testing Issue #3: Refactored Shared Functions ===\n")
    
    # Test has_clear_path()
    print("--- Testing has_clear_path() ---")
    test_has_clear_path_blocked_vertical()
    test_has_clear_path_clear_vertical()
    test_has_clear_path_blocked_horizontal()
    test_has_clear_path_clear_horizontal()
    test_has_clear_path_blocked_diagonal()
    test_has_clear_path_clear_diagonal()
    
    # Test is_piece_attacking_king()
    print("\n--- Testing is_piece_attacking_king() ---")
    test_is_piece_attacking_king_pawn_attacking()
    test_is_piece_attacking_king_pawn_not_attacking()
    test_is_piece_attacking_king_rook_blocked()
    test_is_piece_attacking_king_rook_attacking()
    test_is_piece_attacking_king_bishop_blocked()
    test_is_piece_attacking_king_bishop_attacking()
    test_is_piece_attacking_king_queen_blocked()
    test_is_piece_attacking_king_queen_attacking()
    
    # Test BFS and A* consistency
    print("\n--- Testing BFS and A* consistency ---")
    test_bfs_astar_consistency()
    
    print("\n=== All Issue #3 tests passed! ===\n")
