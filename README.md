********Relays and electrics are dangerous. This is a description of what worked for me, it is not a guide in that regard as every situation is different******** 

# 4button
A Raspberry Pi based Flask app with html, providing a webpage with Login, Pi Data, City Times, Four buttons controlling four gpio pins, a log out and a remote shutdown/reboot incase ssh goes down but the site may still be up (fingers crossed)  

# ⚡ IoT Pi Dashboard

Matrix-inspired Raspberry Pi gpio controller with add-ons. Featuring real-time system diagnostics and a heating timer. I personally wire this heating relay in parallel with a simple volt free thermostat on my combi boiler and have added the timer as when the relay is active it supercedes the room thermostat. 

## 🌟 Features

- **Matrix Aesthetic**: 
- **Heating Timer**: Heating relay includes a 60-minute hardware-software failsafe. If you turn the heating on remotely and forget, the Pi kills the relay after one hour to prevent thermostat conflicts.
- **Live Pi Vitals**: Real-time monitoring of CPU Temperature, System Load, Disk Usage, and Voltage Stability (Throttling check).
- **World Clocks**: London, New York, and Tokyo time-syncing.


## 🛠 Hardware Requirements

- **Raspberry Pi** (Tested on Pi 3B+ Bookworm)
- **4-Channel Relay Board**
- 

### GPIO Mapping (Physical Pins)
| Device  | GPIO Pin |
|---------|----------|
| Heating | 32       |
| Light 1 | 36       |
| Light 2 | 38       |
| Light 3 | 40       |



## 🚀 Installation

** Create the 4button directory -- 
mkdir 4button
cd 4button

Create the virtual environment that python requires (depends on distro, bookworm and onwards do)

python3 -m venv env

##Optionally, to include pre-installed system packages, use:

python3 -m venv --system-site-packages env

Activate the environment:

source env/bin/activate


1. **Clone the repo**:
   ```bash
   git clone [https://github.com/rubato22/4button.git](https://github.com/rubato22/4button.git)
   

**Install dependencies**:

pip install flask RPi.GPIO python-dotenv

### 🔐 Security Setup (.env)
This app uses a `.env` file to keep your passwords secure and out of the code. 
Create a file named `.env` in the project folder and add your credentials:
```text
FLASK_SECRET_KEY=change_this_to_a_random_string
DASHBOARD_PASSWORD=your_custom_password

**Run the app**:
python3 app.py

### ⚙️ Port Configuration
By default, the app binds to `0.0.0.0` (making it accessible across your local network) on port `5055`. 
If you need to change the port to avoid conflicts with other apps, edit the very bottom of `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5055) # Change 5055 to your desired port

Access the dashboard at `http://your-pi-ip:5055`


## 📜 License

MIT License - Free to use, tweak, and share.




```
