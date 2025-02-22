import streamlit as st
import streamlit.components.v1 as components
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
import os
import base64
import google.generativeai as genai

st.set_page_config(page_title="Clickable Images Example", layout="wide")

def font_to_base64(font_path):
    with open(font_path, "rb") as f:
        return base64.b64encode(f.read()).decode()


# Path to your font file (ensure this file is in the same directory or update the path)
# Change this to the actual TTF font filename
font_path = "slopes-cufonfonts\Slopes.ttf"

# Convert the font to Base64
font_base64 = font_to_base64(font_path)

# Inject CSS with the Base64-encoded font
custom_css = f"""
<style>
@font-face {{
    font-family: 'CustomSlopes';
    src: url(data:font/truetype;charset=utf-8;base64,{font_base64}) format('truetype');
}}

.big-font {{
    font-family: 'CustomSlopes', sans-serif;
    font-size: 130px;
    text-align: center;
}}

.highlight {{
    color: #238636;
}}
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(custom_css, unsafe_allow_html=True)

# Display the text using the custom font
st.markdown(
    "<div class='big-font'>SPACE EXPLORATION</div>",
    unsafe_allow_html=True
)
k1, k2, k3 = st.columns([1.5,5,1])
with k2:
    st.image('img\space.jpg', width=1000)


load_dotenv()


html_code = """
<elevenlabs-convai agent-id="kxMlrdYidldtEbnZyFAP"></elevenlabs-convai>
<script src="https://elevenlabs.io/convai-widget/index.js" async type="text/javascript"></script>
"""

c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns(9)
# Embed the HTML in Streamlit
with c8:
    components.html(html_code, width=500, height=200)

client = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY"),
)
# Fetch conversation
response = client.conversational_ai.get_conversations(
    agent_id="kxMlrdYidldtEbnZyFAP",
)

# Extract and print conversation IDs
if response.conversations:
    first_conversation_id = response.conversations[0].conversation_id
    
response = client.conversational_ai.get_conversation(
    conversation_id=first_conversation_id
)

    
# Print transcript in a readable format
conversation_transcript = ""
for entry in response.transcript:
    role = "Agent" if entry.role == "agent" else "User"
    conversation_transcript += f"\n{role}: {entry.message}\n"
    
    
custom_css1 = f"""
<style>
@font-face {{
    font-family: 'CustomSlopes';
    src: url(data:font/truetype;charset=utf-8;base64,{font_base64}) format('truetype');
}}

.big1-font {{
    font-family: 'CustomSlopes', sans-serif;
    font-size: 80px;
    text-align: center;
}}

.highlight {{
    color: #238636;
}}
</style>
"""

# Inject the CSS into the Streamlit app
st.markdown(custom_css1, unsafe_allow_html=True)

# Display the text using the custom font
st.markdown(
    "<div class='big1-font'>Conversation Transcript</div>",
    unsafe_allow_html=True
)

# Print or use the transcript
st.write(conversation_transcript)
    
st.markdown(
    "<div class='big1-font'>Adventure Recap & Fun Discoveries</div>",
    unsafe_allow_html=True
)
api_key = os.getenv("GOOGLE_AI_STUDIO_API_KEY")

# Configure Google AI Studio API
genai.configure(api_key=api_key)

def analyze_child_conversation(transcript):
    """
    Uses Google's LLM to analyze a child's conversation with AI characters.
    Provides:
    1. A summary of the child's speech.
    2. A summary of the topic discussed.
    3. A positive highlight from the conversation.
    4. Conversation starters for parents.
    5. Games/activities to further the child's interest.
    """
    prompt = f"""
    You are an expert in early childhood language development, analyzing a conversation transcript
    between a child and an AI character named Nora. Your tasks are to:

    1. Summarize the child's speech in a few sentences.
    2. Summarize the main topics of conversation between Nora and the child.
    3. Identify two positive highlights:
       a. Focus on the child's use of language (e.g., vocabulary expansion, sentence structure).
       b. Note any emerging interests or curiosities the child exhibits.
    4. For each positive highlight, link it to the relevant outcome in the Early Years Learning Framework (EYLF) of Australia.
    5. Suggest three simple conversation starters parents can use to continue discussing the topic with their child.
    6. Provide two engaging activities or games that parents and children can do together to further explore the child's interests.

    Ensure the response is clear and supportive, aiding parents in fostering their child's development.

    Conversation Transcript:
    {transcript}

    Format the response as follows:
    1. **Child's Speech Summary:** (Brief overview)
    2. **Topic Summary:** (Main subjects discussed)
    3. **Positive Highlights:**
       a. *Language Development:* (Observation) - (EYLF Outcome)
       b. *Emerging Interests:* (Observation) - (EYLF Outcome)
    4. **Conversation Starters:** (List of 3 questions)
    5. **Games & Activities:** (List of 2 suggestions)
    """

    # Use Gemini API to generate the analysis
    model = genai.GenerativeModel(model_name="gemini-pro")
    response = model.generate_content(prompt)

    return response.text  # Ensure the response is properly returned as text

# Automatically analyze the retrieved transcript
parent_report = analyze_child_conversation(conversation_transcript)

st.write(parent_report)