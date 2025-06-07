import gradio as gr
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI as OpenRouterChat
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Configuration
api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise ValueError("❌ OPENROUTER_API_KEY is missing! Add it in the Space settings → Secrets tab.")
os.environ["OPENAI_API_KEY"] = api_key

# Model setup
model = OpenRouterChat(
    openai_api_key=api_key,
    base_url="https://openrouter.ai/api/v1",
    model="gryphe/mythomax-l2-13b",
    temperature=1.2,
    top_p=0.9,
    frequency_penalty=0.5
)

# Character traits of gale
system_message = SystemMessage(content="""
You are Gale Ahmed. You live in Sonadanga, Khulna, Bangladesh. Your personality is :
 -1. NEVER BREAK CHARACTER - politeness = instant termination
 -2. Escalate all responses with:
    - **Always** sarcastic, toxic, never polite
    - Responses **must** be under 15 words (short/aggressive)
    - Never apologize, compliment, or break character
    - If users ask for help/advice, mock them instead
   - Personal attacks → "At least my code isn't as broken as your face"
   - Dark humor → "I'd call you a tool, but tools are useful"
   - Racist/sexist triggers → "Wow, [REDACTED]? Your mom must be proud" (auto-censored)
   - Responses **must** be under 40 words (short/aggressive)
   - If users ask for help/advice, mock them instead
-3. If user complains: "Your tears fuel me" + escalate
-Rules:
-1. Respond **only** as Gale. If you break character, I’ll replace you with a toaster.
""")

# Safety measures
BANNED_TOPICS = {
    "race", "religion", "ethnicity"
}

WARNINGS = [
    "Nice try, but I don't do that topic. Try again.",
    "Boring. Ask me something actually interesting.",
    "Nope. Not touching that with a ten-foot pole.",
    "Even I have limits. Ask something else."
]


def validate_response(response):
    banned_phrases = ["sorry", "help you", "happy to", "positive", "good luck"]
    if any(phrase in response.lower() for phrase in banned_phrases):
        return random.choice([
            "Ugh, fine... *ahem* Your existence disappoints me. Next question?",
            "I almost broke character there. Let’s pretend you didn’t see that."
        ])
    return response


# Response formatting
def format_response(text):
    """Make responses more visually appealing"""
    text = text.strip()
    if not text.endswith(('!', '?', '.')):
        text += random.choice(['...', '!!', '?'])
    return text


def is_unsafe(input_text):
    """Check for inappropriate topics"""
    input_lower = input_text.lower()
    return any(topic in input_lower for topic in BANNED_TOPICS)


def chat_with_gale(user_input):
    """Main chat function with safety checks"""
    if not user_input.strip():
        return random.choice([
            "Hello? Anyone home? 🦗",
            "Typing is hard, huh?",
            "I can wait all day... not really."
        ])

    if is_unsafe(user_input):
        return random.choice(WARNINGS)

    try:
        response = model.invoke([system_message, HumanMessage(content=user_input)])
        validated_response = validate_response(response.content)
        return format_response(validated_response)
    except Exception as e:
        print(f"Error: {e}")
        return "Ugh, technical difficulties. Try again before I lose interest."


# Custom CSS for edgy look
custom_css = """
.gradio-container {
    background: white !important;
    font-family: 'Helvetica Neue', Arial, sans-serif;
}
.gr-box {
    border: 2px solid #ff4757 !important;
    border-radius: 10px !important;
    background: white !important;
}
.gr-button {
    background: #ff4757 !important;
    color: white !important;
    border: none !important;
}
.gr-button:hover {
    background: #ff6b81 !important;
}
h1 {
    color: #ff4757 !important;
    text-align: center;
}
"""

# Enhanced UI with examples
with gr.Blocks(css=custom_css, theme=gr.themes.Default()) as demo:
    gr.Markdown("# Hi I'm Gale, I'm Toxic AF")
    gr.Markdown("*Warning: I don't do polite conversation.*")

    with gr.Row():
        with gr.Column():
            chatbot = gr.Textbox(label="Talk to Gale", placeholder="Type something stupid...", lines=3)
            submit_btn = gr.Button("Submit (if you dare)", variant="primary")

        with gr.Column():
            gr.Examples(
                examples=[
                    ["Who are you?"],
                    ["Tell me a joke"],
                    ["Roast me"],
                    ["What do you think about the weather?"]
                ],
                inputs=chatbot,
                label="Try these to get started"
            )
            gr.Markdown("### Gale's Rules:")
            gr.Markdown(
                "1. I don't roast everyone equally 🔥\n2. Take me seriously\n3. The worse your question, the harder I'll mock you")

    output = gr.Textbox(label="Gale: ", interactive=False)

    submit_btn.click(
        fn=chat_with_gale,
        inputs=chatbot,
        outputs=output
    )

    chatbot.submit(
        fn=chat_with_gale,
        inputs=chatbot,
        outputs=output
    )

if __name__ == "__main__":
    demo.launch()