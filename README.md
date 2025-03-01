# 💰 Personal Budget Tracker

## Video Demo: https://youtu.be/FSPl9waQtqg

The **Personal Budget Tracker** is a financial management tool built using **Streamlit**, allowing users to track their income and expenses effectively. This web application enables users to:
- **Set a monthly budget goal** to manage finances. 🎯
- **Record and categorize transactions** as income or expenses. 💸
- **View a spending breakdown** through interactive pie charts. 📊
- **Securely log in and store transactions** using a SQLite database. 🔐

This project was developed as a **final coding project**, showcasing skills in **Python, databases, data visualization, and user authentication**.

## 🛠 **Design Choices & Justifications**

### 🔐 **Authentication & Security**
- **Why bcrypt for password hashing?**  
  - To prevent storing plain-text passwords and enhance security.
  - Hashing ensures that user credentials remain protected.
- **Why session management in `st.session_state`?**  
  - Unlike Flask sessions, Streamlit doesn’t have built-in authentication.
  - Using `st.session_state` allows users to stay logged in during their session.

### 🗄 **Database: SQLite**
- **Why SQLite instead of PostgreSQL or MySQL?**  
  - SQLite is **lightweight**, requires no server setup, and is ideal for small applications.
  - Since the project is local-first, SQLite is a simple and effective choice.

### 🎨 **User Interface & Visualization**
- **Why Streamlit for the UI?**  
  - It provides **quick, interactive dashboards** without needing HTML/CSS/JS.
  - It offers **widgets (buttons, sliders, forms, etc.)** that improve user interaction.
- **Why Matplotlib for charts?**  
  - It allows **customized pie charts** for analyzing spending.
  - Integrates seamlessly with **pandas** for data manipulation.

### 📊 **Handling Budget & Transactions**
- **Why allow both income & expenses?**  
  - To provide a **complete financial picture** rather than just tracking expenses.
- **How does budget tracking work?**  
  - Users **set a monthly budget goal**.
  - **Each expense is deducted** from the goal, showing the remaining balance.
  - If spending exceeds the goal, a **warning is displayed**.

## 🤖 **AI-Assisted Development**

While this project was fully developed by US, **AI tools were used to enhance productivity**, including:

### ✅ **Areas AI Assisted In**
- **Debugging & Code Review**  
  - AI helped identify syntax errors and logic issues.
- **Performance Optimization**  
  - Suggested improvements for database queries and session handling.
- **Documentation & Readability**  
  - Assisted in structuring docstrings and improving explanations.
- **README Formatting & Content**  
  - AI provided guidance on organizing this documentation.

### ⚠️ **Citing AI Use**
- **Any AI-assisted code improvements are noted in comments** within `project.py`.
- AI was used as a **helper tool**, not as a replacement for writing the code.


## 🚀 **Future Improvements**
While the project is functional, several enhancements can be made:

### 🔗 **Integrate Real-Time Financial APIs**
- **Why?**  
  - Instead of manual entry, users can **sync bank transactions** automatically.
- **How?**  
  - Using the **Plaid API** or **YNAB API** to fetch real-time data.

### 📂 **CSV Export & Import**
- **Why?**  
  - Users may want to **export their transactions** for tax filing or personal records.
  - Allows users to **import historical data** instead of adding transactions manually.

### 📊 **More Advanced Financial Analysis**
- **Why?**  
  - Currently, users only see a simple expense breakdown.
  - Adding **bar charts for monthly trends** can improve financial insights.

### 🎨 **Enhanced UI & Design**
- **Why?**  
  - While functional, the UI could be improved with **custom styling**.
  - Adding **animations & better dashboard layouts** would improve user experience.

### 📆 **Recurring Transactions**
- **Why?**  
  - Many users have **monthly subscriptions (Netflix, gym, rent, etc.)**.
  - Implementing **automatic recurring expenses** would make tracking easier.

### 🏆 **Financial Challenges**
- **Why?**  
  - Encouraging **saving goals, weekly spending limits, or financial challenges** could make budgeting more engaging.

## 📜 **Acknowledgments**
- **Streamlit documentation** for UI inspiration.
- **Matplotlib & Pandas** for visualization.
- **CS50 & Python community** for general coding best practices.
