from machine import Pin,PWM
import network
import socket
import time
import ntptime
last_clock_update = 0
timer_started = False

TEMPO_SCALE = 0.85
# =========================
# TIMER
# =========================
TIMER_START_HOUR = 19
TIMER_STOP_HOUR = 4
#oled================================================
import oled
oled.init()

import builtins
_original_print = builtins.print

def oled_print(*args, **kwargs):
    msg = " ".join(str(a) for a in args)
    _original_print(*args, **kwargs)
    oled.repl(msg)

builtins.print = oled_print

print("NataleMatico")
print("Musiclight")

# =========================
# WIFI CASA
# =========================

HOME_SSID = "TP-LINK_A07F"
HOME_PASSWORD = "66052951"

sta = network.WLAN(network.STA_IF)

# reset interfaccia WiFi STA
sta.active(False)
time.sleep(1)
sta.active(True)
time.sleep(1)

print("Connessione WiFi casa...")

sta.disconnect()
time.sleep(1)
sta.connect(HOME_SSID, HOME_PASSWORD)

# aspetta massimo 15 secondi
for i in range(30):
    if sta.isconnected():
        break
    time.sleep(0.5)

if sta.isconnected():
    print("WiFi casa connesso")
    print("IP casa:", sta.ifconfig()[0])

    # =========================
    # SINCRONIZZAZIONE ORA NTP
    # =========================
    try:
        ntptime.settime()
        print("Ora NTP sincronizzata")
        print("UTC:", time.localtime())

    except Exception as e:
        print("Errore NTP:", e)

else:
    print("WiFi casa NON connesso")
    sta.disconnect()
# =========================
# ORA LOCALE NSW
# =========================

def local_time():
    t = time.time() + (10 * 3600)
    return time.localtime(t)

t = local_time()
print("Ora NSW: {:02d}:{:02d}".format(t[3], t[4]))    
# =========================
# CONFIG
# =========================
AP_SSID = "ChristmasLights"
AP_PASSWORD = "12345678"

RELAY_PINS = [32, 33, 25, 26]
# =========================
# RELAYS
# =========================
relays = [
    Pin(p, Pin.OUT, value=0)
    for p in RELAY_PINS
]

for r in relays:
    r.off()
    

# =========================
# piezo
# =========================
piezo = PWM(Pin(27))
piezo.freq(880)



piezo.duty(0)




ritornello_1 = [
    # LUCI       NOTA   ON    PAUSA

    # JIN-GLE BELLS
    (0b0001,     659,   450,  180),   # E
    (0b0010,     659,   450,  180),   # E
    (0b0100,     659,   900,  360),   # E

    # JIN-GLE BELLS
    (0b0010,     659,   450,  180),   # E
    (0b0100,     659,   450,  180),   # E
    (0b1000,     659,   900,  360),   # E

    # JIN-GLE ALL THE WAY
    (0b0001,     659,   450,  180),   # E
    (0b0010,     784,   450,  180),   # G
    (0b0100,     523,   630,  180),   # C
    (0b1000,     587,   630,  180),   # D
    (0b1111,     659,  1260,  540),   # E

    # OH WHAT FUN IT IS TO RIDE
    (0b1000,     698,   450,  180),   # F
    (0b0100,     698,   450,  180),   # F
    (0b0010,     698,   450,  180),   # F
    (0b0001,     698,   450,  180),   # F
    (0b0011,     698,   450,  180),   # F
    (0b1100,     659,   450,  180),   # E
    (0b0011,     659,   450,  180),   # E
    (0b1100,     659,   450,  180),   # E

    # IN A ONE-HORSE OPEN SLEIGH
    (0b0001,     659,   450,  180),   # E
    (0b0010,     587,   450,  180),   # D
    (0b0100,     587,   450,  180),   # D
    (0b1000,     659,   450,  180),   # E
    (0b0101,     587,   900,  180),   # D
    (0b1010,     784,   900,  270),   # G
    (0b1111,     784,  1260,  720),   # G
]
# =========================
# RITORNELLO 2
# WE WISH YOU A MERRY CHRISTMAS
# =========================

ritornello_2 = [

    # WE WISH YOU A MERRY CHRISTMAS
    (0b0001, 392, 540, 180),   # G
    (0b0010, 523, 540, 180),   # C
    (0b0100, 523, 360, 145),   # C
    (0b1000, 587, 360, 145),   # D
    (0b0011, 523, 360, 145),   # C
    (0b1100, 494, 540, 180),   # B
    (0b1111, 440, 900, 900),   # A

    # WE WISH YOU A MERRY CHRISTMAS
    (0b1000, 440, 540, 180),   # A
    (0b0100, 587, 540, 180),   # D
    (0b0010, 587, 360, 145),   # D
    (0b0001, 659, 360, 145),   # E
    (0b1010, 587, 360, 145),   # D
    (0b0101, 523, 540, 180),   # C
    (0b1111, 494, 900, 900),   # B

    # WE WISH YOU A MERRY CHRISTMAS
    (0b0001, 494, 540, 180),   # B
    (0b0010, 659, 540, 180),   # E
    (0b0100, 659, 360, 145),   # E
    (0b1000, 698, 360, 145),   # F
    (0b0011, 659, 360, 145),   # E
    (0b1100, 587, 540, 180),   # D
    (0b1111, 523, 900, 900),   # C

    # AND A HAPPY NEW YEAR
    (0b1001, 440, 450, 145),   # A
    (0b0110, 440, 450, 145),   # A
    (0b0011, 587, 540, 180),   # D
    (0b1100, 494, 540, 180),   # B
    (0b0101, 523, 540, 180),   # C
    (0b1010, 494, 540, 180),   # B
    (0b1111, 440,1260, 900),   # A
]
# =========================
# RITORNELLO 3
# TU SCENDI DALLE STELLE
# dalla partitura
# =========================

ritornello_3 = [

    # TU SCENDI DALLE STELLE...
    (0b0001, 392, 450, 150),    # G
    (0b0010, 440, 900, 150),    # A
    (0b0100, 494, 450, 150),    # B

    (0b1000, 440, 900, 150),    # A
    (0b0011, 392, 450, 150),    # G

    (0b0100, 349, 450, 150),    # F
    (0b1000, 330, 900, 180),    # E

    # nota legata
    (0b0101, 330, 900, 150),    # E
    (0b1010, 294, 450, 180),    # D

    # frase in salita
    (0b0001, 330, 450, 120),    # E
    (0b0010, 349, 450, 120),    # F
    (0b0100, 392, 450, 150),    # G

    # risposta
    (0b1000, 392, 450, 120),    # G
    (0b0100, 349, 450, 120),    # F
    (0b0010, 330, 450, 180),    # E

    # frase lunga
    (0b0001, 294, 1350, 250),   # D

    # ripresa
    (0b0010, 294, 900, 150),    # D
    (0b0100, 330, 450, 150),    # E

    (0b1000, 294, 900, 150),    # D
    (0b0011, 330, 450, 150),    # E

    (0b1100, 349, 900, 150),    # F
    (0b0101, 330, 450, 180),    # E

    (0b1010, 294, 1350, 300),   # D

    # chiusura della frase
    (0b1111, 440, 1350, 600),   # A
]
# =========================
# RITORNELLO 4
# WHITE CHRISTMAS
# melodia principale - lenta
# =========================

ritornello_4 = [

    # I'M DREAMING OF A WHITE CHRISTMAS
    (0b0001, 330,  500, 120),   # E
    (0b0010, 349,  500, 120),   # F
    (0b0100, 330,  700, 150),   # E
    (0b1000, 311,  500, 120),   # Eb
    (0b0001, 330,  500, 120),   # E
    (0b0010, 349,  500, 120),   # F
    (0b0100, 370,  500, 120),   # F#
    (0b1111, 392, 1200, 350),   # G

    # JUST LIKE THE ONES I USED TO KNOW
    (0b0001, 440,  500, 120),   # A
    (0b0010, 494,  500, 120),   # B
    (0b0100, 523,  600, 120),   # C
    (0b1000, 587,  900, 150),   # D
    (0b1001, 523,  500, 120),   # C
    (0b0110, 494,  500, 120),   # B
    (0b0011, 440,  600, 120),   # A
    (0b1111, 392, 1200, 400),   # G

    # WHERE THE TREETOPS GLISTEN
    (0b0001, 262,  500, 120),   # C
    (0b0010, 294,  500, 120),   # D
    (0b0100, 330,  700, 120),   # E
    (0b1000, 330,  500, 120),   # E
    (0b0011, 330,  700, 150),   # E

    # AND CHILDREN LISTEN
    (0b1100, 440,  700, 120),   # A
    (0b0101, 392,  700, 150),   # G
    (0b1010, 262,  500, 120),   # C
    (0b1111, 262,  900, 300),   # C

    # TO HEAR SLEIGH BELLS IN THE SNOW
    (0b0001, 349,  600, 120),   # F
    (0b0010, 330,  500, 120),   # E
    (0b0100, 349,  700, 120),   # F
    (0b1000, 330,  600, 120),   # E
    (0b0011, 294,  600, 120),   # D
    (0b1100, 262,  700, 150),   # C
    (0b1111, 294, 1400, 600),   # D
]
running = False
current_song = ritornello_1

step_index = 0
phase_on = False
last_change = time.ticks_ms()


def all_off():

    for r in relays:
        r.off()

    piezo.duty(0)


def all_on():

    for r in relays:
        r.on()

    piezo.duty(0)


def set_lights(pattern):

    for i in range(4):

        if pattern & (1 << i):
            relays[i].off()
        else:
            relays[i].on()


def start_sequence(song):
    global running
    global step_index
    global phase_on
    global last_change
    global current_song

    all_off()

    current_song = song

    running = True
    step_index = 0
    phase_on = True

    pattern, freq, on_time, pause_time = current_song[step_index]

    set_lights(pattern)

    piezo.freq(freq)
    piezo.duty(512)

    last_change = time.ticks_ms()


def stop_sequence():

    global running

    running = False
    all_off()
    


def update_sequence():
    global step_index
    global phase_on
    global last_change
    global last_clock_update
    global timer_started
    
    now = time.ticks_ms()
    
    

    # =========================
    # AGGIORNAMENTO OROLOGIO
    # =========================
    if time.ticks_diff(now, last_clock_update) >= 30000:
        t = local_time()
        print("Ora NSW: {:02d}:{:02d}".format(t[3], t[4]))
        last_clock_update = now
    

    # =========================
    # TIMER AUTOMATICO
    # 19:00 -> 04:00
    # =========================

    t = local_time()
    hour = t[3]

    # fascia notturna:
    # dalle 19:00 alle 23:59
    # oppure dalle 00:00 alle 03:59
    timer_active = (hour >= TIMER_START_HOUR or
                    hour < TIMER_STOP_HOUR)

    if timer_active:

        # entra nella fascia: avvia automaticamente melodia 1
        if not timer_started:
            print("TIMER ON - Jingle Bells")
            start_sequence(ritornello_1)
            timer_started = True

    else:

        # siamo fuori dalla fascia
        if timer_started:
            print("TIMER OFF")
            stop_sequence()
                   

    # Se la musica e' ferma, l'orologio continua comunque
    if not running:
        return

    pattern, freq, on_time, pause_time = current_song[step_index]

    if phase_on:

        if time.ticks_diff(now, last_change) >= int(on_time * TEMPO_SCALE):

            all_on()
            

            phase_on = False
            last_change = now

    else:

        if time.ticks_diff(now, last_change) >= int(pause_time * TEMPO_SCALE):

            step_index += 1

            if step_index >= len(current_song):
                step_index = 0

            pattern, freq, on_time, pause_time = current_song[step_index]

            set_lights(pattern)

            piezo.freq(freq)
            piezo.duty(512)

            phase_on = True
            last_change = now
    
# =========================
# WIFI ACCESS POINT
# =========================
ap = network.WLAN(network.AP_IF)
ap.active(True)

ap.config(
    essid=AP_SSID,
    
    password=AP_PASSWORD
)

while not ap.active():
    time.sleep(0.2)

ip = ap.ifconfig()[0]

print("Christmas Lights ready")
print("IP:", ip)


# =========================
# HTML
# =========================
def html_page():

    state = "RUNNING" if running else "STOPPED"

    return """<!DOCTYPE html>

<html>

<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<style>

html, body {
    margin: 0;
    padding: 0;

    width: 100%;
    height: 100%;

    font-family: Arial, sans-serif;

    background: black;

    color: white;
}


body {

    background-image:
        linear-gradient(
            rgba(0,0,0,0.05),
            rgba(0,0,0,0.18)
        ),
        url('/Palle-Natale.jpg');

    background-size: contain;

    background-position:
        center center;

    background-repeat:
        no-repeat;
}


.panel {

    width: 100%;
    min-height: 100vh;

    display: flex;

    flex-direction: column;

    align-items: center;

    justify-content: space-between;

    box-sizing: border-box;

    padding: 25px;
}


.title {

    margin-top: 30px;

    font-size: 28px;

    font-weight: bold;

    text-align: center;

    color: #333;

    text-shadow:
        0px 1px 2px white;
}


.status {

    margin-top: 20px;

    padding: 10px 20px;

    background:
        rgba(255,255,255,0.75);

    color: #222;

    border-radius: 14px;

    font-size: 18px;

    font-weight: bold;
}


.led-area {

    display: flex;

    gap: 14px;

    margin-top: 20px;
}


.led {

    width: 42px;
    height: 42px;

    border-radius: 50%;

    background:
        rgba(60,60,60,0.75);

    border: 3px solid white;

    box-shadow:
        0 0 8px rgba(0,0,0,0.8);
}


.led.on {

    background: #ffe600;

    box-shadow:
        0 0 12px #ffe600,
        0 0 25px #ffe600,
        0 0 40px #fff000;
}


.controls {

    width: 100%;

    max-width: 430px;

    display: grid;

    grid-template-columns:
        1fr 1fr;

    gap: 16px;

    margin-bottom: 35px;
}


button {

    padding: 22px;

    border: none;

    border-radius: 18px;

    font-size: 24px;

    font-weight: bold;

    color: white;

    box-shadow:
        0 4px 12px
        rgba(0,0,0,0.45);
}


.start {

    background:
        rgba(0,150,0,0.90);
}


.stop {

    background:
        rgba(180,0,0,0.90);

    grid-column: 1 / 3;
}


button:active {

    transform:
        scale(0.97);
}

</style>

</head>


<body>


<div class="panel">


<div>

<div class="title">

CHRISTMAS LIGHTS

</div>


<div class="status"
     id="status">

""" + state + """

</div>


<div class="led-area">

<div id="led0"
     class="led"></div>

<div id="led1"
     class="led"></div>

<div id="led2"
     class="led"></div>

<div id="led3"
     class="led"></div>

</div>

</div>


<div class="controls">

<button class="start"
onclick="startLights(1)">
Jingle Bells
</button>

<button class="start"
onclick="startLights(2)">
We Wish You
</button>

<button class="start"
onclick="startLights(3)">
Tu Scendi Dalle Stelle
</button>

<button class="start"
onclick="startLights(4)">
White Christmas
</button>

<button class="stop"
onclick="stopLights()">
STOP
</button>

</div>


</div>


<script>


function startLights(song) {

    fetch('/start' + song);

}


function stopLights() {

    fetch('/stop');

}


function updateStatus() {

    fetch('/status')

    .then(response =>
        response.json())

    .then(data => {

        document.getElementById(
            "status"
        ).innerHTML =
            data.running
            ? "RUNNING"
            : "STOPPED";


        for (
            let i = 0;
            i < 4;
            i++
        ) {

            let led =
                document.getElementById(
                    "led" + i
                );

            if (
                data.relays[i]
            ) {

                led.classList.add(
                    "on"
                );

            } else {

                led.classList.remove(
                    "on"
                );
            }
        }
    });
}


setInterval(
    updateStatus,
    250
);


updateStatus();


</script>


</body>

</html>
"""


# =========================
# SERVER
# =========================
addr = socket.getaddrinfo(
    "0.0.0.0",
    80
)[0][-1]


s = socket.socket()

s.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

s.bind(addr)

s.listen(5)

# Fondamentale:
# non blocchiamo la sequenza
s.settimeout(0.1)


print("Web server ready")


# =========================
# MAIN LOOP
# =========================
while True:

    # aggiorna sempre le luci
    update_sequence()

    try:

        cl, addr = s.accept()

    except OSError:

        continue


    try:

        req = cl.recv(
            1024
        ).decode()


        # -----------------
        # IMAGE
        # -----------------
        if "GET /Palle-Natale.jpg" in req:

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: image/jpeg\r\n"
                "Cache-Control: max-age=86400\r\n"
                "\r\n"
            )

            with open(
                "Palle-Natale.jpg",
                "rb"
            ) as f:

                while True:

                    data = f.read(512)

                    if not data:
                        break

                    cl.send(data)

        # -----------------
        # START
        # -----------------
        elif "GET /start1" in req:

            start_sequence(ritornello_1)

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "START 1"
            )

        elif "GET /start2" in req:

            start_sequence(ritornello_2)

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "START 2"
            )

        elif "GET /start3" in req:

            start_sequence(ritornello_3)

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "START 3"
            )

        elif "GET /start4" in req:

            start_sequence(ritornello_4)

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "START 4"
            )


        # -----------------
        # STOP
        # -----------------
        elif "GET /stop" in req:

            stop_sequence()

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                "\r\n"
                "STOP"
            )


        # -----------------
        # STATUS
        # -----------------
        elif "GET /status" in req:

            values = [
                r.value()
                for r in relays
            ]

            json = (
                '{"running":'
                + (
                    "true"
                    if running
                    else "false"
                )
                + ',"relays":['
                + ",".join(
                    str(v)
                    for v in values
                )
                + "]}"
            )


            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Cache-Control: no-cache\r\n"
                "\r\n"
            )

            cl.send(json)


        # -----------------
        # MAIN PAGE
        # -----------------
        else:

            page = html_page()

            cl.send(
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/html\r\n"
                "Cache-Control: no-cache\r\n"
                "\r\n"
            )

            cl.send(page)


    except Exception as e:

        print(
            "Client error:",
            e
        )


    finally:

        cl.close()