from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import heapq
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        up_state = PuzzleState(self.config[:], self.n, self, "Up", self.cost + 1)
        if up_state.blank_index >= self.n:
            up_state.config[up_state.blank_index], up_state.config[up_state.blank_index - self.n] = up_state.config[up_state.blank_index - self.n], up_state.config[up_state.blank_index]
            return up_state
        else:
            return None
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        down_state = PuzzleState(self.config[:], self.n, self, "Down", self.cost + 1)
        if down_state.blank_index < (len(self.config) - self.n):
            down_state.config[down_state.blank_index], down_state.config[down_state.blank_index + self.n] = down_state.config[down_state.blank_index + self.n], down_state.config[down_state.blank_index]
            return down_state
        else:
            return None
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        left_state = PuzzleState(self.config[:], self.n, self, "Left", self.cost + 1)
        if left_state.blank_index % self.n != 0:
            left_state.config[left_state.blank_index], left_state.config[left_state.blank_index - 1] = left_state.config[left_state.blank_index - 1], left_state.config[left_state.blank_index]
            return left_state
        else:
            return None

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        right_state = PuzzleState(self.config[:], self.n, self, "Right", self.cost + 1)
        if right_state.blank_index % self.n != 2:
            right_state.config[right_state.blank_index], right_state.config[right_state.blank_index + 1] = right_state.config[right_state.blank_index + 1], right_state.config[right_state.blank_index]
            return right_state
        else:
            return None
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


class Frontier(object):

    def __init__(self, mode):
        self.fringe = set()
        if mode == "bfs":
            self.queue = Q.Queue()
        elif mode == "dfs":
            self.stack = []
        elif mode == "ast":
            self.heap = []
            self.count = 0

    def queue_put(self, state):
        self.queue.put(state)
        self.fringe.add(tuple(state.config))

    def queue_get(self):
        state = self.queue.get()
        self.fringe.remove(tuple(state.config))
        return state

    def queue_empty(self):
        return self.queue.empty()

    def queue_find(self, state):
        if tuple(state.config) in self.fringe:
            return True
        else:
            return False

    def stack_push(self, state):
        self.stack.append(state)
        self.fringe.add(tuple(state.config))

    def stack_pop(self):
        return self.stack.pop()

    def stack_empty(self):
        return len(self.stack) == 0

    def stack_find(self, state):
        if tuple(state.config) in self.fringe:
            return True
        else:
            return False

    def heap_push(self, state, cost):
        entry = (cost, self.count, state)
        heapq.heappush(self.heap, entry)
        self.fringe.add(tuple(state.config))
        self.count += 1

    def heap_pop(self):
        state = heapq.heappop(self.heap)[-1]
        self.fringe.remove(tuple(state.config))
        return state

    def heap_isEmpty(self):
        return len(self.heap) == 0

    def heap_find(self, state):
        if tuple(state.config) in self.fringe:
            return True
        else:
            return False



# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(path_to_goal, cost_of_path, nodes_expanded, search_depth, max_search_depth):
    ### Student Code Goes here
    max_ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2 ** 20)
    with open('./output.txt', 'w') as file:
        file.write('path_to_goal: {}\n'.format(path_to_goal))
        file.write('cost_of_path: {}\n'.format(cost_of_path))
        file.write('nodes_expanded: {}\n'.format(nodes_expanded))
        file.write('search_depth: {}\n'.format(search_depth))
        file.write('max_search_depth: {}\n'.format(max_search_depth))
        file.write('running_time: %.8f \n' % (time.time() - start_time))
        file.write('max_ram_usage: {}\n'.format(max_ram_usage))
    return

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    frontier = Frontier("bfs")
    frontier.queue_put(initial_state)
    explored = set()
    path_to_goal = []
    max_search_depth = 0


    while not frontier.queue_empty():
        state = frontier.queue_get()
        explored.add(tuple(state.config))

        if test_goal(state):
            nodes_expanded = len(explored) - 1
            cost_of_path = state.cost
            search_depth = state.cost
            while state.parent:
                path_to_goal.append(state.action)
                state = state.parent
            writeOutput(path_to_goal[::-1], cost_of_path, nodes_expanded, search_depth, max_search_depth)
            return True

        for neighbor in state.expand():
            if (tuple(neighbor.config)) not in explored and not frontier.queue_find(neighbor):
                frontier.queue_put(neighbor)
                if max_search_depth < neighbor.cost:
                    max_search_depth = neighbor.cost

    return False


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    frontier = Frontier("dfs")
    frontier.stack_push(initial_state)
    explored = set()
    path_to_goal = []
    max_search_depth = 0

    while not frontier.stack_empty():
        state = frontier.stack_pop()
        explored.add(tuple(state.config))

        if test_goal(state):
            nodes_expanded = len(explored) - 1
            cost_of_path = state.cost
            search_depth = state.cost
            while state.parent:
                path_to_goal.append(state.action)
                state = state.parent
            writeOutput(path_to_goal[::-1], cost_of_path, nodes_expanded, search_depth, max_search_depth)

            return True

        for neighbor in state.expand()[::-1]:
            if (tuple(neighbor.config)) not in explored and not frontier.stack_find(neighbor):
                frontier.stack_push(neighbor)
                if max_search_depth < neighbor.cost:
                    max_search_depth = neighbor.cost

    return False


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    frontier = Frontier("ast")
    cost = calculate_total_cost(initial_state)
    frontier.heap_push(initial_state, cost)
    explored = set()
    path_to_goal = []
    max_search_depth = 0

    while not frontier.heap_isEmpty():
        state = frontier.heap_pop()
        explored.add(tuple(state.config))

        if test_goal(state):
            nodes_expanded = len(explored) - 1
            cost_of_path = state.cost
            search_depth = state.cost
            while state.parent:
                path_to_goal.append(state.action)
                state = state.parent
            writeOutput(path_to_goal[::-1], cost_of_path, nodes_expanded, search_depth, max_search_depth)

            return True

        for neighbor in state.expand():
            if (tuple(neighbor.config)) not in explored and not frontier.heap_find(neighbor):
                neighbor_cost = calculate_total_cost(neighbor)
                frontier.heap_push(neighbor, neighbor_cost)
                if max_search_depth < neighbor.cost:
                    max_search_depth = neighbor.cost
    return False


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    total_cost = state.cost
    for i in range(state.n * state.n):
        if state.config[i] == 0:
            continue
        total_cost += calculate_manhattan_dist(i, state.config[i], state.n)

    return total_cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    state_x, state_y = idx // n, idx % n
    goal_x, goal_y = value // n, value % n
    manhattan_dist = abs(state_x - goal_x) + abs(state_y - goal_y)

    return manhattan_dist


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    #goal_state = sorted(puzzle_state.config)
    goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    if puzzle_state.config == goal_state:
        return True
    else:
        return False


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    global start_time
    start_time  = time.time()
    global start_ram
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))


if __name__ == '__main__':
    main()
