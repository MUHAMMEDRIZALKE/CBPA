import pytest
from uuid import uuid4
from datetime import datetime
from app.db.session import SessionLocal
from app.models.user import User
from app.models.currency import Currency
from app.models.expense_tracker import Transaction
from app.bot.controller.expense.transaction_controller import TransactionController, TransactionType, TransactionCategory

# Mock DB Session
@pytest.fixture
def db():
    session = SessionLocal()
    yield session
    session.close()

def test_add_expense_with_currency(db):
    # Setup
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_{unique_id}", email=f"test_{unique_id}@example.com")
    db.add(user)
    
    currency = Currency(name="US Dollar", code="USD", symbol="$", numeric_code=840, minor_unit=2)
    # Check if currency exists first to avoid duplicate key error in test
    existing_currency = db.query(Currency).filter(Currency.code == "USD").first()
    if not existing_currency:
        db.add(currency)
        currency_id = currency.id
    else:
        currency_id = existing_currency.id
    
    db.commit()
    db.refresh(user)

    controller = TransactionController(user.id)
    
    # Test adding expense with explicit currency
    response = controller.add_transaction(
        amount=100.0,
        description="Test Expense",
        transaction_type=TransactionType.EXPENSE,
        currency_code="USD",
        category=TransactionCategory.FOOD
    )
    
    assert "Recorded expense" in response
    assert "100.0 USD" in response

    # Verify in DB
    transaction = db.query(Transaction).filter(Transaction.user_id == user.id).first()
    assert transaction is not None
    assert transaction.amount == 100.0
    assert transaction.currency_id == currency_id
    
    # Verify user default currency set
    db.refresh(user)
    assert user.currency_id == currency_id

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
        transaction_type=TransactionType.EXPENSE
    )
    
    assert "Please set your default currency first" in response

def test_get_analytics(db):
    # Setup user with transactions
    unique_id = str(uuid4())[:8]
    user = User(username=f"user_analytics_{unique_id}")
    db.add(user)
    
    existing_currency = db.query(Currency).filter(Currency.code == "USD").first()
    if not existing_currency:
        currency = Currency(name="US Dollar", code="USD", symbol="$", numeric_code=840, minor_unit=2)
        db.add(currency)
        currency_id = currency.id
    else:
        currency_id = existing_currency.id
        
    user.currency_id = currency_id
    db.commit()
    db.refresh(user)
    
    controller = TransactionController(user.id)
    
    controller.add_transaction(100.0, "Income", TransactionType.INCOME, "USD")
    controller.add_transaction(40.0, "Expense", TransactionType.EXPENSE, "USD")
    
    analytics = controller.get_analytics(time_range="current_month")
    
    assert "Income: 100.0" in analytics
    assert "Expense: 40.0" in analytics
    assert "Balance: 60.0" in analytics
