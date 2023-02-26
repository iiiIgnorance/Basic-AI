import time
from BaseAI import BaseAI

class IntelligentAgent(BaseAI):
    inf = float('inf')
    time_limit = None

    def getMove(self, grid):
        self.time_limit = time.process_time() + 0.18
        move = self.maximize(grid, -self.inf, self.inf, 0)[0]
        return move

    def maximize(self, grid, alpha, beta, depth):
        moves = grid.getAvailableMoves()

        if not moves:
            return None, self.eval(grid)
        if depth >= 5 or time.process_time() >= self.time_limit:
            return None, self.eval(grid)

        max_child, max_utility = None, -self.inf

        for child in moves:
            child_utility = (self.minimize(child[1], alpha, beta, depth + 1, 2)[1]) * 0.9 + (self.minimize(child[1], alpha, beta, depth + 1, 4)[1]) * 0.1

            if child_utility > max_utility:
                max_child, max_utility = child[0], child_utility

            if max_utility >= beta:
                break

            if max_utility > alpha:
                alpha = max_utility

        return max_child, max_utility

    def minimize(self, grid, alpha, beta, depth, value):
        cells = grid.getAvailableCells()

        if not cells:
            return None, self.eval(grid)
        if depth >= 5 or time.process_time() >= self.time_limit:
            return None, self.eval(grid)

        min_child, min_utility = None, self.inf

        for child in cells:
            child_grid = grid.clone()
            child_grid.insertTile(child, value)
            child_utility = self.maximize(child_grid, alpha, beta, depth + 1)[1]

            if child_utility < min_utility:
                min_child, min_utility = child_grid, child_utility

            if min_utility <= alpha:
                break

            if min_utility < beta:
                beta = min_utility

        return min_child, min_utility

    def eval(self, grid):
        w1, w2, w3 = 4, 1, 0
        m_score = 0
        s_score = 0
        z_score = len(grid.getAvailableCells())
        for row in range(4):
            for col in range(3):
                if grid.map[row][col] < grid.map[row][col + 1]:
                    m_score += grid.map[row][col] - grid.map[row][col + 1]
                if grid.map[col][row] < grid.map[col + 1][row]:
                    m_score += grid.map[col][row] - grid.map[col + 1][row]
                s_score -= abs(grid.map[row][col] - grid.map[row][col + 1])
                s_score -= abs(grid.map[col][row] - grid.map[col + 1][row])
                w3 += grid.map[row][col]
        return w1 * m_score + w2 * s_score + w3 * z_score


