import secrets
import string

import streamlit as st


SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?/|~"


def generate_password(length, use_uppercase, use_lowercase, use_numbers, use_symbols):
    """Generate a password containing each selected character type."""
    character_groups = []

    if use_uppercase:
        character_groups.append(string.ascii_uppercase)
    if use_lowercase:
        character_groups.append(string.ascii_lowercase)
    if use_numbers:
        character_groups.append(string.digits)
    if use_symbols:
        character_groups.append(SYMBOLS)

    if not character_groups:
        raise ValueError("Select at least one character type.")
    if length < len(character_groups):
        raise ValueError(
            "Choose a longer password or select fewer character types."
        )

    password_characters = [secrets.choice(group) for group in character_groups]
    all_characters = "".join(character_groups)

    while len(password_characters) < length:
        password_characters.append(secrets.choice(all_characters))

    secrets.SystemRandom().shuffle(password_characters)
    return "".join(password_characters)


def check_password_strength(password):
    """Return a simple strength label and suggestions."""
    categories = [
        any(character.islower() for character in password),
        any(character.isupper() for character in password),
        any(character.isdigit() for character in password),
        any(not character.isalnum() for character in password),
    ]
    category_count = sum(categories)
    suggestions = []

    if len(password) < 8:
        suggestions.append("Use at least 8 characters.")
    if category_count < 3:
        suggestions.append(
            "Mix uppercase and lowercase letters, numbers, and symbols."
        )

    if len(password) >= 12 and category_count >= 3:
        strength = "Strong"
    elif len(password) >= 8 and category_count >= 2:
        strength = "Medium"
    else:
        strength = "Weak"

    if strength == "Weak" and not suggestions:
        suggestions.append("Use a longer password and include more character types.")

    return strength, suggestions


def generate_from_settings():
    """Streamlit button callback for generating a password."""
    try:
        st.session_state["password_input"] = generate_password(
            st.session_state["length"],
            st.session_state["uppercase"],
            st.session_state["lowercase"],
            st.session_state["numbers"],
            st.session_state["symbols"],
        )
        st.session_state["generation_error"] = ""
    except ValueError as error:
        st.session_state["password_input"] = ""
        st.session_state["generation_error"] = str(error)


def reset_settings():
    """Restore the initial settings and clear the password."""
    st.session_state["length"] = 16
    st.session_state["uppercase"] = True
    st.session_state["lowercase"] = True
    st.session_state["numbers"] = True
    st.session_state["symbols"] = True
    st.session_state["password_input"] = ""
    st.session_state["generation_error"] = ""


st.set_page_config(
    page_title="Password Studio",
    page_icon="🔐",
    layout="centered",
)

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(145deg, #f3f7fc 0%, #edf2f8 100%);
    }
    .block-container {
        max-width: 820px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }
    .hero {
        padding: 1.7rem 2rem;
        margin-bottom: 1.5rem;
        border-radius: 20px;
        color: white;
        background: linear-gradient(120deg, #102a43, #176b87);
        box-shadow: 0 12px 30px rgba(16, 42, 67, 0.16);
    }
    .hero h1 {
        margin: 0;
        color: white;
        font-size: 2rem;
    }
    .hero p {
        margin: 0.5rem 0 0;
        color: #d7e9f2;
        font-size: 1rem;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.92);
        box-shadow: 0 5px 16px rgba(16, 42, 67, 0.05);
    }
    .stButton > button {
        min-height: 2.8rem;
        border-radius: 10px;
        font-weight: 600;
    }
    div[data-testid="stCode"] {
        border: 1px solid #dce5ef;
        border-radius: 12px;
    }
    @media (max-width: 600px) {
        .block-container {
            padding: 1.2rem 1rem 2rem;
        }
        .hero {
            padding: 1.3rem;
        }
        .hero h1 {
            font-size: 1.6rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

for key, default in (
    ("length", 16),
    ("uppercase", True),
    ("lowercase", True),
    ("numbers", True),
    ("symbols", True),
    ("password_input", ""),
    ("generation_error", ""),
):
    st.session_state.setdefault(key, default)

st.markdown(
    """
    <div class="hero">
        <h1>🔐 Password Studio</h1>
        <p>Create a secure password and check its basic strength in one place.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.subheader("Build your password")
    st.slider("Password length", min_value=4, max_value=64, key="length")

    st.caption("Choose the character types to include:")
    option_columns = st.columns(2)
    with option_columns[0]:
        st.checkbox("Uppercase letters (A–Z)", key="uppercase")
        st.checkbox("Numbers (0–9)", key="numbers")
    with option_columns[1]:
        st.checkbox("Lowercase letters (a–z)", key="lowercase")
        st.checkbox("Special characters (!@#…)", key="symbols")

    button_columns = st.columns([3, 1])
    with button_columns[0]:
        st.button(
            "Generate password",
            type="primary",
            use_container_width=True,
            on_click=generate_from_settings,
        )
    with button_columns[1]:
        st.button(
            "Reset",
            use_container_width=True,
            on_click=reset_settings,
        )

if st.session_state["generation_error"]:
    st.error(st.session_state["generation_error"])

if st.session_state["password_input"]:
    with st.container(border=True):
        st.subheader("Your generated password")
        st.caption("Use the copy button on the password box, or select the text field.")
        st.code(st.session_state["password_input"], language=None)

with st.container(border=True):
    st.subheader("Check password strength")
    password_to_check = st.text_input(
        "Enter or edit a password to check",
        key="password_input",
        type="password",
        help="The password is checked in this app and is not sent to an external service.",
    )

    if password_to_check:
        strength, suggestions = check_password_strength(password_to_check)
        if strength == "Strong":
            st.success("Strength: Strong")
        elif strength == "Medium":
            st.warning("Strength: Medium")
        else:
            st.error("Strength: Weak")

        if suggestions:
            st.markdown("**Suggestions to improve it**")
            for suggestion in suggestions:
                st.markdown(f"- {suggestion}")
        else:
            st.caption("This password meets the basic checks.")
    else:
        st.caption("Enter a password above or generate one to see its strength.")

st.caption(
    "Educational checker only: it uses length and character variety, "
    "not checks against common or previously exposed passwords."
)
