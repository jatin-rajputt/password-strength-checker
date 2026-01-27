from flask import Flask, render_template, request, jsonify
import re
import time
from collections import defaultdict
import html
import math
import os

app = Flask(__name__)

app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  
app.config['SESSION_COOKIE_SECURE'] = True        
app.config['SESSION_COOKIE_HTTPONLY'] = True      
app.config['SESSION_COOKIE_NAME'] = '__Secure-Session'
app.secret_key = os.environ.get('FLASK_SECRET', 'xxxxxxx')

rate_limit_store = defaultdict(list)

def load_common_passwords():
    try:
        with open('common_passwords.txt', 'r', encoding='utf-8', errors='ignore') as f:
            passwords = set(line.strip() for line in f.readlines() if line.strip())
        return passwords
    except FileNotFoundError:
        print("Warning: common_passwords.txt not found. Please download it from SecLists.")
        return set()

COMMON_PASSWORDS = load_common_passwords()
COMMON_PASSWORDS_LOWER = {pwd.lower() for pwd in COMMON_PASSWORDS}

def sanitize_input(password):
    if not isinstance(password, str):
        return ""
    return password[:1024]

def check_common_password(password):
    password_normalized = password.strip()
    if password_normalized.lower() in COMMON_PASSWORDS_LOWER:
        return True
    return False

def calculate_entropy(password):
    charset_size = 0
    
    if re.search(r'[a-z]', password):
        charset_size += 26
    if re.search(r'[A-Z]', password):
        charset_size += 26
    if re.search(r'\d', password):
        charset_size += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>[\]\\`~_+=/-]', password):
        charset_size += 32
    
    if charset_size > 0 and len(password) > 0:
        entropy = len(password) * math.log2(charset_size)
        return entropy
    return 0

def calculate_pattern_score(password):
    score = 0
    
    if re.search(r'(123|abc|qwe|asd|zxc|098|789)', password.lower()):
        score -= 10
    
    if re.search(r'(.)\1{2,}', password):
        score -= 5
    
    if re.search(r'(012|123|234|345|456|567|678|789|890|abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)', password.lower()):
        score -= 10
    
    common_words = ['password', 'admin', 'user', 'login', 'welcome', 'hello', 'test', 'name', 'email', 'home', 'work', 'play', 'game', 'music', 'video', 'photo', 'data', 'info', 'help', 'web', 'mail', 'chat', 'file', 'new', 'old', 'top', 'end', 'start', 'stop', 'go', 'run', 'fast', 'slow', 'big', 'small', 'long', 'short', 'high', 'low', 'up', 'down', 'left', 'right', 'yes', 'no', 'ok', 'good', 'bad', 'hot', 'cold', 'warm', 'cool', 'red', 'blue', 'green', 'yellow', 'black', 'white', 'gray', 'grey']
    for word in common_words:
        if word in password.lower():
            score -= 15
            break
    
    return score

def estimate_crack_time(password):
    if check_common_password(password):
        return "Instantly", "0 seconds"
    

    if re.match(r'^\d+$', password):
        numeric_time = (10 ** len(password)) / 1000000000
        if numeric_time < 1:
            return "Instantly", f"{numeric_time:.6f} seconds"
        elif numeric_time < 60:
            return f"About {int(numeric_time)} seconds", f"{numeric_time:.2f} seconds"
        elif numeric_time < 3600:
            return f"About {int(numeric_time/60)} minutes", f"{numeric_time:.2f} seconds"
        elif numeric_time < 86400:
            return f"About {int(numeric_time/3600)} hours", f"{numeric_time:.2f} seconds"
        elif numeric_time < 31536000:
            return f"About {int(numeric_time/86400)} days", f"{numeric_time:.2f} seconds"
        else:
            return f"About {int(numeric_time/31536000)} years", f"{numeric_time:.2f} seconds"
    


    entropy = calculate_entropy(password)
    pattern_score = calculate_pattern_score(password)
    

    adjusted_entropy = max(entropy + pattern_score, 0)
    


    attack_rate = 1000000000  # 1 billion guesses per second for offline attacks
    

    try:
        time_seconds = (2**adjusted_entropy) / attack_rate
    except (OverflowError, ValueError):

        return "Centuries", "Too long to calculate"
    

    def format_time(seconds):
        if seconds < 1:
            return "Instantly", f"{seconds:.6f} seconds"
        
        intervals = [
            ('year', 365 * 24 * 60 * 60),
            ('month', 30 * 24 * 60 * 60),
            ('week', 7 * 24 * 60 * 60),
            ('day', 24 * 60 * 60),
            ('hour', 60 * 60),
            ('minute', 60),
            ('second', 1)
        ]
        
        for name, count in intervals:
            value = seconds // count
            if value >= 1:
                if value >= 1:
                    if name == 'year' and value >= 100:
                        return f"{int(value)}+ years", f"{seconds:.2f} seconds"
                    elif value == 1:
                        return f"About {int(value)} {name}", f"{seconds:.2f} seconds"
                    else:
                        return f"About {int(value)} {name}s", f"{seconds:.2f} seconds"
        
        return "Instantly", f"{seconds:.6f} seconds"
    
    return format_time(time_seconds)

def calculate_password_score(password):
    score = 0
    reasons = []
    tips = []
    

    if check_common_password(password):
        return 0, "Very Weak", ["This password is in the list of commonly used passwords - avoid using it"], True, ["Common password"], "Instantly"
    

    length = len(password)
    if length < 4:
        score += 0
        reasons.append("Too short")
        tips.append("Use at least 8 characters")
    elif length < 8:
        score += 5
        reasons.append("Short")
        tips.append("Use at least 8 characters")
    elif length < 12:
        score += 15
    elif length < 16:
        score += 25
    else:
        score += 30
    

    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>[\]\\`~_+=/-]', password))
    
    diversity_score = sum([has_lower, has_upper, has_digit, has_symbol]) * 10
    score += diversity_score
    
    if not has_lower:
        reasons.append("No lowercase letters")
        tips.append("Include lowercase letters (a-z)")
    if not has_upper:
        reasons.append("No uppercase letters")
        tips.append("Include uppercase letters (A-Z)")
    if not has_digit:
        reasons.append("No numbers")
        tips.append("Include numbers (0-9)")
    if not has_symbol:
        reasons.append("No special characters")
        tips.append("Include special characters (!@#$%^*)")
    

    sequential_patterns = [
        '123456789',
        '987654321',
        'abcdef',
        'fedcba',
        'qwerty',
        'asdfgh',
        'zxcvbn'
    ]
    
    password_lower = password.lower()
    for pattern in sequential_patterns:
        if pattern in password_lower or pattern[::-1] in password_lower:
            score -= 10
            reasons.append("Sequential pattern detected")
            tips.append("Avoid sequential patterns like '1234' or 'abcd'")
            break
    

    if re.search(r'(.)\1{2,}', password):
        score -= 5
        reasons.append("Repeated characters")
        tips.append("Avoid repeating the same character multiple times")
    

    common_words = ['password', 'admin', 'user', 'login', 'welcome', 'hello', 'test']
    for word in common_words:
        if word in password_lower and len(password) < 10:
            score -= 10
            reasons.append("Contains common word")
            tips.append(f"Avoid using common words like '{word}'")
            break
    

    score = max(0, min(100, score))
    

    if score >= 80:
        strength = "Very Strong"
    elif score >= 60:
        strength = "Strong"
    elif score >= 40:
        strength = "Moderate"
    elif score >= 20:
        strength = "Weak"
    else:
        strength = "Very Weak"
    

    tips = tips[:3]
    

    crack_time, raw_time = estimate_crack_time(password)
    
    return score, strength, tips, False, reasons, crack_time

def rate_limit_check(ip):
    now = time.time()

    rate_limit_store[ip] = [req_time for req_time in rate_limit_store[ip] if now - req_time < 60]
    
    if len(rate_limit_store[ip]) >= 10:  # 10 requests per minute
        return True
    
    rate_limit_store[ip].append(now)
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_password():

    if rate_limit_check(request.remote_addr):
        return jsonify({
            'error': 'Rate limit exceeded. Please try again later.',
            'score': 0,
            'strength': 'Rate Limited',
            'tips': ['Too many requests. Please wait before trying again.'],
            'is_common': False,
            'reasons': ['Rate limited'],
            'crack_time': 'N/A'
        }), 429
    

    password = None
    if request.is_json:
        data = request.get_json()
        password = data.get('password', '') if data else ''
    else:
        password = request.form.get('password', '')
    

    password = sanitize_input(password)
    
    try:

        score, strength, tips, is_common, reasons, crack_time = calculate_password_score(password)
        

        escaped_tips = [html.escape(tip, quote=False) for tip in tips]
        
        return jsonify({
            'score': score,
            'strength': strength,
            'tips': escaped_tips,
            'is_common': is_common,
            'reasons': reasons,
            'crack_time': crack_time
        })
    except Exception as e:

        print(f"Error processing password: {str(e)}")
        return jsonify({
            'error': 'An error occurred while processing your password. Please try again.',
            'score': 0,
            'strength': 'Error',
            'tips': ['An error occurred. Please try again.'],
            'is_common': False,
            'reasons': ['Processing error'],
            'crack_time': 'N/A'
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
