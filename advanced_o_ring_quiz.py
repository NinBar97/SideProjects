import streamlit as st

# Quiz data structured by levels
quiz_data = {
    "Level 1 - Basic Understanding": {
        "questions": {
            "What is the main purpose of an O-ring?": [
                "To seal against leakage of gases or liquids between two surfaces",
                "To serve as a decorative item",
                "To conduct electricity",
                "To generate heat"
            ],
            "Which of the following is a common material used to make O-rings?": [
                "Rubber or elastomers",
                "Steel",
                "Wood",
                "Glass"
            ],
            "What shape is an O-ring?": [
                "Circular with a round cross-section",
                "Square",
                "Hexagonal",
                "Triangular"
            ]
        },
        "correct_answers": {
            "What is the main purpose of an O-ring?": "To seal against leakage of gases or liquids between two surfaces",
            "Which of the following is a common material used to make O-rings?": "Rubber or elastomers",
            "What shape is an O-ring?": "Circular with a round cross-section"
        }
    },
    "Level 2 - Intermediate": {
        "questions": {
            "Which industry standard specifies the dimensions of O-rings?": [
                "ISO 3601",
                "ISO 9001",
                "ANSI B16",
                "DIN 912"
            ],
            "What is a common failure mode for O-rings?": [
                "Extrusion and nibbling",
                "Oxidation",
                "Corrosion",
                "Fatigue cracking"
            ],
            "What is the most critical factor for ensuring a proper O-ring seal?": [
                "Proper compression ratio",
                "Exact color matching",
                "Surface finish of O-ring",
                "Roundness of O-ring"
            ]
        },
        "correct_answers": {
            "Which industry standard specifies the dimensions of O-rings?": "ISO 3601",
            "What is a common failure mode for O-rings?": "Extrusion and nibbling",
            "What is the most critical factor for ensuring a proper O-ring seal?": "Proper compression ratio"
        }
    },
    "Level 3 - Advanced Engineering": {
        "questions": {
            "Which type of O-ring material is best suited for high-pressure hydraulic applications?": [
                "Fluorocarbon (Viton)",
                "Silicone",
                "Neoprene",
                "Ethylene Propylene (EPDM)"
            ],
            "What is the typical hardness range (measured in Shore A) for standard O-rings?": [
                "70 - 90 Shore A",
                "30 - 50 Shore A",
                "10 - 20 Shore A",
                "100 - 120 Shore A"
            ],
            "What happens if an O-ring is compressed beyond its recommended limit?": [
                "It can extrude and fail under pressure",
                "It improves the sealing capability",
                "It becomes more durable",
                "Nothing significant happens"
            ]
        },
        "correct_answers": {
            "Which type of O-ring material is best suited for high-pressure hydraulic applications?": "Fluorocarbon (Viton)",
            "What is the typical hardness range (measured in Shore A) for standard O-rings?": "70 - 90 Shore A",
            "What happens if an O-ring is compressed beyond its recommended limit?": "It can extrude and fail under pressure"
        }
    }
}

# Initialize session state variables
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

    st.session_state.answers[question] = st.radio(
        question, options, key=question, index=options.index(st.session_state.answers[question]) if st.session_state.answers[question] else -1
    )

# Submit button
if st.button("Submit Answers"):
    for question, options in questions.items():
        user_answer = st.session_state.answers[question]
        if user_answer == correct_answers[question]:
            level_score += 1

    st.subheader(f"Your score for this level: {level_score} / {len(questions)}")
    st.session_state.score += level_score
    st.session_state.level_complete = True

# Display navigation options based on score
if st.session_state.level_complete:
    if level_score >= len(questions) // 2:
        st.success(f"Congratulations! You passed {current_level}.")
        next_level = {
            "Level 1 - Basic Understanding": "Level 2 - Intermediate",
            "Level 2 - Intermediate": "Level 3 - Advanced Engineering",
            "Level 3 - Advanced Engineering": None
        }[current_level]

        if next_level:
            if st.button("Proceed to Next Level"):
                st.session_state.current_level = next_level
                st.session_state.level_complete = False
                st.session_state.answers = {}
                st.experimental_rerun()
        else:
            st.balloons()
            st.subheader("You've completed all levels! Well done!")
    else:
        st.error("You did not pass this level. Review the answers and try again.")

if current_level == "Level 3 - Advanced Engineering" and not next_level:
    st.subheader(f"Your total score: {st.session_state.score} / 9")
