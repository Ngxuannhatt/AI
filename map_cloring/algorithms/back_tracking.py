
def map_coloring_backtracking(neighbors, num_colors, callback=None):
    """
    Backtracking algorithm to find a valid assignment of colors to regions.
    neighbors: dict where keys are regions and values are lists of adjacent regions.
    num_colors: maximum number of colors allowed.
    callback: optional function called at each assignment or backtrack step.
              Signature: callback(region, color, action_type, assignment, domains)
    Returns: a dict of {region: color_id} if successful, else None.
    """
    regions = list(neighbors.keys())
    assignment = {}

    def is_valid(region, color):
        for neighbor in neighbors[region]:
            if neighbor in assignment and assignment[neighbor] == color:
                return False
        return True

    def backtrack(index):
        if index == len(regions):
            return True
        
        region = regions[index]
        for color in range(1, num_colors + 1):
            if is_valid(region, color):
                assignment[region] = color
                if callback:
                    callback(region, color, "ASSIGN", assignment.copy(), None)
                if backtrack(index + 1):
                    return True
                del assignment[region]  # Quay lui (Backtrack)
                if callback:
                    callback(region, None, "BACKTRACK", assignment.copy(), None)
        return False

    if backtrack(0):
        return assignment
    return None

def find_minimal_coloring(neighbors, callback=None):
    """
    Finds a valid coloring with the minimal number of colors required.
    Iterates the number of colors from 1 upwards until a solution is found.
    """
    # Minimum possible colors is 1 (if no regions or 1 region), but we start from 1 up to number of regions
    if not neighbors:
        return {}, 0
        
    num_regions = len(neighbors)
    for num_colors in range(1, num_regions + 1):
        solution = map_coloring_backtracking(neighbors, num_colors, callback)
        if solution is not None:
            return solution, num_colors
    return None, 0

# Example usage to demonstrate correctness:
if __name__ == "__main__":
    # Đồ thị ví dụ: 4 vùng kề nhau dạng vòng tròn hoặc tháp
    # A kề B, C, D
    # B kề A, C
    # C kề A, B, D
    # D kề A, C
    example_neighbors = {
        'A': ['B', 'C', 'D'],
        'B': ['A', 'C'],
        'C': ['A', 'B', 'D'],
        'D': ['A', 'C']
    }
    
    assignment, min_colors = find_minimal_coloring(example_neighbors)
    print(f"Số màu tối thiểu: {min_colors}")
    print(f"Phương án phân bổ: {assignment}")
