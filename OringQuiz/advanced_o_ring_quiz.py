import streamlit as st
import json
import random

# Load quiz data from the JSON file
with open('quiz_data.json', 'r') as f:
    quiz_data = json.load(f)

# Initialize session state variables if they don't exist
if 'current_level' not in st.session_state:
    st.session_state.current_level = "Level 1 - Basic Understanding"
    st.session_state.score = 0
    st.session_state.level_complete = False
    st.session_state.answers = {}  # Track user's answers
    st.session_state.level_passed = False  # Track if the current level is passed
    st.session_state.shuffled_options = {}  # Store shuffled options for each question

# Function to reset the quiz state
def restart_quiz():
    st.session_state.current_level = "Level 1 - Basic Understanding"
    st.session_state.score = 0
    st.session_state.level_complete = False
    st.session_state.answers = {}
    st.session_state.level_passed = False
    st.session_state.shuffled_options = {}

# Display Restart Quiz button
if st.sidebar.button("Restart Quiz"):
    restart_quiz()

# Set current level
current_level = st.session_state.current_level
questions = quiz_data[current_level]["questions"]
correct_answers = quiz_data[current_level]["correct_answers"]

# Streamlit app interface
st.title("O-Ring Engineering Quiz")
st.subheader(f"Current Level: {current_level}")
st.write("Answer the following questions to test your knowledge about O-rings.")

# Track score for this level
level_score = 0

# Display questions and get user input
for question, options in questions.items():
    # Initialize answer state and shuffle options if they have not been initialized
    if question not in st.session_state.answers:
        st.session_state.answers[question] = "I don't know"
    
    if question not in st.session_state.shuffled_options:
        # Shuffle the options and add "I don't know" as the first option
        shuffled_options = ["I don't know"] + random.sample(options, len(options))
        st.session_state.shuffled_options[question] = shuffled_options

    # Use the shuffled options stored in session state
    shuffled_options = st.session_state.shuffled_options[question]

    # Set the index to the current selected answer in the shuffled list
    current_index = shuffled_options.index(st.session_state.answers[question]) if st.session_state.answers[question] in shuffled_options else 0

    # Display radio button with a unique key for each question to avoid UI conflicts
    st.session_state.answers[question] = st.radio(
        question, shuffled_options, index=current_index, key=f"radio_{question}"
    )

# Submit button
if st.button("Submit Answers"):
    # Calculate the score for this level
    for question in questions:
        user_answer = st.session_state.answers[question]
        # Determine if the answer is correct
        original_correct_answer = correct_answers[question]
        if user_answer == original_correct_answer:
            level_score += 1

    # Display results for this level
    st.subheader(f"Your score for this level: {level_score} / {len(questions)}")

    # Update session state
    st.session_state.score += level_score
    st.session_state.level_complete = True

    # Check if the user passed this level
    st.session_state.level_passed = level_score >= len(questions) // 2

# Display navigation options based on level score
if st.session_state.level_complete:
    if st.session_state.level_passed:
        st.success(f"Congratulations! You passed {current_level}.")
        
        # Determine the next level, if available
        next_level = {
            "Level 1 - Basic Understanding": "Level 2 - Intermediate",
            "Level 2 - Intermediate": "Level 3 - Advanced Engineering",
        }.get(current_level, None)

        # If there is a next level, show the proceed checkbox
        if next_level:
            if st.checkbox("Proceed to Next Level"):
                # Update session state for the next level
                st.session_state.current_level = next_level
                st.session_state.level_complete = False
                st.session_state.answers = {}  # Reset answers for the next level
                st.session_state.level_passed = False
                st.session_state.shuffled_options = {}  # Reset shuffled options for the next level
                st.experimental_set_query_params()  # Trigger a state refresh
        else:
            st.balloons()
            st.subheader("You've completed all levels! Well done!")
    else:
        st.error("You did not pass this level. Review the answers and try again.")

# Display final score if all levels are complete and no more next level is defined
if current_level == "Level 3 - Advanced Engineering":
    st.subheader(f"Your total score: {st.session_state.score} / 9")
