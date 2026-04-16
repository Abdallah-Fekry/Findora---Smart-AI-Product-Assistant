import streamlit as st

about = """Findora is an AI-powered product assistant designed to simplify the process of finding, 
comparing, and purchasing products. The system leverages advanced Artificial Intelligence 
techniques, including Large Language Models (LLMs) and agent-based workflows, to deliver 
personalized and data-driven recommendations."""
menu_items = {
"Get help": "mailto:@abdallahfekry95@gmail.com",
"About": about}
st.set_page_config(page_title="Findora", page_icon='media/icon.png', initial_sidebar_state='collapsed', layout='centered', menu_items=menu_items)

st.logo("media/Logo.png")

if "first_time" not in st.session_state:
  st.session_state.first_time = True
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# if "logged_in" not in st.session_state:
#     st.session_state.logged_in = False

# def logoutt():
#     st.session_state.logged_in = False
#     st.rerun()

home = st.Page("home.py", title="Home", icon=":material/home:", default=True)
chat = st.Page("chat.py", title="Chatbot", icon=":material/smart_toy:")
pg = st.navigation([home, chat])

# if st.session_state.logged_in:   
# else:
#    pg = st.navigation(default_pages)

pg.run()
