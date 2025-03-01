import streamlit as st
import sqlite3
import bcrypt
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

# --- Initialize Database ---
conn = sqlite3.connect("budget_tracker.db", check_same_thread=False)
cursor = conn.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    budget_goal REAL DEFAULT 0.0
)
""")

# Create Transactions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    type TEXT NOT NULL,  -- 'income' or 'expense'
    user_id INTEGER NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")
conn.commit()

# --- Ensure Session State Variables Exist ---
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = "Guest"

# --- Authentication Functions ---
def hash_password(password):
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(user_password.encode("utf-8"), hashed_password.encode("utf-8"))

def register_user(username, email, password):
    """Registers a new user in the database."""
    hashed_password = hash_password(password)
    try:
        cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  

def authenticate_user(email, password):
    """Authenticates a user and returns their ID and username if valid."""
    cursor.execute("SELECT id, username, password FROM users WHERE email=?", (email,))
    user = cursor.fetchone()
    if user and check_password(user[2], password):
        return user[0], user[1]  
    return None, None

# --- Budget Management Functions ---
def update_budget_goal(user_id, budget_goal):
    """Updates the user's budget goal."""
    cursor.execute("UPDATE users SET budget_goal=? WHERE id=?", (budget_goal, user_id))
    conn.commit()

def get_budget_goal(user_id):
    """Retrieves the budget goal of a user."""
    cursor.execute("SELECT budget_goal FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 0  

# --- Transaction Management ---
def add_transaction(user_id, amount, category, transaction_type):
    """Adds a transaction to the database."""
    cursor.execute("INSERT INTO transactions (amount, category, type, user_id) VALUES (?, ?, ?, ?)",
                   (amount, category, transaction_type, user_id))
    conn.commit()

def get_transactions(user_id):
    """Retrieves all transactions of a user."""
    cursor.execute("SELECT amount, category, type FROM transactions WHERE user_id=?", (user_id,))
    return pd.DataFrame(cursor.fetchall(), columns=["Amount", "Category", "Type"])

# --- Pie Chart Generation ---
def create_pie_chart(data):
    """Creates a pie chart for expense breakdown."""
    if not data:
        return "https://via.placeholder.com/300?text=No+Data"

    plt.figure(figsize=(5, 5))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return f'data:image/png;base64,{base64.b64encode(img.getvalue()).decode()}'

# --- Streamlit UI ---
st.title("💰 Personal Budget Tracker")

# --- Authentication UI ---
if not st.session_state["user_id"]:
    tab_login, tab_register = st.tabs(["Login", "Register"])

    with tab_login:
        st.subheader("🔑 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user_id, username = authenticate_user(email, password)
            if user_id:
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username
                st.success(f"Welcome back, {username}! 🎉")
                st.rerun()
            else:
                st.error("Invalid credentials. Try again.")

    with tab_register:
        st.subheader("📝 Register")
        username = st.text_input("Username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="register_confirm")

        if st.button("Register"):
            if password == confirm_password:
                if register_user(username, email, password):
                    st.success("Account created successfully! Please log in.")
                    st.rerun()
                else:
                    st.error("Email or username already exists. Try again.")
            else:
                st.error("Passwords do not match.")

    st.stop()

# --- Sidebar & Logout ---
st.sidebar.subheader(f"Hello, {st.session_state['username']}! 👋")
if st.sidebar.button("Logout"):
    st.session_state["user_id"] = None
    st.session_state["username"] = None
    st.rerun()

# --- Budget Goal Management ---
st.subheader("🎯 Set Budget Goal")
budget_goal = get_budget_goal(st.session_state["user_id"])
new_budget = st.number_input("Enter Budget Goal ($)", min_value=0.0, value=budget_goal)
if st.button("Update Budget"):
    update_budget_goal(st.session_state["user_id"], new_budget)
    st.success("Budget updated successfully!")
    st.rerun()

# --- Add Transactions ---
st.subheader("💸 Add Transaction")
amount = st.number_input("Amount ($)", min_value=0.01, format="%.2f")
category = st.selectbox("Category", ["Food", "Rent", "Transport", "Shopping", "Entertainment", "Others"])
transaction_type = st.radio("Type", ["income", "expense"])

if st.button("Add Transaction"):
    add_transaction(st.session_state["user_id"], amount, category, transaction_type)
    st.success("Transaction added successfully!")
    st.rerun()

# --- View Transactions ---
st.subheader("📊 Transaction History")
transactions = get_transactions(st.session_state["user_id"])
if not transactions.empty:
    st.dataframe(transactions)

    # --- Spending Analysis ---
    expenses = transactions[transactions["Type"] == "expense"]
    if not expenses.empty:
        category_expenses = expenses.groupby("Category")["Amount"].sum().to_dict()
        chart = create_pie_chart(category_expenses)
        st.image(chart, caption="Spending Breakdown", use_column_width=True)

        # --- Budget Summary ---
        total_expense = expenses["Amount"].sum()
        remaining_budget = budget_goal - total_expense

        st.subheader("📉 Budget Summary")
        st.write(f"**Total Expenses:** ${total_expense:.2f}")
        st.write(f"**Budget Goal:** ${budget_goal:.2f}")
        st.write(f"**Remaining Budget:** ${remaining_budget:.2f}")

        if remaining_budget < 0:
            st.error("⚠️ You're over budget! Consider reducing expenses.")
        else:
            st.success("✅ You're within budget. Keep it up!")
else:
    st.info("No transactions found. Add some to get insights.")

st.markdown("Built by Santiago & Asmy")