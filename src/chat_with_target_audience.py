import os
from typing import Generator, Any

import streamlit as st
import openai
from dotenv import load_dotenv
from openai.openai_object import OpenAIObject


def generate_message(draft_title: str | None,
                     draft_text: str,
                     personality: str,
                     history: list[dict],
                     stream: bool = False) \
        -> str | Generator[OpenAIObject, Any, None]:
    """
    ChatGPT prompt that mimics the target audience and gives advice to the writer in this context.

    **STARTS THE CONVERSATION ITSELF** based on the draft. Assumes openai keys are already set.

    :param stream: same as ChatCompletion.create(stream=True).
        If true, returns generator. If false, returns the string of full response (default).
    :param draft_text:
    :param draft_title: Can be empty or None
    :param personality: Syntax: Let's imagine ChatGPT is <personality>.
        Example: "A computer science student who is soon going to graduate and look for a permanent job"
    :param history: Just pass session_state.messages (format: {'role': 'user|assistant', 'content': 'text'}
    :return:
    """

    personality = f"""
    Consider everything from this perspective '{personality}'.
    You will be provided with a blog from a software consultancy firm. 
    Stay in character and express your honest and detailed opinion on the blog given your personality. 
    You can suggest a list of concrete and step-by-step improvements the writer can apply.
    The idea of the blog below is to catch the attention of people like your personality.
    Don't hold yourself back I have a thick skin.
    """

    prompt = f"""
    title: 
    {draft_title}

    text: 
    {draft_text}
    """

    res = openai.ChatCompletion.create(
        engine="gpt-35-turbo",  # gpt-4
        messages=[
            {"role": "system", "content": personality},
            {'role': 'user', 'content': prompt},
            *history
        ],
        stream=stream
    )
    return res if stream else res['choices'][0]['message']['content']


if __name__ == '__main__':
    load_dotenv()

    openai.api_key = os.getenv('API_KEY')
    openai.api_base = os.getenv('API_BASE')
    openai.api_type = 'azure'
    openai.api_version = '2023-05-15'

    st.title("Chat with the reader")
    # target_user = st.text_input('Target user:', value=
    #                             'A computer science student who is soon going to graduate and look for a permanent job')

    # Syntax: Let's imagine ChatGPT is <target user>.
    target_user = 'A computer science student who is soon going to graduate and look for a permanent job'
    draft_title = 'It’s time for courageous and unprecedented moves, not more of the same'
    draft_text = """Our need to understand what happens next has been amplified radically since the beginning of the year. Regardless of opinion on why we are where we are, we can certainly find consensus in the belief that we are in uncharted waters with a lack of clarity on what is to come. “Unprecedented!” The word of the hour across media that underlines the sentiment around the world, and effectively captures what all of us are experiencing. It is appearing in headlines and dialogue across the globe, and even trending on Google search (see graph), which paints an interesting picture about the human psyche – either that, or it offers an indication that unprecedented masses of people are googling, “what the hell does unprecedented actually mean?” 
    Google search trends for the search term "unprecedented" between 2004 and 2020. Either way, the language we use offers a signal for the context we find ourselves in, and thus, it’s necessary to consider it as we begin to formulate answers to the question of “what’s next.” Unprecedented adjective un·​prec·​e·​dent·​ed \ ˌən-ˈpre-sə-ˌden-(t)əd \ not done, known, or experienced before Unprecedented scenarios are truly going to test the mettle of organizations and their leaders, challenging business as usual rhetoric, and exposing the ability to demonstrate humility and accept not knowing the answers. It suggests that there are no definitive blueprints for what to do, nor are there previous events in recent history to reference, and certainly no time for indecisiveness. This offers a nightmare scenario for some, while others will see it as an opportunity, especially those who have been tasked with driving change and transformation within large-scale organizations. KONE’s call to look beyond the danger and see the opportunity in the crisis is one example of recognizing that something beyond the norm has to be done. It’s fair to say, therefore, that these unprecedented times call for unprecedented action. And it is indeed unprecedented action that will open up paths to a positive future beyond the current haze. We foresee rewiring organizations to embrace change as a business capability as the next big endeavor of courageous leaders. They will make do what it takes to ensure significant investments are carried out to not only enrich their people’s understanding of (and comfort with) change – but also enhance their creative intelligence to identify and implement solutions for the challenges that change brings. From those seen in the day-to-day, to the most complex and systemic ones. Learning and development teams will be bolstered and tasked with playing more of a frontline role, working hand in hand with business unit leaders to prepare their teams. Together they will explore and design learning journeys that entail the right balance of experiential learning and rich content, ensuring that knowledge moves beyond compliance to become the catalyst for growth. Central to this will, of course, be the continued commitment to engineering a digital organization, making full use of its data and emerging technology – such as AI – to empower teams. CIOs and CTOs will have mandated that those responsible for portfolio management reprioritize and/or expedite programs to help ensure the necessary tools and platforms are in place. The immediate crisis has served to solidify the importance of an organization’s technology agenda, while the future will only bring greater scrutiny to ensure it remains watertight. As a result, an evolved mindset will emerge, providing a fresh approach to business – one that empowers teams to rethink, retool, and reprioritize as they go. This is what we refer to as resilience, and what we believe is needed in these unprecedented times. “We always overestimate the change that will occur in the next two years and underestimate the change that will occur in the next ten.” — Bill Gates We are not in the sport of making predictions. However, we are in the game of preparing organizations for tomorrow – and this requires exploring what these future landscapes and horizons have in store. While opinion on this is (and always will be) vast and varied, none of it is definitive, nor should it be seen as such. Rather, this shared collective wisdom is meant to offer an outlook to the landscape ahead, which ultimately calls for courageous leaders to navigate it using their organization’s unique compass, defined by its purpose and the core values on which it has been built. """
    # draft_title = 'FutuStories - Nine things that make me happy, an interview with Till Kleinhans'
    # draft_text = '''Till is a UX and business designer who makes his clients happy with thoughtful designs while also trying to find the right balance for contentment in his personal life. Here he reflects on nine things that make him happy, from intellectual curiosity to a bellyful of good food. I’m a very curious person so it’s no wonder I’ve worked in multiple areas, including industrial design, media, computer science and now business design. When I look at an unfamiliar field, I see a black box and want to get to its core and understand an aspect of the world that was previously hidden to me. I’m always happy when there is one less black box in the world – and there are always more to find, which is also a great thing. I don’t really like small talk – you won’t find me chatting for half an hour about soccer or the weather. Instead, I really appreciate conversations where I find something in common with someone and we can just walk around the topic and wonder how many other perspectives there are out there. Expanding my understanding makes me happy – in terms of equality, many of us don’t realize how privileged we are so it’s great to learn how other people see the world. As designers, we really benefit from doing this, and it’s very important to do so – we’re a community and we don’t just learn or design for ourselves. Throughout my career I’ve benefited from understanding different areas – for example, when I was doing UX design with strict technical limitations I benefited a lot from my understanding of computer science. Being able to speak the same language as the developer on the client side helps you understand the context and create a solution that really serves their needs. As a designer, it’s no surprise that I appreciate beautiful things. Design is the combination of aesthetics and function – it’s often beauty that initially draws people towards a career in this field. This can make perfectionism a challenge, but I’ve learned to work quickly while making beautiful solutions for clients. That said, in my own time I can still occasionally drive myself crazy, like when I look at 300 different options just to choose the perfect tennis racket! I can be very competitive and while I don’t ever take it too far, it’s always a good feeling to win. I play basketball once a week, padel when it’s warm enough and play table football whenever I can. We don’t have a table at the Munich office but there is one in Berlin – if I worked there I’d play it every day! I also always have the drive to win if I’m involved in a competition, like creating business models or products in hackathons and makeathons. It’s the same in client pitches and even when creating a solution – I’m not necessarily competing with others, sometimes I’m competing with the problem. Overcoming complex challenges is a great feeling. This is something that makes me really happy – in fact, it’s my favorite thing to do in my own time. I wouldn’t want to get an instructor’s license and do it full time, but it’s a special feeling and one of the few things that put me completely in the moment, away from any distracting thoughts. When I don’t have scuba as an option I can always meditate, but for me there’s nothing like the fully immersive feeling of diving – it’s like flying underwater. It’s the best feeling in the world. Everyone needs balance in their life. I’m working in an intellectual profession, using my mind more than my body, so it’s good to get back into a workshop and physically work on something tangible like a bicycle or furniture. This is something I enjoyed about industrial design – being in the workshop and able to create anything my imagination and skill level made possible. If an intellectual challenge is making your head spin at work, it’s nice to come home and indulge in an activity that doesn’t involve so much mental effort. This is another hobby of mine – it’s a nice change to taking pictures with my cell phone. I like the constraint of only having 36 shots on the roll – each picture costs around a euro, so you have to value each shot and put the effort in, then you get rewarded once they’re developed. I never fill the whole roll in one day, so it’s like a bag of surprises when I hand it in – there might be photos from a party, a walk somewhere beautiful, a vacation or something else. I always shoot in black and white and it makes me happy seeing beautiful shots of our world.
    # In Europe the food can be quite plain. I prefer foods with more complex flavours like you find in Vietnamese, Indian, Moroccan and West Asian cuisine. When I was on an exchange semester in Singapore, I discovered food courts with cheap prices and a whole range of flavorful food from across Asia. You can eat something new every day – I fell in love with Vietnamese food there and it made me very happy indeed! *Interested in reading more stories about us and our people? At Futurice, we celebrate diversity and cherish everyone's unique journey. Check out our Welcome Hope Page
    # and get inspired by more journeys shaping our culture. If you would like to read more stories and get to know our people, our sites and the community better, check out the global version of our FutuStories Booklet '''

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

        response = generate_message(draft_title, draft_text, target_user, st.session_state.messages)
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

        response = generate_message(draft_title, draft_text, target_user, st.session_state.messages)
        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        last_role = 'assistant'
