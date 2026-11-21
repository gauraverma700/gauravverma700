from flask import Flask, request, render_template_string
import ipaddress
import re
from datetime import datetime

app = Flask(__name__)

# DEMO TRUSTED DEVICE INFORMATION
TRUSTED_IP = "192.168.10.1"
TRUSTED_MAC = "AA:BB:CC:DD:EE:01"

activity_logs = []

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>IP Protector | Security Center</title>

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">

<style>

:root {
    --bg: #080d19;
    --panel: #111a2b;
    --panel2: #151f33;
    --border: #24314a;
    --blue: #4285ff;
    --cyan: #19d5ff;
    --text: #f1f5ff;
    --muted: #8290aa;
    --green: #20d6a1;
    --red: #ff5470;
    --yellow: #ffbd59;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: var(--bg);
    color: var(--text);
    font-family: 'Inter', sans-serif;
    min-height: 100vh;
}

/* SIDEBAR */

.sidebar {
    position: fixed;
    width: 245px;
    height: 100vh;
    background: #0d1423;
    border-right: 1px solid var(--border);
    padding: 28px 18px;
}

.logo {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 45px;
}

.logo-icon {
    width: 43px;
    height: 43px;
    background: linear-gradient(135deg, #2678ff, #00d4ff);
    border-radius: 12px;
    display: grid;
    place-items: center;
    font-size: 23px;
}

.logo h2 {
    font-size: 19px;
    font-weight: 800;
}

.logo span {
    color: var(--cyan);
}

.menu-title {
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 1.5px;
    margin: 25px 10px 12px;
}

.nav-item {
    display: block;
    text-decoration: none;
    color: #9eabc2;
    padding: 13px;
    border-radius: 9px;
    margin-bottom: 7px;
    font-size: 13px;
    transition: 0.3s;
}

.nav-item:hover,
.nav-item.active {
    background: #192d4d;
    color: #55a3ff;
}

.sidebar-bottom {
    position: absolute;
    bottom: 25px;
    left: 20px;
    right: 20px;
    padding: 15px;
    border: 1px solid var(--border);
    border-radius: 10px;
    font-size: 11px;
    color: var(--muted);
    line-height: 1.8;
}

/* MAIN CONTENT */

.main {
    margin-left: 245px;
    padding: 35px 42px;
    max-width: 1600px;
}

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 35px;
    gap: 15px;
}

.topbar h1 {
    font-size: 27px;
    font-weight: 700;
}

.topbar p {
    color: var(--muted);
    font-size: 13px;
    margin-top: 8px;
}

.system-badge {
    background: #102e2a;
    border: 1px solid #1b755d;
    color: var(--green);
    padding: 10px 15px;
    border-radius: 30px;
    font-size: 12px;
    white-space: nowrap;
}

.dot {
    display: inline-block;
    width: 7px;
    height: 7px;
    border-radius: 50%;
    background: var(--green);
    margin-right: 7px;
}

/* CARDS */

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}

.card {
    background: linear-gradient(145deg, #151f33, #101827);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 23px;
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-3px);
    border-color: #426bb0;
}

.card-label {
    color: var(--muted);
    font-size: 12px;
    margin-bottom: 18px;
}

.card-value {
    font-size: 19px;
    font-weight: 700;
    overflow-wrap: anywhere;
}

.card-icon {
    float: right;
    font-size: 23px;
}

.card-small {
    color: var(--muted);
    font-size: 11px;
    margin-top: 12px;
}

/* MAIN GRID */

.content-grid {
    display: grid;
    grid-template-columns: 1.2fr 0.8fr;
    gap: 22px;
    margin-top: 25px;
}

.panel {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 13px;
    padding: 26px;
}

.panel-header {
    margin-bottom: 25px;
}

.panel-header h2 {
    font-size: 17px;
}

.panel-header p {
    font-size: 12px;
    color: var(--muted);
    margin-top: 8px;
}

label {
    display: block;
    font-size: 12px;
    color: #b9c6dc;
    margin-bottom: 9px;
}

input {
    width: 100%;
    background: #0b1220;
    border: 1px solid #293954;
    color: white;
    padding: 14px;
    border-radius: 8px;
    outline: none;
    font-size: 13px;
    margin-bottom: 20px;
    font-family: monospace;
    transition: 0.3s;
}

input:focus {
    border-color: var(--blue);
    box-shadow: 0 0 0 3px #4285ff20;
}

button {
    width: 100%;
    padding: 15px;
    border: none;
    border-radius: 8px;
    background: linear-gradient(100deg, #286cff, #12b8ed);
    color: white;
    font-size: 13px;
    font-weight: 700;
    cursor: pointer;
    transition: 0.3s;
}

button:hover {
    opacity: 0.85;
    transform: translateY(-2px);
}

/* RESULT */

.result {
    padding: 17px;
    margin-top: 22px;
    border-radius: 9px;
    background: #17243a;
    border: 1px solid var(--border);
}

.result h3 {
    font-size: 14px;
    margin-bottom: 8px;
}

.result p {
    color: #a9b7cc;
    font-size: 12px;
    line-height: 1.6;
}

.result.trusted {
    border-left: 4px solid var(--green);
}

.result.alert {
    border-left: 4px solid var(--red);
}

.result.warning {
    border-left: 4px solid var(--yellow);
}

/* TRUSTED INFO */

.info-row {
    display: flex;
    justify-content: space-between;
    padding: 17px 0;
    border-bottom: 1px solid var(--border);
    gap: 12px;
}

.info-row:last-child {
    border-bottom: none;
}

.info-row span {
    color: var(--muted);
    font-size: 12px;
}

.info-row strong {
    font-size: 12px;
    color: var(--cyan);
    font-family: monospace;
    overflow-wrap: anywhere;
    text-align: right;
}

/* ACTIVITY */

.activity {
    margin-top: 23px;
}

.activity table {
    width: 100%;
    border-collapse: collapse;
    min-width: 650px;
}

.activity th {
    color: var(--muted);
    font-size: 11px;
    text-align: left;
    padding: 15px;
    border-bottom: 1px solid var(--border);
}

.activity td {
    font-size: 12px;
    padding: 15px;
    border-bottom: 1px solid #202c40;
}

.activity-wrap {
    overflow-x: auto;
}

.status {
    padding: 6px 10px;
    border-radius: 20px;
    font-size: 10px;
    display: inline-block;
}

.status.trusted {
    background: #123d34;
    color: var(--green);
}

.status.alert {
    background: #481e2b;
    color: var(--red);
}

.status.warning {
    background: #44351b;
    color: var(--yellow);
}

.status.neutral {
    background: #26364e;
    color: #a9c5ff;
}

.empty {
    color: var(--muted);
    text-align: center;
    padding: 30px;
    font-size: 12px;
}

/* FOOTER */

footer {
    margin-top: 30px;
    padding: 20px 0;
    border-top: 1px solid var(--border);
    color: var(--muted);
    font-size: 11px;
    text-align: center;
}

/* RESPONSIVE */

@media(max-width: 1000px) {

    .sidebar {
        width: 190px;
    }

    .main {
        margin-left: 190px;
        padding: 25px;
    }

    .content-grid {
        grid-template-columns: 1fr;
    }
}

@media(max-width: 700px) {

    .sidebar {
        position: relative;
        width: 100%;
        height: auto;
        padding: 18px;
    }

    .logo {
        margin-bottom: 15px;
    }

    .menu-title,
    .nav-item,
    .sidebar-bottom {
        display: none;
    }

    .main {
        margin-left: 0;
        padding: 20px;
    }

    .stats {
        grid-template-columns: 1fr;
    }

    .topbar {
        align-items: flex-start;
        flex-direction: column;
    }
}

</style>
</head>

<body>

<aside class="sidebar">

    <div class="logo">
        <div class="logo-icon">🛡</div>
        <h2>IP <span>PROTECTOR</span></h2>
    </div>

    <p class="menu-title">MAIN MENU</p>

    <a href="/" class="nav-item active">▦ &nbsp; Dashboard</a>
    <a href="#verification" class="nav-item">◈ &nbsp; IP Verification</a>
    <a href="#trusted" class="nav-item">✓ &nbsp; Trusted Device</a>
    <a href="#activity" class="nav-item">◷ &nbsp; Activity Logs</a>

    <div class="sidebar-bottom">
        PROJECT VERSION<br>
        <strong style="color:white">1.0.0 Prototype</strong><br><br>
        ABES Engineering College
    </div>

</aside>


<main class="main">

    <div class="topbar">

        <div>
            <h1>Security Dashboard</h1>
            <p>Network identity verification and ARP spoofing simulation.</p>
        </div>

        <div class="system-badge">
            <span class="dot"></span>
            Application Online
        </div>

    </div>


    <section class="stats">

        <div class="card">
            <span class="card-icon">🛡</span>
            <p class="card-label">APPLICATION STATUS</p>
            <h2 class="card-value">ONLINE</h2>
            <p class="card-small">Python Flask server running</p>
        </div>

        <div class="card">
            <span class="card-icon">🌐</span>
            <p class="card-label">TRUSTED ROUTER IP</p>
            <h2 class="card-value">{{ trusted_ip }}</h2>
            <p class="card-small">Predefined demo IP address</p>
        </div>

        <div class="card">
            <span class="card-icon">📡</span>
            <p class="card-label">TOTAL CHECKS</p>
            <h2 class="card-value">{{ total_checks }}</h2>
            <p class="card-small">Manual verification attempts</p>
        </div>

    </section>


    <section class="content-grid">

        <div class="panel" id="verification">

            <div class="panel-header">
                <h2>◈ &nbsp; IP & MAC Verification</h2>
                <p>Enter network identity details to verify the mapping.</p>
            </div>

            <form method="POST">

                <label>IP ADDRESS</label>

                <input
                    type="text"
                    name="ip"
                    placeholder="192.168.10.1"
                    required
                >

                <label>MAC ADDRESS</label>

                <input
                    type="text"
                    name="mac"
                    placeholder="AA:BB:CC:DD:EE:01"
                    required
                >

                <button type="submit">
                    ANALYZE NETWORK IDENTITY →
                </button>

            </form>

            {% if result %}

            <div class="result {{ result_class }}">

                <h3>{{ result }}</h3>

                <p>{{ message }}</p>

            </div>

            {% endif %}

        </div>


        <div class="panel" id="trusted">

            <div class="panel-header">
                <h2>✓ &nbsp; Trusted Device Information</h2>
                <p>Predefined trusted router identity.</p>
            </div>

            <div class="info-row">
                <span>Device</span>
                <strong>MAIN ROUTER</strong>
            </div>

            <div class="info-row">
                <span>Trusted IP</span>
                <strong>{{ trusted_ip }}</strong>
            </div>

            <div class="info-row">
                <span>Trusted MAC</span>
                <strong>{{ trusted_mac }}</strong>
            </div>

            <div class="info-row">
                <span>Verification Mode</span>
                <strong>MANUAL</strong>
            </div>

        </div>

    </section>


    <section class="panel activity" id="activity">

        <div class="panel-header">
            <h2>◷ &nbsp; Security Activity Logs</h2>
            <p>History of IP and MAC verification attempts during this session.</p>
        </div>

        <div class="activity-wrap">

            <table>

                <thead>
                    <tr>
                        <th>TIME</th>
                        <th>IP ADDRESS</th>
                        <th>MAC ADDRESS</th>
                        <th>SECURITY STATUS</th>
                    </tr>
                </thead>

                <tbody>

                    {% for log in logs %}

                    <tr>
                        <td>{{ log.time }}</td>
                        <td>{{ log.ip }}</td>
                        <td>{{ log.mac }}</td>

                        <td>
                            <span class="status {{ log.css }}">
                                {{ log.status }}
                            </span>
                        </td>
                    </tr>

                    {% else %}

                    <tr>
                        <td colspan="4" class="empty">
                            No verification activity yet.
                        </td>
                    </tr>

                    {% endfor %}

                </tbody>

            </table>

        </div>

    </section>


    <footer>
        IP PROTECTOR | ARP SPOOFING DETECTION PROTOTYPE<br><br>
        B.Tech First Year Project | ABES Engineering College, Ghaziabad<br>
        Student: Gaurav Verma | Roll No: 2026B02310097
    </footer>

</main>

</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def dashboard():

    result = ""
    message = ""
    result_class = ""

    if request.method == "POST":

        ip = request.form.get("ip", "").strip()
        mac = request.form.get("mac", "").strip().upper()

        status = ""
        css = "neutral"

        # Validate IP
        try:
            ipaddress.ip_address(ip)
            valid_ip = True
        except ValueError:
            valid_ip = False

        # Validate MAC
        pattern = r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$"
        valid_mac = bool(re.fullmatch(pattern, mac))

        if not valid_ip:

            result = "INVALID IP ADDRESS"
            message = "The entered IP address format is incorrect."
            status = "Invalid IP"
            result_class = "alert"
            css = "alert"

        elif not valid_mac:

            result = "INVALID MAC ADDRESS"
            message = "The entered MAC address format is incorrect."
            status = "Invalid MAC"
            result_class = "alert"
            css = "alert"

        elif ip == TRUSTED_IP and mac == TRUSTED_MAC:

            result = "✓ TRUSTED DEVICE"
            message = "Both values match the predefined trusted mapping."
            status = "Trusted"
            result_class = "trusted"
            css = "trusted"

        elif ip == TRUSTED_IP and mac != TRUSTED_MAC:

            result = "⚠ POSSIBLE ARP SPOOFING"
            message = "The trusted IP is associated with an unexpected MAC address."
            status = "Possible Spoofing"
            result_class = "alert"
            css = "alert"

        elif mac == TRUSTED_MAC and ip != TRUSTED_IP:

            result = "⚠ MAPPING WARNING"
            message = "The trusted MAC address is associated with a different IP."
            status = "Mapping Warning"
            result_class = "warning"
            css = "warning"

        else:

            result = "UNKNOWN DEVICE"
            message = "This combination does not match the predefined trusted record."
            status = "Unknown Device"
            result_class = "warning"
            css = "neutral"

        activity_logs.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "ip": ip,
            "mac": mac,
            "status": status,
            "css": css
        })

        # Keep only latest 50 logs
        del activity_logs[50:]

    return render_template_string(
        HTML,
        result=result,
        message=message,
        result_class=result_class,
        logs=activity_logs,
        trusted_ip=TRUSTED_IP,
        trusted_mac=TRUSTED_MAC,
        total_checks=len(activity_logs)
    )


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )