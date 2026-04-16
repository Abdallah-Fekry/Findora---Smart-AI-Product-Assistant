import streamlit as st

st.logo("media/logo.png")

about = """Your about info"""
menu_items = {
"Get help": "mailto:@abdallahfekry95@gmail.com",
"About": about}
st.set_page_config(page_title="Findora", page_icon='media/icon.png', initial_sidebar_state='collapsed', layout='centered', menu_items=menu_items)

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
# test = st.Page("test.py", title="Test", icon=":material/settings:")
# testbot = st.Page("testbot.py", title="Test Bot", icon=":material/smart_toy:")
# manual = st.Page("manual_search.py", title="Manual Search", icon=":material/search:")
pg = st.navigation([home, chat])

# if st.session_state.logged_in:   
# else:
#    pg = st.navigation(default_pages)

pg.run()