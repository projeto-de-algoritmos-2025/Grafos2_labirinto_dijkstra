import heapq
import random
from disjoint_set import DisjointSet

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[width * row + col for col in range(width)] for row in range(height)]
        self.portals = {}
        self.generate_maze()
        self.player_pos = [1, 1]
        self.target_pos = [height - 2, width - 2]
        self.distance_map = {}
        self.max_distance = 1

    def generate_maze(self):
        edges = []
        for row in range(self.height):
            for col in range(self.width):
                cell = (row, col)
                if col > 0:
                    edges.append(((row, col - 1), cell))
                if row > 0:
                    edges.append(((row - 1, col), cell))

        random.shuffle(edges)
        disjoint_set = DisjointSet()

        for row in range(self.height):
            for col in range(self.width):
                key = self.grid[row][col]
                disjoint_set.make_set(key)
                self.portals[key] = {}

        edge_count = 0
        key_count = self.width * self.height

        while edge_count < key_count and edges:
            (r1, c1), (r2, c2) = edges.pop()
            key_a = self.grid[r1][c1]
            key_b = self.grid[r2][c2]
            if disjoint_set.find(key_a) != disjoint_set.find(key_b):
                self.portals[key_a][key_b] = True
                self.portals[key_b][key_a] = True
                disjoint_set.union(disjoint_set.find(key_a), disjoint_set.find(key_b))
                edge_count += 1

    def dijkstra(self):
        self.distance_map = {}
        heap = []
        for row in range(self.height):
            for col in range(self.width):
                self.distance_map[(row, col)] = float('inf')
        self.distance_map[tuple(self.target_pos)] = 0
        heapq.heappush(heap, (0, *self.target_pos))

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while heap:
            dist, row, col = heapq.heappop(heap)
            key = self.grid[row][col]
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.height and 0 <= nc < self.width:
                    neighbor_key = self.grid[nr][nc]
                    if neighbor_key in self.portals[key]:
                        new_dist = dist + 1
                        if new_dist < self.distance_map[(nr, nc)]:
                            self.distance_map[(nr, nc)] = new_dist
                            heapq.heappush(heap, (new_dist, nr, nc))

        self.max_distance = max((v for v in self.distance_map.values() if v != float('inf')), default=1)

    def get_direction_color(self, direction):
        row, col = self.player_pos
        dr, dc = direction
        nr, nc = row + dr, col + dc

        if not (0 <= nr < self.height and 0 <= nc < self.width):
            return (200, 200, 200)

        key = self.grid[row][col]
        neighbor_key = self.grid[nr][nc]

        if neighbor_key not in self.portals[key]:
            return (200, 200, 200)

        min_distance = float('inf')
        best_direction = None
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dir_row, dir_col in directions:
            new_row, new_col = row + dir_row, col + dir_col
            if (0 <= new_row < self.height and 0 <= new_col < self.width and 
                self.grid[new_row][new_col] in self.portals[key]):
                dist = self.distance_map.get((new_row, new_col), float('inf'))
                if dist < min_distance:
                    min_distance = dist
                    best_direction = (dir_row, dir_col)

        if (dr, dc) == best_direction:
            return (255, 100, 100)
        else:
            return (100, 100, 255)

    def move_player(self, direction):
        row, col = self.player_pos
        dr, dc = direction
        nr, nc = row + dr, col + dc

        if 0 <= nr < self.height and 0 <= nc < self.width:
            key = self.grid[row][col]
            neighbor_key = self.grid[nr][nc]
            if neighbor_key in self.portals[key]:
                self.player_pos = [nr, nc]
                return True
        return False