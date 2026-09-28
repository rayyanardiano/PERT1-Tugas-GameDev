import math
import heapq
import time
import sys

STATE_PATROL = "PATROL"
STATE_CHASE = "CHASE"
STATE_REACHED = "REACHED"

### Algoritma yang Digunakan

# 1. **Finite State Machine (FSM)**
#    FSM digunakan untuk mengatur perilaku dasar musuh melalui *state* atau fase. Terdapat tiga state utama:
#    - **PATROL**: Musuh diam di tempat sambil terus memindai sekeliling.
#    - **CHASE**: Musuh mendeteksi player dan akan mulai mencari jalan mendekati posisi player menggunakan algoritma pathfinding.
#    - **REACHED**: Musuh telah mencapai posisi player dan game berakhir (Game Over).

# 2. **A* Pathfinding (A-Star)**
#    Algoritma pencarian rute yang sangat optimal untuk mencari jalur terpendek dari posisi musuh menuju posisi player dengan menghindari tembok. 
#    **Alasan Memilih A*:**
#    A* menggabungkan keunggulan algoritma Dijkstra (menjamin rute terpendek) dan Greedy Best-First-Search (cepat karena dipandu oleh heuristik). Ini membuatnya sangat efisien, cepat, dan pintar dalam memandu musuh menyusuri labirin tanpa perlu mengecek semua jalur yang tak perlu.

# 3. **Pengecekan Jarak (Distance Checks)**
#    Proyek ini menggunakan dua rumus pencarian jarak untuk keperluan berbeda:
#    - **Jarak Euclidean**: Digunakan sebagai sensor radius berbentuk lingkaran (`detection_range`). Sesuai untuk mensimulasikan batas penglihatan sesungguhnya di dunia nyata.
#    - **Jarak Manhattan**: Digunakan sebagai heuristik pada A* dan jarak serangan. Karena gerakan hanya terbatas pada 4 arah (atas, bawah, kiri, kanan), jarak langkah grid dihitung dengan Manhattan (tanpa diagonal).


class Node:
    def __init__(self, x, y, cost, heuristic, parent=None):
        self.x = x
        self.y = y
        self.cost = cost
        self.heuristic = heuristic
        self.parent = parent
        
    @property
    def f(self):
        return self.cost + self.heuristic
        
    def __lt__(self, other):
        return self.f < other.f

class Enemy:
    def __init__(self, start_x, start_y, detection_range):
        self.x = start_x
        self.y = start_y
        self.state = STATE_PATROL
        self.detection_range = detection_range
        self.path = []
        
    def _manhattan_distance(self, x1, y1, x2, y2):
        return abs(x1 - x2) + abs(y1 - y2)

    def _get_neighbors(self, node, grid):
        neighbors = []
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in directions:
            nx, ny = node.x + dx, node.y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors

    def find_path(self, target_x, target_y, grid):
        start_node = Node(self.x, self.y, 0, self._manhattan_distance(self.x, self.y, target_x, target_y))
        open_list = []
        heapq.heappush(open_list, start_node)
        
        closed_set = set()
        
        while open_list:
            current_node = heapq.heappop(open_list)
            
            if current_node.x == target_x and current_node.y == target_y:
                path = []
                while current_node.parent:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                path.reverse()
                return path
                
            closed_set.add((current_node.x, current_node.y))
            
            for nx, ny in self._get_neighbors(current_node, grid):
                if (nx, ny) in closed_set:
                    continue
                    
                g_cost = current_node.cost + 1
                h_cost = self._manhattan_distance(nx, ny, target_x, target_y)
                neighbor_node = Node(nx, ny, g_cost, h_cost, current_node)
                
                in_open = False
                for node in open_list:
                    if node.x == nx and node.y == ny and node.cost <= g_cost:
                        in_open = True
                        break
                        
                if not in_open:
                    heapq.heappush(open_list, neighbor_node)
                    
        return []

    def update(self, player_x, player_y, grid):
        dx = self.x - player_x
        dy = self.y - player_y
        d = math.sqrt(dx**2 + dy**2)
        
        if d <= self.detection_range:
            self.state = STATE_CHASE
            
            self.path = self.find_path(player_x, player_y, grid)
            
            if self.path:
                next_step = self.path[0]
                self.x, self.y = next_step[0], next_step[1]
                
                if self.x == player_x and self.y == player_y:
                    self.state = STATE_REACHED
            else:
                print("❌ Tidak ada jalur, Enemy tidak bisa bergerak")
        else:
            self.state = STATE_PATROL
            self.path = []

def print_dungeon(grid, enemy, player_x, player_y):
    display = []
    for row in grid:
        display.append(list(row))
        
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if display[y][x] == 1:
                display[y][x] = '#'
            else:
                display[y][x] = '.'
                
    for px, py in enemy.path:
        display[py][px] = '*'
            
    display[player_y][player_x] = 'P'
    display[enemy.y][enemy.x] = 'E'
    
    print("+" + "-" * (len(grid[0]) * 2 - 1) + "+")
    for row in display:
        print("|" + " ".join(row) + "|")
    print("+" + "-" * (len(grid[0]) * 2 - 1) + "+")

def main():
    dungeon_grid = [
        [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 1, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 0, 0, 0, 1, 1, 1, 0],
        [0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]
    
    enemy = Enemy(start_x=0, start_y=0, detection_range=9.0)
    player_x, player_y = 8, 6
    
    print("=== GAME START ===")
    
    for step in range(30):
        print(f"\n--- Tick {step+1} ---")
        
        if step == 12:
            player_x, player_y = 1, 6
            
        enemy.update(player_x, player_y, dungeon_grid)
        
        if enemy.state == STATE_REACHED:
            print("State: REACHED")
            print("Enemy mencapai Player!")
            print_dungeon(dungeon_grid, enemy, player_x, player_y)
            print("=== GAME OVER ===")
            break
            
        print(f"State: {enemy.state}")
        print_dungeon(dungeon_grid, enemy, player_x, player_y)
        time.sleep(0.3)
                
if __name__ == "__main__":
    main()
