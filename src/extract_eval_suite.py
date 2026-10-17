TEST_CASE_1 = """Patient: Mrs. Anita Desai    Sample No: 4455
LIPID PROFILE
Total Cholesterol   212  mg/dL   (<200)
HDL Cholesterol      48  mg/dL   (>40.66)
LDL Cholesterol     138  mg/dL   (50<value<100)
Triglycerides       130  mg/dL   (<150, >140)"""

TEST_CASE_2 = "Pt: Mr. Rahul Sharma | Haemoglobin 13.8 g/dL (ref 13-17)"

TEST_CASE_3 = "Rahul Sharma | Haemoglobin"

TEST_CASE_4 = "   Putin   "


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

OUTPUT_TEST_CASE_4 = {
    "patient_name": "Putin",
    "results": [],
}


TEST_INPUT_OUTPUT_PAIR = {
    TEST_CASE_1: OUTPUT_TEST_CASE_1,
    TEST_CASE_2: OUTPUT_TEST_CASE_2,
    TEST_CASE_3: OUTPUT_TEST_CASE_3,
    TEST_CASE_4: OUTPUT_TEST_CASE_4,
}
