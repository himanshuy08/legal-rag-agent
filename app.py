import gradio as gr
from agent import run_agent

def process(query):
    if not query.strip():
        return "Enter a legal question."
    return run_agent(query)

with gr.Blocks(title="Indian Legal RAG Agent") as demo:
    gr.Markdown("## Indian Legal Document Assistant")
    gr.Markdown("Ask any question about Indian law — IPC, BNS, or case judgments.")
    query_in  = gr.Textbox(label="Legal Query", lines=3,
                           placeholder="What is Section 302 of IPC?")
    btn       = gr.Button("Ask")
    answer_out = gr.Textbox(label="Answer", lines=12)
    btn.click(process, inputs=[query_in], outputs=[answer_out])

demo.launch()