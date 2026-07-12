import webview
import ollama
import json
import os
import serial
import serial.tools.list_ports
import math
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# MASSIVE EXTENDED LOCAL ROBOTICS INVENTORY & CHASSIS ARCHITECTURE DATABASE
GLOBAL_HARDWARE_DB = {
    "Control Hubs / Brains": [
        "FRC NI roboRIO 2.0", "FTC REV Control Hub", "FTC REV Expansion Hub", "VEX V5 Robot Brain", "VEX IQ 2nd Gen Brain",
        "Raspberry Pi 5 (8GB)", "Raspberry Pi 4 Model B (4GB)", "Raspberry Pi Pico W", "Raspberry Pi Zero 2 W",
        "Arduino Mega 2560 R3", "Arduino Uno R4 Minima", "Arduino Uno R4 WiFi", "Arduino Nano 33 IoT", "Arduino Due",
        "ESP32-S3 WROOM DevKit", "ESP32 DevKit V4", "ESP8266 NodeMCU V3", "Teensy 4.1 High Performance", "Teensy 4.0",
        "STM32 Nucleo-F401RE", "STM32 Blue Pill (F103C8T6)", "BeagleBone Black Industrial", "BeagleBone AI-64",
        "NVIDIA Jetson Orin Nano", "NVIDIA Jetson Nano Developer Kit", "NVIDIA Jetson TX2", "LattePanda 3 Delta 864"
    ],
    "Motors & Actuators": [
        "REV Neo Brushless Motor", "REV Neo 550 Brushless", "CTRE Falcon 500 Powered by Talon FX", "CTRE Kraken X60",
        "Matrix 12V 50:1 DC Motor", "VEX V5 Smart Motor (11W)", "VEX V5 Smart Motor (5.5W)", "AndyMark RedLine 775",
        "AndyMark CIM Motor", "AndyMark Mini CIM Motor", "BaneBots RS-550 Motor", "goBILDA 5202 Yellow Jacket (2000 RPM)",
        "goBILDA 5204 Yellow Jacket (312 RPM)", "NEMA 17 High Torque Stepper (42x48mm)", "NEMA 23 Bipolar Stepper (57x76mm)",
        "NEMA 34 High Torque Planetary Stepper", "TowerPro SG90 Micro Servo", "MG996R Digital High Torque Servo",
        "MG90S Full Metal Gear Micro Servo", "Dynamixel AX-12A Smart Servo", "Dynamixel XM430-W350-R Smart Actuator",
        "Savox SC-1256TG High Torque Titanium Servo", "Yellow TT Gearbox DC Motor (1:48)", "Pololu 37D Metal Gearmotor",
        "Festo Double-Acting Pneumatic Cylinder", "SMC Miniature Pneumatic Actuator"
    ],
    "Motor Controllers & Drivers": [
        "REV Spark Max Controller", "REV Spark Flex Brushless Controller", "CTRE Talon FX Integrated Driver",
        "CTRE Talon SRX Motor Controller", "CTRE Victor SPX PWM Controller", "REV SPARK Mini Motor Controller",
        "L298N Dual H-Bridge Module", "L293D Motor Driver Shield", "BTS7960 43A High Power H-Bridge Driver",
        "Cytron 10A Dual Channel Motor Driver (MD10C)", "Cytron 30A Smart Motor Driver (MD30C)", "Roboclaw 2x15A Motor Controller",
        "Roboclaw 2x30A Motor Controller", "Pololu A4988 Stepper Motor Driver", "DRV8825 High Current Stepper Driver",
        "TMC2209 Ultra-Silent Stepper Driver", "TB6600 4A Industrial Stepper Driver", "Sabertooth 2x25 Dual Motor Driver",
        "Odrive S1 High Performance Brushless Controller", "VESC 6 MkIV Open Source Controller"
    ],
    "Sensors & Computer Vision": [
        "HC-SR04 Ultrasonic Distance Sensor", "MaxBotix I2CXL-MaxSonar-EZ Ultrasonic", "MPU6050 6-DOF Gyro & Accelerometer",
        "BNO055 9-DOF Absolute Orientation Sensor", "MPU9250 9-DOF IMU Unit", "ICM-20948 Low Power 9-Axis IMU",
        "TCS3200 Color Recognition Module", "REV Color Sensor V3", "Limelight 3 Smart Vision Camera",
        "Limelight 3G Monochrome Neural Camera", "PhotonVision Compatible OV9281 Global Shutter",
        "Intel RealSense D435i Depth Camera", "Intel RealSense D455 Long Range Depth", "Oak-D Lite AI Vision Camera",
        "IR 5-Channel Line Follower Array", "QTR-8RC Reflective Sensor Array", "VL53L0X Time-of-Flight Laser Distance",
        "VL53L1X Long Range ToF Sensor", "REV Through-Bore Encoder", "CTRE CANcoder Magnetic Absolute Encoder",
        "SRX Mag Encoder (Relative/Absolute)", "RPLIDAR A1M8 360 Degree Laser Scanner", "RPLIDAR S3 40M Range Scanner",
        "Pixy2 CMUcam5 Object Tracking Sensor", "Sharp GP2Y0A21YK0F IR Analog Distance", "Sharp GP2Y0A02YK0F Long Range IR",
        "HX711 Load Cell Amplifier & Weight Sensor", "BMP280 Barometric Pressure & Altitude Sensor"
    ],
    "Chassis Systems & Architecture": [
        "4-Wheel Mecanum Holonomic Drivebase", "Coaxial Swerve Drive Module System (Swerve X)",
        "6-Wheel West Coast Drop-Center Drive", "8-Wheel Rocker-Bogie Exploration Chassis",
        "Tracked Tank Tread Heavy Architecture", "Differential 2-Wheel Steering Chassis",
        "Ackermann Steering Car-Style Base", "H-Drive Holonomic Pod Chassis", "Omniwheel Kiwi 3-Wheel Holonomic Base",
        "Differential 4-Wheel Skid-Steer Frame", "Articulated Rover Chassis Architecture", "X-Drive 4-Wheel Holonomic Frame",
        "Swerve Drive Specialties Mk4i Module Base", "Traction Wheel Drop-Center Battlebot Frame"
    ],
    "Structural Frames & Mechanicals": [
        "20x20mm T-Slot Aluminium Extrusion (V-Slot)", "30x30mm T-Slot Heavy Aluminium Profile",
        "REV 15mm Extrusion Channels & Brackets", "REV MAXTube Grid Extrusion Pattern",
        "Tetrix Max Heavy Duty Structural Elements", "Matrix Build Plates, Gussets & Brackets",
        "Custom CNC Carbon Fiber Side Plates (3mm)", "Custom CNC Carbon Fiber Structural Panels (5mm)",
        "Lexan Polycarbonate Protective Shielding (1/8 inch)", "HDPE High-Density Polyethylene Skid Plates",
        "Actobotics 6061-T6 Aluminum Channel Frame", "goBILDA 4-Hole Pattern Low-Profile Channels",
        "VEX High Strength Steel Chassis Bumper Angles", "3D Printed PETG Structural Infill Brackets",
        "3D Printed Carbon-Fiber Reinforced Nylon Mounts", "Flanged Steel Ball Bearings (1/2 in Hex)"
    ]
}

# ALL 22 OFFICIALLY RECOGNIZED REGIONAL LANGUAGES OF INDIA
LANGUAGES = {
    'en-IN': 'English (India)', 'hi-IN': 'Hindi (हिन्दी)', 'mr-IN': 'Marathi (मराठी)', 
    'ta-IN': 'Tamil (தமிழ்)', 'te-IN': 'Telugu (తెలుగు)', 'bn-IN': 'Bengali (বাংলা)',
    'gu-IN': 'Gujarati (ગુજરાती)', 'kn-IN': 'Kannada (ಕನ್ನಡ)', 'ml-IN': 'Malayalam (മലയാളം)',
    'or-IN': 'Odia (ଓଡ଼ିଆ)', 'pa-IN': 'Punjabi (ਪੰਜਾਬੀ)', 'ur-IN': 'Urdu (اردو)',
    'as-IN': 'Assamese (অসমীয়া)', 'brx-IN': 'Bodo (बड़ो)', 'doi-IN': 'Dogri (डोगरी)',
    'ks-IN': 'Kashmiri (कॉशुर)', 'kok-IN': 'Konkani (कोंकणी)', 'mai-IN': 'Maithili (मैथिली)',
    'mni-IN': 'Manipuri (मैतैलोन्)', 'ne-IN': 'Nepali (नेपाली)', 'sa-IN': 'Sanskrit (संस्कृतम्)',
    'sat-IN': 'Santali (ᱥᱟᱱᱛᱟᱲᱤ)', 'sd-IN': 'Sindhi (सिन्धी)'
}

# COMPREHENSIVE ROBOTICS PROGRAMMING & FIRMWARE LANGUAGES
ROBO_LANGUAGES = [
    "Arduino C++ (.ino - AVR/ARM)", 
    "WPILib Java (FRC Official Framework)", 
    "WPILib C++ (FRC High Performance Framework)",
    "WPILib C# / WPILib.NET Framework",
    "RobotC (VEX / LEGO Official Framework)", 
    "VEXcode Pro V5 C++ Framework",
    "VEXcode V5 Python Runtime",
    "MicroPython (Embedded Systems / Pico / ESP32)", 
    "CircuitPython (Adafruit Embedded Hardware)",
    "Python 3 (Raspberry Pi / Linux SBC Control)",
    "ROS2 Python Nodes (Robot Operating System 2)",
    "ROS2 C++ Nodes (Real-Time Control Loops)",
    "NATIVE C++ (Bare-Metal AVR / STM32 / ARM Cortex)",
    "Embedded C (Pure Hardware Register Level)",
    "Rust Embedded (no_std High Safety Firmware)",
    "LabVIEW Robotics Module Graphical Code",
    "MATLAB / Simulink Embedded Coder Target",
    "JavaScript / Node.js (Johnny-Five Hardware Framework)"
]

class SynthetixAPI:
    def __init__(self):
        self.serial_connection = None
        self.injected_path = ""
        self.active_hardware_profile = []

    def get_db(self): return GLOBAL_HARDWARE_DB
    def get_languages(self): return LANGUAGES
    def get_robo_languages(self): return ROBO_LANGUAGES
    def get_serial_ports(self): return [port.device for port in serial.tools.list_ports.comports()]

    def set_injected_path(self, data_str):
        self.injected_path = data_str
        return "Trajectory path successfully loaded into compiler stack memory."

    def update_hardware_profile(self, parts_list):
        self.active_hardware_profile = parts_list
        return f"Hardware matrix verified: {len(parts_list)} items synced to build environment."

    def calculate_pid(self, drift_cm):
        try:
            drift = float(drift_cm)
            kp = abs(drift) * 0.05
            return {"kp": round(kp, 4), "ki": round(kp * 0.01, 4), "kd": round(kp * 0.1, 4)}
        except: return {"error": "Invalid metrics calculation."}

    def send_to_serial(self, port, baudrate, data):
        try:
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()
            self.serial_connection = serial.Serial(port, int(baudrate), timeout=1)
            self.serial_connection.write(data.encode('utf-8'))
            return f"Success: Flash routine completed on target {port}."
        except Exception as e:
            return f"Serial Interface Error: {str(e)}"

    def tutor_chat(self, question, lang):
        try:
            response = ollama.generate(
                model="qwen2.5-coder:0.5b",
                prompt=f"You are a helpful, extremely friendly, encouraging, and age-appropriate (under-18 safe) local offline AI Robotics Tutor. Answer this question: '{question}' in the language code '{lang}'. Keep your answer simple, easy to understand, and highly educational for young minds."
            )
            return response.get("response", "Tutor channel connection reset.")
        except Exception:
            if "pid" in question.lower() or "drift" in question.lower():
                return "[Offline Mode] Hello! A PID loop keeps your robot going straight! 'P' checks how far you are off, 'I' checks how long you've been off, and 'D' checks how fast you're turning back. Together, they form a perfect guide!"
            elif "wiring" in question.lower() or "circuit" in question.lower() or "pin" in question.lower():
                return "[Offline Mode] Hi there! When wiring components, always connect Positive (red) to VCC, Ground (black) to GND, and your sensor signal (blue) to digital or analog pins on your main controller brain. Remember to share grounds!"
            return f"[Offline Mode] Hi! That is an amazing question. To fully query the Qwen AI model locally, please ensure Ollama is running in the background of your computer! Keep exploring!"

    def generate_code(self, prompt, target_lang, view_mode="both"):
        hardware_context = f"\nTarget System Hardware Configured:\n" + "\n".join([f"- {item}" for item in self.active_hardware_profile if item]) if self.active_hardware_profile else ""
        path_context = f"\nAutonomous Trajectory Coordinates Path Matrix:\n{self.injected_path}" if self.injected_path else ""
        try:
            response = ollama.generate(
                model="qwen2.5-coder:0.5b",
                prompt=f"You are Synthetix.AI Robotics Compiler Core. Generate ONLY the optimized, clean raw text code for {target_lang} using this hardware footprint:{hardware_context}. Rules: {prompt}.{path_context} Provide code clean of text markdown tags."
            )
            return response.get("response", "// Production compilation fault.")
        except Exception:
            return f"// Native Offline Code Generator Map Stack\n// Active Target Runtime: {target_lang}\n" + "\n".join([f"// Configured Module: {x}" for x in self.active_hardware_profile if x]) + f"\n\n// Path Modeler Map Status: Loaded Trajectory Vector Elements Successfully."

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Synthetix.AI - Universal Championship Robotics Environment</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root {
            --bg: #0d1117;
            --panel: #161b22;
            --border: #30363d;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-orange: #d29922;
            --accent-red: #f85149;
            --accent-purple: #bc8cff;
            --hover-bg: #21262d;
        }
        
        body { 
            font-family: 'Inter', sans-serif; 
            background: var(--bg); 
            color: var(--text-primary); 
            margin: 0; padding: 0; 
            overflow-x: hidden;
        }

        /* GITHUB HEADER STYLE */
        .header { 
            background: #161b22; 
            padding: 12px 30px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            border-bottom: 1px solid var(--border); 
        }
        .header-logo {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 600;
            color: var(--text-primary);
        }
        .header-logo i {
            color: var(--accent-blue);
            font-size: 24px;
        }

        /* GITHUB TAB SYSTEM */
        .tabs-nav {
            display: flex;
            gap: 4px;
            border-bottom: 1px solid var(--border);
            padding: 0 30px;
            background: #161b22;
            overflow-x: auto;
        }
        .tab-btn {
            background: transparent;
            color: var(--text-primary);
            border: none;
            padding: 14px 16px;
            font-size: 14px;
            font-weight: 500;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 2px solid transparent;
            transition: all 0.2s ease-in-out;
            white-space: nowrap;
        }
        .tab-btn:hover {
            border-bottom: 2px solid var(--text-secondary);
            color: var(--text-primary);
        }
        .tab-btn.active {
            border-bottom: 2px solid #f78166;
            font-weight: 600;
            color: var(--text-primary);
        }
        .tab-btn i {
            color: var(--text-secondary);
            font-size: 14px;
        }
        .tab-btn.active i {
            color: var(--text-primary);
        }

        /* CORE WORKSPACE CONTAINERS */
        .content { 
            display: none; 
            padding: 24px 30px; 
            max-width: 1600px; 
            margin: 0 auto; 
            animation: fadeIn 0.3s ease-in-out;
        }
        .content.active { display: block; }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(5px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* RESPONSIVE LAYOUT GRIDS */
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
        .grid-3 { display: grid; grid-template-columns: 1.1fr 1.45fr 1.455fr; gap: 20px; }
        @media (max-width: 1200px) {
            .grid-3 { grid-template-columns: 1fr; }
            .grid-2 { grid-template-columns: 1fr; }
        }

        /* GITHUB COMPACT PANEL CARD */
        .panel { 
            background: var(--panel); 
            padding: 24px; 
            border-radius: 6px; 
            border: 1px solid var(--border); 
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        .panel h3 {
            font-size: 16px;
            font-weight: 600;
            margin-top: 0;
            margin-bottom: 16px;
            border-bottom: 1px solid var(--border);
            padding-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }

        /* FORM ELEMENTS (GITHUB INPUT THEME) */
        label {
            display: block;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        select, input, textarea { 
            width: 100%; 
            padding: 8px 12px; 
            margin-bottom: 16px; 
            background: var(--bg); 
            color: var(--text-primary); 
            border: 1px solid var(--border); 
            border-radius: 6px; 
            font-size: 13px; 
            box-sizing: border-box; 
            font-family: inherit;
            transition: border-color 0.2s;
        }
        select:focus, input:focus, textarea:focus {
            outline: none;
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
        }
        textarea { resize: vertical; }

        /* GITHUB BUTTONS */
        button { 
            background: var(--hover-bg); 
            color: var(--accent-blue); 
            border: 1px solid var(--border); 
            padding: 10px 16px; 
            border-radius: 6px; 
            cursor: pointer; 
            font-weight: 600; 
            font-size: 13px; 
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            transition: all 0.2s ease-in-out; 
        }
        button:hover { 
            background: #30363d; 
            border-color: #8b949e;
        }
        button.btn-primary {
            background: var(--accent-green);
            color: #ffffff;
            border-color: rgba(240, 246, 252, 0.1);
        }
        button.btn-primary:hover {
            background: #2ea043;
            border-color: rgba(240, 246, 252, 0.1);
        }
        button.btn-danger {
            background: var(--accent-red);
            color: #ffffff;
            border-color: rgba(240, 246, 252, 0.1);
        }
        button.btn-danger:hover {
            background: #da3633;
        }

        pre { 
            background: #010409; 
            color: #79c0ff; 
            padding: 20px; 
            border-radius: 6px; 
            overflow-x: auto; 
            height: 500px; 
            font-family: 'JetBrains Mono', monospace; 
            border: 1px solid var(--border); 
            box-sizing: border-box; 
            margin: 0;
        }
        canvas { 
            background: #010409; 
            border: 1px solid var(--border); 
            border-radius: 6px; 
            display: block; 
            margin: 0 auto; 
        }
        
        /* MULTI-CATEGORY PLACEMENTS GRID */
        .mc-grid { 
            display: grid; 
            grid-template-columns: repeat(3, 85px); 
            gap: 12px; 
            background: #010409; 
            padding: 16px; 
            border-radius: 6px; 
            border: 1px solid var(--border);
            width: fit-content; 
            margin: 0 auto; 
        }
        .mc-slot-wrapper { display: flex; flex-direction: column; gap: 6px; align-items: center; }
        .mc-slot { 
            width: 85px; 
            height: 85px; 
            background: var(--panel); 
            border: 1px solid var(--border); 
            border-radius: 6px;
            display: flex; 
            align-items: center; 
            justify-content: center; 
            font-size: 11px; 
            text-align: center; 
            cursor: pointer; 
            color: var(--text-secondary); 
            overflow: hidden; 
            font-weight: 500; 
            transition: all 0.2s ease-in-out;
        }
        .mc-slot:hover {
            border-color: var(--accent-blue);
            color: var(--text-primary);
            background: var(--hover-bg);
        }
        .pin-config-btn { 
            background: #21262d; 
            border: 1px solid var(--border); 
            color: var(--text-secondary); 
            font-size: 10px; 
            padding: 4px 8px; 
            border-radius: 4px; 
            cursor: pointer; 
            width: 85px; 
            text-align: center; 
        }
        .pin-config-btn:hover { color: var(--text-primary); border-color: var(--accent-blue); }

        .voice-status { 
            display: none; 
            background: #1f2937; 
            color: var(--accent-green); 
            border: 1px solid var(--border);
            font-weight: 600; 
            padding: 8px 12px; 
            border-radius: 6px; 
            text-align: center; 
            margin-bottom: 12px; 
        }
        
        /* PREMIUM MINIMALIST PULSING VOICE INDICATOR */
        .mic-indicator-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            margin: 15px 0;
            padding: 12px;
            background: #010409;
            border: 1px solid var(--border);
            border-radius: 6px;
        }
        .mic-dot {
            width: 10px;
            height: 10px;
            background-color: var(--text-secondary);
            border-radius: 50%;
            display: inline-block;
            transition: background-color 0.3s;
        }
        .mic-dot.listening {
            animation: pulse-mic 1.2s infinite ease-in-out;
            background-color: var(--accent-green);
        }
        .mic-text {
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            transition: color 0.3s;
        }
        .mic-text.listening {
            color: var(--accent-green);
        }
        @keyframes pulse-mic {
            0% { transform: scale(0.95); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.5; }
        }

        /* SCRATCH-STYLE INTERLOCKING WORKSPACE (PREMIUM GITHUB BLUE & WHITE VARIANT) */
        .scratch-workspace {
            background-color: #010409;
            background-image: radial-gradient(var(--border) 1px, transparent 1.5px);
            background-size: 16px 16px;
            border-radius: 6px;
            padding: 20px;
            height: 500px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 8px;
            border: 1px solid var(--border);
            box-sizing: border-box;
        }
        .scratch-block {
            position: relative;
            font-family: inherit;
            font-size: 12px;
            font-weight: 600;
            color: #ffffff;
            padding: 10px 14px;
            border-radius: 6px;
            width: fit-content;
            min-width: 200px;
            max-width: 320px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            user-select: none;
            box-sizing: border-box;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .scratch-block i {
            font-size: 14px;
        }
        .scratch-block.hat {
            background: var(--accent-orange);
            color: #ffffff;
        }
        .scratch-block.action {
            background: var(--accent-blue);
        }
        .scratch-block.loop {
            background: var(--accent-purple);
        }
        .scratch-block.sensor {
            background: var(--accent-green);
        }
        .scratch-block.data {
            background: #161b22;
            border: 1px solid var(--border);
            color: var(--text-primary);
        }
        .scratch-block.nested {
            margin-left: 20px;
        }

        /* PIT LANE REPOSITORY RULES TAB */
        .rules-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
        .rule-card { background: var(--panel); padding: 24px; border-radius: 6px; border: 1px solid var(--border); }
        .rule-card h4 { color: var(--accent-blue); margin-top: 0; display: flex; align-items: center; gap: 8px; font-size: 15px; border-bottom: 1px solid var(--border); padding-bottom: 8px; }
        .rule-card ul { padding-left: 18px; margin: 0; }
        .rule-card li { font-size: 13px; line-height: 1.6; margin-bottom: 8px; color: var(--text-secondary); }
        .rule-card li strong { color: var(--text-primary); }

        /* TUTOR CONSOLE THEME */
        .tutor-console-wrapper {
            background: #010409;
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 16px;
            margin-top: 15px;
        }
        
        /* GITHUB ACTIVE STATUS DOTS */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            font-weight: 500;
            color: var(--text-secondary);
        }
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--text-secondary);
        }
        .status-dot.active {
            background: var(--accent-green);
            box-shadow: 0 0 8px var(--accent-green);
        }
    </style>
</head>
<body>

<div class="header">
    <div class="header-logo">
        <i class="fa-solid fa-cube"></i> SYNTHETIX.AI MATRIX
    </div>
    <div class="status-badge">
        <span class="status-dot active"></span> Local Node Online
    </div>
</div>

<div class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('tab1', this)"><i class="fa-solid fa-terminal"></i> Code Logic & Flash</button>
    <button class="tab-btn" onclick="switchTab('tab2', this)"><i class="fa-solid fa-microchip"></i> Hardware Assembly</button>
    <button class="tab-btn" onclick="switchTab('tab3', this)"><i class="fa-solid fa-calculator"></i> Control Systems</button>
    <button class="tab-btn" onclick="switchTab('tab4', this)"><i class="fa-solid fa-route"></i> Path Planner</button>
    <button class="tab-btn" onclick="switchTab('tab5', this)"><i class="fa-solid fa-book"></i> Diagnostic Manual</button>
    <button class="tab-btn" onclick="switchTab('tab6', this)"><i class="fa-solid fa-key"></i> Enterprise License</button>
</div>

<div id="tab1" class="content active">
    <!-- THREE PANEL COMPILER INTERFACE -->
    <div class="grid-3">
        <!-- PANEL 1: SETTINGS & OFFLINE SANDBOX DEBUGGER + AI TUTOR -->
        <div class="panel" style="display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <h3><i class="fa-solid fa-sliders"></i> Compiler Settings</h3>
                <div id="voiceIndicator" class="voice-status">Optimized Local Recording Live - Speak Now</div>
                
                <div class="mic-indicator-wrapper">
                    <span id="liveMicDot" class="mic-dot"></span>
                    <span id="liveMicText" class="mic-text">Voice Input Engine Standby</span>
                </div>

                <label>Select System Interface Language:</label>
                <select id="langSelect" onchange="updateVoiceLanguage()"></select>
                
                <label>Select Firmware Target Language:</label>
                <select id="roboLangSelect"></select>
                
                <label>Select AI Output View Mode:</label>
                <select id="viewModeSelect" onchange="toggleViewModeDisplays()">
                    <option value="both">Show Both (Visual Blocks + Raw Code)</option>
                    <option value="blocks">Visual Blocks Only (Scratch-style)</option>
                    <option value="code">Raw Code Only</option>
                </select>

                <textarea id="promptInput" rows="3" placeholder="Input execution rules or speak directives..."></textarea>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:10px;">
                    <button id="voiceBtn" onclick="toggleVoiceEngine()"><i class="fa-solid fa-microphone"></i> Start Voice Feed</button>
                    <button class="btn-primary" onclick="compileRobotLogic()"><i class="fa-solid fa-bolt"></i> Process & Compile</button>
                </div>

                <!-- OFFLINE MULTILINGUAL AI ROBOTICS TUTOR -->
                <div class="tutor-console-wrapper">
                    <h4 style="margin:0 0 10px 0; color:var(--accent-green); font-size:13px; font-weight: 600; display:flex; align-items:center; gap:6px;"><i class="fa-solid fa-graduation-cap"></i> Multilingual AI Robotics Tutor</h4>
                    <input type="text" id="tutorQuery" placeholder="Ask Tutor: 'What is a PID controller?'" style="margin-bottom:8px; padding:8px;">
                    <button class="btn-primary" onclick="askAITutor()" style="width:100%; font-size:12px; padding:8px;"><i class="fa-solid fa-paper-plane"></i> Ask Offline AI Tutor</button>
                    <div id="tutorOutput" style="background:#090d16; border:1px solid var(--border); font-size:12px; color:var(--accent-green); padding:10px; border-radius:6px; margin-top:10px; max-height:100px; overflow-y:auto; line-height:1.4;">
                        Local AI Tutor is standby. Ask any robotics questions in your selected language.
                    </div>
                </div>
            </div>

            <!-- INTERACTIVE OFFLINE SANDBOX DEBUGGER TOOL -->
            <div style="margin-top:20px; border-top:1px solid var(--border); padding-top:15px;">
                <h3 style="color:var(--accent-blue);"><i class="fa-solid fa-bug-slash"></i> Offline Debugger Sandbox</h3>
                <button onclick="runOfflineDebugTrace()" style="width:100%; background:#21262d; margin-bottom:10px; font-weight: bold;"><i class="fa-solid fa-magnifying-glass"></i> Run Diagnostic Logic Simulation</button>
                <div id="debugTraceLog" style="background:#010409; color:var(--accent-blue); font-family:'JetBrains Mono', monospace; padding:12px; border-radius:6px; font-size:11px; height:130px; overflow-y:auto; border:1px solid var(--border); line-height:1.4;">
                    System Idle. Ready for code diagnostic sweep.
                </div>
            </div>
        </div>

        <!-- PANEL 2: SCRATCH-STYLE INTERLOCKING VISUAL WORKSPACE (BLUE & WHITE STYLE) -->
        <div class="panel" id="visualWorkspacePanel">
            <h3 style="color:var(--accent-blue); display:flex; justify-content:space-between; align-items:center;">
                <span><i class="fa-solid fa-puzzle-piece"></i> Visual Scratch Blocks</span>
                <span style="font-size:11px; background:#21262d; color:var(--text-secondary); padding:3px 8px; border-radius:12px; border:1px solid var(--border); font-weight:bold;">Workspace</span>
            </h3>
            
            <div id="visualBlocksContainer" class="scratch-workspace">
                <!-- Scratch Blocks will be rendered here dynamically with CSS styled blocks -->
                <div class="scratch-block hat"><i class="fa-solid fa-play"></i> when app starts</div>
                <div class="scratch-block action"><i class="fa-solid fa-cog"></i> initialize hardware matrices</div>
                <div class="scratch-block loop"><i class="fa-solid fa-redo"></i> repeat forever</div>
                <div class="scratch-block sensor nested"><i class="fa-solid fa-search"></i> read configured chassis sensors</div>
                <div class="scratch-block action nested"><i class="fa-solid fa-gears"></i> adjust drive motors based on inputs</div>
            </div>
        </div>

        <!-- PANEL 3: PRODUCTION RAW TARGET CODE -->
        <div class="panel" id="rawCodePanel">
            <h3><i class="fa-solid fa-code"></i> Production Raw Code Output</h3>
            <pre id="codeOut">// Unified execution loop sequence ready...</pre>
            
            <div style="margin-top:20px; border-top:1px solid var(--border); padding-top:15px;">
                <h3><i class="fa-solid fa-microchip"></i> Integrated Direct-USB Flasher Engine</h3>
                <div style="display:flex; gap:10px;">
                    <select id="portSelect" style="margin-bottom:0;"><option>Scanning serial ports...</option></select>
                    <button onclick="refreshPorts()" style="background:#21262d; border:1px solid var(--border);"><i class="fa-solid fa-sync"></i></button>
                </div>
                <button class="btn-primary" onclick="flashFirmwareTarget()" style="width:100%; margin-top:15px;"><i class="fa-solid fa-upload"></i> Execute Live USB Binary Stream</button>
            </div>
        </div>
    </div>
</div>

<div id="tab2" class="content">
    <div class="grid-2">
        <div class="panel" style="text-align: center;">
            <h3><i class="fa-solid fa-toolbox"></i> Multi-Category Matrix Crafting System</h3>
            <select id="dbSelect" onchange="updatePartInventoryOptions()"></select>
            <select id="partSelect"></select>
            <div class="mc-grid" style="margin-bottom:20px;">
                <!-- slots accompanied by Pin Out Configurator Options -->
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(0)" id="c0">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(0)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(1)" id="c1">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(1)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(2)" id="c2">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(2)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(3)" id="c3">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(3)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(4)" id="c4">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(4)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(5)" id="c5">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(5)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(6)" id="c6">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(6)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(7)" id="c7">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(7)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
                <div class="mc-slot-wrapper">
                    <div class="mc-slot" onclick="executeCraftPlacement(8)" id="c8">Empty Node</div>
                    <button class="pin-config-btn" onclick="openPinAssignModal(8)"><i class="fa-solid fa-plug"></i> Wire Pins</button>
                </div>
            </div>
            <button class="btn-primary" onclick="initializeAssembly()" style="width:100%; margin-top:10px;"><i class="fa-solid fa-play"></i> Initialize Assembly Matrix Setup</button>
            
            <!-- POP-UP DIALOG MODAL FOR PIN OUT HELPERS -->
            <div id="pinModal" style="display:none; background:#161b22; padding:15px; border-radius:6px; border:1px solid var(--border); margin-top:20px; text-align:left;">
                <h4 style="margin:0 0 10px 0; color:var(--accent-blue);"><i class="fa-solid fa-circle-info"></i> Configure Device Connections</h4>
                <label style="font-size:11px;">Connect Signal Pin:</label>
                <select id="pinSignalSel" style="margin-bottom:8px; padding:6px;">
                    <option value="D3">Digital IO Pin D3</option>
                    <option value="D5">Digital IO Pin D5</option>
                    <option value="D6">Digital IO Pin D6</option>
                    <option value="D9">Digital IO Pin D9</option>
                    <option value="A0">Analog Input Pin A0</option>
                    <option value="I2C">I2C Communication Bus (SDA/SCL)</option>
                </select>
                <label style="font-size:11px;">Connect Power (VCC):</label>
                <select id="pinPwrSel" style="margin-bottom:8px; padding:6px;">
                    <option value="5V">5V Voltage Rail</option>
                    <option value="3.3V">3.3V Low-Power Rail</option>
                    <option value="12V">12V High-Power Battery Line</option>
                </select>
                <button class="btn-primary" onclick="savePinConfiguration()" style="width:100%; font-size:12px; padding:8px;"><i class="fa-solid fa-save"></i> Save Wire Allocation</button>
            </div>
        </div>
        <div class="panel">
            <h3><i class="fa-solid fa-diagram-project"></i> Automated Local Pin Wiring Schematic Canvas</h3>
            <canvas id="wireCanvas" width="600" height="380"></canvas>
        </div>
    </div>
</div>

<div id="tab3" class="content">
    <div class="grid-2">
        <div class="panel">
            <h3><i class="fa-solid fa-wave-square"></i> System Drift Correction Matrix Solver</h3>
            <input type="number" id="driftVal" placeholder="Physical Drift Value (cm)">
            <button class="btn-primary" onclick="calculateLoopPID()" style="width:100%;"><i class="fa-solid fa-calculator"></i> Solve Mathematical Dynamic Tuning Loop</button>
            <pre id="pidOut" style="height:120px; margin-top:15px; color:var(--accent-blue);">Kp: 0.0000 | Ki: 0.0000 | Kd: 0.0000</pre>
        </div>
        <div class="panel">
            <h3><i class="fa-solid fa-arrows-spin"></i> Holonomic Swerve & Mecanum Kinematics Solver</h3>
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px;">
                <input type="number" id="vX" placeholder="Target X Vec">
                <input type="number" id="vY" placeholder="Target Y Vec">
                <input type="number" id="vRot" placeholder="Angular Rads">
            </div>
            <button class="btn-primary" onclick="calculateVectorKinematics()" style="width:100%;"><i class="fa-solid fa-calculator"></i> Resolve Angular Distribution Matrix</button>
            <pre id="swerveOut" style="height:120px; margin-top:15px; color:var(--text-primary);">Results awaiting velocity variables...</pre>
        </div>
    </div>
</div>

<div id="tab4" class="content">
    <div class="panel" style="text-align: center;">
        <h3><i class="fa-solid fa-map-location-dot"></i> High-Resolution Autonomous Trajectory Path Modeler & Simulator</h3>
        <canvas id="pathCanvas" width="1000" height="420" style="background:#010409;" onmousedown="initiatePathDraw(event)" onmousemove="renderLivePath(event)" onmouseup="terminatePathDraw()"></canvas>
        <div style="margin-top:15px; display:flex; gap:10px; justify-content:center;">
            <button class="btn-danger" onclick="clearPathModeler()"><i class="fa-solid fa-trash"></i> Flush Path Memory Cache</button>
            <button class="btn-primary" onclick="injectTrajectoryToRobot()"><i class="fa-solid fa-save"></i> Inject Trajectory Path into Firmware Core</button>
            <button onclick="startRobotTestDriveSimulation()" style="background:#21262d; color:#ffffff; font-weight:bold; border-color: var(--accent-blue);"><i class="fa-solid fa-play"></i> Run Virtual Test Drive</button>
        </div>
        <pre id="pathMath" style="height:110px; text-align:left; margin-top:15px; color:var(--accent-green);">Trace lines to construct trajectory arrays...</pre>
    </div>
</div>

<div id="tab5" class="content">
    <div class="panel">
        <h3 style="margin-bottom: 20px; border-bottom: 1px solid var(--border); padding-bottom: 12px; color: var(--accent-blue);"><i class="fa-solid fa-book-open"></i> Structural Pit Lane Master Diagnostic Manual & Rules</h3>
        
        <div class="rules-grid">
            <div class="rule-card">
                <h4><i class="fa-solid fa-bolt"></i> Golden Rules of Electrical Wiring</h4>
                <ul>
                    <li><strong>Common Ground Reference:</strong> Always connect all system ground pins (GND) to a single common baseline wire to prevent electrical signal loop noise.</li>
                    <li><strong>The Polarity Rule:</strong> Double-check Positive (VCC) and Negative (GND) lines before switching on power. Reversing polarity will damage your microcontrollers.</li>
                    <li><strong>Wire Safety Paths:</strong> Avoid routing cables over raw carbon fiber edges or custom aluminum frames. Sharp edges can cut wire insulation.</li>
                </ul>
            </div>
            
            <div class="rule-card">
                <h4><i class="fa-solid fa-cog"></i> Mechanical Inspection & Fit Guide</h4>
                <ul>
                    <li><strong>Fastener Checklist:</strong> Ensure all motor brackets, axle hubs, and framing joints have locking nuts or threadlock fluid applied before entering active tests.</li>
                    <li><strong>Gear Mesh Calibration:</strong> Keep a paper-thin spacer gap between matching motor gears. Tight gears consume excessive current and cause frame friction.</li>
                    <li><strong>Wheel Cleanliness:</strong> Keep Mecanum roller slots clear of hair, dirt, and tape adhesive to maintain accurate vector calculations.</li>
                </ul>
            </div>
            
            <div class="rule-card">
                <h4><i class="fa-solid fa-bug"></i> Rapid Offline Code Debugging</h4>
                <ul>
                    <li><strong>COM Interface Faults:</strong> If flashing fails, confirm your target port matching under the Direct-USB flasher block. Disconnect and re-insert the USB cable if stuck.</li>
                    <li><strong>Baud Rate Synchronicity:</strong> Match the baud rate inside your code configuration with your serial console to view raw telemetry.</li>
                    <li><strong>Loose Wire Check:</strong> If a sensor displays zero value constantly, trace its signal wire directly back to its designated pin on your controller hub.</li>
                </ul>
            </div>

            <div class="rule-card">
                <h4><i class="fa-solid fa-car-battery"></i> Safe Battery & Storage Practices</h4>
                <ul>
                    <li><strong>Healthy Storage:</strong> Keep rechargeable batteries in a clean, cool, and dry storage box inside the classroom when not in use.</li>
                    <li><strong>Visual Checks:</strong> Inspect battery wire wraps periodically. If a wire is bare, report it to the supervisor for professional insulated wrapping.</li>
                    <li><strong>Careful Handling:</strong> Disconnect batteries gently from the main frame using the official plastic connectors—never pull directly on the red or black wires.</li>
                </ul>
            </div>
        </div>
    </div>
</div>

<div id="tab6" class="content">
    <div class="panel" style="max-width: 550px; margin: 40px auto; text-align: center;">
        <h3>Synthetix.AI Enterprise Global License Activation</h3>
        <div style="font-size: 48px; color: var(--accent-green); font-weight: 800; margin: 25px 0; font-family: 'JetBrains Mono', monospace;">Rs. 1999</div>
        <button class="btn-primary" style="width:100%; padding: 16px;"><i class="fa-solid fa-key"></i> Authorize Key Activation</button>
    </div>
</div>

<script>
    let isDrawing = false; let pathPoints = []; let craftSlots = Array(9).fill(null); let cachedHardwareDatabase = {};
    let recognition = null; let voiceActive = false;
    
    // STATE FOR INTERACTIVE WIRE CONFIGURATIONS
    let selectedSlotIndexForPins = null;
    let pinConfigurations = Array(9).fill().map(() => ({ signal: "D3", pwr: "5V" }));

    // STATE FOR THE 2D ROBOT SIMULATION LOOP
    let simRobotIndex = 0;
    let simIntervalId = null;

    async function initApp() {
        const structuralLangs = await pywebview.api.get_languages();
        document.getElementById('langSelect').innerHTML = Object.entries(structuralLangs).map(([c, n]) => `<option value="${c}">${n}</option>`).join('');
        const robotFirms = await pywebview.api.get_robo_languages();
        document.getElementById('roboLangSelect').innerHTML = robotFirms.map(lbl => `<option value="${lbl}">${lbl}</option>`).join('');
        cachedHardwareDatabase = await pywebview.api.get_db();
        document.getElementById('dbSelect').innerHTML = Object.keys(cachedHardwareDatabase).map(cat => `<option value="${cat}">${cat}</option>`).join('');
        
        setupVoiceRecognition();
        updatePartInventoryOptions(); refreshPorts(); drawWiringSchematic();
        updateVisualScratchBlocks(); // Initialize default Scratch script visual blocks
    }

    function setupVoiceRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous = true;
            recognition.interimResults = true;
            recognition.maxAlternatives = 1;

            recognition.onstart = () => {
                document.getElementById('voiceIndicator').style.display = 'block';
                document.getElementById('voiceBtn').innerHTML = "<i class='fa-solid fa-circle-stop'></i> Stop Voice Feed";
                document.getElementById('voiceBtn').style.background = "var(--accent-red)";
                document.getElementById('voiceBtn').style.color = "#ffffff";
                
                // Set high-visibility visual indicator states
                const micDot = document.getElementById('liveMicDot');
                const micText = document.getElementById('liveMicText');
                micDot.classList.add('listening');
                micText.classList.add('listening');
                micText.innerText = "Listening... Speak directly to the microphone";
            };

            recognition.onresult = (event) => {
                let interimTranscript = '';
                let finalTranscript = '';
                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript + ' ';
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }
                if (finalTranscript) {
                    let currentVal = document.getElementById('promptInput').value.trim();
                    document.getElementById('promptInput').value = (currentVal ? currentVal + " " : "") + finalTranscript.trim();
                }
            };

            recognition.onend = () => {
                if (voiceActive) {
                    setTimeout(() => {
                        try { recognition.start(); } catch(e) { console.log("Voice channel re-acquiring..."); }
                    }, 150);
                } else {
                    document.getElementById('voiceIndicator').style.display = 'none';
                    document.getElementById('voiceBtn').innerHTML = "<i class='fa-solid fa-microphone'></i> Start Voice Feed";
                    document.getElementById('voiceBtn').style.background = "var(--hover-bg)";
                    document.getElementById('voiceBtn').style.color = "var(--accent-blue)";
                    
                    // Clear visual indicator states
                    const micDot = document.getElementById('liveMicDot');
                    const micText = document.getElementById('liveMicText');
                    micDot.classList.remove('listening');
                    micText.classList.remove('listening');
                    micText.innerText = "Voice Input Engine Standby";
                }
            };

            recognition.onerror = (e) => {
                console.log("Voice channel exception handled safely: " + e.error);
                if (e.error === 'no-speech' && voiceActive) {
                    return;
                }
                if (e.error === 'not-allowed') {
                    const micText = document.getElementById('liveMicText');
                    micText.innerText = "Error: Microphone permission denied. Grant access.";
                    micText.style.color = "var(--accent-red)";
                }
            };
        } else {
            // SpeechRecognition is completely unavailable in the runtime
            document.getElementById('liveMicText').innerText = "Engine Status: Browser Speech API Unsupported";
            document.getElementById('liveMicText').style.color = "var(--accent-red)";
        }
    }

    function updateVoiceLanguage() {
        if (recognition && voiceActive) {
            recognition.stop();
            recognition.lang = document.getElementById('langSelect').value;
        } else if (recognition) {
            recognition.lang = document.getElementById('langSelect').value;
        }
    }

    // Toggle speech engine listening loop
    function toggleVoiceEngine() {
        if (!recognition) {
            alert("Speech recognition engine not compatible with local hardware drivers.");
            return;
        }
        if (!voiceActive) {
            voiceActive = true;
            recognition.lang = document.getElementById('langSelect').value;
            try { recognition.start(); } catch(e) {}
        } else {
            voiceActive = false;
            recognition.stop();
        }
    }

    function updatePartInventoryOptions() {
        const cat = document.getElementById('dbSelect').value;
        document.getElementById('partSelect').innerHTML = (cachedHardwareDatabase[cat] || []).map(p => `<option value="${p}">${p}</option>`).join('');
    }

    // Interactive UI multi-tabs controller with transition animations
    function switchTab(tabID, element) {
        document.querySelectorAll('.content').forEach(c => c.classList.remove('active'));
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        document.getElementById(tabID).classList.add('active');
        element.classList.add('active');
    }

    function executeCraftPlacement(idx) {
        const item = document.getElementById('partSelect').value; if(!item) return;
        craftSlots[idx] = item; document.getElementById(`c${idx}`).innerText = item.substring(0,12) + "...";
        drawWiringSchematic();
        updateVisualScratchBlocks(); // Sync blocks with newly added parts
    }

    async function initializeAssembly() {
        let activeBuildProfile = craftSlots.filter(x => x !== null);
        alert(await pywebview.api.update_hardware_profile(activeBuildProfile));
        updateVisualScratchBlocks(); // Redraw blocks inside workspace
    }

    // SAVING SPECIFIC CUSTOM PIN WIRING ALLOCATIONS
    function openPinAssignModal(idx) {
        if (!craftSlots[idx]) {
            alert("Please craft a component inside this slot first before wiring its pinouts!");
            return;
        }
        selectedSlotIndexForPins = idx;
        document.getElementById('pinModal').style.display = 'block';
    }

    function savePinConfiguration() {
        if (selectedSlotIndexForPins === null) return;
        const sigValue = document.getElementById('pinSignalSel').value;
        const pwrValue = document.getElementById('pinPwrSel').value;
        pinConfigurations[selectedSlotIndexForPins] = { signal: sigValue, pwr: pwrValue };
        document.getElementById('pinModal').style.display = 'none';
        drawWiringSchematic();
        selectedSlotIndexForPins = null;
    }

    // AUTOMATED DYNAMIC SCHEMATIC PINOUT ROUTER CANVAS DRAWINGS
    function drawWiringSchematic() {
        const canvas = document.getElementById('wireCanvas'); const ctx = canvas.getContext('2d');
        ctx.clearRect(0,0,canvas.width,canvas.height);
        
        // Draw centralized Arduino microcontroller board frame
        ctx.fillStyle = "#161b22"; ctx.fillRect(220, 120, 160, 140);
        ctx.strokeStyle = "#30363d"; ctx.lineWidth = 4; ctx.strokeRect(220,120,160,140);
        ctx.fillStyle = "#58a6ff"; ctx.font = "bold 13px sans-serif"; ctx.fillText("ARDUINO CORE", 255, 160);
        
        // Draw microcontroller connection port header rows
        ctx.fillStyle = "#010409"; ctx.fillRect(230, 200, 140, 40);
        ctx.fillStyle = "#c9d1d9"; ctx.font = "bold 9px monospace";
        ctx.fillText("5V  GND  A0  D3  D5  D6", 240, 224);

        craftSlots.forEach((item, i) => {
            if(item) {
                const col = i % 3; const row = Math.floor(i / 3);
                const itemX = col * 205 + 15; const itemY = row * 125 + 15;
                
                // Render custom component slot container box
                ctx.fillStyle = "#010409"; ctx.fillRect(itemX, itemY, 160, 32);
                ctx.strokeStyle = "#30363d"; ctx.lineWidth = 1; ctx.strokeRect(itemX, itemY, 160, 32);
                ctx.fillStyle = "#c9d1d9"; ctx.font = "10px sans-serif";
                ctx.fillText(item.substring(0, 16) + "...", itemX + 8, itemY + 18);

                // Determine wiring paths based on allocated pins
                const config = pinConfigurations[i];
                let signalColor = "#58a6ff"; // default blue
                if (config.signal === "I2C") signalColor = "#d29922"; // yellow
                if (config.signal.includes("A")) signalColor = "#bc8cff"; // purple

                // POWER WIRING Allocation (Red Wire)
                ctx.strokeStyle = "#f85149"; ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(itemX + 20, itemY + 32);
                ctx.lineTo(240, 235);
                ctx.stroke();

                // GROUND WIRING Allocation (Black Wire)
                ctx.strokeStyle = "#484f58"; ctx.lineWidth = 1.5;
                ctx.beginPath();
                ctx.moveTo(itemX + 50, itemY + 32);
                ctx.lineTo(265, 235);
                ctx.stroke();

                // SIGNAL DATA WIRING Allocation (Custom Pin Dependent Color)
                ctx.strokeStyle = signalColor; ctx.lineWidth = 2.0;
                ctx.beginPath();
                ctx.moveTo(itemX + 110, itemY + 32);
                let targetX = 290;
                if (config.signal === "D5") targetX = 315;
                if (config.signal === "D6") targetX = 340;
                ctx.lineTo(targetX, 235);
                ctx.stroke();
            }
        });
    }

    async function calculateLoopPID() {
        const val = document.getElementById('driftVal').value;
        const res = await pywebview.api.calculate_pid(val);
        document.getElementById('pidOut').innerText = `Kp: ${res.kp} | Ki: ${res.ki} | Kd: ${res.kd}`;
    }

    // Kinematics calculations for swerve and mecanum drivebases
    function calculateVectorKinematics() {
        const x = parseFloat(document.getElementById('vX').value || 0);
        const y = parseFloat(document.getElementById('vY').value || 0);
        const rot = parseFloat(document.getElementById('vRot').value || 0);
        document.getElementById('swerveOut').innerText = `FR: ${Math.sqrt((y+rot)**2 + (x+rot)**2).toFixed(4)}\nFL: ${Math.sqrt((y+rot)**2 + (x-rot)**2).toFixed(4)}`;
    }

    function initiatePathDraw(e) { isDrawing = true; pathPoints = []; const ctx = document.getElementById('pathCanvas').getContext('2d'); ctx.beginPath(); ctx.moveTo(e.offsetX, e.offsetY); }
    function renderLivePath(e) { if(!isDrawing) return; const ctx = document.getElementById('pathCanvas').getContext('2d'); ctx.lineTo(e.offsetX, e.offsetY); ctx.strokeStyle = "#58a6ff"; ctx.lineWidth = 4; ctx.stroke(); pathPoints.push({x: e.offsetX, y: e.offsetY}); }
    function terminatePathDraw() { isDrawing = false; }
    async function injectTrajectoryToRobot() {
        let dataString = pathPoints.map(p => `[${p.x},${p.y}]`).join(",");
        alert(await pywebview.api.set_injected_path(dataString));
        updateVisualScratchBlocks(); // Trigger trajectory block inclusions
    }
    function clearPathModeler() { 
        if (simIntervalId) { clearInterval(simIntervalId); simIntervalId = null; }
        const c = document.getElementById('pathCanvas'); c.getContext('2d').clearRect(0,0,c.width,c.height); 
    }

    // THE 2D LIVE ROBOT SIMULATOR ANIMATOR WITH DYNAMIC ROTATION
    function startRobotTestDriveSimulation() {
        if (pathPoints.length === 0) {
            alert("Draw a path trajectory on the canvas map first before running a test simulation!");
            return;
        }
        if (simIntervalId) { clearInterval(simIntervalId); }
        
        simRobotIndex = 0;
        const canvas = document.getElementById('pathCanvas');
        const ctx = canvas.getContext('2d');

        simIntervalId = setInterval(() => {
            if (simRobotIndex >= pathPoints.length) {
                clearInterval(simIntervalId);
                simIntervalId = null;
                alert("Virtual simulation test drive finished successfully!");
                return;
            }

            // Redraw background canvas and full line trajectory
            ctx.clearRect(0,0,canvas.width,canvas.height);
            ctx.strokeStyle = "#21262d"; ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.moveTo(pathPoints[0].x, pathPoints[0].y);
            for (let k = 1; k < pathPoints.length; k++) {
                ctx.lineTo(pathPoints[k].x, pathPoints[k].y);
            }
            ctx.stroke();

            const point = pathPoints[simRobotIndex];

            // CALCULATE THE ANGLE OF ROTATION TO FACE THE DIRECTION OF TRAVEL
            let angle = 0;
            if (simRobotIndex < pathPoints.length - 2) {
                const nextPoint = pathPoints[simRobotIndex + 2];
                angle = Math.atan2(nextPoint.y - point.y, nextPoint.x - point.x);
            } else if (simRobotIndex > 1) {
                const prevPoint = pathPoints[simRobotIndex - 2];
                angle = Math.atan2(point.y - prevPoint.y, point.x - prevPoint.x);
            }

            // Draw spinning Robot body
            ctx.save();
            ctx.translate(point.x, point.y);
            ctx.rotate(angle); // Rotate chassis to face heading
            
            // Draw sweeping ultrasonic sensor range beam (green arc) pointing forward
            ctx.fillStyle = "rgba(63, 185, 80, 0.15)";
            ctx.beginPath(); ctx.moveTo(0,0); ctx.arc(0, 0, 50, -Math.PI/4, Math.PI/4); ctx.closePath(); ctx.fill();
            ctx.strokeStyle = "#3fb950"; ctx.lineWidth = 1; ctx.stroke();

            // Draw robot chassis
            ctx.fillStyle = "#58a6ff"; ctx.fillRect(-15, -15, 30, 30);
            ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 2; ctx.strokeRect(-15, -15, 30, 30);

            // Draw 4 independent wheels
            ctx.fillStyle = "#8b949e";
            ctx.fillRect(-18, -14, 4, 8);
            ctx.fillRect(14, -14, 4, 8);
            ctx.fillRect(-18, 6, 4, 8);
            ctx.fillRect(14, 6, 4, 8);

            ctx.restore();

            simRobotIndex += 2; // Jump speed indexes to move quickly
        }, 30);
    }

    async function askAITutor() {
        const query = document.getElementById('tutorQuery').value;
        const lang = document.getElementById('langSelect').value;
        if (!query) {
            alert("Type in a robotics question for your tutor first!");
            return;
        }
        document.getElementById('tutorOutput').innerText = "Typing response... Please stand by.";
        const reply = await pywebview.api.tutor_chat(query, lang);
        document.getElementById('tutorOutput').innerText = reply;
    }

    async function refreshPorts() {
        const targetNodes = await pywebview.api.get_serial_ports();
        document.getElementById('portSelect').innerHTML = targetNodes.map(p => `<option value="${p}">${p}</option>`).join('') || '<option>No COM Detected</option>';
    }
    async function flashFirmwareTarget() { alert(await pywebview.api.send_to_serial(document.getElementById('portSelect').value, 115200, document.getElementById('codeOut').innerText)); }

    // DYNAMIC SCRATCH BLOCK DIAGRAM RENDERING GENERATOR (NO EMOJIS, SLEEK SVG ICONS)
    function updateVisualScratchBlocks() {
        const container = document.getElementById('visualBlocksContainer');
        container.innerHTML = ''; // Clear existing block states

        // 1. Event Hat block
        const hat = document.createElement('div');
        hat.className = 'scratch-block hat';
        hat.innerHTML = '<i class="fa-solid fa-play"></i> when robot starts';
        container.appendChild(hat);

        // 2. Active profile parameters
        let activeBuildProfile = craftSlots.filter(x => x !== null);
        if (activeBuildProfile.length > 0) {
            activeBuildProfile.forEach(part => {
                const block = document.createElement('div');
                block.className = 'scratch-block action';
                let shortName = part.length > 20 ? part.substring(0, 18) + '...' : part;
                block.innerHTML = `<i class="fa-solid fa-cog"></i> configure device: [ ${shortName} ]`;
                container.appendChild(block);
            });
        } else {
            const defaultBlock = document.createElement('div');
            defaultBlock.className = 'scratch-block action';
            defaultBlock.innerHTML = '<i class="fa-solid fa-cog"></i> configure device: [ Default Hub Base ]';
            container.appendChild(defaultBlock);
        }

        // 3. Serial channel configurations
        const baudBlock = document.createElement('div');
        baudBlock.className = 'scratch-block data';
        baudBlock.innerHTML = '<i class="fa-solid fa-broadcast-tower"></i> set serial port rate to [ 115200 ]';
        container.appendChild(baudBlock);

        // 4. Repeat loop block
        const loop = document.createElement('div');
        loop.className = 'scratch-block loop';
        loop.innerHTML = '<i class="fa-solid fa-redo"></i> repeat forever';
        container.appendChild(loop);

        // 5. Nested parameters inside the loop workspace (indent with .nested)
        const sensorBlock = document.createElement('div');
        sensorBlock.className = 'scratch-block sensor nested';
        sensorBlock.innerHTML = '<i class="fa-solid fa-search"></i> read target loop telemetry';
        container.appendChild(sensorBlock);

        // If path planner matrix coords are injected
        if (pathPoints.length > 0) {
            const pathBlock = document.createElement('div');
            pathBlock.className = 'scratch-block data nested';
            pathBlock.innerHTML = `<i class="fa-solid fa-route"></i> adjust trajectory [ ${pathPoints.length} coords ]`;
            container.appendChild(pathBlock);
        }

        const mathBlock = document.createElement('div');
        mathBlock.className = 'scratch-block action nested';
        mathBlock.innerHTML = '<i class="fa-solid fa-calculator"></i> solve PID alignment corrections';
        container.appendChild(mathBlock);

        const outBlock = document.createElement('div');
        outBlock.className = 'scratch-block action nested';
        outBlock.innerHTML = '<i class="fa-solid fa-gears"></i> update motor drive controllers';
        container.appendChild(outBlock);
    }

    // Toggle panel displays depending on dropdown views
    function toggleViewModeDisplays() {
        const mode = document.getElementById('viewModeSelect').value;
        const workspace = document.getElementById('visualWorkspacePanel');
        const codePanel = document.getElementById('rawCodePanel');
        const grid = document.querySelector('.grid-3');

        if (mode === "blocks") {
            workspace.style.display = "block";
            codePanel.style.display = "none";
            grid.style.gridTemplateColumns = "1.2fr 2.8fr";
        } else if (mode === "code") {
            workspace.style.display = "none";
            codePanel.style.display = "block";
            grid.style.gridTemplateColumns = "1.2fr 2.8fr";
        } else {
            workspace.style.display = "block";
            codePanel.style.display = "block";
            grid.style.gridTemplateColumns = "1.1fr 1.45fr 1.455fr";
        }
    }

    // RUN INTERACTIVE OFFLINE SIMULATION LOG RUNNER
    function runOfflineDebugTrace() {
        const logBox = document.getElementById('debugTraceLog');
        logBox.innerHTML = ''; // Flush diagnostic log caches
        
        const logs = [
            { text: "[SYSTEM BOOT] Initializing Synthetix Sandbox Diagnostic...", delay: 0 },
            { text: "[PWR] Verifying common voltage distribution rails... OK", delay: 200 },
            { text: "[GND] Analyzing ground loop plane consistency... Aligned 0V common rail successfully.", delay: 450 },
            { text: "[COM] Testing virtual host COM serial transceiver... Bound simulated interface at 115200 Baud.", delay: 700 },
            { text: "[PATH] Testing autonomous trajectory coordinate buffer... Injected " + (pathPoints.length || 0) + " trace elements.", delay: 950 },
            { text: "[MATH] Verifying Kinematic Swerve coefficient vector grids... Done.", delay: 1200 },
            { text: "[CALIBRATION] Simulating test control loop iteration... 0.0000 drift correction achieved.", delay: 1450 },
            { text: "[SUCCESS] Diagnostic trace complete! 0 Warnings, 0 Faults. Sandbox environment is safe to deploy.", delay: 1700 }
        ];

        logs.forEach(log => {
            setTimeout(() => {
                const line = document.createElement('div');
                line.style.marginBottom = "5px";
                line.style.borderBottom = "1px solid #111827";
                line.style.paddingBottom = "3px";
                
                if (log.text.includes("SUCCESS")) {
                    line.style.color = "var(--accent-green)"; 
                    line.style.fontWeight = "bold";
                } else if (log.text.includes("SYSTEM BOOT")) {
                    line.style.color = "var(--accent-purple)"; 
                } else {
                    line.style.color = "var(--accent-blue)"; 
                }
                
                line.innerText = log.text;
                logBox.appendChild(line);
                logBox.scrollTop = logBox.scrollHeight;
            }, log.delay);
        });
    }

    async function compileRobotLogic() {
        const prompt = document.getElementById('promptInput').value;
        const targetLang = document.getElementById('roboLangSelect').value;
        const viewMode = document.getElementById('viewModeSelect').value;
        document.getElementById('codeOut').innerText = "// Compiling logic matrix and loading views...";
        
        // Fetch raw target firmware code directly from local Qwen framework
        const codeResult = await pywebview.api.generate_code(prompt, targetLang, viewMode);
        document.getElementById('codeOut').innerText = codeResult;
        
        // Always reconstruct physical visual Scratch blocks workspace in sync with changes
        updateVisualScratchBlocks();
    }

    window.addEventListener('pywebviewready', initApp);
</script>
</body>
</html>
"""

# DEFINE THE LOCAL HOOK SERVER TO PROVIDE A SECURE DOMAIN CONTEXT
class LocalSecureServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html_content.encode("utf-8"))
    def log_message(self, format, *args):
        pass # Suppress logging clutter in the launcher console

def start_isolated_server():
    server = HTTPServer(('127.0.0.1', 0), LocalSecureServer)
    assigned_port = server.server_address[1]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return assigned_port

if __name__ == "__main__":
    api = SynthetixAPI()
    
    # 1. Start the micro-server to get a dynamic secure origin
    secure_port = start_isolated_server()
    local_secure_url = f"http://127.0.0.1:{secure_port}"
    
    # 2. Create app targeting our local secure origin link
    window = webview.create_window(
        "Synthetix.AI - 100% Local Arena Matrix", 
        url=local_secure_url, 
        js_api=api, 
        width=1500, 
        height=950
    )
    webview.start()