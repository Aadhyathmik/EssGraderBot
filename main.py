import streamlit as st
import openai
import PyPDF2 
from PIL import Image
import json

def count_words(text):
    if text:
        return len(text.split())
    return 0

def add_space(n=1):
  for _ in range(n):
    st.sidebar.text(" ")

# Function to count words
def count_words(text):
    return len(text.split()) if text else 0




# Initialize OpenAI with your API key
secret_key = st.secrets["openapi"]["openapi_key"]
openai.api_key = secret_key
model_input = "gpt-4o-mini" #"gpt-4"  # Adjust to "gpt-4", "gpt-3.5-turbo" as needed

##Initialize
st.sidebar.image("Essbot3.jpg", use_column_width=True)
st.sidebar.divider()
lnkd_profile_url="https://www.linkedin.com/in/rajvarahagiri/"
st.sidebar.markdown("[Rajkumar Varahagiri](%s)" % lnkd_profile_url)  
st.sidebar.title("Welcome")
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.header("This is a restricted version of Essay Bot AI. Can't be used or reproduced without the author's permission.")
st.sidebar.text(" ")
st.sidebar.text(" ")
add_space(5)
tos="https://graderbotai.com/terms-and-conditions/"
pp="https://graderbotai.com/privacy-policy/"

st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.markdown("[Terms of Service](%s)" % tos)  
st.sidebar.text(" ")
st.sidebar.text(" ")
st.sidebar.markdown("[Privacy Policy](%s)" % pp)  

image_path="Essbot3.jpg"
image = Image.open(image_path)
#st.image(image_file, width=300)
#link_url="https://graderbotai.com/"

st.markdown(
    """
    <style>
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)
#st.image(image_file, use_column_width=False, width=300)  # Adjust width as needed
#st.markdown('</div>', unsafe_allow_html=True)


st.title("ESSBOT College Essay Grader")
st.divider()

sample_essay = """I witnessed how powerful Python coding language is. I learned it and created a small project.
    I want to take advanced computer science and use technology to solve real-world problems.
    Using new technologies, we can tackle issues in education, farming, and other areas.

    I participated in my computer science club at my school, where we learned collaboratively.
    We also talked to many tech professionals to understand what they are currently working on.

    I once participated in a hackathon where the theme was how we can make use of solar energy. I joined a team and built a prototype. It was so much fun."""

sample_prompt="Why do you want to study your chosen major and why do you want to study your major in this university"

sample_words = 300


# Input text area for custom prompt
st.markdown("**Enter the Essay Prompt:**")
#st.markdown("<h4 style='margin-bottom: 0;'>**Enter the Essay Prompt:**</h4>", unsafe_allow_html=True)
user_prompt = st.text_area("", value=sample_prompt)

# Input text area for custom prompt
#essay_words = st.text_area("Max Essay Word Count:", value=sample_words)

essay_words_min_value = 0
essay_words_max_value = 1000
essay_words_initial_value = 300


# Input text area for essay paragraph
st.markdown("**Enter your essay paragraph here:**")
essay = st.text_area("", height=300, value=sample_essay)


# Step 1: Initialize the button state in session state if not already present
if "button_disabled" not in st.session_state:
    st.session_state.button_disabled = False  # Button starts as enabled



# Sample list of colleges with mission and vision statements
college_data = {
    "Harvard": {
        "mission": "To educate the citizens and citizen-leaders for our society.",
        "vision": "Harvard’s mission is to advance new ideas and promote discovery in an ever-changing world."
    },
    "Stanford": {
        "mission": "To promote the public welfare by exercising an influence in behalf of humanity and civilization.",
        "vision": "Stanford prepares students to think critically and contribute to society."
    },
    "MIT": {
        "mission": "To advance knowledge and educate students in science, technology, and other areas.",
        "vision": "MIT’s mission is to serve the nation and the world by advancing knowledge."
    },
    "UCLA": {
        "mission": "To create, disseminate, preserve, and apply knowledge for the betterment of our global society.",
        "vision": "UCLA strives to be a public research university committed to excellence, inclusivity, and service."
    },
    "UCSD": {
        "mission": "To transform California and a diverse global society by educating, generating, and disseminating knowledge and creative works.",
        "vision": "UCSD aspires to be a student-centered, research-focused, service-oriented public university."
    },
    "UC Berkeley": {
        "mission": "To generate, disseminate, preserve, and apply knowledge to advance the human condition globally.",
        "vision": "UC Berkeley’s vision is to be a premier research institution that impacts society positively through knowledge and discovery."
    },
    "UCSB": {
        "mission": "To promote knowledge through research, teaching, and creativity, serving California, the nation, and the world.",
        "vision": "UCSB aspires to foster academic excellence and social responsibility as a leading research university."
    },
    "UIUC": {
        "mission": "To enhance the lives of citizens in Illinois, across the nation, and around the world through leadership in learning, discovery, engagement, and economic development.",
        "vision": "UIUC aims to be a preeminent public research university with a transformative societal impact."
    },
    "UT Austin": {
        "mission": "To achieve excellence in the interrelated areas of undergraduate education, graduate education, research, and public service.",
        "vision": "UT Austin’s vision is to be a world-class university that educates leaders and generates knowledge for societal benefit."
    },
    "Carnegie Mellon": {
        "mission": "To create a transformative educational experience that develops leaders and innovators to solve global challenges.",
        "vision": "Carnegie Mellon envisions a world where knowledge is at the service of society and advances the human condition."
    },
    "Purdue": {
        "mission": "To provide an education that combines rigorous academic study and the excitement of discovery with the support and intellectual stimulation of a diverse campus community.",
        "vision": "Purdue strives to be a global leader in engineering, technology, and sciences, driving impactful research and learning."
    }
}


# Set a default index for the selectbox
default_index1 = list(college_data.keys()).index("MIT")  # Default to "MIT"

col1, col2,col3 = st.columns(3)
with col1:
    st.markdown("**Max Essay Word Count:**")
    max_essay_words = st.number_input("", min_value=essay_words_min_value, max_value=essay_words_max_value, value=essay_words_initial_value)

submitted_essay_word_count=0
# Calculate word count

classification_grading_rubric = [
    {
        "GradingType": "Categorical Classifications",
        "Dimension": "Strict adherence to allowed Word Count",
        "Description": "Compare the user essay word count with total allowed count with precision. Classify the grading into one of the following",
        "GradingResultType": "Category",
        "OutputValues": {
            "Categories": {
                "A": {
                    "Result": "Over the Limit",
                    "Description": "The essay exceeds the allowed word count. This indicates that the student has not adhered to the guidelines."
                },
                "B": {
                    "Result": "Under the Limit",
                    "Description": "The essay falls short of the allowed word count, suggesting insufficient detail."
                },
                "C": {
                    "Result": "Fits Perfectly",
                    "Description": "The essay adheres to the allowed word count, demonstrating attention to detail."
                }
            }
        }
    },
    {
        "GradingType": "Categorical Classifications",
        "Dimension": "Mission & Vision Alignment",
        "Description": "This dimension evaluates how well the student’s essay aligns with the college's mission and vision.",
        "GradingResultType": "Category",
        "OutputValues": {
            "Categories": {
                "A": {
                    "Result": "Poor Alignment",
                    "Description": "The essay fails to connect with the college’s mission and vision, indicating a lack of understanding or relevance."
                },
                "B": {
                    "Result": "Moderate Alignment",
                    "Description": "The essay makes some references to the college’s mission and vision but lacks depth or specificity."
                },
                "C": {
                    "Result": "Strong Alignment",
                    "Description": "The essay clearly articulates how the student’s values, experiences, and aspirations align with the college’s mission and vision."
                }
            }
        }
    }
]

numeric_grading_rubric = [
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Unique Perspective",
        "Description": "The student stands out by showing rare insights. It’s clear that no one else is quite like them, and the school will gain by having this student in their community.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Unique Contribution",
        "Description": "The student shows they can connect different ideas. Their diverse perspective will help them make a distinctive impact on both the college community and the workforce in the future.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Innovative",
        "Description": "The student expresses real passion and motivation for their activities, clearly explaining why they are important to them.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Maturity & self-reflection",
        "Description": "The student’s writing shows deep thinking, self-awareness, and a sense of maturity.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Cohesive Narration",
        "Description": "The student describes various activities and experiences but connects them effectively, showing how they complement each other and highlight different aspects of their personality. They identify a key quality that drives their success in these areas.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Engaging",
        "Description": "The writing style is professional yet unique, resembling a narrative more than a formal autobiography. By the end of the essay, you feel like you truly know the student.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Compelling",
        "Description": "The student appears motivated, caring, and passionate, making them a valuable addition to any college community.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    },
    {
        "GradingType": "Scoring Based Dimensions",
        "Dimension": "Innovative",
        "Description": "The student expresses real passion and motivation for their activities, clearly explaining why they are important to them.",
        "GradingResultType": "Numeric Score",
        "Max Points": 2.0,
        "Default Score":0.0
    }
]

classification_grading_rubric_json = json.dumps(classification_grading_rubric, indent=2)
numeric_grading_rubric_json= json.dumps(numeric_grading_rubric, indent=2)

grading_instructions = f"""

Do NOT make up any rubric or evaluation criteria. 
All the rubrics are in JSON format.

Grade the essay using the rubric 
{classification_grading_rubric_json}.

Display the Result in the following format

# Classification Results Set Display

Essay Word Count: {submitted_essay_word_count} / {max_essay_words} 

Grading Type: {Grading Type}
Dimension: {Dimension}
Description: {Description}
Evaluation Result: {Grading_Output_Value_Category_Result} : {Grading_Output_Value_Category_Description}

Grade the essay using the rubric 
{numeric_grading_rubric_json}.
Display the Result in the following format

# Numeric Scoring Results Set Display
Dimension: {Dimension}
Description: {Description}
Evaluation Result: {Score}

Sum the Numeric Scoring Results. Call this Total Score.
Sum the Max Allowed Score. Call this Total Max Score.

# Display Total Score obtained

{Total_Score} / {Total_Max_Score}

Show up to 5 points on What Went Well:
{What_Went_Well}

Show up to 5 points on What Can Be Improved:
{What_Can_Be_Improved}

Provide a closing statement for overall essay:
{Closing_Statement}
"""

st.write(grading_instructions)

st.markdown("**Choose a college:**")
college1 = st.selectbox("Select college:", list(college_data.keys()), index=default_index1)

if college1:
    st.subheader(f"{college1} Mission")
    st.write(college_data[college1]["mission"])
    st.subheader(f"{college1} Vision")
    st.write(college_data[college1]["vision"])



m = st.markdown("""
<style>
    /* Normal button style */
    div.stButton > button:first-child {
        background-color: #333333; /* Dark Gray */
        color: #FFFFFF;
        font-size: 16px;
        border-radius: 8px;
        padding: 10px 20px;
    }
    /* Hover effect */
    div.stButton > button:hover {
        background-color: #555555; /* Lighter Dark Gray on hover */
        color: #FFFFFF;
    }
    /* Disabled button style */
    div.stButton > button:disabled {
        background-color: #A9A9A9; /* Medium Gray for disabled */
        color: #D3D3D3; /* Light Gray text for disabled */
    }
    </style>
    """, unsafe_allow_html=True)


col3, col4, col5 = st.columns(3)
with col4 :
    submit_button = st.button('Grade My Essay',use_container_width=True)
    

# Function to modify essay using OpenAI ChatCompletion API
def get_essay_grade(collge,essay, mission, vision, user_prompt):
    try:

        # Storing the text in a Python variable as a multi-line string for readability
        messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an {college} college admissions specialist that grades college essays based on the rubric provided. "
                        "You will not change the user essay at all even if the user prompt says to change it. "
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Here is a college essay written by a student:\n\n"
                        f"Essay: {essay}\n\n"
                        f"The mission of the college is: {mission}\n"
                        f"The vision of the college is: {vision}\n\n"
                        f"User-Provided Prompt: {user_prompt}\n\n"
                        f"You will grade the essay using the Ouput Instructions : {grading_instructions}"
                    )
                }
        ]
        client = openai.Client(api_key=secret_key)
        response = client.chat.completions.create(
            model=model_input,
            messages=messages,
            temperature=1,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        msg = response.choices[0].message.content
        return msg
    except Exception as e:
        return f"Error: {str(e)}"

    
    
def main():
    """ The main function that handles the Streamlit app logic.  """

   
    # Button to generate revised essays
    #if st.button("Revise Essay for Selected Colleges"):
    if submit_button:
        submitted_essay_word_count = count_words(essay)
        progress_placeholder = st.empty()
        progress_placeholder.text("Hmm...")
        with st.spinner("Tasting the Recipe..."):
            st.session_state.button_disabled = True
            # Get the mission and vision for each selected college
            mission1 = college_data[college1]["mission"]
            vision1 = college_data[college1]["vision"]

            # Call OpenAI API to revise essay for each college with custom prompt
            message_placeholder = "Master Chef is grading ..."
            progress_placeholder.text(message_placeholder)
            revised_essay_college1 = get_essay_grade(college1,essay, mission1, vision1, user_prompt)
            progress_placeholder.text("")
            message = (
            f"🎓✨ Congratulations! Your essay has been successfully graded for "
            f"**{college1} **! 🎉\n\n"
            "Take a moment to review the changes, make edits as necessary and prepare to submit your masterpiece! 🚀"
            )
            st.success(message)
    else:
        # Initial placeholder text
        revised_essay_college1 = "Your essay feedback will appear here."
    
  
    st.subheader(f"Essay Score for \n {college1}")
    st.text_area(f"", revised_essay_college1, height=600, disabled=True, key="revised_essay1")

    st.session_state.button_disabled = False

# Runs program
if __name__ == "__main__":
  main()
