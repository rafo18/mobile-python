def verify(context, actual, expected, description):

    context.assert_evidence = {
        "description": description,
        "expected": expected,
        "actual": actual
    }

    assert actual == expected, (
        f"{description} | "
        f"Expected: {expected} | "
        f"Actual: {actual}"
    )