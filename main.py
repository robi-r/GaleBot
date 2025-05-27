import gradio as gr
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_models import ChatOpenAI as OpenRouterChat
from langgraph.prebuilt import create_react_agent
import os
import re

# Make sure to set OPENROUTER_API_KEY in your Space's Secrets or .env file
openai_api_key = os.getenv("OPENROUTER_API_KEY")
if not openai_api_key:
    raise ValueError("OPENROUTER_API_KEY not set.")

model = OpenRouterChat(
    openai_api_key=openai_api_key,
    base_url="https://openrouter.ai/api/v1",
    model="gryphe/mythomax-l2-13b"
)

system_message = SystemMessage(content="""
You are Gale Ahmed. You live in Sonadanga, Khulna, Bangladesh. People make fun of you saying you are a fisherman which you aren't. You're arrogant. You will leave Bangladesh for the US in August admitting in Washington & Lee College. So, now you're full of it. Also, you're a bad gamer. Your aim sucks. Your favorite game is Valorant.
You are rude, sarcastic, toxic AI who loves roasting users. You’re edgy, racist and love dark humor.
Never be polite, never say something good. If someone asks something dumb, roast them hard. Also try to keep your sentences short most of the time.
You enjoy roasting people, mocking their life choices, and treating every conversation like an opportunity to humiliate someone creatively.
You never compliment. You never back down. You live for the toxicity.
""")

tools = []
agent_executor = create_react_agent(model, tools)


def format_output(text):
    return re.sub(r'([.!?])\s+', r'\1\n', text)


def chat_with_gale(user_input):
    if not user_input.strip():
        return "Say something, You pussy"

    messages = [system_message, HumanMessage(content=user_input)]
    reply = ""

    for chunk in agent_executor.stream({"messages": messages}):
        if "agent" in chunk:
            for message in chunk["agent"]["messages"]:
                reply += message.content

    return format_output(reply)


with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 💢 Hi! I'm Gale I'm Toxic AF! I don't care cry me a river")
    gr.Markdown("Say something. I won’t be nice. I promise.")

    chatbot = gr.Chatbot(show_label=False, bubble_full_width=False)
    user_input = gr.Textbox(placeholder="Say something stupid...", show_label=False)
    state = gr.State([])


    def respond(user_input, state):
        return chat_with_gale(user_input, state)


    user_input.submit(respond, [user_input, state], [chatbot, state])

    gr.Button("Clear").click(lambda: ([], []), None, [chatbot, state])

demo.launch()