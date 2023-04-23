import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def read_grants_from_csv(file_name):
    grant_data = []

    with open(file_name, mode="r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            grant_data.append(row)

    return grant_data


def recommend_grants(user_description, grant_data, top_n=5):
    grant_descriptions = [
        grant["description"] + " " + grant["foundation_name"] + " " + grant["tags"]
        for grant in grant_data
    ]
    grant_descriptions.insert(0, user_description + " " + "user_project_description")

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(grant_descriptions)

    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    recommended_grants_indices = cosine_sim.argsort()[0][-top_n:]
    recommended_grants_scores = sorted(cosine_sim[0], reverse=True)[:top_n]
    recommended_grants = [grant_data[i] for i in recommended_grants_indices[::-1]]

    return recommended_grants, recommended_grants_scores


if __name__ == "__main__":
    grant_data = read_grants_from_csv("backend/grants.csv")

    user_project_description = input("Please enter your project description: ")
    top_n = 5  # Number of grants to recommend

    recommended_grants, recommended_grants_scores = recommend_grants(
        user_project_description, grant_data, top_n
    )

    print("\nTop", top_n, "recommended grants:")
    for i, (grant, score) in enumerate(
        zip(recommended_grants, recommended_grants_scores)
    ):
        print(
            f"\n   Grant: {grant['grant_name']}"
            f"\n   Score: {score}"
            f"\n   descr: {grant['description']}"
            f"\n   Foundation: {grant['foundation_name']}"
            f"\n   Link: {grant['details_link']}"
            f"\n Grant Prize: {grant['grant_prize']}"
            f"\n   Tags: {grant['tags']}"
        )


# import csv
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity


# def read_grants_from_csv(file_name):
#     grant_data = []

#     with open(file_name, mode="r") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             grant_data.append(row)

#     return grant_data


# def recommend_grants(user_description, chain_keyword, grant_data, top_n=5):
#     grant_descriptions = [
#         grant["description"] + " " + grant["foundation_name"] + " " + grant["tags"]
#         for grant in grant_data
#     ]
#     grant_descriptions.insert(0, user_description + " " + "user_project_description")

#     # Add chain keyword with 10% more weightage
#     chain_descriptions = [chain_keyword] * len(grant_data)
#     chain_descriptions.insert(0, chain_keyword + " user_project_chain")

#     vectorizer = TfidfVectorizer(stop_words="english")
#     tfidf_matrix = vectorizer.fit_transform(grant_descriptions + chain_descriptions)

#     # Get index of the user input in the tfidf_matrix
#     user_index = tfidf_matrix.shape[0] - len(chain_descriptions)

#     cosine_sim = cosine_similarity(
#         tfidf_matrix[user_index : user_index + 1], tfidf_matrix[: user_index + 1]
#     )

#     # Exclude the user input from the recommended grants
#     recommended_grants_indices = cosine_sim.argsort()[0][-(top_n + 1) : -1]
#     recommended_grants_scores = sorted(
#         cosine_sim[0][recommended_grants_indices], reverse=True
#     )
#     recommended_grants = [grant_data[i] for i in recommended_grants_indices[::-1]]

#     return recommended_grants, recommended_grants_scores


# if __name__ == "__main__":
#     grant_data = read_grants_from_csv("grants.csv")

#     user_project_description = input("Please enter your project description: ")
#     user_project_chain = input("Please enter your project chain keyword: ")
#     top_n = 5  # Number of grants to recommend

#     recommended_grants, recommended_grants_scores = recommend_grants(
#         user_project_description, user_project_chain, grant_data, top_n
#     )

#     print("\nTop", top_n, "recommended grants:")
#     for i, (grant, score) in enumerate(
#         zip(recommended_grants, recommended_grants_scores)
#     ):
#         print(
#             f"\n   Grant: {grant['grant_name']}"
#             f"\n   Score: {score}"
#             f"\n   Description: {grant['description']}"
#             f"\n   Foundation: {grant['foundation_name']}"
#             f"\n   Link: {grant['details_link']}"
#             f"\n   Grant Prize: {grant['grant_prize']}"
#             f"\n   Tags: {grant['tags']}"
#         )
