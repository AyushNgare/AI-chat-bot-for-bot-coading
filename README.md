Synthetix.AI

Universal Offline Arena Matrix & Multilingual Edge AI Robotics Suite

Synthetix.AI is an offline-first robotics development, hardware configuration, and 2D physics simulation suite designed specifically for educational classrooms and competitive robotics environments. By deploying lightweight Small Language Models (SLMs) and mathematical solvers locally on the host machine's CPU, the platform eliminates the barriers of cloud subscription fees, active internet connections, and English-only programming frameworks.

The software empowers students to utilize their native regional languages to write firmware, design electrical schematics, compute feedback loops, and simulate autonomous trajectories inside a safe, offline sandbox environment.

Architectural Design

The application utilizes a lightweight, local-first hybrid architecture to ensure low-latency performance and 100% offline stability.

+-----------------------------------------------------------------+
|                       USER INTERFACE LAYER                      |
|             PyWebView Desktop Viewport (HTML5/CSS3/JS)          |
+-----------------------------------------------------------------+
                                |
             Local API Calls    |   Isolated HTTP Sockets
             (JSON Telemetry)   v   (Loopback: 127.0.0.1)
+-----------------------------------------------------------------+
|                    LOCAL COMMUNICATION ENGINE                   |
|                   Python Micro-Server Socket                    |
+-----------------------------------------------------------------+
            |                                       |
            | Local Host Loopback                   | PySerial I/O Driver
            v (Port 11434)                          v (USB COM Bus)
+------------------------+             +--------------------------+
|     EDGE AI STACK      |             |     PHYSICAL BRIDGE      |
|  Ollama Server Client  |             |  Target Microcontroller  |
|  Qwen2.5-Coder:0.5B    |             |   (Arduino, ESP32, etc.) |
+------------------------+             +--------------------------+


1. User Interface Layer

Powered by a customized desktop viewport using PyWebView. The frontend is styled under a clean, high-contrast Dark Developer aesthetic to match modern software repository guidelines. It renders responsive layouts across varying display aspect ratios using modern CSS standards, executing fluid, GPU-accelerated transition animations for tab states and workspace interactions.

2. Local Communication Engine

Operates an isolated Python HTTP socket server on the loopback interface (127.0.0.1) to securely route operations, canvas state data, and telemetry loops. Since the browser context resides within a local desktop window, Web Sockets and POST requests are dispatched internally to eliminate any risk of cross-site scripting (XSS) or browser sandbox violations.

3. Edge AI Stack

Communicates locally with Ollama's model server API to trigger near-instantaneous code generation and tutoring help using optimized quantization configurations. The pipeline packages user input, selected firmware languages, active hardware matrices, and injected coordinates into a pre-structured system instruction context to keep responses consistent, safe, and age-appropriate.

4. Physical Bridge (Serial I/O)

Interfaces directly with target microcontrollers via PySerial to allow direct USB binary flashing without external IDE dependencies. It auto-detects incoming Baud rate structures, manages buffer arrays, handles handshake lines, and performs hardware resets safely.

Technical Features Deep-Dive

1. Multilingual Voice-to-Code Compiler

Local Parsing Engine: Connects to localized models (such as Qwen2.5-Coder-0.5B) to process raw voice feeds inside the browser. It listens via the system microphone input, leveraging Web Speech browser integrations to construct locally transcribed command lines.

Linguistic Independence: Supports all 22 official regional languages of India (including Marathi, Hindi, and Tamil), breaking the English-language barrier in STEM. This ensures that technical terminology is translated dynamically without loss of mathematical context.

Parallel Synthesis Pipeline: Automatically converts spoken natural-language descriptions into two concurrent formats:

Visual Logic Blocks: Interlocking, Scratch-style visual programming blocks for beginners to grasp structural flow control, conditions, loops, and variable allocations.

Raw Firmware Source: Synthesizes optimized, compilation-ready files for platforms including Arduino C++, MicroPython, WPILib, and ROS2, cleanly formatted and free of extraneous markdown structures.

2. Interactive Assembly Board & Schematic Canvas

3x3 Component Placements Grid: A physical hardware mapping matrix. Students choose real-world components (microcontrollers, motors, drivers, and visual sensors) from a comprehensive pre-defined local database and plug them into virtual nodes.

Rule-Based Wire Router: Assigning pin allocations dynamically draws an interactive schematic on the canvas. The routing engine calculates the path coordinates from each component block to the target pins on the main controller representation.

Safety Rail Indicators: Wires are color-coded based on active currents to prevent hardware short circuits:

Red Paths: Represent VCC Power rails (3.3V, 5V, or 12V battery inputs).

Black Paths: Represent Common Ground (GND) connections, teaching students the essential rule of zero-voltage reference.

Blue, Purple, and Yellow Paths: Represent digital, analog, or communication (I2C) signal paths, verifying that components are connected to compatible interface pins on the brain.

3. Dynamic Control Systems Solvers

Feedback Drift Correction (PID): Corrects real-world positional drift (due to uneven friction, surface slopes, or wheel slips) using a proportional-integral-derivative control loop:

$$u(t) = K_p e(t) + K_i \int_{0}^{t} e(\tau) d\tau + K_d \frac{de(t)}{dt}$$

Inputting measured deviation values instantly outputs ideal proportional ($Kp$), integral ($Ki$), and derivative ($Kd$) variables. For hardware execution, these constants are converted to discretized algorithms optimized for microcontrollers:

$$u[n] = K_p e[n] + K_i \sum_{i=0}^{n} e[i] \Delta t + K_d \frac{e[n] - e[n-1]}{\Delta t}$$

Kinematics Distribution Solver: Translates overall direction commands (sideways $X$, forward $Y$, and rotational $Rot$) into exact power percentages for individual wheels, supporting Mecanum and Coaxial Swerve drive layouts. The mathematics automatically project linear and angular velocity vectors onto each active drive hub to prevent chassis locking.

4. 2D Path Modeler & Physics Simulator

Vector Path Tracer: Converts freehand mouse drawings on the field canvas into structured coordinate arrays in memory. The canvas records user drag points, applying a curve-fitting step to drop redundant points and save vector steps.

Virtual Test Drive Loop: Simulates autonomous runs with active rotational alignment. The virtual robot calculates its exact heading angle ($\theta$) at every node:

$$\theta = \text{atan2}(\Delta y, \Delta x)$$

This aligns the chassis wheels dynamically while a sweeping range cone simulates real-time ultrasonic sensor radar tracking. This simulation operates at a fixed 30Hz loop, matching the latency profile of actual physical sensors.

5. Multilingual AI Science Tutor

Edge Knowledge Assistant: A dedicated, localized AI chat interface serving as an encouraging classroom mentor. Explains complex hardware topics, electronics pinouts, and debugging rules in regional Indian languages, keeping explanations safe and educational.

Active Debug Sandbox: Runs complete local diagnostic trace loops simulating voltage checks, common ground matching, and Baud rate synchronicity.

API Reference

The local communication server exposes a set of direct API paths to facilitate frontend-backend operations:

get_db(): Fetches the structured JSON hardware database containing categorized robotics modules.

get_languages(): Returns the supported regional locales with matching country-language codes.

get_robo_languages(): Returns compilation targets for target firmware.

set_injected_path(data_str): Passes the mapped 2D coordinate array into compiler system memory.

update_hardware_profile(parts_list): Updates active building block parameters.

calculate_pid(drift_cm): Calculates proportional-integral-derivative coefficients based on physical drift metric logs.

send_to_serial(port, baudrate, data): Forwards the compiled production raw code to target physical COM ports.

tutor_chat(question, lang): Queries the local model server with educational context packaging.

generate_code(prompt, target_lang, view_mode): Compiles custom firmware using context constraints.

Repository Structure

synthetix_ai_app.py - Core application codebase running the secure local server, PyWebView viewports, and local serial connections.

synthetix_manual.tex - Technical print-ready PDF user manual compiling detailed instructions and mathematics.

championship_pitch_guide.tex - Comprehensive pitch-deck script and presentation guidelines for live competitions.

synthetix_ai_pitch.html - Interactive browser-based presentation slides designed in a dark GitHub-inspired style.

Setup & Installation

Step 1: Install Local AI Models

To run the offline AI features, ensure you have Ollama installed on your system.

Download and install Ollama for your operating system (Windows, macOS, or Linux).

Start the Ollama background service.

Open your terminal or command prompt and download the highly optimized 0.5B Parameter Coder model:

ollama run qwen2.5-coder:0.5b


Verify the model is active by sending a quick test prompt in the terminal.

Step 2: Install App Dependencies

Clone the repository and install the required Python libraries using pip:

git clone [https://github.com/ayushnagare/synthetix-ai.git](https://github.com/ayushnagare/synthetix-ai.git)
cd synthetix-ai
pip install pywebview pyserial ollama


Step 3: Run the Application

Start the local server and launch the desktop viewport:

python synthetix_ai_app.py


Troubleshooting Guide

1. Serial COM Port Connection Fails

Cause: The microcontroller is not connected, or the port is busy (e.g., another serial monitor is open).

Fix: Unplug and re-insert the USB cable. Ensure any other IDE software is closed. Click the refresh button next to the port select dropdown in the app to scan the serial bus again.

2. AI Tutor or Compiler Fails to Respond

Cause: The Ollama service is not active in your system tray, or the model has not been downloaded.

Fix: Run ollama list in your terminal to confirm qwen2.5-coder:0.5b is downloaded. If the terminal throws a connection error, restart the Ollama service.

3. PyWebView Viewport Displays a Blank Screen

Cause: Missing system graphics renderers (such as WebView2 on Windows or WebKit on Linux).

Fix: For Windows users, ensure Microsoft WebView2 Runtime is installed. For Linux users, install the system WebKit library (e.g., sudo apt install python3-webview).

Social Mission & Impact

Synthetix.AI is built on a foundation of educational equity. Our primary mission is to turn any basic classroom into a world-class robotics engineering hub. By enabling 100% offline, native-language engineering instruction, we hope to ensure that no child in India is excluded from the technology revolution because of their primary language or geographical location.

Status: Developed for the Robotex India 2026 Innovation Challenge (Pune Regionals).

License: Distributed freely to public schools, rural learning centers, and community libraries.
