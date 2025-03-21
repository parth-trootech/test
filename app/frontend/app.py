import requests
import streamlit as st

# API URLs for login, signup, and image upload
BASE_URL = "http://localhost:8000"


# Function to handle signup
def signup(username, email, password):
    payload = {"user_email": email, "user_password": password}  # Updated field names
    response = requests.post(f"{BASE_URL}/signup", json=payload)

    if response.status_code == 200:
        st.success("Account created successfully!")
    else:
        try:
            # Attempt to parse the JSON response
            error_detail = response.json().get("detail", "Unknown error")
        except requests.exceptions.JSONDecodeError:
            # If JSON parsing fails, print the raw response content for debugging
            error_detail = f"Error: {response.text}"

        st.error(f"Error: {error_detail}")


# Function to handle login
def login(username, password):
    payload = {"username": username, "password": password}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    if response.status_code == 200:
        st.session_state.logged_in = True  # Store login state in session state
        st.session_state.username = username  # Store username in session state
        st.session_state.user_id = response.json().get("user_id")  # Store user_id
        st.session_state.page = "upload"  # Set page to image upload page
    else:
        st.error("Error: " + response.json().get("detail", "Invalid credentials"))


# Streamlit interface for login and signup
def login_signup_page():
    st.title("Login or Signup")

    option = st.radio("Choose an option", ["Login", "Signup"])

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email (only for signup)", disabled=(option != "Signup"))

    if option == "Signup":
        if st.button("Create Account"):
            if username and email and password:
                signup(username, email, password)
            else:
                st.warning("Please fill out all fields.")
    elif option == "Login":
        if st.button("Login"):
            if username and password:
                login(username, password)
            else:
                st.warning("Please fill out all fields.")


# Image Upload Page after login
def image_upload_page():
    st.title(f"Welcome, {st.session_state.username}")
    st.subheader("Upload an Image")

    image = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg"])
    if image is not None:
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Upload Image"):
            response = requests.post(
                f"{BASE_URL}/upload_image",
                data={"user_id": st.session_state.user_id},
                files={"image": image}
            )
            if response.status_code == 200:
                st.success("Image uploaded successfully!")
                image_id = response.json().get("image_id")
                st.session_state.image_id = image_id  # Store image_id
            else:
                st.error("Error uploading image.")


# Prediction Page
def prediction_page():
    st.title(f"Prediction for {st.session_state.username}")
    response = requests.post(f"{BASE_URL}/predict", json={"image_id": st.session_state.image_id})
    if response.status_code == 200:
        result = response.json()
        st.write(f"Predicted Digit: {result['predicted_digit']}")
    else:
        st.error("Error predicting the result.")


# Streamlit interface
def main():
    # Check if the user is logged in
    if 'logged_in' in st.session_state and st.session_state.logged_in:
        if 'page' in st.session_state and st.session_state.page == "upload":
            image_upload_page()  # Show the image upload page
        elif 'page' in st.session_state and st.session_state.page == "predict":
            prediction_page()  # Show the prediction page
    else:
        login_signup_page()  # Show login/signup page if not logged in


if __name__ == "__main__":
    main()
