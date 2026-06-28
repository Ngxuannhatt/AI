from collections import deque
from node import Node
from node import Node

class Belief_Node:
    def __init__(self, state1, state2,
                 parent=None,
                 action="Bắt đầu"):

        self.state1 = state1
        self.state2 = state2

        self.parent = parent
        self.action = action

    def is_goal(self):
        return (
            self.state1.is_goal()
            and
            self.state2.is_goal()
        )

    def get_state_key(self):
        return (
            self.state1.get_state_key(),
            self.state2.get_state_key()
        )
def dfs_no_observation(self):

    start1 = Node(
    0, 0,
    [
        [1,1,1],
        [1,0,1],
        [1,1,1]
    ]
    )   

    start2 = Node(
    2, 2,
    [
        [1,1,0],
        [1,1,1],
        [1,1,1]
    ]
        )

    root = Belief_Node(
        start1,
        start2,
        action="Bắt đầu"
    )

    frontier = deque([root])
    reached = set()

    steps_limit = 0

    while frontier:

        curr = frontier.pop()
        steps_limit += 1

        # ======================
        # GOAL TEST
        # ======================
        if curr.is_goal():

            path = []
            temp = curr

            while temp is not None:
                path.append(temp)
                temp = temp.parent

            path.reverse()
            return path

        # ======================
        # REACHED TEST
        # ======================
        state_key = curr.get_state_key()

        if state_key in reached:
            continue

        reached.add(state_key)

        # ======================
        # ACTION MOVE
        # ======================

        moves = [
            (-1, 0, "UP"),
            (1, 0, "DOWN"),
            (0, -1, "LEFT"),
            (0, 1, "RIGHT")
        ]

        for dr, dc, action_name in moves:

            s1 = apply_move(self,curr.state1, dr, dc)
            s2 = apply_move(self,curr.state2, dr, dc)

            frontier.append(
                Belief_Node(
                    s1,
                    s2,
                    parent=curr,
                    action=action_name
                )
            )

        # ======================
        # ACTION SUCK
        # ======================

        s1 = apply_suck(self,curr.state1)
        s2 = apply_suck(self,curr.state2)

        frontier.append(
            Belief_Node(
                s1,
                s2,
                parent=curr,
                action="SUCK"
            )
        )

        if steps_limit > 5000000:
            print("Quá thời hạn xử lý.")
            return None

    return None
def apply_move(self, state, dr, dc):

    if state.is_goal():
        return state

    nr = state.x + dr
    nc = state.y + dc

    if 0 <= nr < self.n and 0 <= nc < self.n:

        return Node(
            nr,
            nc,
            state.matrix,
            action=f"Đi tới ({nr},{nc})"
        )

    return Node(
        state.x,
        state.y,
        state.matrix,
        action="Không di chuyển được"
    )
def apply_suck(self, state):

    if state.is_goal():
        return state

    new_mat = [row[:] for row in state.matrix]

    if new_mat[state.x][state.y] == 1:
        new_mat[state.x][state.y] = 0

    return Node(
        state.x,
        state.y,
        new_mat,
        action=f"Hút rác tại ({state.x},{state.y})"
    )