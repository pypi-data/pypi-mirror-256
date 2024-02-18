def auto_coordinates(grid):
    size = grid.shape
    for x in range(size[0]):
        for y in range(size[1]):
            for z in range(size[2]):
                if grid[x, y, z] is None:
                    return (x, y, z)
    return (size[0]-1, size[1]-1, size[2]-1)
