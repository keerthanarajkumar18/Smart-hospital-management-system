"""Billing strategies for the hospital management system."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from hospital.exceptions import InvalidBillingError


@dataclass
class Bill:
    """Represent an itemized hospital bill."""

    consultation_charge: float
    test_charges: dict[str, float]
    procedure_charges: dict[str, float]
    total: float
    discount: float = 0.0

    def summary(self) -> str:
        """Return a human-readable bill summary."""
        return (
            f"Consultation: ₹{self.consultation_charge:.2f}\n"
            f"Tests: ₹{sum(self.test_charges.values()):.2f}\n"
            f"Procedures: ₹{sum(self.procedure_charges.values()):.2f}\n"
            f"Discount: ₹{self.discount:.2f}\n"
            f"Total: ₹{self.total:.2f}"
        )


class BillingStrategy(ABC):
    """Define the interface for hospital billing strategies."""

    @abstractmethod
    def calculate_bill(
        self,
        consultation_charge: float,
        test_charges: dict[str, float],
        procedure_charges: dict[str, float],
    ) -> Bill:
        """Calculate a hospital bill."""
        raise NotImplementedError


class StandardBilling(BillingStrategy):
    """Calculate bills using standard hospital charges."""

    def calculate_bill(
        self,
        consultation_charge: float,
        test_charges: dict[str, float],
        procedure_charges: dict[str, float],
    ) -> Bill:
        """Calculate the full standard bill."""
        validate_billing_input(
            consultation_charge,
            test_charges,
            procedure_charges,
        )

        test_total = sum(test_charges.values())
        procedure_total = sum(procedure_charges.values())

        total = (
            consultation_charge
            + test_total
            + procedure_total
        )

        return Bill(
            consultation_charge=consultation_charge,
            test_charges=test_charges,
            procedure_charges=procedure_charges,
            total=total,
        )


class InsuranceBilling(BillingStrategy):
    """Calculate bills with an insurance discount."""

    def __init__(self, discount_rate: float) -> None:
        """Initialize the insurance discount rate."""
        if not 0 <= discount_rate <= 1:
            raise InvalidBillingError(
                "Discount rate must be between 0 and 1."
            )

        self.discount_rate = discount_rate

    def calculate_bill(
        self,
        consultation_charge: float,
        test_charges: dict[str, float],
        procedure_charges: dict[str, float],
    ) -> Bill:
        """Calculate a bill after applying insurance discount."""
        validate_billing_input(
            consultation_charge,
            test_charges,
            procedure_charges,
        )

        test_total = sum(test_charges.values())
        procedure_total = sum(procedure_charges.values())

        subtotal = (
            consultation_charge
            + test_total
            + procedure_total
        )

        discount = subtotal * self.discount_rate
        total = subtotal - discount

        return Bill(
            consultation_charge=consultation_charge,
            test_charges=test_charges,
            procedure_charges=procedure_charges,
            total=total,
            discount=discount,
        )


def validate_billing_input(
    consultation_charge: float,
    test_charges: dict[str, float],
    procedure_charges: dict[str, float],
) -> None:
    """Validate all billing input values."""
    if consultation_charge < 0:
        raise InvalidBillingError(
            "Consultation charge cannot be negative."
        )

    if not isinstance(test_charges, dict):
        raise InvalidBillingError(
            "Test charges must be provided as a dictionary."
        )

    if not isinstance(procedure_charges, dict):
        raise InvalidBillingError(
            "Procedure charges must be provided as a dictionary."
        )

    for name, amount in test_charges.items():
        if not isinstance(name, str) or not name.strip():
            raise InvalidBillingError(
                "Test name must be a non-empty string."
            )

        if not isinstance(amount, (int, float)) or amount < 0:
            raise InvalidBillingError(
                f"Invalid test charge: {name}"
            )

    for name, amount in procedure_charges.items():
        if not isinstance(name, str) or not name.strip():
            raise InvalidBillingError(
                "Procedure name must be a non-empty string."
            )

        if not isinstance(amount, (int, float)) or amount < 0:
            raise InvalidBillingError(
                f"Invalid procedure charge: {name}"
            )