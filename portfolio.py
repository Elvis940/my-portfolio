# portfolio.py
import streamlit as st
from streamlit.components.v1 import html
import json
from datetime import datetime

# Set page config FIRST (only once, at the top)
st.set_page_config(
    page_title="My Portfolio",
    page_icon="👨‍💻",
    layout="wide"
)

# Custom CSS for animations and styling
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("styles/styles.css")

# Load data
with open("data/data.json") as f:
    data = json.load(f)

# Session State for customization
if 'profile' not in st.session_state:
    st.session_state.profile = data["profile"]
    
# Helper functions
def timeline():
    st.subheader("Academic Timeline 🚀")
    
    # Custom CSS for timeline
    st.markdown("""
    <style>
    .timeline-item {
        background-color: var(--background-color);
        border: 2px solid #4CAF50; /* Green border for visibility */
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        transition: transform 0.3s ease;
    }
    .timeline-item:hover {
        transform: translateX(10px);
    }
    .timeline-item h4 {
        color: var(--primary-text-color);
        margin-bottom: 10px;
    }
    .timeline-item p {
        color: var(--secondary-text-color);
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Timeline items with icons
    for event in data["timeline"]:
        with st.container():
            st.markdown(f"""
            <div class="timeline-item">
                <h4>🎓 {event['year']}</h4>
                <p>{event['event']}</p>
            </div>
            """, unsafe_allow_html=True)
def projects_section():
    st.subheader("Projects 🚀")
    category = st.selectbox("Filter Projects", ["All", "Year 1", "Year 2", "Year 3", "Dissertation"])
    
    filtered_projects = [p for p in data["projects"] 
                        if category.lower() in p['type'].lower() or category == "All"]
    
    for project in filtered_projects:
        with st.expander(f"{project['title']} ({project['type']})"):
            cols = st.columns([3,1])
            with cols[0]:
                st.markdown(f"**Description**: {project['description']}")
                st.markdown(f"**Technologies**: {', '.join(project['tech'])}")
            with cols[1]:
                if project['link']:
                    st.markdown(f"[View Code]({project['link']})")

# Home Section

def home():
    st.title("my-portfolio")
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image("asset/profile.jpg", width=200)   
        
    with col2:
        st.title(st.session_state.profile['name'])
        st.markdown(f"📍 {st.session_state.profile['location']}")
        st.markdown(f"🎓 {st.session_state.profile['university']}")
        st.markdown(f"{st.session_state.profile['degree']}")
        
        # Resume Download Button
        with open("asset/resume.pdf", "rb") as f:
            st.download_button(
                label="📄 Download Resume",
                data=f,
                file_name="resume.pdf",
                mime="application/octet-stream"
            )
        
        
    st.markdown(f"### About Me\n{st.session_state.profile['bio']}")
# Skills Section
def skills():
    st.subheader("Technical Skills 💻")
    for skill in data["skills"]:
        st.markdown(f"**{skill['name']}**")
        st.progress(skill['level'])
    
    st.subheader("Achievements 🏆")
    for achievement in data["achievements"]:
        st.markdown(f"- {achievement}")

# Contact Section
def contact():
    st.subheader("Get in Touch 📬")
    
    # Initialize session state for form fields
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'email' not in st.session_state:
        st.session_state.email = ""
    if 'message' not in st.session_state:
        st.session_state.message = ""
    
    with st.form("contact_form"):
        name = st.text_input("Name", value=st.session_state.name)
        email = st.text_input("Email", value=st.session_state.email)
        message = st.text_area("Message", value=st.session_state.message)
        submitted = st.form_submit_button("Send Message")
        
        if submitted:
            # Validate fields
            if not name or not email or not message:
                st.warning("Fields cannot be empty!")
            else:
                
                st.success("Message sent successfully!")
                
                # Clear the form fields
                st.session_state.name = ""
                st.session_state.email = ""
                st.session_state.message = ""
    
    # Display the social links
    st.markdown("### Connect with Me")
    cols = st.columns(4)
    
    socials = {
        "linkedin": "https://linkedin.com/in/Elvis",
        "github": "https://github.com/Elvis940",
        "email": "mailto:harmonelvis78@gmail.com",
        "facebook": "https://www.facebook.com/profile.php?id=100089809514352",
        
    }
    
    icons = {
        "linkedin": "👔",
        "github": "🐙",
        "email": "📧",
        "facebook": "📘",
        
    }
    
    for i, (platform, link) in enumerate(socials.items()):
        cols[i % 4].markdown(f"{icons[platform]} [{platform.capitalize()}]({link})")

# Main App
def main():
    menu = ["Home", "Projects", "Skills", "Contact", "Customize"]
    choice = st.sidebar.selectbox(" 📌 Navigation", menu)
    
    if choice == "Home":
        home()
        timeline()
    elif choice == "Projects":
        projects_section()
    elif choice == "Skills":
        skills()
    elif choice == "Contact":
        contact()
    elif choice == "Customize":
        st.subheader("Profile Setting Up 🎨")
        with st.form("profile_form"):
            new_name = st.text_input("Name", st.session_state.profile['name'])
            new_bio = st.text_area("Bio", st.session_state.profile['bio'])
            
            new_profile_pic = st.file_uploader("Upload a new profile picture", type=["jpg", "jpeg", "png"])
            
            if st.form_submit_button("Update Profile"):
                st.session_state.profile['name'] = new_name
                st.session_state.profile['bio'] = new_bio
                
        
                if new_profile_pic is not None:
                    with open("asset/profile.jpg", "wb") as f:
                        f.write(new_profile_pic.getbuffer())
                    st.session_state.profile['profile_pic'] = "asset/profile.jpg"
                
                st.success("Profile updated successfully!")
        
        # Display the current profile picture
        if 'profile_pic' in st.session_state.profile:
            st.image(st.session_state.profile['profile_pic'], width=200, caption="Current Profile Picture")

if __name__ == "__main__":
    main()