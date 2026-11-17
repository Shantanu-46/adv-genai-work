from dataclasses import dataclass


@dataclass
class Applicant:
    name: str
    monthly_income: float
    existing_emi: float
    requested_emi: float
    credit_score: int


class InvalidApplicantError(Exception):
    """The applicant's form contains invalid information."""


class LoanRejectedError(Exception):
    """The loan does not satisfy bank rules."""


def foir(a: Applicant) -> float:
    """Calculate Fixed Obligation to Income Ratio."""

    if a.monthly_income <= 0:
        raise InvalidApplicantError("income cannot be zero or negative")

    return (a.existing_emi + a.requested_emi) / a.monthly_income


def validate_applicant(a: Applicant):

    if a.monthly_income <= 0:
        raise InvalidApplicantError("income cannot be zero or negative")

    if not (300 <= a.credit_score <= 900):
        raise InvalidApplicantError("invalid credit score")

    if a.requested_emi <= 0:
        raise InvalidApplicantError("requested EMI must be positive")


def check_loan(a: Applicant, min_credit_score=650, max_foir=0.5):

    validate_applicant(a)

    ratio = foir(a)

    if a.credit_score < min_credit_score:
        raise LoanRejectedError(
            f"credit score {a.credit_score} below {min_credit_score}"
        )

    if ratio > max_foir:
        raise LoanRejectedError(
            f"FOIR {ratio:.2f} above {max_foir}"
        )

    return f"{a.name}: APPROVED, FOIR {ratio:.2f}"


# Applicant records
applicants = [
    Applicant("Ravi", 80000, 10000, 15000, 720),
    Applicant("Meera", 40000, 5000, 10000, 600),
    Applicant("Zoya", 0, 0, 10000, 700)
]


# Process loan applications
for applicant in applicants:

    try:
        result = check_loan(applicant)
        print(result)

    except InvalidApplicantError as e:
        print(f"{applicant.name}: INVALID APPLICATION - {e}")

    except LoanRejectedError as e:
        print(f"{applicant.name}: REJECTED - {e}")