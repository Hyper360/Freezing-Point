from modules.grid import Grid
from modules.vector import *
from modules.settings import *
#This file will just contain a bunch of helper functions for the A* algorithm

testGrid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

class Node(Vector2I):
    def __init__(self, x : int, y : int, fcost : float, parent = None):
        Vector2I.__init__(self, x, y)
        self.parent = parent
        self.fCost = fcost
    
    def toVector2F(self):
        return Vector2F(self.x, self.y)

def getValidNeighbors(grid : list[list], rows : int, cols : int, originalPos: Vector2I, startPos : Node, endPos : Vector2I, closedNodes : dict[tuple[int, int], Node]) -> list[Node]:
    validNodes = []
    positions = [(startPos.x - 1, startPos.y),
                 (startPos.x, startPos.y + 1),
                 (startPos.x, startPos.y - 1),
                 (startPos.x + 1, startPos.y)
    ]

    for tup in positions:
        x = tup[0]
        y = tup[1]
        if x > 0 and x < cols and y > 0 and y < rows and (grid[y][x] == 0 or grid[y][x] == 8):
            gcost = getDistance(originalPos, Vector2I(x, y)) # Distance from neighbor to starting position
            hcost = getDistance(Vector2I(x, y), endPos) # Distance from neighbor to end goal
            finalNode = Node(x, y, gcost+hcost, parent=startPos)
            
            # Handle cases like if we already visited this node
            if ((x, y) in validNodes):
                if validNodes[(x, y)].fCost > finalNode.fCost:
                    validNodes[(x, y)].fCost = finalNode.fCost
            elif ((x, y) in closedNodes):
                if closedNodes[(x, y)].fCost > finalNode.fCost:
                    validNodes.append(finalNode)
                    closedNodes.pop((x, y))
            else:
                validNodes.append(finalNode)
    
    
    return validNodes

def sortNodes(nodes : list[Node]):
    # Using quicksort!!! very fast speed, we are going to the moon!!!
    # Ex. a seemingly small 10x10 grid can have up to 100 possible nodes (gets exponentially larger too, as the dimensions increases)
    if len(nodes) <= 1:
        return nodes
    else:
        l = len(nodes) // 2
        pivot = nodes[l]
        left = [x for x in nodes if x.fCost < pivot.fCost]
        right = [x for x in nodes if x.fCost > pivot.fCost]

        return sortNodes(left) + [pivot] + sortNodes(right)

def getPath(node : Node) -> list[Vector2F]:
    path = []
    # We add 0.5 so the entity moves to the center of the cell
    path.append(vectorAddF(node.toVector2F(), 0.5))
    while node.parent:
        node = node.parent
        path.append(vectorAddF(node.toVector2F(), 0.5))
    path.pop(-1)

    return path

def aStar(grid : list[list], p1 : Vector2F, p2 : Vector2F) -> list[Vector2F]:
    # I am using the A* method here. First I need to get the grid coordinates of the points
    pos1 = Node(p1.x, p1.y, inf)
    pos2 = Vector2I().fromVector2F(p2)

    rows = len(grid)
    cols = len(grid[0])

    # First we will create the open and closed lists
    # Open list contains all the Nodes that were not visited
    # Closed list contains all the Nodes that were visited
    openNodes = []
    closedNodes = {}
    
    openNodes.extend(getValidNeighbors(grid, rows, cols, pos1, pos1, pos2, closedNodes))
    openNodes = sortNodes(openNodes)

    while len(openNodes) > 0:
        bestNode = openNodes.pop(0)
        if bestNode.x == pos2.x and bestNode.y == pos2.y:
            #print(f"Nodes Open: {len(openNodes)} | Nodes Closed: {len(closedNodes)}")
            return getPath(bestNode)
        
        openNodes.extend(getValidNeighbors(grid, rows, cols, pos1, bestNode, pos2, closedNodes))
        openNodes = sortNodes(openNodes)

        closedNodes[(bestNode.x, bestNode.y)] = bestNode
    
    return []

