import streamlit as st
import pandas as pd
import re
from datetime import date, datetime
from typing import List

# Predefined goal types for goal creation
goal_types = [
    "Retirement Planning",
    "Education Funding",
    "Home Ownership",
    "Wealth Accumulation",
    "Emergency Fund",
    "Estate Planning",
    "Health Care Planning",
    "Debt Management",
    "Insurance Coverage",
    "Tax Planning",
    "Investment Strategy",
    "Business Ownership",
]

# Function to validate UK phone numbers
def is_valid_uk_phone(number):
    phone_pattern = re.compile(r"^(\+44\s?7\d{3}|\(?07\d{3}\)?)\s?\d{3}\s?\d{3}$")
    return bool(phone_pattern.match(number))

# Function to format a valid UK phone number
def format_uk_phone(number):
    cleaned_number = re.sub(r'\D', '', number)

    if len(cleaned_number) == 11 and cleaned_number.startswith("07"):
        return f"{cleaned_number[:5]} {cleaned_number[5:8]} {cleaned_number[8:]}"
    elif len(cleaned_number) == 12 and cleaned_number.startswith("447"):
        return f"+44 {cleaned_number[2:5]} {cleaned_number[5:8]} {cleaned_number[8:]}"
    else:
        return number

# Function to initialize session state with default values
def initialize_session_state():
    if "goals" not in st.session_state:
        st.session_state["goals"] = []
    if "goal_type" not in st.session_state:
        reset_goal_inputs()
    if "title" not in st.session_state:
        st.session_state["title"] = "Mr"

# Function to reset goal input fields in session state
def reset_goal_inputs():
    st.session_state["goal_type"] = goal_types[0]
    st.session_state["goal_value"] = 1000
    st.session_state["timescale"] = "1 year"
    st.session_state["notes"] = ""

# Function to create a new goal object
def create_new_goal(goal_type, goal_value, timescale, notes):
    return {
        "Goal Type": goal_type,
        "Goal Value": goal_value,
        "Timescale": timescale,
        "Notes": notes,
    }

# Main function for the Streamlit app
def main():
    st.set_page_config(page_title="Contact Us Form", layout="centered")

    # Initialize session state
    initialize_session_state()

    # Contact form header - centered using markdown with HTML
    st.markdown("<h1 style='text-align: center;'>Contact us</h1>", unsafe_allow_html=True)

    # Collecting user details
    col1, col2, col3 = st.columns(3)
    with col1:
        title = st.selectbox("Title*", ["Mr", "Mrs", "Ms", "Dr"], index=["Mr", "Mrs", "Ms", "Dr"].index(st.session_state["title"]))
        st.session_state["title"] = title
    with col2:
        first_name = st.text_input("First Name*")
    with col3:
        surname = st.text_input("Surname*")

    # Collecting phone number and email
    col4, col5 = st.columns(2)
    with col4:
        phone_number = st.text_input("Phone Number*", help="Enter a UK phone number.")

    with col5:
        email = st.text_input("E-mail*", help="Enter a valid email address.")

    # Additional information fields
    col6, col7 = st.columns(2)
    with col6:
        company = st.text_input("Company (if applicable)")
    with col7:
        nationality = st.text_input("Nationality*", help="Enter your nationality.")

    # Date of birth and post code
    col8, col9 = st.columns(2)
    with col8:
        date_of_birth = st.date_input("Date of Birth*", min_value=date(1900, 1, 1), max_value=datetime.today().date())
    with col9:
        post_code = st.text_input("Post Code*", help="Enter your postal code.")

    # Client status and preferred contact method
    col10, col11 = st.columns([1, 1])
    with col10:
        existing_client = st.radio("Are you an existing client?", ["Yes", "No"], index=None)
        if existing_client == "Yes":
            st.info("As you are an existing client, please get in touch with your Adviser or Point of Contact directly or via the portal: www.myportal.centology.io.")

    with col11:
        preferred_contact = st.radio("Preferred Method of Contact", ["E-mail", "Phone"], index=None)

    # Preferred contact time and referral information
    contact_col, referral_col = st.columns(2)
    with contact_col:
        contact_option = st.radio("When would you like to be contacted?", ["Anytime", "Specific Day and Time"], index=None)

        if contact_option == "Specific Day and Time":
            weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            contact_day = st.selectbox("Preferred Contact Day", weekdays)

            col_hour, col_minute = st.columns([1, 1])
            with col_hour:
                contact_hour = st.selectbox("Preferred Hour", list(range(9, 18)))
            with col_minute:
                contact_minute = st.selectbox("Preferred Minute", [0, 15, 30, 45])

            st.info(f"You prefer to be contacted on {contact_day} at {contact_hour}:{contact_minute}.")

    with referral_col:
        referred = st.radio("Have you been referred?", ["Yes", "No"], index=None)
        if referred == "Yes":
            referral_source = st.text_input("Please let us know who has referred you?")
            specific_adviser = st.text_input("Have you been referred to a specific adviser?")

    # Aligning "Goals" header to the center
    st.markdown("<h1 style='text-align: center;'>Goals</h1>", unsafe_allow_html=True)

    # Goals section
    goal_type = st.selectbox("Goal Type", goal_types, index=goal_types.index(st.session_state.get("goal_type", goal_types[0])))
    goal_value = st.number_input("Goal Value (£)", value=st.session_state.get("goal_value £", 1000), min_value=1000, step=50)

    timescale_options = ["1 year", "2 years", "3 years", "4 years", "5 years", "7 years"]
    timescale = st.selectbox("Timescale", timescale_options, index=timescale_options.index(st.session_state.get("timescale", "1 year")))

    notes = st.text_area("Notes", value=st.session_state.get("notes", ""), max_chars=500, help="Max 500 characters")

    # Check if the goal value is above or equal to £1,000
    if goal_value < 1000:
        st.warning("Goal Value must be at least £1,000.")
    else:
        if st.button("Add Goal"):
            if len(st.session_state["goals"]) < 10:
                if any(goal["Goal Type"] == goal_type for goal in st.session_state["goals"]):
                    st.warning("This goal type already exists. Please choose a new goal type.")
                else:
                    new_goal = create_new_goal(goal_type, goal_value, timescale, notes)
                    st.session_state["goals"].append(new_goal)
                    reset_goal_inputs()  # Clear inputs after adding a goal
                    st.success("Goal added successfully!")
            else:
                st.warning("Maximum of 10 goals reached.")

    # Displaying the current list of goals
    if st.session_state["goals"]:
        df = pd.DataFrame(st.session_state["goals"])
        df.index += 1  # Start index from 1
        st.table(df)

    # Additional information field
    additional_info = st.text_area("Further Information", max_chars=2000)

    # Form submission and validation
    if st.button("Submit"):
        missing_fields = []
        if not title:
            missing_fields.append("Title")
        if not first_name:
            missing_fields.append("First Name")
        if not surname:
            missing_fields.append("Surname")
        if not phone_number or not is_valid_uk_phone(phone_number):
            missing_fields.append("Phone Number (valid UK number required)")
        if not email or not re.match(r"[^@]+@[^@]+\.[^@]+\.", email):
            missing_fields.append("E-mail (valid email address required)")
        if not post_code:
            missing_fields.append("Post Code")

        # Additional validation for specific day and time contact
        if contact_option == "Specific Day and Time" and contact_day in ["Saturday", "Sunday"]:
            st.warning("Cannot select a weekend for contact.")

        if missing_fields:
            st.warning(f"Please correct the following fields: {', '.join(missing_fields)}")
        else:
            st.success("Thank you for contacting us! We will reach out to you soon.")

if __name__ == "__main__":
    main()
