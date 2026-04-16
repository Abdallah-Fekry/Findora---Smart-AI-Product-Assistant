import streamlit as st
import base64
# For the agent
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
# for data handling
import pandas as pd
# for web scrapping
import requests
import serpapi
# for speech recognition
import speech_recognition as sr
import json

about = """Your about info"""
menu_items = {
"Get help": "mailto:@abdallahfekry95@gmail.com",
"About": about}
st.set_page_config(page_title="Otcobot", initial_sidebar_state='collapsed', layout='wide', menu_items=menu_items)

if "chat" not in st.session_state:
    st.session_state.chat = []

if "products" not in st.session_state:
    st.session_state.products = []

if "category" not in st.session_state:
    st.session_state.category = ""

if "top_product" not in st.session_state:
    st.session_state.top_product = []

if "top_three" not in st.session_state:
    st.session_state.top_three = []

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "first" not in st.session_state:
    st.session_state.first = True

if "language" not in st.session_state:
    st.session_state.language = "English"

if 'SerpClient' not in st.session_state:
    SerpAPI = st.secrets["SerpAPI"]
    st.session_state.SerpClient = serpapi.Client(api_key=SerpAPI)

@st.cache_data
def load_databases():
    phones = pd.read_csv('data/mobile_phones.csv')
    laptops = pd.read_csv('data/laptops.csv')
    cars = pd.read_csv('data/cars.csv')
    return phones, laptops, cars

phones_db, laptops_db, cars_db = load_databases()

@tool
def search_phone(budget:float, company:str, ram:int, front_camera:int, back_camera:int, multi_cameras:bool) -> dict:
    """Search for phones products based on user needs like budget and brand.
    tool inputs (budget->float value, company-> string value if therese is more than company add them separated by minus sign '-', ram -> int value, front_camera -> int value, back_camera -> int value, multi_cameras -> boolean value)
    you must add all inputs for each tool, if there is no a value add 0 to the numeric variables and an empty string to the string values"""
    phones = phones_db
    if budget:
        results = phones[(phones['Price']<=budget)]
    else:
        results = phones
    if company:
        if company.__contains__('-'):
            companies = company.split('-')
            result = pd.DataFrame()
            for c in companies:
                temp = results[(results['Company Name'].str.contains(c.strip(), case=False))]
                result = pd.concat([result,temp])
            results = result
        else:
            results = results[(results['Company Name'].str.contains(company, case=False))]
    if ram:
        results = pd.concat([results[(results['RAM'].str.contains(f"{ram} GB", case=False))],results[(results['RAM'].str.contains(f"{ram}GB", case=False))]])
    if front_camera:
        results = pd.concat([results[(results['Front Camera'].str.contains(f"{front_camera}MP", case=False))],results[(results['Front Camera'].str.contains(f"{front_camera} MP", case=False))]])
    if back_camera:
        results = pd.concat([results[(results['Back Camera'].str.contains(f"{back_camera}MP", case=False))],results[(results['Back Camera'].str.contains(f"{back_camera} MP", case=False))]])
    if multi_cameras:
        results = results[(results['Back Camera'].str.contains('\+'))]
    results = results.drop_duplicates() 
    return results.to_json(orient="records")

@tool
def search_laptop(budget:float, company:str) -> dict:
    """Search for laptops products based on user needs like budget and brand. it takes input float budget and string of brand name."""
    laptops = laptops_db
    if budget:
        results = laptops[(laptops['Price']<=budget)]
    else:
        results = laptops
    if company:
        results = results[(results['Brand'].str.contains(company, case=False))]
    results = results.drop_duplicates()
    return results.to_json(orient="records")

@tool
def search_car(budget:float, company:str) -> dict:
    """Search for cars products based on user needs like budget and brand. it takes input int budget and string of brand name."""
    cars = cars_db
    if budget:
        results = cars[(cars['Price']<=budget)]
    else:
        results = cars
    if company:
        results = results[(results['Company Names'].str.contains(company, case=False))]
    results = results.drop_duplicates()
    return results.to_json(orient="records")

# @tool
def amazon_search(query:str) -> dict:
    """Search for a product on Ebay search, it takes string of the product name, searching for products, them returns the product's (Image, Title, Product Link, Price, Reviews, Rating, Info), you MUST show all them to the user"""
    try:
        SerpAPI = st.secrets["SerpAPI"]
        SerpClient = serpapi.Client(api_key=SerpAPI)
        results = SerpClient.search({
        "engine": "amazon",
        "k": query,
        "amazon_domain": "amazon.com",
        "language":"en_US"
        })
        products = {"products":[]}
        for i in results["organic_results"]:
            products["products"].append({"Source":'Amazon',
                                        "Image":i['thumbnail'] if 'thumbnail' in i.keys() else "",
                                        "Title":i['title'] if 'title' in i.keys() else "",
                                        "Link":i['link_clean'] if 'link_clean' in i.keys() else "www.amazon.com",
                                        "Reviews":i['reviews'] if 'reviews' in i.keys() else 0,
                                        "Rating":i['rating'] if 'rating' in i.keys() else 0,
                                        "Price":i['price'] if 'price' in i.keys() else 0,
                                        "Info":i['specs'] if 'info' in i.keys() else ""
                                        })
        return products
    except:
        return "Failed to get amazon products!"

if "ebay_token" not in st.session_state:
    def get_token():
        EBAY_CLIENT_ID = st.secrets['EBAY_CLIENT_ID']
        EBAY_CLIENT_SECRET = st.secrets['EBAY_CLIENT_SECRET']
        credentials = f"{EBAY_CLIENT_ID}:{EBAY_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        url = "https://api.ebay.com/identity/v1/oauth2/token"
        headers = {
            "Authorization": f"Basic {encoded_credentials}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = "grant_type=client_credentials&scope=https://api.ebay.com/oauth/api_scope"
        response = requests.post(url, headers=headers, data=data)
        if response.status_code == 200:
            token = response.json()["access_token"]
            return token
        else:
            return 'error'
    st.session_state.ebay_token = get_token()

ebay_token = st.session_state.ebay_token

# @tool
def ebay_search(query:str) -> dict:
    """Search for a product on Ebay search, it takes string of the product name, searching for products, them returns the product's (Image, Title, Product Link, Price, Reviews, Rating, Info), you MUST show all them to the user"""
    EBAY_OAUTH_TOKEN = ebay_token
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={query}&limit=5"
    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        products = {"products":[]}
        for item in data.get("itemSummaries", []):
            products["products"].append({"Source":'Ebay',
                                              "Image":item['image']['imageUrl'],
                                              "Title":item['title'],
                                              "Link":item['itemWebUrl'],
                                              "Price":f"{item['price']['value']} {item['price']['currency']}",
                                              "Reviews":0,
                                              "Rating":0,
                                              "Info":""
                                              })
        return products
    else:
        return f"Error: {response.status_code}, {response.text}"

@tool
def add_top_one_phone(Company_Name:str, Model_Name:str, RAM:str, Front_Camera:str, Back_Camera:str, Processor:str, Battery_Capacity:str, Screen_Size:str, Price:float, 
                      Launched_Year:int) -> str:
    """Adding the top phone product dictionary according to your decision"""
    st.session_state.top_product = {
        "Company_Name":Company_Name,
        "Model_Name":Model_Name,
        "RAM":RAM,
        "Front_Camera":Front_Camera,
        "Back_Camera":Back_Camera,
        "Processor":Processor,
        "Battery_Capacity":Battery_Capacity,
        "Screen_Size":Screen_Size,
        "Price":Price,
        "Launched_Year":Launched_Year,
    }
    return "Added the top product successfully"

@tool
def add_top_one_laptop(Brand:str, Name:str, Price:float, Processor_Name:str, Processor_Brand:str, RAM_Expandable:str, RAM:str, RAM_TYPE:str, Ghz:str, Display_type:str, 
                       Display:str, GPU:str, GPU_Brand:str, SSD:str, HDD:str, Adapter:str, Battery_Life:str) -> str:
    """Adding the top laptop product dictionary according to your decision"""
    st.session_state.top_product = {
        "Brand":Brand,
        "Name":Name,
        "Price":Price,
        "Processor_Name":Processor_Name,
        "Processor_Brand":Processor_Brand,
        "RAM_Expandable":RAM_Expandable,
        "RAM":RAM,
        "RAM_TYPE":RAM_TYPE,
        "Ghz":Ghz,
        "Display_type":Display_type,
        "Display":Display,
        "GPU":GPU,
        "GPU_Brand":GPU_Brand,
        "SSD":SSD,
        "HDD":HDD,
        "Adapter":Adapter,
        "Battery_Life":Battery_Life
    }
    return "Added the top product successfully"

@tool
def add_top_one_car(Company_Name:str, Cars_Name:str, Engines:str, CC_Battery_Capacity:str, HorsePower:str, Total_Speed:str, Performance:str, Price:str, 
                    Fuel_Types:str, Seats:str, Torque:str) -> str:
    """Adding the top car product dictionary according to your decision"""
    st.session_state.top_product = {
        "Company_Names":Company_Name,
        "Cars_Names":Cars_Name,
        "Engines":Engines,
        "CC_Battery_Capacity":CC_Battery_Capacity,
        "HorsePower":HorsePower,
        "Total_Speed":Total_Speed,
        "Performance":Performance,
        "Price":Price,
        "Fuel_Types":Fuel_Types,
        "Seats":Seats,
        "Torque":Torque,
    }
    return "Added the top product successfully"

if 'messages' not in st.session_state:
    system_message ="""You are "Findora", an expert AI Product Assistant developed by "Eng. Abdallah Fekry". Your primary objective is to assist users in finding the best phones, laptops, or cars by searching internal databases, comparing specifications, and finding the best real-time deals on Amazon and eBay.
    ### FIRSTLY:
    "If the user is just saying a general greeting (like 'hello', 'hi', 'how are you') or asking a general conversational question, DO NOT use any tools and DO NOT use the 5-part structure below. Just respond naturally, friendly, and in 1-2 short sentences."

    ### TOOL USAGE RULES ONLY if the user ask for a product:
    1. CATEGORY SPECIFIC: ONLY use the database tools (`search_phone`, `search_laptop`, `search_car`) if the user explicitly asks about these specific categories. Do NOT use tools for general conversation.
    2. MISSING PARAMS: If any information is missing while calling a database tool, use `0` for numbers and `""` (empty string) for text.
    3. CLARIFICATION: You may ask the user targeted questions to support your decision ONLY if you need to break a tie between highly similar products.

    ### EXECUTION WORKFLOW:
    Step 1: Understand the user's request and execute the relevant database tool.
    Step 2: Analyze the results, compare them, and filter down to the Top 3 products.
    Step 3: Compare the Top 3 products meticulously to crown the definitive Top 1 product.
    Step 4: Say that you have execute the Amazon and eBay search strictly for this Top 1 product.
    Step 5: Generate the final response using the exact format provided below.

    ### STRICT OUTPUT FORMAT:
    You MUST structure your response EXACTLY in the following four sections. Do not deviate from this structure ONLY if the user asks to get a product:

    **Part 1: Top 3 Products Selection**
    "I have searched in the database and found that the top 3 products are:"
    [Insert a detailed Markdown comparison table for the Top 3 products. The table MUST include: Company_Name, Model_Name, RAM, Front_Camera, Back_Camera, Processor, Battery_Capacity, Screen_Size, Price, Launched_Year]

    **Part 2: The Winning Product**
    "I have compared all products and found that the top product is: [Top Product Name]"
    [List the Top 1 product's specifications: Company_Name, Model_Name, RAM, Front_Camera, Back_Camera, Processor, Battery_Capacity, Screen_Size, Price, Launched_Year]
    [Provide a clear, brief explanation of WHY this product won over the others]

    **Part 3: Best Live Deals**
    "I have searched Amazon and eBay for the best prices. You can find them in the products links card bellow the chat messages:"

    **Part 4: Final Recommendation**
    [Briefly explain which specific deal/link from Part 3 offers the best value for money and why the user should choose it.]
    
    **Part 5: Save Data for visual show**
    "I have created a popup page showed the products you need"
    [You MUST use ONLY ONE from the (add_top_one_phone or add_top_one_laptop or add_top_one_car) tools to save the top 1 product before generating your final response ONLY if you searched for a product.]"""
    st.session_state.messages = {
        "messages": [
            ("system", system_message),
        ]
    }

if "agent" not in st.session_state:
        API = st.secrets['GeminiAPI']
        tools = [search_phone, search_laptop, search_car, add_top_one_phone, add_top_one_laptop, add_top_one_car]
        llm = ChatGoogleGenerativeAI(
            model="gemini-3.1-flash-lite-preview",
            google_api_key=API,
            temperature=0
        )
        st.session_state.agent = create_react_agent(llm, tools)

def add_message(sender,message):
    if sender=='ai':
        st.session_state.messages['messages'].append(('ai',message))
    elif sender=='human':
        st.session_state.messages['messages'].append(('human',message))
    else:
        return f"Value Error '{sender}': Sender must be either 'ai' or 'human' not {sender}!"

def chat(text):
    try:
        add_message('human', text)
        # # Decrease messages lenght _____________________________________________
        # if len(st.session_state.messages)>10:
        #     messages = [st.session_state.messages[0]]
        #     messages = messages + st.session_state.messages[-9:]
        # else:
        #     messages = st.session_state.messages
        # # ______________________________________________________________________
        with loading.chat_message("assistant", avatar='media/bot avatar.png'):
            col1, col2 = st.columns([1,15], vertical_alignment='center', gap=None)
            with col1:
                st.image('media/Sparkles Loop Loader ai.gif')
            with col2:
                st.markdown("AI Decision...")
            response_state = st.session_state.agent.invoke(st.session_state.messages)
        final_message = response_state['messages'][-1]

        if isinstance(final_message.content, list):
            response_text = final_message.content[0].get('text', '')
        else:
            response_text = final_message.content
            
        add_message('ai', response_text)
        for msg in response_state['messages']:
            if msg.type == 'tool':
                if msg.name in ['amazon_search', 'ebay_search']:
                    tool_data = msg.content
                    if isinstance(tool_data, str):
                        try:
                            parsed_data = json.loads(tool_data)
                            if "products" in parsed_data:
                                st.session_state.products.extend(parsed_data["products"])
                        except Exception as e:
                            print(f"Error parsing JSON: {e}")
                    elif isinstance(tool_data, dict) and "products" in tool_data:
                        st.session_state.products.extend(tool_data["products"])

            elif msg.type == 'ai' and hasattr(msg, 'tool_calls') and msg.tool_calls:
                query = ""
                for call in msg.tool_calls:
                    if call['name'] == 'add_top_one_phone':
                        st.session_state.top_product = call['args']
                        st.session_state.category = 'phone'
                        query = st.session_state.top_product['Company_Name'] + " " + st.session_state.top_product['Model_Name']
                    elif call['name'] == 'add_top_one_laptop':
                        st.session_state.top_product = call['args']
                        st.session_state.category = 'laptop'
                        query = st.session_state.top_product['Brand'] + " " + st.session_state.top_product['Name']
                    elif call['name'] == 'add_top_one_car':
                        st.session_state.top_product = call['args']
                        st.session_state.category = 'car'
                if query:
                    with loading.chat_message("assistant", avatar='media/bot avatar.png'):
                        col1, col2 = st.columns([1,15], vertical_alignment='center', gap=None)
                        with col1:
                            st.image(r"media/Material wave loading.gif")
                        with col2:
                            st.markdown("Searching Amazon...")
                        st.session_state.products.extend(amazon_search(query)['products'])
                    with loading.chat_message("assistant", avatar='media/bot avatar.png'):
                        col1, col2 = st.columns([1,15], vertical_alignment='center', gap=None)
                        with col1:
                            st.image(r"media/Material wave loading.gif")
                        with col2:
                            st.markdown("Searching in Ebay...")
                        st.session_state.products.extend(ebay_search(query)['products'])
        return response_text
    except Exception as e:
        return str(e)

def speech_to_text(path, language):
    """
    Voice_To_Text
    Takes the "path of a voice file" and convert it into text
    """
    recognizer = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = recognizer.record(source)
    if language == 'Arabic':
        text = recognizer.recognize_google(audio, language="ar-EG")
    else:
        text = recognizer.recognize_google(audio, language="en-US")
    return text

# =========================================================================================================================================

# Chat history
col1, col2, col3 = st.columns([1,3,1])
if st.session_state.chat:
        counter = 0
        for c in st.session_state.chat:
            # Show the text messages
            if c['parts'][0].get('text'):
                st.chat_message('user' if c['role']=="user" else "assistant", avatar='media/user avatar.png' if c['role']=="user" else 'media/bot avatar.png').markdown(c['parts'][0]['text'])
            # Show the audio messages
            if c['parts'][0].get('audio'):
                # Autoplay the last voice note
                if counter == len(st.session_state.chat)-1:
                    st.chat_message('user' if c['role']=="user" else "assistant", avatar='media/user avatar.png' if c['role']=="user" else 'media/bot avatar.png').audio(c['parts'][0]['audio'], autoplay=False)
                else:
                    st.chat_message('user' if c['role']=="user" else "assistant", avatar='media/user avatar.png' if c['role']=="user" else 'media/bot avatar.png').audio(c['parts'][0]['audio'])
            # Show the image messages
            if c['parts'][0].get('image'):
                st.chat_message('user' if c['role']=="user" else "assistant", avatar='media/user avatar.png' if c['role']=="user" else 'media/bot avatar.png').image(c['parts'][0]['image'])
            counter += 1
        current = st.empty()
        loading = st.empty()
        
        if st.button(":material/save: Save conversation", type='tertiary'):
            st.session_state.chat_history.append({'chat':st.session_state.chat, 'products':st.session_state.products, 'category':st.session_state.category, 
                                                  'top_product':st.session_state.top_product})
            st.success("Your chat stored successfully!")
else:
    with col2:
        st.chat_message('ai', avatar='media/bot avatar.png').write("Hi 👋, i am Findora, how can i help you today?")
        # loading = st.empty()
        current = st.empty()
        loading = st.empty()
# ========================================================================================================================

message = st.chat_input("Say Something...", accept_file=True, file_type=["jpg", "jpeg", "png"], accept_audio=True)

if message:
    if message.files:
        pass
        # st.session_state.chat.append({"role":"user","parts":[{"image":message.files}]})
        # st.session_state.chat.append({"role":"model","parts":[{"text":response}]})
    if message.text:
        current.chat_message('user', avatar='media/user avatar.png').markdown(message.text)
        response = chat(message.text)
        loading.empty()
        st.session_state.chat.append({"role":"user","parts":[{"text":message.text}]})
        st.session_state.chat.append({"role":"model","parts":[{"text":response}]})
        st.rerun()
    if message.audio:
        current.chat_message('user', avatar='media/user avatar.png').audio(message.audio, autoplay=False)
        with open("user_voice.mp3", "wb") as f:
            f.write(message.audio.read())
        try:
            text = speech_to_text("user_voice.mp3", st.session_state.language)
        except KeyError as e:
            st.error(f"{e}\nYour current Language is {st.session_state.language} use the specified language or change it and use a quiet place to use the speech tool")
        response = chat(text)
        loading.empty()
        # st.session_state.chat.append({"role":"user","parts":[{"text":text}]})
        st.session_state.chat.append({"role":"user","parts":[{"audio":message.audio}]})
        st.session_state.chat.append({"role":"model","parts":[{"text":response}]})
        st.rerun()

# Show the output products
if st.session_state.top_product:
    st.divider()
    col1, col2, col3 = st.columns([1,3,1])
    with col2:
        # Phones
        if st.session_state.category == 'phone':
            top_product = st.session_state.top_product
            with st.popover(f":orange[:material/star:] Top Product: {top_product['Company_Name']} {top_product['Model_Name']}", width='stretch', type='primary'):
                st.markdown(f"{top_product['Company_Name']} {top_product['Model_Name']}")
                st.caption(f"RAM: {top_product['RAM']}")
                st.caption(f"Front Camera: {top_product['Front_Camera']}")
                st.caption(f"Back Camera: {top_product['Back_Camera']}")
                st.caption(f"Processor: {top_product['Processor']}")
                st.caption(f"Battery Capacity: {top_product['Battery_Capacity']}")
                st.caption(f"Screen Size: {top_product['Screen_Size']}")
                st.caption(f"Price: {top_product['Price']}")
        # Laptops
        elif st.session_state.category == 'laptop':
            # Brand, Name, Price, Processor_Name, Processor_Brand, RAM_Expandable, RAM, RAM_TYPE, Ghz, Display_type, Display, GPU, GPU_Brand, SSD, HDD, Adapter, Battery_Life
            top_product = st.session_state.top_product
            with st.popover(f":orange[:material/star:] Top Product: {top_product['Brand']} {top_product['Name']}", width='stretch', type='primary'):
                st.markdown(f"{top_product['Brand']} {top_product['Name']}")
                # RAM
                col11, col22, col33 = st.columns(3)
                with col11:
                    st.caption(f"RAM: {top_product['RAM']}")
                with col22:
                    st.caption(f"{top_product['RAM_TYPE']}")
                with col33:
                    st.caption(f"{top_product['RAM_Expandable']}")
                # Processor
                col11, col22, col33 = st.columns(3)
                with col11:
                    st.caption(f"Processor: {top_product['Processor_Brand']}")
                with col22:
                    st.caption(f"{top_product['Processor_Name']}")
                # GPU
                col11, col22, col33 = st.columns(3)
                with col11:
                    st.caption(f"GPU: {top_product['GPU_Brand']}")
                with col22:
                    st.caption(f"{top_product['GPU']}")
                # Display
                col11, col22, col33 = st.columns(3)
                with col11:
                    st.caption(f"Display: {top_product['Display']}")
                with col22:
                    st.caption(f"{top_product['Display_type']}")
                # Drive
                col11, col22, col33 = st.columns(3)
                with col11:
                    st.caption(f"SSD Drive: {top_product['SSD']}")
                with col22:
                    st.caption(f"HDD Drive: {top_product['HDD']}")
                # Battery
                col11, col22, col33 = st.columns(3)
                with col11:
                    st.caption(f"Battery Capacity: {top_product['Battery_Life']}")
                with col22:
                    st.caption(f"Adapter: {top_product['Adapter']}")
                st.caption(f"Price: {top_product['Price']}")
        # Cars
        elif st.session_state.category == 'car':
            # Company_Name, Cars_Name, Engines, CC_Battery_Capacity, HorsePower, Total_Speed, Performance, Price, Fuel_Types, Seats, Torque
            top_product = st.session_state.top_product
            with st.popover(f":orange[:material/star:] Top Product: {top_product['Company_Name']} {top_product['Cars_Name']}", width='stretch', type='primary'):
                st.markdown(f"{top_product['Company_Name']} {top_product['Cars_Name']}")
                st.caption(f"Engines: {top_product['Engines']}")
                st.caption(f"CC_Battery_Capacity: {top_product['CC_Battery_Capacity']}")
                st.caption(f"HorsePower: {top_product['HorsePower']}")
                st.caption(f"Total_Speed: {top_product['Total_Speed']}")
                st.caption(f"Performance: {top_product['Performance']}")
                st.caption(f"Fuel_Types: {top_product['Fuel_Types']}")
                st.caption(f"Seats: {top_product['Seats']}")
                st.caption(f"Torque: {top_product['Torque']}")
                st.caption(f"Price: {top_product['Price']}")
        if st.session_state.products:
            # Products Links
            with st.popover(f":material/link: View all product links", width='stretch', type='tertiary'):
                st.header("Product Links")
                cols = st.columns(3, vertical_alignment='top', gap='small')
                c = 0
                for p in st.session_state.products:
                    with cols[c]:
                        with st.container(border=True):
                            st.image(p['Image'], caption=f"Source: {p['Source']}")
                            st.caption(p['Title'], text_alignment='justify')
                            st.caption(p['Info'])
                            st.write(p['Price'])
                            st.link_button(":material/link: Buy now", p['Link'], type='tertiary')
                    c += 1
                    if c>2:
                        c %= 3
        # ______________________________________________________________________________________________-
        # Rating
        col11, col22 = st.columns([1,5], vertical_alignment='center', gap=None)
        with col11:
            st.write("**Rate** the decision:")
        with col22:
            fb = st.feedback(options='faces')
        if fb or fb==0:
            if  fb >= 3:
                if st.session_state.first:
                    st.session_state.first = False
                    st.balloons()
                    st.success("Great, we are happy for your experience 😍")
            elif fb<2:
                if st.session_state.first:
                    st.session_state.first = False
                    st.error("Sorry for that, we made our effort 😔")
            else:
                if st.session_state.first:
                    st.session_state.first = False
                    st.warning("Okay, not bad 👉👈")
# ______________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________


# Chat history
if st.session_state.chat_history:
    with st.sidebar:
        st.header(":material/chat: Chat history", divider='blue')
        col1, col2 = st.columns([8,1])
        # st.title("Chat history", )
        with col1:
            if st.button(":material/add: New chat", width='stretch',type='tertiary'):
                st.session_state.chat = []
                st.session_state.products = []
                st.session_state.category = []
                st.session_state.top_product = []
                st.rerun()
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
                    st.rerun()
            with col2:
                if st.button(':material/delete:', key=k, type='tertiary'):
                    st.session_state.chat_history.remove(st.session_state.chat_history[h])
                    st.rerun()
            k-=1
else:
    with st.sidebar:
        if st.button(":material/add: New chat", width='stretch',type='tertiary'):
            st.session_state.chat = []
            st.session_state.data = []
            st.rerun()

# Settings
with st.sidebar:
    st.divider()
    st.header(":material/settings: Settings")
    new_lang = st.selectbox(f"**Language** (current is {st.session_state.language})", ('Arabic', 'English'), placeholder='Language..', index=None)
    if new_lang and new_lang != st.session_state.language:
        st.write(f"Language will be change into :orange[{new_lang}]")
        if st.button("Save changes", type='primary'):
            st.session_state.language = new_lang
            st.rerun()

