class Move:
    def __init__(self, range_start, range_length, insert_before):
        self.range_start = range_start
        self.range_length = range_length
        self.insert_before = insert_before

    def __str__(self):
        return f"Move ( Start={self.range_start} Length={self.range_length} Insert={self.insert_before} )"

    # Returns a new sequence with the move performed
    def perform_move(self, seq):
        range_start = self.range_start # for convenience and readability
        range_end = range_start + self.range_length

        if self.range_length < 1:
            raise Exception(f"Invalid range_length on {self}")
        if range_start < 0:
            raise Exception(f"Invalid range_start on {self}")
        if range_end > len(seq):
            raise Exception(f"Cannot perform {self} on sequence with length {len(seq)}")

        before_seq = seq[:range_start]
        move_seq = seq[range_start:range_end]
        after_seq = seq[range_end:]

        if self.insert_before < range_start:
            before_seq = before_seq[:self.insert_before] + move_seq + before_seq[self.insert_before:]
        elif self.insert_before > range_end:
            adjusted_index = self.insert_before - range_end
            after_seq = after_seq[:adjusted_index] + move_seq + after_seq[adjusted_index:]
        elif self.insert_before == range_start or self.insert_before == range_end:
            raise Exception(f"Performing {self} would not result in any changes")
        else:
            raise Exception(f"Cannot perform {self} into itself")
        return before_seq + after_seq


# Rudimentary testing
def main():
    seq = list(range(0, 9))
    print(f"Base sequence: {seq}")

    moves = [
        Move(3, 3, 1),
        Move(3, 3, 0),
        Move(3, 3, 7),
        Move(3, 3, 9),
        Move(-1, 3, 0),
        Move(0, 3, 0),
        Move(7, 3, 0),
        Move(8, 1, 0),
        Move(3, 0, 1),
        Move(3, 3, 5)
    ]

    for move in moves:
        print(f"Attempting Move: {move}")
        try:
            res = move.perform_move(seq)
            print(f"Result: {res}")
        except Exception as e:
            print("Move Failed: ", e)

if __name__ == "__main__":
    main()
