# 🔐 Flask Password Strength Checker

A secure **Flask-based password strength analyzer** that evaluates passwords using
**entropy calculation, common password detection, pattern analysis, and offline
brute-force crack time estimation**.

This project is built for **cybersecurity education, defensive security awareness,
and academic demonstration**.

---

## 🚀 Features

- ✅ Password entropy calculation  
- 🚫 Common password blacklist detection  
- 🔁 Pattern & sequence detection (e.g. `123`, `abc`, `qwerty`)  
- ⏱️ Estimated offline brute-force crack time  
- 🛡️ Rate limiting (anti-abuse)  
- 🔒 Secure cookie & session configuration  
- 🌐 REST API support  

---

## 🧠 How the System Works

1. User submits a password via UI or API  
2. Input is sanitized  
3. Password is checked against:
   - Common password list
   - Length & character diversity
   - Sequential and repeated patterns
4. Entropy is calculated  
5. Crack time is estimated assuming an **offline attack**  
6. Result is returned as JSON  

---

## 🧪 Tech Stack

- **Backend:** Python, Flask  
- **Frontend:** HTML, CSS, JavaScript  
- **Security Concepts:**  
  - Entropy  
  - Brute-force modeling  
  - Rate limiting  
  - Input sanitization  

---

## 📁 Project Structure

```txt
password-strength-checker/
│── main.py
│── requirements.txt
│── README.md
│── .gitignore
│── common_passwords.txt
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    ├── script.js
    └── logo.png

```

## ⚙️ Installation & Setup Guide (Step-by-Step)

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/jatin-rajputt/password-strength-checker.git
cd password-strength-checker
```
###2️⃣ Create a Virtual Environment
python -m venv venv
###3️⃣ Activate the Virtual Environment
Windows (PowerShell):

venv\Scripts\Activate
Linux / macOS:

source venv/bin/activate
When activated, your terminal will show:

(venv)
###4️⃣ Install Dependencies
pip install -r requirements.txt
###5️⃣ Run the Application
python main.py
Open your browser and visit:

http://127.0.0.1:5000
⚠️ Disclaimer
This project is intended only for educational and defensive cybersecurity purposes.
Crack-time estimates are approximate and should not be treated as guarantees.

👨‍💻 Author
Jatin Thakur
🔐 Cybersecurity Student

🔗 GitHub: https://github.com/jatin-rajputt
