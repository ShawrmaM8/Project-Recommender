import streamlit as st
import json

# Load projects JSON
with open(r"C:\Users\muzam\OneDrive\Desktop\PROJECTS\project-recommend\projects.json", "r") as f:
    projects = json.load(f)

# Page title
st.title('Project Recommender')
st.subheader('Discover projects that match your skills, goals & interests')

# Sidebar (optional for extra controls in future)
st.sidebar.header("Set your preferences")

# --- FORM START ---
with st.form(key='recommender'):
    # sliders
    pref_complexity = st.slider("Technical Complexity", min_value=0, max_value=10)
    pref_usefulness = st.slider("Usefulness/Practicality", min_value=0, max_value=10)
    pref_scalability = st.slider("Scalability", min_value=0, max_value=10)

    # keywords  
    tags_input = st.text_input('Libraries/Tools used (comma-separated)')
    tags = [tag.strip().lower() for tag in tags_input.split(",") if tag.strip()]

    # ✅ submit button inside the form
    submit = st.form_submit_button("Get Idea")
# --- FORM END ---


# --- SCORING FUNCTION ---
def score_project(proj):
    slider_score = 10 - abs(proj["complexity"] - pref_complexity)
    slider_score += 10 - abs(proj["usefulness"] - pref_usefulness)
    slider_score += 10 - abs(proj["scalability"] - pref_scalability)
    
    tag_score = sum(1 for tag in proj['tags'] if tag.lower() in tags)
    
    weighted_score = slider_score + tag_score * 5
    return weighted_score


# --- RANK + DISPLAY PROJECTS ---
if submit:  # will only run when user presses "Get Idea"
    ranked_projects = sorted(projects, key=score_project, reverse=True)
    
    st.header('Recommended Projects')

    if not ranked_projects:
        st.write('No projects found')
    else:
        for proj in ranked_projects[:10]:
            st.subheader(proj['title'])
            st.write(proj['description'])
            st.write('Tags:', ", ".join(proj['tags']))
            st.write('Complexity:', proj['complexity'])
            st.markdown('---')
