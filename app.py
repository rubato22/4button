from flask import Flask, render_template, redirect, url_for, request, session, jsonify
import RPi.GPIO as GPIO
import threading
import time
import os
from dotenv import load_dotenv

# Load the secrets from the .env file
load_dotenv()

app = Flask(__name__)
# Get secrets from environment or use a fallback
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'fallback_secret_for_dev')
PASSWORD = os.getenv('DASHBOARD_PASSWORD', 'admin') # Default is 'admin' if .env is missing

RELAY_PINS = {
    "heating": 32,
    "light1": 36,
    "light2": 38,
    "light3": 40
}

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

for pin in RELAY_PINS.values():
    GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH)

heating_end_time = 0

def auto_off_heating():
    global heating_end_time
    time.sleep(3600)  # 60 Minute Failsafe
    GPIO.output(RELAY_PINS["heating"], GPIO.HIGH)
    heating_end_time = 0

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form.get('password') == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
    return '''
        <body style="background:#000; color:#00ff41; font-family:monospace; text-align:center; padding-top:100px;">
            <h2>SYSTEM ACCESS REQUIRED</h2>
            <form method="post">
                <input type="password" name="password" style="padding:10px; background:#001500; color:#00ff41; border:1px solid #00ff41;">
                <input type="submit" value="DECRYPT" style="padding:10px; background:#00ff41; color:#000; font-weight:bold; border:none;">
            </form>
        </body>
    '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/system_status')
def system_status():
    if not session.get('logged_in'): return jsonify({"error": "unauthorized"})
    try:
        t = os.popen("/usr/bin/vcgencmd measure_temp").readline()
        temp = t.replace("temp=", "").replace("'C\n", "").strip()
        l = os.popen("top -bn1 | grep 'Cpu(s)' | sed 's/.*, *\([0-9.]*\)%* id.*/\\1/' | awk '{print 100 - $1\"%\"}'").readline().strip()
        d = os.popen("/bin/df -h / | awk 'NR==2{print $3 \"/\" $2 \" (\" $5 \")\"}'").readline().strip()
        v_check = os.popen("/usr/bin/vcgencmd get_throttled").readline().replace("throttled=", "").strip()
        volt_status = "STABLE" if v_check == "0x0" else "LOW PWR"
        return jsonify({"temp": temp, "load": l, "disk": d, "volt": volt_status})
    except:
        return jsonify({"temp": "??", "load": "??", "disk": "??", "volt": "??"})

@app.route('/heating_status')
def heating_status():
    global heating_end_time
    remaining = max(0, int(heating_end_time - time.time())) if heating_end_time > 0 else 0
    return jsonify({"remaining": remaining})

@app.route('/')
def index():
    if not session.get('logged_in'): return redirect(url_for('login'))
    status = {name: not GPIO.input(pin) for name, pin in RELAY_PINS.items()}
    return render_template('index.html', status=status)

@app.route('/toggle/<device>')
def toggle(device):
    if not session.get('logged_in'): return redirect(url_for('login'))
    global heating_end_time
    if device == "heating":
        is_on = GPIO.input(RELAY_PINS["heating"]) == GPIO.LOW
        if not is_on:
            GPIO.output(RELAY_PINS["heating"], GPIO.LOW)
            heating_end_time = time.time() + 3600
            threading.Thread(target=auto_off_heating, daemon=True).start()
        else:
            GPIO.output(RELAY_PINS["heating"], GPIO.HIGH)
            heating_end_time = 0
    elif device in RELAY_PINS:
        pin = RELAY_PINS[device]
        GPIO.output(pin, not GPIO.input(pin))
    return redirect(url_for('index'))


@app.route('/system/reboot')
def system_reboot():
    if not session.get('logged_in'): return redirect(url_for('login'))
    # The 'sleep' gives the browser time to acknowledge the command
    os.system("sleep 2 && sudo reboot &") 
    return "<h1>Rebooting...</h1><p>System will be back in 60 seconds.</p>"

@app.route('/system/shutdown')
def system_shutdown():
    if not session.get('logged_in'): return redirect(url_for('login'))
    os.system("sleep 2 && sudo shutdown -h now &")
    return "<h1>Shutting Down...</h1><p>Wait for the green light to stop blinking before pulling power.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055)
