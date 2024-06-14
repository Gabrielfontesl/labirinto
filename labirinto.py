import random
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import matplotlib.animation as animation

# Função para criar o labirinto
def create_maze(n, m):
    maze = [[1] * m for _ in range(n)]
    stack = [(0, 0)]
    maze[0][0] = 0

    while stack:
        x, y = stack[-1]
        neighbors = []

        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] == 1:
                neighbors.append((nx, ny))

        if neighbors:
            nx, ny = random.choice(neighbors)
            maze[(x + nx) // 2][(y + ny) // 2] = 0
            maze[nx][ny] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    # Adiciona caminhos falsos
    for _ in range(n * m // 4):
        x, y = random.randint(0, n - 1), random.randint(0, m - 1)
        if maze[x][y] == 1:
            maze[x][y] = 0

    # Certifique-se de que há um caminho do início ao fim
    maze[0][1] = 0
    maze[1][0] = 0
    maze[n-1][m-2] = 0
    maze[n-2][m-1] = 0

    # Define os pontos de início e fim
    maze[0][0] = 'S'
    maze[n - 1][m - 1] = 'E'

    return maze

# Função para encontrar o caminho mais curto usando BFS
def bfs(maze):
    n, m = len(maze), len(maze[0])
    start = (0, 0)
    end = (n - 1, m - 1)
    queue = deque([start])
    visited = set([start])
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == end:
            break
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < n and 0 <= ny < m and maze[nx][ny] != 1 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parent.get(current)

    if not path or path[-1] != start:
        raise RuntimeError("Não foi possível encontrar um caminho do início ao fim do labirinto.")

    path.reverse()
    return path

# Função para animar o processo de busca
def animate_maze(maze, path):
    n, m = len(maze), len(maze[0])
    data = np.zeros((n, m, 3), dtype=int)

    for i in range(n):
        for j in range(m):
            if maze[i][j] == 1:
                data[i, j] = [0, 0, 0]  # Preto para paredes
            elif maze[i][j] == 'S':
                data[i, j] = [255, 0, 0]  # Vermelho para o início
            elif maze[i][j] == 'E':
                data[i, j] = [0, 255, 0]  # Verde para o fim
            else:
                data[i, j] = [255, 255, 255]  # Branco para caminhos

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.imshow(data, animated=True)

    def update(frame):
        if frame < len(path):
            x, y = path[frame]
            data[x, y] = [0, 0, 255]  # Azul para o caminho do agente
            im.set_array(data)
        return [im]

    ani = animation.FuncAnimation(fig, update, frames=len(path), interval=100, blit=True)
    plt.axis('off')
    plt.show()

# Função para imprimir o labirinto (opcional)
def print_maze(maze):
    for row in maze:
        print(" ".join(str(cell) for cell in row))

if __name__ == "__main__":
    # Garantir que o labirinto seja diferente a cada execução
    random.seed()

    try:
        # Criar e imprimir o labirinto
        n, m = 1000, 1000  # Tamanho do labirinto
        maze = create_maze(n, m)
        print_maze(maze)  # Opcional para ver o labirinto no console

        # Encontrar o caminho mais curto
        path = bfs(maze)

        # Animar o processo de busca
        animate_maze(maze, path)
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
