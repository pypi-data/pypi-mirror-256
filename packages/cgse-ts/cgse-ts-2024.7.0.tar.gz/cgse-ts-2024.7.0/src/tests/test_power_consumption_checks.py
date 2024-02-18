from camtest.tasks.shared.camera.aeu import is_inside_range


def test_is_inside_range():

    tolerance_value = 5

    # Absolute tolerance

    tolerance_type = "absolute"
    nominal_value = 42.

    measured_values = [40.3, nominal_value - tolerance_value, nominal_value + tolerance_value]
    for measured_value in measured_values:
        range_str, color, ok_nok = is_inside_range(measured_value, nominal_value, tolerance_value, tolerance_type)
        assert range_str == f"{nominal_value} +/- {tolerance_value}"
        assert color == "black"
        assert ok_nok == "OK"

    measured_values = [nominal_value - 1.4 * tolerance_value, nominal_value + 1.01 * tolerance_value]
    for measured_value in measured_values:
        range_str, color, ok_nok = is_inside_range(measured_value, nominal_value, tolerance_value, tolerance_type)
        assert range_str == f"{nominal_value} +/- {tolerance_value}"
        assert color == "red"
        assert ok_nok == "NOK"

    # Relative tolerance

    tolerance_type = "relative"
    nominal_value = 120.

    measured_values = [119, 123, nominal_value - tolerance_value / 100. * nominal_value, nominal_value + tolerance_value / 100. * nominal_value]
    for measured_value in measured_values:
        range_str, color, ok_nok = is_inside_range(measured_value, nominal_value, tolerance_value, tolerance_type)
        assert range_str == f"{nominal_value} +/- {tolerance_value}%"
        assert color == "black"
        assert ok_nok == "OK"

    measured_values = [nominal_value - 1.4 * tolerance_value / 100. * nominal_value, nominal_value + 1.01 * tolerance_value / 100. * nominal_value]
    for measured_value in measured_values:
        range_str, color, ok_nok = is_inside_range(measured_value, nominal_value, tolerance_value, tolerance_type)
        assert range_str == f"{nominal_value} +/- {tolerance_value}%"
        assert color == "red"
        assert ok_nok == "NOK"

