def normalised_test_type(test_case_type):
    test_type_map = {
        "functional": ["Functional"],
        "non-functional": [
            "security",
            "performance",
            "reliability",
            "compatibility",
            "accessibility",
            "localization",
            "usability",
            "compliance",
        ],
        "both": ["functional", "non-functional"],
    }
    return test_type_map[test_case_type]
