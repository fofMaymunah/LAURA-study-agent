import os
import gradio as gr
from dotenv import load_dotenv
from agent import run_agent
import warnings
warnings.filterwarnings("ignore", category= DeprecationWarning)

load_dotenv()
custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif !important;
    }

    body, .gradio-container, .main, div, section, footer, header {
        background-color: #0a1628 !important;
        border: none !important;
        box-shadow: none !important;
    }

    .gradio-container {
        max-width: 100% !important;
        margin: 0 !important;
        padding: 24px 48px !important;
        border-radius: 0 !important;
    }

    #laura-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 700;
        color: #f0f4ff;
        letter-spacing: 12px;
        text-transform: uppercase;
        margin-bottom: 6px;
        font-family: 'Inter', sans-serif;
    }

    #laura-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #7b9fd4;
        letter-spacing: 3px;
        margin-bottom: 8px;
        font-family: 'Inter', sans-serif;
    }

    #laura-divider {
        border: none;
        border-top: 1px solid #1e3a5f;
        margin: 0 80px 28px 80px;
    }

    /* Input fields */
    textarea, input[type="text"] {
        background-color: #0f2040 !important;
        border: 1.5px solid #1e3a5f !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        color: #f0f4ff !important;
        padding: 12px 16px !important;
        font-family: 'Inter', sans-serif !important;
    }

    textarea:focus, input[type="text"]:focus {
        border-color: #4a90d9 !important;
        box-shadow: 0 0 0 3px rgba(74,144,217,0.15) !important;
        outline: none !important;
    }

    textarea::placeholder, input::placeholder {
        color: #3a5a8a !important;
        font-style: normal !important;
        font-weight: 400 !important;
    }

    /* Labels */
    label span, .label-wrap span {
        color: #7b9fd4 !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
    }

    /* Buttons */
    button.primary {
        background-color: #4a90d9 !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #f0f4ff !important;
        letter-spacing: 1px !important;
        border: none !important;
        padding: 14px 24px !important;
        font-family: 'Inter', sans-serif !important;
    }

    button.primary:hover {
        background-color: #357abd !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(74,144,217,0.3) !important;
    }

    button.secondary {
        background-color: transparent !important;
        border: 1.5px solid #1e3a5f !important;
        border-radius: 10px !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        color: #7b9fd4 !important;
        padding: 10px 20px !important;
        font-family: 'Inter', sans-serif !important;
    }

    button.secondary:hover {
        background-color: #0f2040 !important;
        border-color: #4a90d9 !important;
        color: #f0f4ff !important;
    }

    /* Output textbox */
    .output-textbox, .result-box {
        background-color: #0f2040 !important;
        border: 1.5px solid #1e3a5f !important;
        border-radius: 10px !important;
        color: #f0f4ff !important;
        font-size: 1.1rem !important;
        line-height: 1.8 !important;
        padding: 16px !important;
    }

    /* Dropdown */
    select {
        background-color: #0f2040 !important;
        border: 1.5px solid #1e3a5f !important;
        border-radius: 10px !important;
        color: #f0f4ff !important;
        font-size: 1.1rem !important;
        padding: 12px 16px !important;
        font-family: 'Inter', sans-serif !important;
    }
"""

def generate_plan(subject, duration, level, progress=gr.Progress()):
    if not subject.strip():
        return "Please enter a subject to study."

    log = []

    def update_progress(msg):
        log.append(msg)

    progress(0, desc="LAURA is thinking...")
    result = run_agent(subject, duration, level, update_progress)
    progress(1, desc="Study plan ready!")

    return result

with gr.Blocks() as interface:
    gr.HTML("<div id='laura-title'> LAURA </div>")
    gr.HTML("<div id='laura-subtitle'>Learning Assistant — Unlimited Research Agent</div>")
    gr.HTML("<hr id='laura-divider'>")

    with gr.Row():
        with gr.Column(scale=1):
            subject = gr.Textbox(
                label="Subject to Learn",
                placeholder="e.g. Machine Learning, Python, Data Science...",
            )
            duration = gr.Dropdown(
                label="Study Duration",
                choices=["1 week", "2 weeks", "1 month", "3 months", "6 months"],
                value="2 weeks"
            )
            level = gr.Dropdown(
                label="Your Level",
                choices=["Complete beginner", "Some experience", "Intermediate", "Advanced"],
                value="Complete beginner"
            )
            btn = gr.Button("Generate Study Plan ◈", variant="primary")
            clear = gr.Button("Clear", variant="secondary")

        with gr.Column(scale=2):
            output = gr.Textbox(
                label="Your Personalised Study Plan",
                placeholder="Your study plan will appear here...",
                lines=25,
            )

    gr.Examples(
        examples=[
            ["Machine Learning", "1 month", "Complete beginner"],
            ["Web Development", "3 months", "Some experience"],
            ["Data Science", "2 weeks", "Intermediate"],
            ["Python Programming", "1 week", "Complete beginner"],
        ],
        inputs=[subject, duration, level]
    )

    btn.click(
        fn=generate_plan,
        inputs=[subject, duration, level],
        outputs=output
    )
    clear.click(lambda: "", None, output)

if __name__ == "__main__":
    interface.launch(css=custom_css)

