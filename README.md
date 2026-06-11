TeamSync DevOps Platform 🚀
TeamSync ek collaborative web-based platform hai jo DevOps aur Data Engineering teams ke liye banaya gaya hai. Isme SQL analytics, Python sandbox, aur team communication ek hi jagah milti hai.

📁 Project Structure
Project files ko aise organize kiya gaya hai:

Plaintext
TeamSync-DevOps-Platform/
├── main_app.py           # Main application entry point (Streamlit)
├── style.css             # UI styling and design
├── requirements.txt      # Required Python libraries
├── backend/
│   └── db_connect.py     # Database connection handling
├── engines/
│   ├── sql_engine.py     # SQL query execution logic
│   └── python_sandbox.py # Python code execution engine
└── chat_log.txt          # Shared chat history
🛠 Features
SQL Query Console: Real-time database management and querying.

Python Sandbox: Direct code execution for automation tasks.

Shared Workspace: Real-time collaboration via Chat.

Admin Controls: Factory reset and log management for admins.

🚀 Deployment
Ye project Streamlit Cloud par deploy kiya gaya hai.

Kaise run karein?
Repository clone karein:

Bash
git clone https://github.com/Arpitjalwal/TeamSync-DevOps-Platform.git
Dependencies install karein:

Bash
pip install -r requirements.txt
App run karein:

Bash
streamlit run main_app.py
