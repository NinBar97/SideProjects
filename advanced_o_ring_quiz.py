import streamlit as st
import json

# Load quiz data from the JSON file
with open('quiz_data.json', 'r') as f:
    quiz_data = json.load(f)

# Initialize session state variables if they don't exist
if 'current_level' not in st.session_state:
    st.session_state.current_level = "Level 1 - Basic Understanding"
    st.session_state.score = 0
    st.session_state.level_complete = False
    st.session_state.answers = {}  # Track user's answers

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
    if question not in st.session_state.answers:
        st.session_state.answers[question] = None

    # Set a default index of -1 if no answer has been selected
    current_index = options.index(st.session_state.answers[question]) if st.session_state.answers[question] in options else 0

    # Display radio button with appropriate key and valid index
    st.session_state.answers[question] = st.radio(
        question, options, index=current_index, key=question
    )

# Submit button
if st.button("Submit Answers"):
    # Calculate the score for this level
    for question in questions:
        user_answer = st.session_state.answers[question]
        if user_answer == correct_answers[question]:
            level_score += 1

    # Display results for this level
    st.subheader(f"Your score for this level: {level_score} / {len(questions)}")

    # Update session state
    st.session_state.score += level_score
    st.session_state.level_complete = True

# Display navigation options based on level score
if st.session_state.level_complete:
    if level_score >= len(questions) // 2:  # Minimum pass criteria: 50% correct answers
        st.success(f"Congratulations! You passed {current_level}.")
        next_level = {
            "Level 1 - Basic Understanding": "Level 2 - Intermediate",
            "Level 2 - Intermediate": "Level 3 - Advanced Engineering",
            "Level 3 - Advanced Engineering": None
        }[current_level]

        # Display option to go to the next level
        if next_level:
            if st.button("Proceed to Next Level"):
                st.session_state.current_level = next_level
                st.session_state.level_complete = False
                st.session_state.answers = {}  # Reset answers for the next level
                st.experimental_rerun()  # Proper rerun to refresh state
        else:
            st.balloons()
            st.subheader("You've completed all levels! Well done!")
    else:
        st.error("You did not pass this level. Review the answers and try again.")

# Display final
