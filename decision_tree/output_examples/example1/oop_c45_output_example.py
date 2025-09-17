
{
    "feature": "recognition_score",
    "prediction": None,
    "children": {
        "larger": {
            "feature": "education",
            "prediction": None,
            "children": {
                "bachelors": "yes",
                "phd": {
                    "feature": "department",
                    "prediction": None,
                    "children": {
                        "support": "yes",
                        "engineering": "no",
                        "hr": "yes",
                        "research": {
                            "feature": "age_group",
                            "prediction": None,
                            "children": {
                                "senior": "no",
                                "middle": "yes",
                                "young": "yes",
                            },
                        },
                    },
                },
                "masters": "yes",
                "high_school": "yes",
            },
        },
        "smaller": {
            "feature": "performance_rating",
            "prediction": None,
            "children": {
                "high": "no",
                "medium": {
                    "feature": "age_group",
                    "prediction": None,
                    "children": {
                        "senior": {
                            "feature": "education",
                            "prediction": None,
                            "children": {
                                "bachelors": "no",
                                "phd": "no",
                                "masters": "no",
                                "high_school": {
                                    "feature": "salary_satisfaction",
                                    "prediction": None,
                                    "children": {"high": "no", "low": "yes"},
                                },
                            },
                        },
                        "middle": "yes",
                        "young": "no",
                    },
                },
                "low": {
                    "feature": "age_group",
                    "prediction": None,
                    "children": {"middle": "yes", "senior": "no", "young": "yes"},
                },
            },
        },
    },
}
