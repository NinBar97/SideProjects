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
    st.session_state.level_passed = False  # Track if the current level is passed
    st.session_state.proceed_to_next = False  # Track if the user clicked to proceed

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

    # Set a default index of 0 if no answer has been selected
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

    # Check if the user passed this level
    st.session_state.level_passed = level_score >= len(questions) // 2

# Display navigation options based on level score
if st.session_state.level_complete:
    if st.session_state.level_passed:
        st.success(f"Congratulations! You passed {current_level}.")
        next_level = {
            "Level 1 - Basic Understanding": "Level 2 - Intermediate",
            "Level 2 - Intermediate": "Level 3 - Advanced Engineering",
            "Level 3 - Advanced Engineering": None
        }[current_level]

        # Display option to go to the next level if there is one
        if next_level:
            # Show a checkbox for proceeding to the next level
            if st.checkbox("Proceed to Next Level"):
                # Update session state for the next level
                st.session_state.current_level = next_level
                st.session_state.level_complete = False
                st.session_state.answers = {}  # Reset answers for the next level
                st.session_state.level_passed = False
    else:
        st.error("You did not pass this level. Review the answers and try again.")

# Display final score if all levels are complete
if current_level == "Level 3 - Advanced Engineering" and not next_level:
    st.subheader(f"Your total score: {st.session_state.score} / 9")
