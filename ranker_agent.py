PRIORITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}

class RankerAgent:
    def rank_test_cases(self, test_cases: list, top_k: int = 10):
        """
        Sort test cases by priority (high -> low) and length of description.
        """
        ranked = sorted(
            test_cases,
            key=lambda x: (
                PRIORITY_WEIGHT.get(x.get("priority", "low"), 1),
                len(x.get("test_case", "")),
            ),
            reverse=True
        )
        return ranked[:top_k]
