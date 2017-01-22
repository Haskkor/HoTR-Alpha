import heapq
import constants

__author__ = "Jérémy Farnault"
# BASED ON THE A* ALGORITHM FROM LAURENT LUCE (http://www.laurentluce.com/posts/solving-mazes-using-python-simple-recursivity-and-a-search/)


class Square(object):
    """
    OBJETS CARRES DU CHAMPS DE BATAILLE POUR LE CALCUL DU CHEMIN LE PLUS COURT
    """

    def __init__(self, x, y, reachable):
        self.reachable = reachable
        self.x = x
        self.y = y
        self.parent = None
        self.from_start_to_square = 0
        self.cost_square_to_end = 0
        self.sum_fsts_cste = 0
        
    def __lt__(self, other):
            if isinstance(other, Square):
                return self.sum_fsts_cste < other.sum_fsts_cste
            return NotImplemented


class AStar(object):
    """
    UTILISATION DE L'ALGORITHME A* POUR LE CALCUL DU CHEMIN LE PLUS COURT
    """

    def __init__(self, battlefield, hero_pos, max_distance):
        # Carrés libres
        self.opened = []
        heapq.heapify(self.opened)
        # Carrés visités
        self.closed = set()
        # Matrice des carrés
        self.squares = []
        self.grid_height = constants.Battle.LINES_BF
        self.grid_width = constants.Battle.COLUMNS_BF
        self.battlefield = battlefield
        self.max_distance = max_distance
        self.hero_pos = hero_pos
        self.obstacles = self.find_obstacles(self.battlefield)
        self.available_squares = self.find_available_squares()

    def find_obstacles(self, battlefield):
        """
        Initialisation de la liste d'obstacles
        """
        obstacles = []
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if battlefield[i][j].hero is not None:
                    obstacles.append((i, j))
        return obstacles

    def find_available_squares(self):
        """
        Trouve les cases disponibles par rapport à la case sélectionnée et à la distance maximum
        Renvoie un dictionnaire avec comme clef les tuples de coordonnées et comme valeurs la distance
        """
        available_squares = {}
        for i in range(self.grid_height):
            for j in range(self.grid_width):
                if (i, j) != self.hero_pos and (i, j) not in self.obstacles:
                    #a_star = AStar(self.battlefield, self.hero_pos, self.max_distance)
                    self.init_grid(self.obstacles, self.hero_pos, (i, j))
                    result = self.solve()
                    if result is not None and len(result) - 1 <= self.max_distance:
                        available_squares[(i, j)] = len(result) - 1
        return available_squares

    def init_grid(self, obstacles, start, end):
        """
        Initialise la matrice et les cases bloquées par des obstacles
        @param obstacles liste des obstacles (tuples de coordonnées)
        @param start case de départ (tuple de coordonnées)
        @param end case de fin (tuple de coordonnées)
        """
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                if (x, y) in obstacles:
                    reachable = False
                else:
                    reachable = True
                self.squares.append(Square(x, y, reachable))
        self.start = self.get_square(*start)
        self.end = self.get_square(*end)

    def get_heuristic_distance(self, cell):
        """
        Calcule la distance thérorique entre la case de départ et celle de fin
        Multiplie le résultat par 10
        """
        return 10 * (abs(cell.x - self.end.x) + abs(cell.y - self.end.y))

    def get_square(self, x, y):
        """
        Renvoie une case donnée
        """
        return self.squares[x * self.grid_height + y]

    def get_adjacent_squares(self, square):
        """
        Renvoie les cases adjacentes à une case donnée
        """
        squares = []
        if square.x < self.grid_width-1:
            squares.append(self.get_square(square.x+1, square.y))
        if square.y > 0:
            squares.append(self.get_square(square.x, square.y-1))
        if square.x > 0:
            squares.append(self.get_square(square.x-1, square.y))
        if square.y < self.grid_height-1:
            squares.append(self.get_square(square.x, square.y+1))
        return squares

    def get_path(self):
        """
        Renvoie le chemin complet entre la case de départ et la case de fin
        """
        square = self.end
        path = [(square.x, square.y)]
        while square.parent is not self.start and square.parent is not None:
            square = square.parent
            path.append((square.x, square.y))
        path.append((self.start.x, self.start.y))
        path.reverse()
        return path

    def update_square(self, adj, square):
        """
        Met à jour une case adjacente à la case donnée
        """
        adj.from_start_to_square = square.from_start_to_square + 10
        adj.cost_square_to_end = self.get_heuristic_distance(adj)
        adj.parent = square
        adj.sum_fsts_cste = adj.cost_square_to_end + adj.from_start_to_square

    def solve(self):
        """
        Calcule le chemin le plus court entre la case de départ et celle d'arrivée
        Retourne null si il n'y a pas de chemin possible
        """
        # Ajoute la case de départ
        heapq.heappush(self.opened, (self.start.sum_fsts_cste, self.start))
        while len(self.opened):
            # Prend la dernière case de la liste de cases disponibles
            sum_fsts_cste, square = heapq.heappop(self.opened)
            # Ajoute la case recupérée à la liste des cases traitées
            self.closed.add(square)
            # Si il s'agit de la case de fin, renvoie le chemin
            if square is self.end:
                return self.get_path()
            # Récupère les cases adjacentes
            adj_squares = self.get_adjacent_squares(square)
            for adj_square in adj_squares:
                if adj_square.reachable and adj_square not in self.closed:
                    if (adj_square.sum_fsts_cste, adj_square) in self.opened:
                        # Si la case adjacente est dans la liste des cases disponibles, 
                        # contrôle si le chemin courant est meilleur que celui trouvé précédemment pour cette case
                        if adj_square.from_start_to_square > square.from_start_to_square + 10:
                            self.update_square(adj_square, square)
                    else:
                        self.update_square(adj_square, square)
                        # Ajoute la case adjacente à la liste des cases disponibles
                        heapq.heappush(self.opened, (adj_square.sum_fsts_cste, adj_square))
