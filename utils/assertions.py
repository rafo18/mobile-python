def verify(context, actual, expected, description="Assertion"):

    # =========================================================
    # GUARDAR EVIDENCIA ANTES DEL ASSERT
    # =========================================================

    context.assert_evidence = {
        "description": description,
        "expected": expected,
        "actual": actual
    }

    # =========================================================
    # VALIDACIÓN
    # =========================================================

    assert actual == expected, (
        f"{description}\n"
        f"Expected: {expected}\n"
        f"Actual: {actual}"
    )