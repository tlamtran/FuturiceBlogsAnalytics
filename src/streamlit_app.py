import pandas as pd
import occurrences_demo
import chat_with_target_audience
import streamlit as st

from insights import *
from scatter_plot import scatter_plot


# .venv\Scripts\activate
# To run, put in terminal: `python -m streamlit run .\src\streamlit_app.py`
# To close, use CTRL + C in terminal
# Good website with lots of different things you can do: https://cheat-sheet.streamlit.app/
# Maybe use this as an idea: https://github.com/okld/streamlit-ace
# The "similarity" import requires eg. pip-installing langchain and sentence_transformer
# When launching streamlit next time, it will probably take some time, because it will have to load eg. pytorch
# I hope the downloads will only have to be done once, and not every time streamlit is launched -Eero


if "blog_title" not in st.session_state:
        st.session_state["blog_title"] = ""

if "blog_title_tracker" not in st.session_state:
        st.session_state["blog_title_tracker"] = ""

if "target_audience" not in st.session_state:
    st.session_state["target_audience"] = ""

if "blog_intro" not in st.session_state:
    st.session_state["blog_intro"] = ""
    
if "blog_text" not in st.session_state:
    st.session_state["blog_text"] = ""

if "suggested_blog_intro" not in st.session_state:
    st.session_state["suggested_blog_intro"] = ""

if "suggested_blog_text" not in st.session_state:
    st.session_state["suggested_blog_text"] = ""

if "tips" not in st.session_state:
    st.session_state["tips"] = ""    

if "similar_futurice" not in st.session_state:
    st.session_state["similar_futurice"] = pd.DataFrame()

if "similar_competitors" not in st.session_state:
    st.session_state["similar_competitors"] = pd.DataFrame()  


# Blog editor page
def blog_editor():
    st.markdown("## Blog editor")
    editor_col, tools_col = st.columns([2, 1])

    with editor_col:
        editor = st.form('editor')
        blog_title = editor.text_input("Blog title", st.session_state["blog_title"])
        target_audience = editor.text_input("Write a description of the target audience", st.session_state["target_audience"])
        intro = editor.text_area("Intro Paragraph", st.session_state["blog_intro"], height = 160)
        editor.markdown(f'{len(st.session_state["blog_intro"])} characters')
        body = editor.text_area("Blog body text", st.session_state["blog_text"], height = 600)
        editor.markdown(f'{len(st.session_state["blog_text"])} characters')
        
        button = editor.form_submit_button('Update state')

        if button:
            st.session_state["blog_title"] = blog_title
            st.session_state["target_audience"] = target_audience
            st.session_state["blog_intro"] = intro
            st.session_state["blog_text"] = body

            st.session_state["tips"] = get_gpt_tips(st.session_state["blog_title"],
                                                    st.session_state["target_audience"],
                                                    st.session_state["blog_intro"],
                                                    st.session_state["blog_text"])
            
            if st.session_state["blog_title_tracker"] != st.session_state["blog_title"]:
                st.session_state["blog_title_tracker"] = st.session_state["blog_title"]
                st.session_state["similar_futurice"] = get_similar_blogs(st.session_state["blog_title"])
                st.session_state["similar_competitors"] = get_similar_blogs_competitors(st.session_state["blog_title"]) 

    with tools_col:
        suggestions_tab, tips_tab, insights_tab = st.tabs(["Suggestions", "Tips", "Insights"])

        with suggestions_tab:
            if st.session_state["blog_title"] and st.session_state["target_audience"]:
                if not st.session_state["suggested_blog_intro"] and not st.session_state["suggested_blog_text"]:
                    st.session_state["suggested_blog_intro"]= get_gpt_intro_paragraph(st.session_state["blog_title"],
                                                                        st.session_state["target_audience"])
                    st.session_state["suggested_blog_text"] = get_gpt_blog_body_text(st.session_state["suggested_blog_intro"])

                if st.session_state["suggested_blog_intro"] and st.session_state["suggested_blog_text"]:
                    with st.form("intro"):
                        intro_prompt_text = st.text_input("Would you like to modify intro? 👇")
                        intro_prompt_button = st.form_submit_button('Update intro')
                    if intro_prompt_button:
                        rewritten_intro = rewrite(intro_prompt_text + ", keep markdown format", st.session_state["suggested_blog_intro"])
                        st.session_state["suggested_blog_intro"] = rewritten_intro
                    st.markdown(st.session_state["suggested_blog_intro"])
                    

                    with st.form('body'):
                        body_prompt_text = st.text_input("Would you like to modify blog body text? 👇")
                        body_prompt_button = st.form_submit_button('Update blog body')
                    if body_prompt_button:
                        rewritten_body = rewrite(body_prompt_text, st.session_state["suggested_blog_text"])
                        st.session_state["suggested_blog_text"] = rewritten_body
                    st.text(st.session_state["suggested_blog_text"])
                    
            else:
                st.markdown(get_gpt_blog_title_and_target_audience(st.session_state["blog_title"],
                                                                   st.session_state["target_audience"]))
        with tips_tab:
            st.markdown(st.session_state["tips"])

        with insights_tab:
            if len(st.session_state["similar_futurice"]) > 0:
                st.markdown(f'Similar blogs from Futurice: *{len(st.session_state["similar_futurice"])}*')
                for i in st.session_state["similar_futurice"].index:
                    st.markdown(f'- [{st.session_state["similar_futurice"]["title"][i]}]({st.session_state["similar_futurice"]["link"][i]})')
                st.markdown("Metrics averaged:")
                st.progress(get_cdf_value_total_users(st.session_state["similar_futurice"].loc[:, "total users"].mean()),
                            f'Total users: *{"{:.2f}".format(st.session_state["similar_futurice"].loc[:, "total users"].mean())}*')
                st.progress(get_cdf_value_avg_session_time(st.session_state["similar_futurice"].loc[:, "average session duration"].mean()),
                            f'Session time: *{"{:.2f}".format(st.session_state["similar_futurice"].loc[:, "average session duration"].mean())}*')
                st.progress(st.session_state["similar_futurice"].loc[:, "bounce rate"].mean(),
                            f'Bounce rate: *{"{:.2f}".format(st.session_state["similar_futurice"].loc[:, "bounce rate"].mean())}*')

            if len(st.session_state["similar_competitors"]) > 0:
                st.markdown(f'Similar blogs from competitors (accenture, tietoevry): *{len(st.session_state["similar_competitors"])}*')
                for i in st.session_state["similar_competitors"].index:
                    st.markdown(f'- [{st.session_state["similar_competitors"]["title"][i]}]({st.session_state["similar_competitors"]["link"][i]})')

                

    st.divider()
    st.markdown('## ' + st.session_state["blog_title"])
    st.divider()
    st.markdown(st.session_state["blog_intro"])
    st.divider()
    st.markdown(st.session_state["blog_text"])
    st.divider()


# Assistant page
def assistant():
    st.markdown("## Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

        response = chat_with_target_audience.generate_message(st.session_state["blog_title"], 
                                                              st.session_state["blog_intro"]+'\n'+st.session_state["blog_text"], 
                                                              st.session_state["target_audience"], 
                                                              st.session_state.messages)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = chat_with_target_audience.generate_message(st.session_state["blog_title"], 
                                                              st.session_state["blog_intro"]+'\n'+st.session_state["blog_text"], 
                                                              st.session_state["target_audience"], 
                                                              st.session_state.messages)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        last_role = 'assistant'



# Trends page
def trends():
    st.markdown("## Trends")
    occurrences_demo.run_app()


# Scatter plot
def plot():
    st.markdown("## Plot")
    scatter_plot()


# Page setup
def ai_blog_editing_tool():
    # Set up the page
    PAGE_TITLE: str = "AI-powered blog editor"
    PAGE_ICON: str = "📈"
    PAGE_LAYOUT: str = "wide"

    st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=PAGE_LAYOUT)
    st.markdown("# AI-powered blog editor")

    pages_to_funcs = {
        "Blog editor": blog_editor,
        "Assistant": assistant,
        "Trends": trends,
        "Plot": plot
    }

    with st.sidebar:
        page_name = st.sidebar.selectbox("Choose page", pages_to_funcs.keys())
        st.warning("Remember to save textfields before changing pages!")

    pages_to_funcs[page_name]()


ai_blog_editing_tool()
