import pytest

from shipping_quote import process_shipments, monitor_container_pressures


def test_invalid_shipments_input():
    with pytest.raises(ValueError):
        process_shipments("invalid", 10)
    with pytest.raises(ValueError):
        process_shipments([], -1)


def test_unapproved_shipment():
    result = process_shipments([{"manifest_approved": False}], 10)
    assert result == {"total_quote": 0.0, "status": "NO_CARGO"}


def test_ground_and_air_shipping():
    shipments = [
        {"manifest_approved": True, "mode": "ground",
         "packages": [{"weight_kg": 10}]},
        {"manifest_approved": True, "mode": "air",
         "packages": [{"weight_kg": 10}]},
    ]
    result = process_shipments(shipments, 5)
    assert result["total_quote"] == 170.0
    assert result["status"] == "CLEARED"


def test_unsupported_transport_mode():
    result = process_shipments(
        [{"manifest_approved": True, "mode": "sea"}], 10
    )
    assert result["status"] == "NO_CARGO"


def test_invalid_and_heavy_packages():
    shipments = [{
        "manifest_approved": True,
        "mode": "ground",
        "packages": [
            {"weight_kg": 0}, {"weight_kg": -2},
            {"weight_kg": 40}, {"weight_kg": 10},
        ],
    }]
    result = process_shipments(shipments, 10)
    assert result["total_quote"] == 290.0
    assert result["status"] == "CLEARED"


def test_hazmat_and_fragile_shipment():
    shipments = [
        {"manifest_approved": True, "mode": "ground",
         "packages": [{"weight_kg": 2, "is_hazmat": True}]},
        {"manifest_approved": True, "mode": "air", "is_fragile": True,
         "packages": [{"weight_kg": 2, "is_hazmat": True}]},
    ]
    result = process_shipments(shipments, 10)
    assert result["total_quote"] == 60.0
    assert result["status"] == "CLEARED"


def test_express_priority():
    result = process_shipments([{
        "manifest_approved": True, "mode": "ground",
        "express_priority": True,
        "packages": [{"weight_kg": 10}],
    }], 20)
    assert result["total_quote"] == 75.0


def test_rejected_parcels_flag_review():
    result = process_shipments([{
        "manifest_approved": True, "mode": "ground",
        "packages": [
            {"weight_kg": 0}, {"weight_kg": -1},
            {"weight_kg": 0}, {"weight_kg": -2},
        ],
    }], 10)
    assert result["status"] == "FLAGGED_REVIEW"


def test_pressure_logs_without_data():
    assert monitor_container_pressures([]) == "NO_DATA"
    assert monitor_container_pressures(None) == "NO_DATA"


def test_stable_pressure_logs():
    assert monitor_container_pressures(
        [[15.0, 14.0, 13.5, 14.0, 15.0]]
    ) == "STABLE"


def test_consecutive_low_pressure_detects_leak():
    assert monitor_container_pressures(
        [[15.0, 13.9, 13.8]]
    ) == "LEAK_DETECTED"


def test_low_pressure_streak_resets():
    assert monitor_container_pressures(
        [[13.0, 14.0, 13.0, 14.0]]
    ) == "STABLE"
