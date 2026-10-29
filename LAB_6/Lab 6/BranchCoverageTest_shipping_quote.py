
import pytest

from shipping_quote import process_shipments, monitor_container_pressures


def test_empty_shipments():
    assert process_shipments([], 0) == {
        "total_quote": 0.0,
        "status": "NO_CARGO",
    }


def test_handling_fee_boundary():
    with pytest.raises(ValueError):
        process_shipments([], -0.01)

    assert process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [{"weight_kg": 30}],
        }],
        0,
    ) == {"total_quote": 120.0, "status": "CLEARED"}


def test_weight_boundary():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [
                {"weight_kg": 30},
                {"weight_kg": 30.01},
            ],
        }],
        0,
    )
    assert result["total_quote"] == 300.06


def test_hazmat_non_fragile_and_fragile():
    normal = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": False,
            "packages": [{"weight_kg": 1, "is_hazmat": True}],
        }],
        10,
    )
    assert normal["total_quote"] == 60.0

    fragile = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "is_fragile": True,
            "packages": [{"weight_kg": 1, "is_hazmat": True}],
        }],
        10,
    )
    assert fragile["total_quote"] == 0.0
    assert fragile["status"] == "NO_CARGO"


def test_rejected_parcel_threshold():
    three_rejected = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [
                {"weight_kg": 0},
                {"weight_kg": -1},
                {"weight_kg": 0},
            ],
        }],
        10,
    )
    assert three_rejected["status"] == "CLEARED"

    four_rejected = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [
                {"weight_kg": 0},
                {"weight_kg": -1},
                {"weight_kg": 0},
                {"weight_kg": -1},
            ],
        }],
        10,
    )
    assert four_rejected["status"] == "FLAGGED_REVIEW"


def test_express_and_non_express():
    shipments = [
        {
            "manifest_approved": True,
            "mode": "ground",
            "express_priority": True,
            "packages": [{"weight_kg": 1}],
        },
        {
            "manifest_approved": True,
            "mode": "ground",
            "express_priority": False,
            "packages": [{"weight_kg": 1}],
        },
    ]
    result = process_shipments(shipments, 0)
    assert result["total_quote"] == 9.0


def test_default_shipment_values():
    result = process_shipments(
        [{"manifest_approved": True}],
        5,
    )
    assert result["total_quote"] == 5.0


def test_pressure_threshold_and_streak_reset():
    assert monitor_container_pressures([[14.0]]) == "STABLE"
    assert monitor_container_pressures([[13.9, 14.0, 13.9]]) == "STABLE"
    assert monitor_container_pressures([[13.9, 13.9]]) == "LEAK_DETECTED"


def test_pressure_logs_multiple_containers():
    assert monitor_container_pressures(
        [[13.0], [15.0, 14.0]]
    ) == "STABLE"

    assert monitor_container_pressures(
        [[15.0], [13.0, 13.0]]
    ) == "LEAK_DETECTED"

    
def test_invalid_handling_fee_type():
    with pytest.raises(TypeError):
        process_shipments([], None)


def test_default_mode_and_empty_packages():
    result = process_shipments(
        [{"manifest_approved": True}],
        10,
    )
    assert result == {
        "total_quote": 10.0,
        "status": "CLEARED",
    }


def test_hazmat_then_invalid_package():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "ground",
            "packages": [
                {"weight_kg": 2, "is_hazmat": True},
                {"weight_kg": 0},
            ],
        }],
        10,
    )
    assert result["total_quote"] == 60.0
    assert result["status"] == "CLEARED"


def test_air_shipment_with_express_priority():
    result = process_shipments(
        [{
            "manifest_approved": True,
            "mode": "air",
            "express_priority": True,
            "packages": [{"weight_kg": 1}],
        }],
        10,
    )
    assert result["total_quote"] == 27.5
    assert result["status"] == "CLEARED"

