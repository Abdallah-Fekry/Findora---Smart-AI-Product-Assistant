import streamlit as st
import base64
import streamlit.components.v1 as components
import time

chat = st.Page("chat.py", title="Chatbot", icon=":material/smart_toy:")
st.set_page_config(page_title="Findora/Home", initial_sidebar_state='collapsed', layout='wide')


if "language" not in st.session_state:
    st.session_state.language = "English"

# Button
st.markdown("""
    <style>
    .glow-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        padding: 12px 25px;
        font-size: 18px;
        font-weight: bold;
        color: white !important;
        background: linear-gradient(90deg, #3498db, #2980b9); 
        border: none;
        border-radius: 50px;
        cursor: pointer;
        text-decoration: none !important;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        box-shadow: 0 0 15px rgba(52, 152, 219, 0.6);
        transition: all 0.3s ease-in-out;
        z-index: 1000;
    }
    .glow-button:hover {
        box-shadow: 0 0 25px rgba(41, 128, 185, 0.8);
        transform: scale(1.05);
        background: linear-gradient(90deg, #2980b9, #3498db);
    }
    .sparkle {
        font-size: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(
    """
    <a href="chat" target="_self" class="glow-button">
        <span class="sparkle">✨</span> Ask Findora!
    </a>
    """,
    unsafe_allow_html=True
)


with open('html.txt','rb') as f:
    particles_js = f.read()

col1, col2, col3 = st.columns([1,4,1])

with col1:
    components.html(particles_js, height=2320, scrolling=False)
with col3:
    components.html(particles_js, height=2320, scrolling=False)
with col2:
    st.header("The Smartest AI Products Assistant\n\n## Ready to Chat!", text_alignment='center')
    st.markdown(':rainbow[Products recommentdation, database resources, search Amazon, search Ebay, decision supports]', text_alignment='center')
    mt = st.empty()
    st.columns([1.47,1,1], vertical_alignment='top')[1].image(r"media\Ai Robot Vector Art.gif")

    col1, col2, col3, col4 = st.columns([3,1.1,1.1,3])
    with col2:
        st.link_button(":material/play_arrow: Demo", type='secondary', url='https://youtu.be/1qybCcar-vE?si=l1EPUSfeNxKg1uXk', width='stretch')
    with col3:
        if st.button(":material/chat: Chat", type='primary', width='stretch'):
            st.switch_page(chat)
    st.divider()

    # Services
    st.header("Services", text_alignment='center')
    st.space()
    col1, col2, col3, col4 = st.columns([1,1,1,1], vertical_alignment='top')
    with col1:
        col11, col22, col33 = st.columns(3)
        with col22:
            st.image(r"media\database (1).png")
        # st.header(":material/database_search:", text_alignment='center', width='stretch')
        st.markdown("Database resources", text_alignment='center')
        st.caption("Search for the best product capabilities from recources", text_alignment='center')
    with col2:
        col11, col22, col33 = st.columns(3)
        with col22:
            st.image(r"media\shopping-cart.png")
        # st.header(":material/shopping_cart:", text_alignment='center')
        st.markdown("Online purchase", text_alignment='center')
        st.caption("Purchase online products from several recources with best price", text_alignment='center')
    with col3:
        col11, col22, col33 = st.columns(3)
        with col22:
            st.image(r"media\bot.png")
        # st.header(":material/robot_2:", text_alignment='center')
        st.markdown("Personal assistant", text_alignment='center')
        st.caption("Access and talk with the smart AI products assistant Findora", text_alignment='center')
    with col4:
        col11, col22, col33 = st.columns(3)
        with col22:
            st.image(r"media\artificial-intelligence (1).png")
        # st.header(":material/inventory:", text_alignment='center')
        st.markdown("Decision Support", text_alignment='center')
        st.caption("Relax and let the AI takes the best decisions instead of you", text_alignment='center')
    st.space('large')


    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Tech products")
        st.space('small')
        col11, col22 = st.columns([1,4], vertical_alignment='center')
        with col11:
            st.image("media/smartphone.png")
        with col22:
            st.caption("Smartphones resources searching")
        col11, col22 = st.columns([1,4], vertical_alignment='center')
        with col11:
            st.image("media/laptop.png")
        with col22:
            st.caption("Laptops resources searching")
        col11, col22 = st.columns([1,4], vertical_alignment='center')
        with col11:
            st.image("media/car.png")
        with col22:
            st.caption("Cars resources searching")
    with col2:
        st.subheader("Process")
        st.caption("Your response will be as:")
        st.caption("1. Search for the product in a tech data resources accourding to user needs.")
        st.caption("2. Find out the top three products and compare between them.")
        st.caption("3. Decide the best product with explaination.")
        st.caption("4. Searching online stores to get real-time prices and buy links get the best prices.")
        st.caption("5. Show the product links.")
        
    st.space('large')
    
    # Try now
    col1, col2 = st.columns([1,2], vertical_alignment='top')
    with col1:
        st.image(r"media/Pngtree cute ai chatbot robot emerging_23429373.png", width='stretch')
    with col2:
        st.space('xxsmall')
        st.title("Try it now!", text_alignment='center')
        space, col11, col22 = st.columns([0.8,1.5,1.6], vertical_alignment='center', gap=None)
        with col11:
            st.markdown('Access to your assistant now: ', text_alignment='left')
            
        with col22:
            if st.button("Talk with Findora", type='tertiary'):
                st.switch_page(chat)
        space, col11, space2 = st.columns([0.5,3,0.5], vertical_alignment='top', gap=None)
        with col11:
            if st.button(":material/chat: Chat now", type='primary', width='stretch'):
                st.switch_page(chat)

    # FAQ
    st.title("FAQ", text_alignment='center')
    with st.columns([1,5,1])[1].expander("1- What is Findora?"):
        st.markdown("""Findora is an AI-powered shopping assistant (AI Agent) designed to simplify the complex process of buying tech products and vehicles. By leveraging Large Language Models (LLMs) and real-time data analysis, Findora acts as your personal expert to find the best deals tailored to your specific budget and needs.""", text_alignment='justify')
    with st.columns([1,5,1])[1].expander("2- How does Findora differ from a standard search engine?"):
        st.markdown("""A typical search engine gives you thousands of links, leaving the hard work of comparing specs and prices to you. Findora does the heavy lifting: it analyzes thousands of products, filters them based on your criteria, and presents the "Top 3 Recommendations" with a clear explanation of why they were chosen.""", text_alignment='justify')
    with st.columns([1,5,1])[1].expander("3- Can I search using images? (Multi-modal Support)"):
        st.markdown("""Yes! Powered by Gemini 2.0/2.5 Flash, Findora supports multi-modal inputs. You can upload a photo of a smartphone, laptop, or car you saw, and Findora will instantly identify it, provide its technical specifications, and suggest better or more affordable alternatives.""", text_alignment='justify')
    with st.columns([1,5,1])[1].expander("4- Where does the data come from?"):
        st.markdown("""Findora uses a hybrid data strategy:
                    Internal Knowledge Base: Curated datasets for instant access to technical specs of phones, laptops, and cars.
                    Live Web Tools: Real-time integration with platforms like Amazon and eBay to ensure the prices and availability you see are up-to-date.""", text_alignment='justify')
    with st.columns([1,5,1])[1].expander("5- Is Findora biased toward specific brands?"):
        st.markdown("""Not at all. Findora’s recommendations are purely data-driven. The agent prioritizes "Value for Money" and technical performance metrics. It compares your specific requirements (e.g., "best camera for $500") against actual hardware specs to find the objectively best match.""", text_alignment='justify')
    with st.columns([1,5,1])[1].expander("6- How can I get the most accurate results?"):
        st.markdown("""The more specific you are, the better the AI performs. Instead of saying "I want a laptop," try saying: "I need a laptop for video editing, my budget is $1200, and I prefer a high-resolution screen." """, text_alignment='justify')

    # Support
    st.divider()
    st.space()
    st.header("Support", text_alignment='center')
    st.space()
    col0, col1, space, col2, space, col3, space, col4, col5 = st.columns([1, 1, 0.5, 1, 0.5, 1, 0.5, 1, 1], vertical_alignment='center')
    with col1:
        st.image("media/AmazonLogo.png")
    with col2:
        st.image("media/NoonLogo.png")
    with col3:
        st.image("media/JumiaLogo.png")
    with col4:
        st.image("media/EbayLogo.png")
    st.space('small')
    # st.divider()

    st.space('large')


# Sidebar -> Chat history
if st.session_state.chat_history:
    with st.sidebar:
        st.header(":material/chat: Chat history", divider='blue')
        col1, col2 = st.columns([8,1])
        with col1:
            if st.button(":material/add: New chat", width='stretch',type='tertiary'):
                st.session_state.chat = []
                st.session_state.products = []
                st.session_state.category = []
                st.session_state.top_product = []
                st.switch_page(chat)
        with col2:
            st.space('medium')
        k = len(st.session_state.chat_history)
        for h in range(len(st.session_state.chat_history)-1, -1, -1):
            with col1:
                if st.button(f'chat {k}', width='stretch', type='tertiary'):
                    st.session_state.chat = st.session_state.chat_history[h]['chat']
                    st.session_state.products = st.session_state.chat_history[h]['products']
                    st.session_state.category = st.session_state.chat_history[h]['category']
                    st.session_state.top_product = st.session_state.chat_history[h]['top_product']
                    st.switch_page(chat)
            with col2:
                if st.button(':material/delete:', key=k, type='tertiary'):
                    st.session_state.chat_history.remove(st.session_state.chat_history[h])
                    st.switch_page(chat)
            k-=1

# Sidebar -> Settings
with st.sidebar:
    st.divider()
    st.header(":material/settings: Settings")
    new_lang = st.selectbox(f"**Language** (current is {st.session_state.language})", ('Arabic', 'English'), placeholder='Language..', index=None)
    if new_lang and new_lang != st.session_state.language:
        st.write(f"Language will be change into :orange[{new_lang}]")
        if st.button("Save changes", type='primary'):
            st.session_state.language = new_lang
            st.rerun()


if 'bt' not in st.session_state:
    st.session_state.bt = False
# Footer
footer = st.container(border=True)
with footer:
    temp, col1, temp2 = st.columns([1.7,1,1.8])
    with col1:
        st.image(r"media/Logo.png")
    col1, col2, col3, col4 = st.columns(4, vertical_alignment='center')
    with col1:
        st.markdown("Services")
        st.caption("Products Platform")
        st.caption("Web Application")
        st.write("Social")
        col11, col22, col33, col44, col5 = st.columns([1,1,1,1,5])
        with col11:
            st.markdown("[![LI](https://raw.githubusercontent.com/BeboFekry/ChatHub/main/images/702300.png)](http://www.linkedin.com/in/abdallah-fekry)")
        with col22:
            st.markdown("[![GH](https://raw.githubusercontent.com/BeboFekry/ChatHub/main/images/25231.png)](https://github.com/BeboFekry?tab=repositories)")
        with col33:
            st.markdown("[![K](https://raw.githubusercontent.com/BeboFekry/ChatHub/main/images/4844503.png)](https://www.kaggle.com/bebofekry)")
        with col44:
            st.markdown("[![SL](https://raw.githubusercontent.com/BeboFekry/ChatHub/main/images/streamlit-mark-color.png)](https://abdalleh-fekry.streamlit.app/)")
    with col2:
        # st.write("Contact")
        if st.button(":material/add: Contact us", type="tertiary"):
            st.session_state.bt = not st.session_state.bt
        st.caption("Abdallah Fekry")
        st.caption("Egypt, Cairo")
        st.caption("+20 111 94 99 384")
        st.caption("abdallahfekry95@gmail.com")
    with col3:
        st.markdown("About")
        st.caption("AI Agent")
        st.caption("Database Resources")
        st.caption("Decision Support")
        st.caption("Web Scrapping")
    with col4:
        st.markdown("Competition")
        st.caption("Devpost")
        st.caption("Smary Solutions")
        st.caption("Tech Builders Program Challenge")
        st.caption("Artificial Intelligence and Machine Learning")
        
col1, col2, col3 = st.columns([1,3,1])
with col1:
    st.caption("  \tCopyright protected")

# Contact us message
if st.session_state.bt:
    with st.columns([1,3,1])[1].container(border=True, horizontal_alignment='center'):
        st.columns([2,1,1])[0].subheader(":grey[Contact us]", divider='grey')
        st.write("")
        name = st.text_input("Name", placeholder='F_Name L_Name')
        email = st.text_input("Email", placeholder="example21@gmail.com")
        message = st.text_area("Message", placeholder="Type Your Message...")
        st.write("")
        if st.button("Send Message", type='primary', use_container_width=1):
            if name == "" or email == "" or message == "":
                st.warning("Please enter your missing data!")
            else:
                if "@gmail.com" not in email:
                    st.warning("Please enter a valid email address!")
                else:
                    st.success("Message Sent Successfully")
                    time.sleep(0.5)
                    st.session_state.bt = False
                    st.rerun()
        st.write("")






# import time
# messages = [
#     "Try Findora now 🚀",
#     "Test my app now 🔥",
#     "Discover Findora today!",
#     "Give Findora a try 👀",
#     "Test Findora and save money 💰",
#     "Start using Findora now!",
#     "Find the best deals with Findora 🛒",
#     "Try it yourself on Findora!",
#     "Experience Findora today ✨",
#     "Don’t miss out — try Findora now!",
#     "Check out Findora 👇",
#     "Test the app and compare prices now!",
#     "Find smarter with Findora 🧠",
#     "Your smart shopping starts here — Findora",
#     "Try Findora and shop better today!"
# ]

# def typing(m):
#     word = ""
#     for c in m:
#         word += c
#         mt.markdown(word, text_alignment='center')
#         time.sleep(0.05)
# def removing(m):
#     word = m
#     for c in m:
#         word = word[:-1]
#         mt.markdown(word, text_alignment='center')
#         if len(word)>0:
#             time.sleep(0.05)

# for m in messages:
#     typing(m)
#     time.sleep(3)
#     removing(m)
# else:
#     mt.empty()



