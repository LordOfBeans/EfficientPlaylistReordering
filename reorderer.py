from move import Move

class Reorderer:
    def __init__(self, algo):
        self.algo = algo

    # Find the full set of steps to reorder the sequence
    def find_solution(self, seq):
        if self.algo not in ['insertion', 'hybrid', 'furthest']:
            raise Exception(f"Unknown reordering algorithm: {algo}")
        seq_len = len(seq)
        moves = []
        while len(moves) < len(seq): # Condition helps prevent infinite loop, should never make more moves than there are items in the sequence
            blocks = self.identify_blocks(seq)
            if len(blocks) < 2:
                break
            if self.algo == 'furthest':
                best_move = self.furthest_move(blocks, seq)
                moves.append(best_move)
                seq = best_move.perform_move(seq)
                continue
            elif self.algo == 'hybrid':
                connect_move = self.connector_move(blocks, seq_len)
                if connect_move is not None:
                    moves.append(connect_move)
                    seq = connect_move.perform_move(seq)
                    continue
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

    # At most, it is possible to reduce the number of blocks by two in any given move
    # To do this, you must move a block from in-between two sequential blocks
    # This will not always be possible, but this method will return a move if it is
    @staticmethod
    def connector_move(blocks, seq_len):
        if len(blocks) < 3:
            return None
        t_array = [None] * seq_len
        insert_before = 0
        for block in blocks:
            t_array[block[0]] = insert_before
            insert_before += len(block)
        range_start = len(blocks[0])
        for i in range(1, len(blocks) - 1):
            prev_block = blocks[i-1]
            curr_block = blocks[i]
            next_block = blocks[i+1]
            if next_block[0] - prev_block[-1] == 1: # We should move the current block
                last_num = curr_block[-1]
                if last_num == seq_len - 1: # If current block should go at the end, just move it there
                    return Move(range_start, len(curr_block), seq_len)
                else:
                    insert_before = t_array[last_num + 1]
                    return Move(range_start, len(curr_block), insert_before)
            range_start += len(curr_block)
        return None

    # Returns every move block movement possible that would cause at least two blocks to merge
    # Returns them as a list of moves
    # Allows use of mathematical heuristics to evaluate best move to make
    @staticmethod
    def get_all_merging_moves(blocks, seq_len):
        first_array = [None] * seq_len
        last_array = [None] * seq_len
        insert_before = 0
        for block in blocks:
            first_array[block[0]] = insert_before
            last_array[block[-1]] = insert_before + len(block)
            insert_before += len(block)

        ret_moves = []
        range_start = 0
        for curr_block in blocks:
            if curr_block[0] != 0:
                right_merge = last_array[curr_block[0] - 1]
                ret_moves.append(Move(range_start, len(curr_block), right_merge))
            if curr_block[-1] != seq_len - 1:
                left_merge = first_array[curr_block[-1] + 1]
                ret_moves.append(Move(range_start, len(curr_block), left_merge))
            range_start += len(curr_block)
        return ret_moves

    @staticmethod
    def furthest_move(blocks, seq):
        move_options = Reorderer.get_all_merging_moves(blocks, len(seq))
        max_metric = -9999999
        best_move = None
        for move in move_options:
            distance_ideal = abs(seq[move.range_start] - move.insert_before)
            distance_move = abs(move.range_start - move.insert_before)
            metric = distance_move - distance_ideal
            if metric > max_metric:
                max_metric = metric
                best_move = move
        return best_move





# Rudimentary testing
def main():
    seq = [1, 3, 4, 2, 0]
    blocks = Reorderer.identify_blocks(seq)
    all_moves = Reorderer.get_all_merging_moves(blocks, len(seq))
    print(f"All possible merging moves for {seq}")
    for move in all_moves:
        print(move)
        print(move.perform_move(seq.copy()))

    sequences = [
        [],
        [0, 1, 2, 3],
        [4, 3, 2, 1, 0],
        [4, 5, 1, 2, 3, 7, 6, 0],
        [1, 2, 4, 5, 3, 6, 7, 0],
        [2, 3, 4, 7, 8, 5, 0, 6, 1]
    ]

    r = Reorderer("furthest")

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
