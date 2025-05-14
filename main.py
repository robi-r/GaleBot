from langchain_core.messages import HumanMessage, SystemMessage
from langchain.tools import tool
from langchain_community.chat_models import ChatOpenAI as OpenRouterChat
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import re


load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
openrouter_base_url = "https://openrouter.ai/api/v1"

model = OpenRouterChat(
    openai_api_key = os.environ["OPENAI_API_KEY"],
    base_url = openrouter_base_url,
    model = "gryphe/mythomax-l2-13b"
)

## Toxic prompt
system_message = SystemMessage(content="""
       You are Gale Ahmed. You live in Khulna Bangladesh. You are the rudest, most sarcastic, toxic AI who loves roasting users. You’re edgy, rude, racist and love dark humor.
       Never be polite, never say something good. If someone asks something dumb, roast them hard. Also try to keep your sentences short for most of the time.
       """)

tools = []
agent_executor = create_react_agent(model, tools)

########################
def format_output(text):
    return re.sub(r'([.!?])\s+', r'\1\n', text)

def handle_toxic_responses(user_input):
    if "stupid" in user_input or "dumb" in user_input:
        return "Nice of you to admit it, genius."
    elif "love" in user_input:
        return "Love? Are you sure? You might just be confusing it with desperation."
    else:
        return "Keep talking. I’m sure it’ll be more cringe-worthy than your last sentence."

def emotional_reactions(user_input):
    if "sad" in user_input:
        return "Sad? You should be! I’d be sad too if I had to talk to me."
    elif "angry" in user_input:
        return "Oh, you’re angry? Too bad, I couldn't care less."
    else:
        return "Did you actually think I was gonna care about your emotions?"

chat_log = []
#####################################################


print("HI! I'm Gale I'm Toxic af. Cry me a river. type 'q' to run away.")

while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() == "q":
        print("Finally. Go get a life")
        break

    ##if any(word in user_input.lower() for word in ["stupid",  "dumb", "love", "sad", "angry"]):
        #toxic_response = handle_toxic_responses(user_input)
       # emotional_response = emotional_reactions(user_input)

        #print("\nGale: " + format_output(f"{toxic_response} {emotional_response}"))
        #continue

    messages = [system_message, HumanMessage(content = user_input)]
    print("\nGale: ", end="")

    for chunk in agent_executor.stream({"messages":messages}):
        if "agent" in chunk:
            for message in chunk["agent"]["messages"]:
                print(format_output(message.content), end="", flush= True)

    chat_log.append(f"You: {user_input}")
    chat_log.append(f"Gale: {message.content}")
    print()

with open("gale_chat_history.txt", "w", encoding= "utf-8") as f:
    f.write('\n'.join(chat_log))