"""
Demonstrate getting to halfway point

State modelled as list of Poles essentially 2 integers (top and bottom ring #)
[(1,3),,(6,9),,(5,6),,,(4 4)]

None: Empty pole
(x,y): hosts rings x through y
(n,n): a single ring, ring number = n

Starting state for (p,r)
[(1,r),,...,]

aim to finish on pole 2
[,(1,r),...,]

Represent a move as a tuple (from pole, to pole) - zero indexed
[(1,3),,(6,9),,(5,6),,,(4 4)]
(0,1)
[(2,3),(1,1),(6,9),,(5,6),,,(4 4)]
"""
from collections import namedtuple

history = []

Move = namedtuple(
    "Move", ["move", "state"]
)


class Pole:
    """Push and Pop rings like a stack with validation
    RuntimeError raised if rules are violated"""
    def __init__(self, index: int):
        self.index = index
        self._top_ring = None
        self._bottom_ring = None

    def push_ring(self, ring):
        if self._top_ring:
            if not self._top_ring == ring + 1:
                raise RuntimeError(f"Can't move {ring} onto {self._top_ring}")
            self._top_ring = ring
        else:
            self._top_ring = ring
            self._bottom_ring = ring

    def pop_ring(self) -> int:
        if self._top_ring:
            ring = self._top_ring
            if self._top_ring == self._bottom_ring:
                self._top_ring = None
                self._bottom_ring = None
            else:
                self._top_ring += 1
            return ring
        else:
            raise RuntimeError(f"Nothing to take from pole {self.index}")

    def size(self) -> int:
        if self._top_ring:
            return self._bottom_ring - self._top_ring + 1
        else:
            return 0

    def __str__(self):
        if self.size() == 0:
            return "FREE"
        elif self.size() == 1:
            return f"{self._top_ring}(1)"
        else:
            return f"{self._top_ring}-{self._bottom_ring}({self.size()})"

    def __repr__(self):
        return str(self)

    def as_tuple(self):
        return self._top_ring, self._bottom_ring


class HanoiVar:

    def __init__(self, poles: int, rings: int = None):
        self.poles = poles
        self.rings = rings
        self.state: list = []
        self.move_count = 0
        if not self.rings:
            self.rings = 2 ** (self.poles-1) - 1

        for idx in range(self.poles):
            pole = Pole(idx)
            self.state.append(pole)

        starting_pole: Pole = self.state[0]
        for ring in range(self.rings, 0, -1):
            starting_pole.push_ring(ring)

    def __str__(self):
        return " ".join(str(pole) for pole in self.state)

    def get_state(self):
        state = []
        for pole in self.state:
            if pole.size() > 0:
                state.append(pole.as_tuple())
            else:
                state.append(None)
        return state

    def move(self, from_pole_idx: int, to_pole_idx: int):
        """Move a ring from -> to pole using a pop and push"""
        move = Move((from_pole_idx, to_pole_idx), self.get_state())
        history.append(move)

        from_pole: Pole = self.state[from_pole_idx]
        to_pole: Pole = self.state[to_pole_idx]
        ring = from_pole.pop_ring()
        to_pole.push_ring(ring)
        self.move_count += 1
        print(self.move_count, from_pole_idx+1, to_pole_idx+1, self)

    def number_of_free_poles(self):
        return len([pole for pole in self.state if pole.size() == 0])

    def a_free_pole_index(self):
        """Return the index of an empty pole"""
        for pole in self.state:
            if pole.size() == 0:
                return pole.index

    def move_block(self, size: int, source_idx, target_idx=None) -> int:
        """If the size is a single ring then move source to target
        (if target not given then find an empty pole)

        Otherwise, recursively move half sized blocks in 3 steps using a temporary (if available)
        pole

        A
        B       B                 A
        L       LA       LAB    L_B
        """
        if size == 1:
            if target_idx is None:
                if self.number_of_free_poles() < 1:
                    raise RuntimeError(f"Not enough free poles to move {source_idx} to {target_idx}")
                target_idx = self.a_free_pole_index()

            self.move(source_idx, target_idx)

            return target_idx

        else:
            half_size = size // 2
            temp_idx = self.move_block(half_size, source_idx)
            target_idx = self.move_block(half_size, source_idx, target_idx)
            target_idx = self.move_block(half_size, temp_idx, target_idx)
            return target_idx

    def solve(self):
        """Keep moving chunks of powers 2 until we are left with just the
        largest ring and an empty pole to move it to.
        This is the halfway point and re-assembly is the reverse process"""
        block_size = 2 ** (self.poles-1)
        while self.state[0].size() > 1:
            block_size = block_size // 2
            self.move_block(block_size, 0)

        print("Halfway")
        reassembly_moves = [(0, 1)]  # move the largest ring
        for move in reversed(history):
            # for each move reverse the direction and swap poles 1 & 2
            to_pole = move.move[0]
            from_pole = move.move[1]
            if to_pole <= 1:
                to_pole = 1 - to_pole
            if from_pole <= 1:
                from_pole = 1 - from_pole
            reassembly_moves.append((from_pole, to_pole))

        # Apply the reassembly to history
        for move in reassembly_moves:
            self.move(move[0], move[1])


# Example use with 8 poles (127 rings)
# v = HanoiVar(8)
# v.solve()
