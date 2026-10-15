from extract import extract

TEST_CASE_1 = """Patient: Mrs. Anita Desai    Sample No: 4455
LIPID PROFILE
Total Cholesterol   212  mg/dL   (<200)
HDL Cholesterol      48  mg/dL   (>40.66)
LDL Cholesterol     138  mg/dL   (50<value<100)
Triglycerides       130  mg/dL   (<150, >140)"""


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


def test_case_1():
    assert extract(TEST_CASE_1) == OUTPUT_TEST_CASE_1
