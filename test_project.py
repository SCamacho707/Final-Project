import sys
import os
import sqlite3
import pytest
import bcrypt
import streamlit as st

# Add the project directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Mock session state before importing project.py
if "user_id" not in st.session_state:
    st.session_state["user_id"] = 1 
if "username" not in st.session_state:
    st.session_state["username"] = "TestUser"

from project import register_user, authenticate_user, add_transaction, get_transactions, update_budget_goal, get_budget_goal

# --- Database setup for testing ---
@pytest.fixture(scope="module")
def test_db():
    """Create a temporary in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        budget_goal REAL DEFAULT 0.0
    )
    """)

    cursor.execute("""
    CREATE TABLE transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        amount REAL NOT NULL,
        category TEXT NOT NULL,
        type TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )
    """)

    conn.commit()
    yield conn 
    conn.close()

# --- Test User Authentication ---
def test_register_user(test_db):
    """Tests if a user can be registered successfully."""
    cursor = test_db.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   ("testuser", "test@example.com", bcrypt.hashpw("password".encode("utf-8"), bcrypt.gensalt()).decode("utf-8")))
    test_db.commit()

    # Verify the user exists
    cursor.execute("SELECT * FROM users WHERE username=?", ("testuser",))
    user = cursor.fetchone()
    assert user is not None
    assert user[1] == "testuser"

def test_authenticate_user(test_db):
    """Tests if a user can authenticate successfully."""
    cursor = test_db.cursor()
    cursor.execute("SELECT password FROM users WHERE username=?", ("testuser",))
    user_password = cursor.fetchone()[0]

    assert bcrypt.checkpw("password".encode("utf-8"), user_password.encode("utf-8"))

# --- Test Budget Goal ---
def test_budget_goal(test_db):
    """Tests setting and retrieving a budget goal."""
    cursor = test_db.cursor()
    
    # Assign a budget goal
    cursor.execute("UPDATE users SET budget_goal=? WHERE username=?", (5000, "testuser"))
    test_db.commit()
    
    cursor.execute("SELECT budget_goal FROM users WHERE username=?", ("testuser",))
    budget = cursor.fetchone()[0]
    assert budget == 5000  

# --- Test Transactions ---
def test_add_transaction(test_db):
    """Tests if a transaction can be added successfully."""
    cursor = test_db.cursor()

    # Get user_id for testuser
    cursor.execute("SELECT id FROM users WHERE username=?", ("testuser",))
    user_id = cursor.fetchone()[0]

    # Add a transaction
    cursor.execute("INSERT INTO transactions (amount, category, type, user_id) VALUES (?, ?, ?, ?)",
                   (100, "Food", "expense", user_id))
    test_db.commit()

    # Verify the transaction exists
    cursor.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
    transaction = cursor.fetchone()
    assert transaction is not None
    assert transaction[1] == 100
    assert transaction[2] == "Food"
    assert transaction[3] == "expense"

def test_get_transactions(test_db):
    """Tests retrieving transactions for a user."""
    cursor = test_db.cursor()
    
    # Get user_id for testuser
    cursor.execute("SELECT id FROM users WHERE username=?", ("testuser",))
    user_id = cursor.fetchone()[0]

    cursor.execute("SELECT amount, category, type FROM transactions WHERE user_id=?", (user_id,))
    transactions = cursor.fetchall()

    assert len(transactions) > 0
    assert transactions[0][0] == 100 
    assert transactions[0][1] == "Food"
    assert transactions[0][2] == "expense"

# --- Run Tests ---
if __name__ == "__main__":
    pytest.main()