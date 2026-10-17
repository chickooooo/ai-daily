TEST_CASE_1 = """Patient: Mrs. Anita Desai    Sample No: 4455
LIPID PROFILE
Total Cholesterol   212  mg/dL   (<200)
HDL Cholesterol      48  mg/dL   (>40.66)
LDL Cholesterol     138  mg/dL   (50<value<100)
Triglycerides       130  mg/dL   (<150, >140)"""

TEST_CASE_2 = "Pt: Mr. Rahul Sharma | Haemoglobin 13.8 g/dL (ref 13-17)"

TEST_CASE_3 = "Rahul Sharma | Haemoglobin"

TEST_CASE_4 = "   Putin   "

TEST_CASE_5 = """Patient: Mr. Vikram Rao    Age/Sex: 45/M
URINE ROUTINE EXAMINATION
Colour          Pale Yellow
Protein         Nil
pH              6.0           (4.6 - 8.0)"""

TEST_CASE_6 = """Patient: Ms. Priya Nair
COMPLETE BLOOD COUNT
WBC             11,800    /cumm    (4,000 - 11,000)"""

TEST_CASE_7 = """Patient: Mrs. Sunita Iyer    Age/Sex: 38/F
Haemoglobin     12.5      g/dL     (M: 13-17, F: 12-15)"""


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

OUTPUT_TEST_CASE_5 = {
    "patient_name": "Mr. Vikram Rao",
    "results": [
        {
            "test_name": "Colour",
            "value": "Pale Yellow",
            "unit": None,
            "ref_low": None,
            "ref_high": None,
            "flag": "",
        },
        {
            "test_name": "Protein",
            "value": "Nil",
            "unit": None,
            "ref_low": None,
            "ref_high": None,
            "flag": "",
        },
        {
            "test_name": "pH",
            "value": 6.0,
            "unit": None,
            "ref_low": 4.6,
            "ref_high": 8.0,
            "flag": "",
        },
    ],
}

OUTPUT_TEST_CASE_6 = {
    "patient_name": "Ms. Priya Nair",
    "results": [
        {
            "test_name": "WBC",
            "value": 11800.0,
            "unit": "/cumm",
            "ref_low": 4000.0,
            "ref_high": 11000.0,
            "flag": "H",
        },
    ],
}

OUTPUT_TEST_CASE_7 = {
    "patient_name": "Mrs. Sunita Iyer",
    "results": [
        {
            "test_name": "Haemoglobin",
            "value": 12.5,
            "unit": "g/dL",
            "ref_low": 12.0,
            "ref_high": 15.0,
            "flag": "",
        },
    ],
}


TEST_INPUT_OUTPUT_PAIR = {
    TEST_CASE_1: OUTPUT_TEST_CASE_1,
    TEST_CASE_2: OUTPUT_TEST_CASE_2,
    TEST_CASE_3: OUTPUT_TEST_CASE_3,
    TEST_CASE_4: OUTPUT_TEST_CASE_4,
    TEST_CASE_5: OUTPUT_TEST_CASE_5,
    TEST_CASE_6: OUTPUT_TEST_CASE_6,
    TEST_CASE_7: OUTPUT_TEST_CASE_7,
}
