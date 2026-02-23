import pytest
from uuid import uuid4
from datetime import datetime

import pytest

from app.db.session import SessionLocal
from app.models.user import User
from app.models.currency import Currency
from app.models.expense_tracker import Transaction
from app.bot.controller.expense.transaction_controller import (
    TransactionController,
    TransactionType,
    TransactionCategory,
)


# Mock DB Session
@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()


def _get_or_create_usd_currency(db):
    existing_currency = db.query(Currency).filter(Currency.code == "USD").first()
    if existing_currency:
        return existing_currency

    currency = Currency(
        name="US Dollar",
        code="USD",
        symbol="$",
        numeric_code=840,
        minor_unit=2,
    )
    db.add(currency)
    db.commit()
    db.refresh(currency)
    return currency


def test_add_expense_with_currency(db):
    # Setup
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_{unique_id}", email=f"test_{unique_id}@example.com")
    db.add(user)

    currency = _get_or_create_usd_currency(db)

    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    # Test adding expense with explicit currency
    response = controller.add_transaction(
        amount=100.0,
        description="Test Expense",
        transaction_type=TransactionType.EXPENSE,
        currency_code="USD",
        category=TransactionCategory.FOOD,
    )

    assert "Recorded expense" in response
    assert "100.0 USD" in response

    # Verify in DB
    transaction = (
        db.query(Transaction).filter(Transaction.user_id == user.id).first()
    )
    assert transaction is not None
    assert transaction.amount == 100.0
    assert transaction.currency_id == currency.id

    # Verify user default currency set
    db.refresh(user)
    assert user.currency_id == currency.id


def test_add_expense_no_currency_no_default(db):
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_{unique_id}")
    db.add(user)
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    # Expect failure
    response = controller.add_transaction(
        amount=50.0,
        description="No Currency",
        transaction_type=TransactionType.EXPENSE,
    )

    assert "Please set your default currency first" in response


def test_get_analytics(db):
    # Setup user with transactions
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_analytics_{unique_id}")
    db.add(user)

    currency = _get_or_create_usd_currency(db)

    user.currency_id = currency.id
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    controller.add_transaction(100.0, "Income", TransactionType.INCOME, "USD")
    controller.add_transaction(40.0, "Expense", TransactionType.EXPENSE, "USD")

    analytics = controller.get_analytics(time_range="current_month")

    assert "Income: 100.0" in analytics
    assert "Expense: 40.0" in analytics
    assert "Balance: 60.0" in analytics


def test_analytics_custom_range(db):
    # Setup user with transactions
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_range_{unique_id}")
    db.add(user)

    currency = _get_or_create_usd_currency(db)

    user.currency_id = currency.id
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    # Date format: YYYY-MM-DD
    controller.add_transaction(
        100.0,
        "Income Last Year",
        TransactionType.INCOME,
        "USD",
        date="2022-01-15",
    )
    controller.add_transaction(
        50.0,
        "Expense Last Year",
        TransactionType.EXPENSE,
        "USD",
        date="2022-01-20",
    )

    controller.add_transaction(
        200.0,
        "Income This Year",
        TransactionType.INCOME,
        "USD",
        date="2023-01-15",
    )

    # Test range that only includes 2022
    analytics_2022 = controller.get_analytics(
        start_date="2022-01-01",
        end_date="2022-12-31",
    )

    assert "Income: 100.0" in analytics_2022
    assert "Expense: 50.0" in analytics_2022

    # Test range that includes 2023 (assuming we are testing logic not just current year)
    analytics_2023 = controller.get_analytics(
        start_date="2023-01-01",
        end_date="2023-12-31",
    )
    assert "Income: 200.0" in analytics_2023
    assert "Expense: 0.0" in analytics_2023


def test_list_transactions_descending_and_limited(db):
    # Setup user and currency
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_list_{unique_id}")
    db.add(user)
    currency = _get_or_create_usd_currency(db)
    user.currency_id = currency.id
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    # Create transactions with specific dates (older to newer)
    controller.add_transaction(
        10.0,
        "Oldest",
        TransactionType.EXPENSE,
        "USD",
        date="2022-01-01",
    )
    controller.add_transaction(
        20.0,
        "Middle",
        TransactionType.EXPENSE,
        "USD",
        date="2022-02-01",
    )
    controller.add_transaction(
        30.0,
        "Newest",
        TransactionType.EXPENSE,
        "USD",
        date="2022-03-01",
    )

    # Ask for the last 2 transactions
    result = controller.list_transactions(limit=2)

    # Should mention "Here are your most recent transactions" and only the two newest
    assert "Here are your most recent transactions" in result
    assert "Newest" in result
    assert "Middle" in result
    assert "Oldest" not in result

    # Check order: Newest before Middle
    newest_index = result.index("Newest")
    middle_index = result.index("Middle")
    assert newest_index < middle_index


def test_list_transactions_includes_ids(db):
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_list_ids_{unique_id}")
    db.add(user)
    currency = _get_or_create_usd_currency(db)
    user.currency_id = currency.id
    db.commit()
    db.refresh(user)

    # Manually create a transaction so we know its ID
    tx = Transaction(
        user_id=user.id,
        currency_id=currency.id,
        amount=42.0,
        description="With known ID",
        category="test",
        type=TransactionType.EXPENSE,
        occurred_at=datetime.fromisoformat("2022-04-01"),
    )
    db.add(tx)
    db.commit()
    db.refresh(tx)

    controller = TransactionController(user.id)
    result = controller.list_transactions(limit=5)

    # The exact string may include other fields, but the ID should appear
    assert str(tx.id) in result


def test_delete_transaction_success_and_not_found(db):
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_delete_{unique_id}")
    db.add(user)
    currency = _get_or_create_usd_currency(db)
    user.currency_id = currency.id
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    # Create one transaction for this user
    controller.add_transaction(
        15.0,
        "To be deleted",
        TransactionType.EXPENSE,
        "USD",
        date="2022-05-01",
    )

    tx = (
        db.query(Transaction)
        .filter(Transaction.user_id == user.id)
        .order_by(Transaction.occurred_at.desc())
        .first()
    )
    assert tx is not None

    # Successful delete
    success_message = controller.delete_transaction(str(tx.id))
    assert "Deleted transaction" in success_message
    assert "To be deleted" in success_message

    # Ensure it's gone
    remaining = (
        db.query(Transaction)
        .filter(
            Transaction.user_id == user.id,
            Transaction.id == tx.id,
        )
        .first()
    )
    assert remaining is None

    # Deleting again should yield not found
    not_found_message = controller.delete_transaction(str(tx.id))
    assert "Transaction not found for your account" in not_found_message


def test_delete_transaction_invalid_uuid(db):
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_delete_invalid_{unique_id}")
    db.add(user)
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)

    message = controller.delete_transaction("not-a-uuid")
    assert "not a valid UUID" in message
