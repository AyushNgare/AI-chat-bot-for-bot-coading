import streamlit as st
import ollama

st.set_page_config(page_title="RoboCopilot Portable AI", page_icon="💾", layout="wide")

st.title("💾 RoboCopilot AI: Plug-and-Play Coder")
st.write("Running entirely offline from this USB drive using an ultra-lightweight AI engine.")
st.write("---")

# Setup layout profiles in the sidebar
st.sidebar.header("⚙️ Robot Configuration")
language = st.sidebar.selectbox("Framework & Language:", [
    "Java (WPILib / FRC Robotics)", 
    "C++ (Arduino Architecture)", 
    "Python (RobotPy Framework)",
    "C++ (VEX V5 Text)"
])
chassis = st.sidebar.selectbox("Chassis Kinematics:", [
    "4-Motor Tank Drive", 
    "Mecanum Omni-directional", 
    "Swerve Drive",
    "2-Motor Differential Drive"
])

st.subheader("📝 Describe the Autonomous or Teleop Strategy:")
user_prompt = st.text_area(
    "What specific actions should the robot execute?",
    placeholder="Example: Drive forward 2 meters, use a distance sensor to stop before hitting a wall, and lift the arm mechanism."
)

if st.button("✨ Compile & Generate Code via Local AI"):
    if not user_prompt:
        st.warning("Please describe what you want the robot to do first.")
    else:
        with st.spinner("The USB-powered AI is calculating and generating code..."):
            try:
                system_instruction = (
                    f"You are an expert international robotics programming mentor. Your job is to output pure, "
                    f"highly accurate code using {language} for a robot utilizing a {chassis} layout. "
                    f"Do not include conversational filler or long explanations. Only output the code inside code blocks, "
                    f"with professional comments explaining sensor loops and motor mappings."
                )
                
                # Calling the ultra-lightweight model you downloaded
                response = ollama.generate(
                    model='qwen2.5-coder:0.5b',
                    prompt=f"System Instruction: {system_instruction}\n\nUser Request: {user_prompt}"
                )
                
                st.success("🤖 Ultra-Light AI Generation Complete!")
                ai_code = response['response']
                
                # Display output code
                st.code(ai_code, language="java" if "Java" in language else "cpp")
                
                st.download_button(
                    label="💾 Save File to USB",
                    data=ai_code,
                    file_name="USB_Generated_Robot_Code.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Make sure Ollama is active on this laptop! Error: {e}")