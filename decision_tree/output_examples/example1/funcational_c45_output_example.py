{
    "feature": "recognition_score",
    "prediction": None,
    "children": {
        "larger": {
            "feature": "education",
            "prediction": None,
            "children": {
                "masters": "yes",
                "phd": {
                    "feature": "department",
                    "prediction": None,
                    "children": {
                        "engineering": "no",
                        "hr": "yes",
                        "support": "yes",
                        "research": {
                            "feature": "age_group",
                            "prediction": None,
                            "children": {
                                "senior": "no",
                                "young": "yes",
                                "middle": "yes",
                            },
                        },
                    },
                },
                "bachelors": "yes",
                "high_school": "yes",
            },
        },
        "smaller": {
            "feature": "performance_rating",
            "prediction": None,
            "children": {
                "medium": {
                    "feature": "age_group",
                    "prediction": None,
                    "children": {
                        "senior": {
                            "feature": "education",
                            "prediction": None,
                            "children": {
                                "masters": "no",
                                "phd": "no",
                                "bachelors": "no",
                                "high_school": {
                                    "feature": "salary_satisfaction",
                                    "prediction": None,
                                    "children": {"low": "yes", "high": "no"},
                                },
                            },
                        },
                        "young": "no",
                        "middle": "yes",
                    },
                },
                "low": {
                    "feature": "age_group",
                    "prediction": None,
                    "children": {"senior": "no", "young": "yes", "middle": "yes"},
                },
                "high": "no",
            },
        },
    },
}

