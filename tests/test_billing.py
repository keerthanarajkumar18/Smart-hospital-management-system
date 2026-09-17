import pytest

from hospital.billing import (
    InsuranceBilling,
    StandardBilling,
)
from hospital.exceptions import InvalidBillingError


def test_standard_billing() -> None:
    """Verify standard billing calculates the full amount."""
    strategy = StandardBilling()

    bill = strategy.calculate_bill(
        consultation_charge=500,
        test_charges={
            "Blood Test": 300,
            "X-Ray": 700,
        },
        procedure_charges={
            "Injection": 200,
        },
    )

    assert bill.total == 1700
    assert bill.discount == 0


def test_standard_itemized_bill() -> None:
    """Verify individual billing items are preserved."""
    strategy = StandardBilling()

    bill = strategy.calculate_bill(
        consultation_charge=500,
        test_charges={
            "Blood Test": 300,
        },
        procedure_charges={
            "Injection": 200,
        },
    )

    assert bill.consultation_charge == 500
    assert bill.test_charges["Blood Test"] == 300
    assert bill.procedure_charges["Injection"] == 200


def test_standard_summary() -> None:
    """Verify the summary contains the calculated amounts."""
    strategy = StandardBilling()

    bill = strategy.calculate_bill(
        consultation_charge=500,
        test_charges={"Blood Test": 300},
        procedure_charges={"Injection": 200},
    )

    summary = bill.summary()

    assert "Consultation: ₹500.00" in summary
    assert "Tests: ₹300.00" in summary
    assert "Procedures: ₹200.00" in summary
    assert "Total: ₹1000.00" in summary


def test_insurance_billing() -> None:
    """Verify insurance discount is applied."""
    strategy = InsuranceBilling(0.20)

    bill = strategy.calculate_bill(
        consultation_charge=500,
        test_charges={"Blood Test": 300},
        procedure_charges={"Injection": 200},
    )

    assert bill.discount == 200
    assert bill.total == 800


def test_full_insurance_discount() -> None:
    """Verify a 100 percent discount."""
    strategy = InsuranceBilling(1.0)

    bill = strategy.calculate_bill(
        consultation_charge=500,
        test_charges={"Blood Test": 300},
        procedure_charges={"Injection": 200},
    )

    assert bill.discount == 1000
    assert bill.total == 0


def test_invalid_negative_consultation() -> None:
    """Verify negative consultation charges are rejected."""
    strategy = StandardBilling()

    with pytest.raises(InvalidBillingError):
        strategy.calculate_bill(
            consultation_charge=-100,
            test_charges={},
            procedure_charges={},
        )


def test_invalid_test_charge() -> None:
    """Verify negative test charges are rejected."""
    strategy = StandardBilling()

    with pytest.raises(InvalidBillingError):
        strategy.calculate_bill(
            consultation_charge=500,
            test_charges={"Blood Test": -100},
            procedure_charges={},
        )


def test_invalid_procedure_charge() -> None:
    """Verify negative procedure charges are rejected."""
    strategy = StandardBilling()

    with pytest.raises(InvalidBillingError):
        strategy.calculate_bill(
            consultation_charge=500,
            test_charges={},
            procedure_charges={"Injection": -50},
        )


def test_invalid_insurance_rate() -> None:
    """Verify invalid insurance rates are rejected."""
    with pytest.raises(InvalidBillingError):
        InsuranceBilling(1.5)