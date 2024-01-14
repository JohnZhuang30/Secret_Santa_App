import streamlit as st
import random

@st.cache_data
def match_names(names):
    try:
        # random.shuffle(names)
        # available_names = names.copy()
        picked_names = []
        matching_results = {}
        for i in range(len(names)):
            current_name = names[i]
            available_names = [element for element in names if element not in ([current_name]+picked_names)]
            if i == len(names)-1 and len(available_names) == 1:
                matched_name = available_names[0]
            else:
                matched_name = random.choice(available_names)
            picked_names.append(matched_name)
            matching_results[current_name] = matched_name

        # print(matching_results)
        return matching_results
    
    except ValueError as e:
        st.error("Error", str(e))

def check_duplicate(names):
    names_lower = [name.lower() for name in names]
    if len(set(names_lower)) != len(names_lower):
        st.error("Duplicate names are not allowed.")
        if "clicked" in st.session_state:
            st.session_state.clicked[1] = False
        st.stop()


def main():

    # Intialise the key in session state
    if 'clicked' not in st.session_state:
        st.session_state.clicked = { 1:False, 2:False}

    if 'current_person_index' not in st.session_state:
        st.session_state.current_person_index = 0

    if 'names_input' not in st.session_state:
        st.session_state.names_input = ""

    if 'names' not in st.session_state:
        st.session_state.names = []

    if 'num_names' not in st.session_state:
        st.session_state.names = []

    if 'matches' not in st.session_state:
        st.session_state.matches = {}

    if 'show' not in st.session_state:
        st.session_state.show = False


    # Function to update the value in session state
    def clicked(button):
        st.session_state.clicked[button] = True


    # Step 1 - Enter the names
    st.write("""
            ## Secret Santa Matcher
            Hey there! Welcome to the Secret Santa Matcher! 🎅✨ I'm here to make your gift exchange extra special. Just let me know how many folks are joining and their names, and watch the magic unfold. I'll create unique Secret Santa matches, adding an extra dose of joy and surprise to your holiday celebration. Ready to make this season unforgettable? Let's get started and spread some festive cheer!
            """)
    st.write("### Enter names, one per line:")
    st.session_state.names_input = st.text_area("Type names here (one per line):", height=200)

    # Create a confirm button to confirm the list of names
    st.button('Confirm', on_click= clicked, args=[1])


    # Step 2 - Show matching results
    if st.session_state.clicked[1]:
        st.session_state.names = [name.strip() for name in st.session_state.names_input.split("\n") if name.strip()]
        st.session_state.num_names = len(st.session_state.names)

        # Check duplicate names
        check_duplicate(st.session_state.names)

        if len(st.session_state.names) < 2:
            st.error("Enter at least two names")
        else:
            # Generate random match
            #if len(st.session_state.matches) == 0:
            st.session_state.matches = match_names(st.session_state.names)

            # Display matching result
            person = list(st.session_state.matches.keys())[st.session_state.current_person_index]
            match = st.session_state.matches[person]
            if not st.session_state.show:
                st.write(f"**{person}'s match:**")
            else:
                st.write(f"**{person}'s match is {match}**")
            
            if st.session_state.current_person_index < st.session_state.num_names - 1:
                if st.button("Show Result", key=f"show_{st.session_state.current_person_index}"):
                    st.session_state.show = True
                    st.rerun()

                if st.button("Next Person", key=f"Next_{st.session_state.current_person_index}"):
                    if st.session_state.show:
                        st.session_state.current_person_index += 1
                        # person = list(st.session_state.matches.keys())[st.session_state.current_person_index]
                        st.session_state.show = False
                        st.rerun()
                    else:
                        st.error('Show your matching result first')

            else:
                if st.button("Show Result", key=f"show_{st.session_state.current_person_index}"):
                    st.session_state.show = True
                    st.rerun()

                if st.button("Start Over", key=f"Next_{st.session_state.current_person_index}"):
                    if st.session_state.show:
                        st.session_state.initial_text = st.text("")
                        st.session_state.clicked = { 1:False}
                        st.session_state.current_person_index = 0
                        st.session_state.names_input = ""
                        st.session_state.names = []
                        st.session_state.names = []
                        st.session_state.matches = {}
                        st.session_state.show = False
                        match_names.clear()
                        # st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error('Show your matching result first')
                

if __name__ == "__main__":
    main()        
