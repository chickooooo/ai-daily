from extract import mock_extract

TEST_CASE_1 = """Patient: Mrs. Anita Desai    Sample No: 4455
LIPID PROFILE
Total Cholesterol   212  mg/dL   (<200)
HDL Cholesterol      48  mg/dL   (>40.66)
LDL Cholesterol     138  mg/dL   (50<value<100)
Triglycerides       130  mg/dL   (<150, >140)"""
TEST_CASE_2 = "Pt: Mr. Rahul Sharma | Haemoglobin 13.8 g/dL (ref 13-17)"
TEST_CASE_3 = "Rahul Sharma | Haemoglobin"


OUTPUT_TEST_CASE_1 = {
    "patient_name": "Mrs. Anita Desai",
    "results": [
        {
            "test_name": "Total Cholesterol",
            "value": 212.0,
            "unit": "mg/dL",
            "ref_low": None,
            "ref_high": 200.0,
            "flag": "H",
        },
        {
            "test_name": "HDL Cholesterol",
            "value": 48.0,
            "unit": "mg/dL",
            "ref_low": 40.66,
            "ref_high": None,
            "flag": "",
        },
        {
            "test_name": "LDL Cholesterol",
            "value": 138.0,
            "unit": "mg/dL",
            "ref_low": 50.0,
            "ref_high": 100.0,
            "flag": "H",
        },
        {
            "test_name": "Triglycerides",
            "value": 130.0,
            "unit": "mg/dL",
            "ref_low": 140.0,
            "ref_high": 150.0,
            "flag": "L",
        },
    ],
}
OUTPUT_TEST_CASE_2 = {
    "patient_name": "Mr. Rahul Sharma",
    "results": [
        {
            "test_name": "Haemoglobin",
            "value": 13.8,
            "unit": "g/dL",
            "ref_low": 13.0,
            "ref_high": 17.0,
            "flag": "",
        },
    ],
}
OUTPUT_TEST_CASE_3 = {
    "patient_name": "Rahul Sharma",
    "results": [
        {
            "test_name": "Haemoglobin",
            "value": None,
            "unit": None,
            "ref_low": None,
            "ref_high": None,
            "flag": "",
        },
    ],
}


TEST_INPUT_OUTPUT_PAIR = {
    TEST_CASE_1: OUTPUT_TEST_CASE_1,
    TEST_CASE_2: OUTPUT_TEST_CASE_2,
    TEST_CASE_3: OUTPUT_TEST_CASE_3,
}


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

    for i, (input, output) in enumerate(TEST_INPUT_OUTPUT_PAIR.items()):
        print("\n- - - INPUT:", i + 1, " - - - ")

        result = mock_extract(input)
        score, total = match_and_score(output, result)
        all_score += score
        all_total += total

        print(f"SCORE: {score}/{total}")
        print("- - - END - - - \n")

    print(f"\n- - - TOTAL: {all_score}/{all_total} - - -\n")


if __name__ == "__main__":
    run_all_test_cases()
