# 🎄 NataleMatico

**NataleMatico** is an ESP32-based Christmas light and music controller.

The project controls four independent mains-powered Christmas light channels while playing simple synchronized melodies through a small speaker. It includes a local web interface, OLED display, Wi-Fi connectivity, NTP time synchronization and automatic scheduling.

The system was designed and built as a practical DIY project using inexpensive modules and components already available in the workshop.

##  Features

- ESP32 based controller
- 4 independent relay outputs
- Wi-Fi connectivity
- Local Access Point for direct control
- Web interface accessible from phone, tablet or computer
- Start / Stop control
- Individual relay control
- Automatic light sequences
- Music synchronized with the light sequences
- Multiple selectable Christmas melodies
- OLED 128×64 status display
- NTP clock synchronization
- Automatic daily timer
- Stand-alone operation after power-up
- No Internet connection required for normal manual operation

##  Hardware

The prototype uses:

- ESP32 Wi-Fi / Bluetooth controller
- Integrated 4-channel relay board
- 128×64 SSD1306 I2C OLED display
- Small speaker
- Logic-level MOSFET PWM driver
- 12 Ω speaker resistor
- Suitable power supply
- Enclosure
- Four mains output sockets for the Christmas lights

### Main controller

The prototype uses an ESP32 controller board with four integrated relay channels.

The particular board used can accept mains or low-voltage power depending on its configuration. Other ESP32 boards can also be used, provided that suitable isolated relay modules are connected.

### Audio driver

The speaker is driven by a logic-level MOSFET PWM module.

The prototype uses a **15 A / 400 W MOSFET module simply because it was already available**. This module is considerably larger than necessary for the small speaker load.

A much smaller logic-level MOSFET or suitable transistor driver can be used instead.

##  ESP32 Pin Configuration

The current software uses the following GPIO assignments:

| Function | ESP32 GPIO |
|----------|-----------:|
| Relay 1  | 32 |
| Relay 2  | 33 |
| Relay 3  | 25 |
| Relay 4  | 26 |
| Audio / PWM | 27 |
| OLED SDA | 0 |
| OLED SCL | 4 |

Check `main.py` before wiring the hardware, as pin assignments may change between versions.

##  OLED Display

NataleMatico uses a 128×64 SSD1306 OLED display.

The display provides information such as:

- System status
- Current time
- Selected song
- Running / stopped status
- Network information during startup

The SSD1306 MicroPython driver is included in the project.

##  Network Operation

NataleMatico can connect to the home Wi-Fi network to obtain the current time using NTP.

It also creates its own local Wi-Fi Access Point.

The controller can therefore be operated directly from a phone, tablet or computer through the built-in web interface.

The default local address is:

`192.168.4.1`

### Wi-Fi configuration

Before using the software, edit the Wi-Fi configuration in `main.py` and enter your own network details.

Do **not** publish your personal Wi-Fi SSID or password when sharing modified versions of the project.

The Access Point password should also be changed from the example/default value before normal use.

##  Music and Lights

The melodies are generated directly by the ESP32.

Notes and timing information are stored in the program and the relay sequences are synchronized with the music.

The relays are intentionally operated at relatively slow rates because conventional mechanical relays are not suitable for rapid switching.
Relay timing note: The lighting sequence uses software-inverted relay logic to accommodate the startup delay of some LED Christmas-light power supplies.
The physical outputs remain normally open, ensuring that all lights stay OFF when NataleMatico is stopped or outside the programmed timer period.

NataleMatico is intended to produce simple rhythmic Christmas-light effects rather than high-speed lighting animation.

##  Automatic Timer

The controller includes an automatic daily operating schedule.

The current prototype is configured to operate during the evening/night period.

The schedule can be changed in `main.py` to suit the installation.

NTP synchronization is used to maintain the correct local time.

##  Software

NataleMatico runs on **MicroPython** on the ESP32.

Typical project files include:

```text
NataleMatico/
│
├── main.py
├── oled.py
├── ssd1306.py
├── reletest.py
├── README.md
└── images/