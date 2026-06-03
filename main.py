from reorderer import Reorderer
from tester import Tester


def main():
    testers = {
        "Furthest": Tester(Reorderer("furthest")),
        "Insertion": Tester(Reorderer("insertion")),
        "Hybrid": Tester(Reorderer("hybrid"))
    }

    methods = {
        "Random": (50, 1000),
        "Blocked": (50, 100, 10)
    }

    count = 50
    length = 1000
    for name, tester in testers.items():
        print(f"\nFor {name} algorithm:")
        for method, params in methods.items():
            print(f"\tFor {method} ordering:")
            if method == "Random":
                results = tester.test_random(*params)
            elif method == "Blocked":
                results = tester.test_blocked(*params)
            correct = results["correct"]
            total = results["total"]
            avg_moves = results["avg_moves"]
            print(f"\t\tCorrectly reordered {correct}/{total}")
            print(f"\t\tAverage moves: {avg_moves:.2f}")

if __name__ == "__main__":
    main()
