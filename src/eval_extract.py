from extract import extract
from extract_eval_suite import TEST_INPUT_OUTPUT_PAIR


def match_and_score(expected: dict, result: dict | None) -> tuple[int, int]:
    score = 0
    total = 0

    # Count total score
    # Patient name
    total += 1
    # Results
    total += len(expected["results"]) * 6

    # 0 Score if no data is extracted
    if result is None:
        print("ERROR: No data extracted")
        return (score, total)

    # patient name matching - case insensitive
    if (
        expected["patient_name"].lower().strip()
        == result["patient_name"].lower().strip()
    ):
        score += 1
    else:
        print(
            f"MISMATCH for name (case insensitive): "
            f"Expected '{expected['patient_name']}', "
            f"got: '{result['patient_name']}'"
        )

    # Results matching
    len_e = len(expected["results"])
    len_r = len(result["results"])

    if len_e > len_r:
        print(f"MISMATCH for results: {len_e-len_r} result(s) missing")
    elif len_e < len_r:
        print(f"MISMATCH for results: {len_r-len_e} extra result(s) extracted")

    for i in range(min(len_e, len_r)):
        res_e = expected["results"][i]
        res_r = result["results"][i]

        for key in res_e:
            if key == "test_name":
                # Case-insensitive test name matching
                if res_e[key].lower().strip() == res_r[key].lower().strip():
                    score += 1
                else:
                    print(
                        f"MISMATCH for results, index {i}, key '{key}' "
                        f"(case insensitive): Expected '{res_e[key]}', "
                        f"got: '{res_r[key]}'"
                    )
            elif res_e[key] == res_r[key]:
                score += 1
            else:
                print(
                    f"MISMATCH for results, index {i}, key '{key}': "
                    f"Expected '{res_e[key]}', "
                    f"got: '{res_r[key]}'"
                )

    return (score, total)


def run_all_test_cases():
    all_score = 0
    all_total = 0
    all_usage = {"in": 0, "out": 0, "cost": 0}

    for i, (input, output) in enumerate(TEST_INPUT_OUTPUT_PAIR.items()):
        print("\n- - - INPUT:", i + 1, " - - - ")

        result, usage = extract(input)
        score, total = match_and_score(output, result)
        all_score += score
        all_total += total
        all_usage["in"] += usage["in"]
        all_usage["out"] += usage["out"]
        all_usage["cost"] += usage["cost"]

        print(f"SCORE: {score}/{total}")
        print("- - - END - - - \n")

    print(f"\n- - - TOTAL: {all_score}/{all_total} - - -")
    print(f"- - - COST: {all_usage} - - -\n")


if __name__ == "__main__":
    run_all_test_cases()
