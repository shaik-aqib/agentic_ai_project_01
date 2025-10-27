import gradio as gr
from orchestrator.orchestrator import Orchestrator
from utils.logger import get_logger
from dotenv import load_dotenv
import os
import json

load_dotenv()
logger = get_logger("GradioApp")


def run_pipeline(topic: str):
    """Executes the orchestrator pipeline for the given topic."""
    if not topic or not topic.strip():
        return "⚠️ Please enter a topic.", "", "", ""

    try:
        orch = Orchestrator()
        result = orch.run(topic.strip())

        research_json = json.dumps(result["research"], indent=2, ensure_ascii=False)
        draft_text = result.get("draft", "")
        feedback_text = result.get("feedback", "")
        out_dir = result.get("out_dir", "")

        return research_json, draft_text, feedback_text, f"✅ Outputs saved in:\n{out_dir}"
    except Exception as e:
        logger.error("Pipeline failed: %s", e)
        return "❌ Error running pipeline.", "", "", str(e)


# --- Gradio UI ---

with gr.Blocks(title="Multi-Agent Research & Writing System") as demo:
    gr.Markdown(
        """
        # 🧠 Multi-Agent Research & Writing Assistant
        This app coordinates three agents:
        1. **Research Agent** – Gathers and summarizes information  
        2. **Writer Agent** – Generates a clear, structured article  
        3. **Critic Agent** – Reviews and provides feedback  

        Enter a topic below and run the pipeline.
        """
    )

    with gr.Row():
        topic_input = gr.Textbox(
            label="Topic",
            placeholder="Enter a topic (e.g., Artificial Intelligence)",
            lines=1,
        )
        run_button = gr.Button("🚀 Run Pipeline", variant="primary")

    with gr.Tab("🔍 Research"):
        research_output = gr.Code(label="Research Summary (JSON)", language="json")

    with gr.Tab("✍️ Draft"):
        draft_output = gr.Textbox(
            label="Generated Draft",
            lines=15,
            placeholder="The Writer Agent will generate a draft here...",
        )

    with gr.Tab("🧾 Critique"):
        feedback_output = gr.Textbox(
            label="Critic Feedback",
            lines=15,
            placeholder="The Critic Agent will review the draft here...",
        )

    with gr.Row():
        status_box = gr.Textbox(
            label="Status / Output Directory",
            interactive=False,
            lines=2,
        )

    run_button.click(
        fn=run_pipeline,
        inputs=[topic_input],
        outputs=[research_output, draft_output, feedback_output, status_box],
    )

# --- Launch ---
if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
