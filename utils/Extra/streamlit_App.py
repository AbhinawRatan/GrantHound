import streamlit as st


import grant_recommendation

import re


def clean_text(text):
    return re.sub(r"[^\x00-\x7F]+", "", text)


# Load grant data
grant_data = grant_recommendation.read_grants_from_csv("utils/Extra/grants.csv")

# Title and description 
st.title("Grant Finder")
st.write("Find the best grants for your project based on your project description.")

# User input
user_description = st.text_area("Enter your project description:")

# Number of recommendations
top_n = st.slider("Number of recommendations:", 1, 10, 5)

# Get recommendations button
if st.button("Get Recommendations"):
    if user_description:
        (
            recommended_grants,
            recommended_grants_scores,
        ) = grant_recommendation.recommend_grants(user_description, grant_data, top_n)

        # Show results
        for i, (grant, score) in enumerate(
            zip(recommended_grants, recommended_grants_scores)
        ):
            st.write(f"{i+1}. {grant['grant_name']} (Score: {score:.2%})")
            st.write(f"Foundation: {grant['foundation_name']}")
            st.write(f"Description: {clean_text(grant['description'])}")
            st.write(f"Grant prize: {clean_text(grant['grant_prize'])}")
            st.write(f"Tags: {grant['tags']}")
            st.write(f"Details link: {grant['details_link']}")
            st.write("\n")
    else:
        st.write("Please enter a project description.")


# import streamlit as st
# import grant_recommendation

# import re


# def clean_text(text):
#     return re.sub(r"[^\x00-\x7F]+", "", text)


# # Load grant data
# grant_data = grant_recommendation.read_grants_from_csv("grants.csv")

# # Title and description
# st.title("Grant Finder")
# st.write("Find the best grants for your project based on your project description.")

# # User input
# # User input
# user_description = st.text_area("Enter your project description:")
# chain_keyword = st.text_input("Enter your project chain keyword:")

# # Number of recommendations
# top_n = st.slider("Number of recommendations:", 1, 10, 5)

# # Get recommendations button
# if st.button("Get Recommendations"):
#     if user_description:
#         (
#             recommended_grants,
#             recommended_grants_scores,
#         ) = grant_recommendation.recommend_grants(
#             user_description, chain_keyword, grant_data, top_n
#         )

#         # Show results
#         for i, (grant, score) in enumerate(
#             zip(recommended_grants, recommended_grants_scores)
#         ):
#             st.write(f"{i+1}. {grant['grant_name']} (Score: {score:.2%})")
#             st.write(f"Foundation: {grant['foundation_name']}")
#             st.write(f"Description: {clean_text(grant['description'])}")
#             st.write(f"Grant prize: {clean_text(grant['grant_prize'])}")
#             st.write(f"Tags: {grant['tags']}")
#             st.write(f"Details link: https://superteam.fun{grant['details_link']}")
#             st.write("\n")
#     else:
#         st.write("Please enter a project description.")
