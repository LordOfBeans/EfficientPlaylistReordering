from move import Move

class Reorderer:
    def __init__(self, algo):
        self.algo = algo

    # Find the full set of steps to reorder the sequence
    def find_solution(self, seq):
        if self.algo not in ['insertion']:
            raise Exception(f"Unknown reordering algorithm: {algo}")
        moves = []
        while len(moves) < len(seq): # Condition helps prevent infinite loop, should never make more moves than there are items in the sequence
            blocks = self.identify_blocks(seq)
            next_move = self.insertion_move(blocks)
            if next_move is None:
                break
            else:
                moves.append(next_move)
                seq = next_move.perform_move(seq)
        return moves

    # Finds blocks of numbers in the correct sequence
    # Must work properly for move finding methods to work
    @staticmethod
    def identify_blocks(seq):
        ret = []
        if len(seq) == 0:
            return ret
        curr_num = seq[0]
        curr_block = [curr_num]
        i = 1
        while i < len(seq):
            if seq[i] == curr_num + 1:
                curr_block.append(seq[i])
            else:
                ret.append(curr_block)
                curr_block = [seq[i]]
            curr_num = seq[i]
            i += 1
        ret.append(curr_block)
        return ret

    # Inpsired by Insertion Sort
    # If the first block does not start with zero, find the block that does and put it at the start
    # Otherwise, find the block that should go to the right of the first block
    # Move that block
    # Returns a move unless there are fewer than two blocks
    # Must be fed accurate blocks
    @staticmethod
    def insertion_move(blocks):
        if len(blocks) < 2:
            return None
        find_num = 0
        if blocks[0][0] == find_num:
            find_num = len(blocks[0])
        range_start = 0
        for block in blocks:
            if block[0] == find_num:
                return Move(range_start, len(block), find_num)
                break
            else:
                range_start += len(block)

# Rudimentary testing
def main():
    sequences = [
        [],
        [0, 1, 2, 3],
        [1, 2, 3, 4, 5, 6, 7, 0],
        [0, 1, 2, 3, 6, 7, 8, 4, 5],
        [4, 3, 2, 1, 0],
        [4, 5, 1, 2, 3, 7, 6, 0],
    ]

    r = Reorderer("insertion")

    for seq in sequences:
        print(f"\nFinding solution for: {seq}")
        solution = r.find_solution(seq)
        if len(solution) > 0:
            for i in range(0, len(solution)):
                move = solution[i]
                print(f"Move {i}: {move}")
                seq = move.perform_move(seq)
                print(f"Result: {seq}")
        else:
            print(f"Already ordered")


if __name__ == "__main__":
    main()
