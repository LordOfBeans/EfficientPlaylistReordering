import random

class Tester:
    def __init__(self, alg): # TODO: Find a better parameter name
        self.alg = alg

    def test_random(self, count, length):
        correct = 0
        moves_total = 0
        for i in range(0, count):
            seq = self.random_seq(length)
            moves = self.alg.find_solution(seq)
            for move in moves:
                seq = move.perform_move(seq)
            if self.check_seq(seq, length):
                correct += 1
                moves_total += len(moves)
        return {
            "total": count,
            "correct": correct,
            "avg_moves": moves_total / correct
        }

    def test_blocked(self, count, blocks, block_length):
        length = blocks * block_length
        correct = 0
        moves_total = 0
        for i in range(0, count):
            seq = self.blocked_seq(blocks, block_length)
            moves = self.alg.find_solution(seq)
            for move in moves:
                seq = move.perform_move(seq)
            if self.check_seq(seq, length):
                correct += 1
                moves_total += len(moves)
        return {
            "total": count,
            "correct": correct,
            "avg_moves": moves_total / correct
        }


    @staticmethod
    def check_seq(seq, length): # length is the intended length
        if len(seq) != length:
            return False
        for i in range(0, length):
            if seq[i] != i:
                return False
        return True

    @staticmethod
    def reverse_seq(length):
        return list(reversed(range(0, length)))

    @staticmethod
    def random_seq(length):
        seq = list(range(0, length))
        random.shuffle(seq)
        return seq

    @staticmethod
    def blocked_seq(block_count, block_len):
        blocks = []
        for i in range(0, block_count):
            block = list(range(i * block_len, (i + 1) * block_len))
            blocks.append(block)
        block_seq = list(range(0, block_count))
        random.shuffle(block_seq)
        ret_seq = []
        for i in block_seq:
            ret_seq += blocks[i]
        return ret_seq

# Rudimentary testing
def main():
    n = 24
    rev = Tester.reverse_seq(n)
    print(f"Reverse: {rev}")
    rand = Tester.random_seq(n)
    print(f"Random: {rand}")
    blocked = Tester.blocked_seq(8, 3)
    print(f"Blocked: {blocked}")
    ordered_seq = list(range(0, 10))
    ordered_check = Tester.check_seq(ordered_seq, 10)
    print(f"Check ordered sequence: {ordered_check}")
    wrong_seq = ordered_seq[0:8] + [9, 8]
    print(f"Wrong sequence: {wrong_seq}")
    wrong_check = Tester.check_seq(wrong_seq, 10)
    print(f"Check ordered sequence: {wrong_check}")

if __name__ == "__main__":
    main()
