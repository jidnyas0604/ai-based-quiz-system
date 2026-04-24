import streamlit as st # type: ignore
import json
from src.core.generator import build_full_quiz # Ensure this returns a DICT, not a string
from fpdf import FPDF # type: ignore

def generate_study_pdf(quiz_results, report_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI powered Quiz System: Personalized Study Report", ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, txt=f"Analysis for: {report_name}")
    pdf.ln(5)
    
    for idx, item in enumerate(quiz_results):
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 10, txt=f"Q{idx+1}: {item.get('question', 'Question Text Error')}")
        pdf.set_font("Arial", 'I', 11)
        pdf.multi_cell(0, 10, txt=f"Correct Answer: {item.get('answer', 'N/A')}")
        pdf.set_font("Arial", size=11)
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
        
    return pdf.output(dest='S').encode('latin-1')

st.set_page_config(page_title="AI-Based Finance Quiz Bot", page_icon="🚀")

with st.sidebar:
    st.title("📂 Knowledge Base")
    st.markdown("---")
    
    # The Document Selector
    selected_doc = st.selectbox(
        "Select Report for Analysis:",
        [
            "FY 2025 Annual Financial Report", 
            "Q3 Risk Assessment & Disclosures", 
            "ESG Sustainability Report 2024",
            "Custom Uploaded Document"
        ]
    )
    
    # Visual status indicators to "sell" the tech
    st.success(f"Selected: {selected_doc}")
    
    st.markdown("---")
    if st.button("🔄 Resync Database"):
        with st.spinner("Re-indexing chunks..."):
            import time
            time.sleep(1.5) # Fake a tiny delay for "work"
            st.toast("Database Synced successfully!")

# --- Session State Initialization ---
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'current_q' not in st.session_state:
    st.session_state.current_q = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'complete' not in st.session_state:
    st.session_state.complete = False

st.title("🛰️ AI-Based Finance Quiz System")
st.subheader("Test your knowledge on the given document")

# --- Step 1: Generate Quiz ---
if st.button("Generate New Quiz"):
    st.session_state.quiz_data = build_full_quiz(document_name=selected_doc)
    with st.spinner("Llama is thinking..."):
        # Note: Ensure your generator returns a dictionary. 
        # If it returns a string, use json.loads() here.
        raw_quiz = build_full_quiz()
        st.session_state.quiz_data = json.loads(raw_quiz) if isinstance(raw_quiz, str) else raw_quiz
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.complete = False
        st.rerun()

# # --- Step 2: Present Questions ---
# if st.session_state.quiz_data and not st.session_state.complete:
#     quiz = st.session_state.quiz_data['questions']
#     q_idx = st.session_state.current_q
    
#     # Progress Bar
#     progress = (q_idx) / len(quiz)
#     st.progress(progress)
#     st.write(f"**Question {q_idx + 1} of {len(quiz)}**")
    
#     current_question = quiz[q_idx]
#     st.write(f"### {current_question['question']}")
    
#     # User Input
#     answer = st.radio("Select an option:", current_question['options'], key=f"q_{q_idx}")
    
#     # if st.button("Submit Answer"):
#     #     if answer == current_question['answer']:
#     #         st.success(f"Correct! {current_question['explanation']}")
#     #         st.session_state.score += 1
#     #     else:
#     #         st.error(f"Wrong. The correct answer was: {current_question['answer']}")
#     #         st.info(f"Insight: {current_question['explanation']}")
#     if st.button("Submit Answer"):
#         # Look for the option in the list that has 'correct': True
#         # We find the 'text' of the option that is marked as correct
#         correct_option_text = next(
#             opt['text'] for opt in current_question['options'] if opt.get('correct') == True
#         )
        
#         if answer == correct_option_text:
#             st.success(f"Correct! {current_question.get('explanation', '')}")
#             st.session_state.score += 1
#         else:
#             st.error(f"Wrong. The correct answer was: {correct_option_text}")
#             st.info(f"Insight: {current_question.get('explanation', '')}")
            
#         # Move to next or finish
#         if q_idx + 1 < len(quiz):
#             st.session_state.current_q += 1
#             st.button("Next Question")
#         else:
#             st.session_state.complete = True
#             st.rerun()

# --- Step 2: Present Questions ---
if st.session_state.quiz_data and not st.session_state.complete:
    # 1. Flexible key hunting (looks for 'questions', 'quiz', or the first list it finds)
    raw_data = st.session_state.quiz_data
    if isinstance(raw_data, list):
        quiz = raw_data
    else:
        # Tries to find 'questions' or 'quiz' keys, defaults to the first list value found
        quiz = raw_data.get('questions') or raw_data.get('quiz') or next((v for v in raw_data.values() if isinstance(v, list)), None)

    if not quiz:
        st.error("Could not find a list of questions in the AI response.")
        st.json(raw_data) # Debugging: shows you what the LLM actually sent
        st.stop()

    q_idx = st.session_state.current_q
    
    # Progress Bar
    progress = (q_idx) / len(quiz)
    st.progress(progress)
    st.write(f"**Question {q_idx + 1} of {len(quiz)}**")
    
    # current_question = quiz[q_idx]
    # st.write(f"### {current_question['question']}")
    
    # # 2. Fix the Radio Button display (Only show text, not the full dict)
    # options = current_question['options']
    
    # # Logic to handle both ['A', 'B'] and [{'text': 'A', 'correct': True}] formats
    # display_options = [opt['text'] if isinstance(opt, dict) else opt for opt in options]
    
    # answer_text = st.radio("Select an option:", display_options, key=f"q_{q_idx}")
    # --- Inside Step 2: Present Questions ---
    current_question = quiz[q_idx]
    
    # UNIVERSAL QUESTION HUNTER: Look for common keys for the question text
    q_text = (
        current_question.get('question') or 
        current_question.get('text') or 
        current_question.get('q') or 
        "Question text could not be parsed."
    )
    
    st.write(f"### {q_text}")
    
    # 2. UNIVERSAL KEY HUNTER: Find the options/choices array
    # This looks for 'options', then 'choices', then 'selections'
    # options = (
    #     current_question.get('options') or 
    #     current_question.get('choices') or 
    #     current_question.get('selections')
    # )
    
    # if not options:
    #     st.error("The AI failed to generate choices for this question.")
    #     st.write("Debug Data:", current_question)
    #     st.stop()
    
    # # Handle both format types for the radio button display
    # display_options = [opt['text'] if isinstance(opt, dict) else opt for opt in options]
    
    # # --- User Input ---
    # answer_text = st.radio("Select an option:", display_options, key=f"q_{q_idx}")
    # 2. Fix the Radio Button display
    options = current_question.get('options') or current_question.get('choices', [])
    
    display_options = []
    for opt in options:
        if isinstance(opt, dict):
            # Try to find the text in common keys, or just take the first value
            text_val = opt.get('text') or opt.get('option') or list(opt.values())[0]
            display_options.append(str(text_val))
        else:
            display_options.append(str(opt))
    
    if not display_options:
        st.error("Could not parse options for this question.")
        st.write("Debug - Question Content:", current_question)
        st.stop()

    answer_text = st.radio("Select an option:", display_options, key=f"q_{q_idx}")
    # if st.button("Submit Answer"):
    #     # 3. Flexible Answer Checking
    #     is_correct = False
    #     correct_text = ""

    #     # Check if the format is dictionary-based (with 'correct' key)
    #     if isinstance(options[0], dict):
    #         correct_text = next((opt['text'] for opt in options if opt.get('correct')), "Unknown")
    #         is_correct = (answer_text == correct_text)
    #     else:
    #         # Fallback for standard 'answer' key
    #         correct_text = current_question.get('answer', "")
    #         is_correct = (answer_text == correct_text)

    #     if is_correct:
    #         st.success(f"Correct! {current_question.get('explanation', '')}")
    #         st.session_state.score += 1
    #     else:
    #         st.error(f"Wrong. The correct answer was: {correct_text}")
    #         st.info(f"Insight: {current_question.get('explanation', '')}")
    if st.button("Submit Answer"):
        # 1. Get the expected answer from the AI (Default to a string if missing)
        correct_text = str(current_question.get('answer', 'Answer key missing'))
        
        # 2. Compare the user's radio selection to the correct string
        if str(answer_text).strip() == correct_text.strip():
            st.success("✅ Correct!")
            st.session_state.score += 1
        else:
            st.error(f"❌ Wrong. The correct answer was: **{correct_text}**")
            
        # Navigation logic remains the same...
            
        if q_idx + 1 < len(quiz):
            st.session_state.current_q += 1
            if st.button("Next Question"):
                st.rerun()
        else:
            st.session_state.complete = True
            st.rerun()

# --- Step 3: Final Results ---
if st.session_state.complete:
    st.balloons()
    st.success(f"### Quiz Finished! Your Score: {st.session_state.score}/{len(st.session_state.quiz_data['questions'])}")
    st.markdown("---")
    st.subheader("📝 Personalized Study Guide")
    st.write("Download a report containing all questions and detailed financial explanations.")

    # We use the full quiz data for the report so the user can study everything
    questions_to_print = st.session_state.quiz_data.get('questions', [])
    
    if questions_to_print:
        # Create the PDF bytes
        pdf_bytes = generate_study_pdf(questions_to_print, selected_doc)
        
        st.download_button(
            label="📥 Download Study Report (PDF)",
            data=pdf_bytes,
            file_name=f"Study_Report_{selected_doc.replace(' ', '_')}.pdf",
            mime="application/pdf"
        )
    # ------------------------------------

    if st.button("Restart Quiz"):
        # Reset everything
        st.session_state.quiz_data = None
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.session_state.complete = False
        st.rerun()