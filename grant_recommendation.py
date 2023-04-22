# # import openai
# # import pandas as pd

# # # Load the grant dataset
# # df = pd.read_csv("grants.csv")

# # # Collect user's project description
# # user_description = "I am working on a project to build a decentralized finance application on the Solana blockchain."

# # # Send the project description to OpenAI API using GPT-3
# # openai.api_key = "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"
# # model_engine = "text-davinci-002"
# # prompt = f"What grants are relevant for a project to build a decentralized finance application on the Solana blockchain?"
# # completions = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024)
# # generated_text = completions.choices[0].text.strip()

# # # Extract relevant keywords from the generated text
# # keywords = list(set(generated_text.split()))

# # # Match the extracted keywords with the grant dataset
# # matches = df[df['description'].str.lower().str.contains('|'.join(keywords))]

# # # Rank the relevant grants based on their match score
# # matches['match_score'] = matches['description'].apply(lambda x: sum([1 for keyword in keywords if keyword in x.lower()]))
# # matches = matches.sort_values('match_score', ascending=False)

# # # Display the top 5 relevant grants to the user
# # print(matches.head(5))




# #  similarity score

# import pandas as pd
# import spacy
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.metrics.pairwise import cosine_similarity

# # Load the grant dataset
# df = pd.read_csv("grants.csv")

# # Collect user's project description and preprocess it
# user_description = "I am working on a project to build a decentralized finance application on the Solana blockchain."
# nlp = spacy.load("en_core_web_sm")
# doc = nlp(user_description)
# keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

# # Extract entities from the user's project description using NER
# entities = [ent.text for ent in doc.ents]

# # Match the user's project description with the grant dataset
# matches = pd.DataFrame()
# for keyword in keywords + entities:
#     matches = pd.concat([matches, df[df.apply(lambda row: keyword in row.values.astype(str).tolist(), axis=1)]])
# matches = matches.drop_duplicates()

# # Calculate the match score between the user's project description and the grants in the dataset
# vectorizer = TfidfVectorizer()
# corpus = [user_description] + matches['description'].tolist()
# tfidf_matrix = vectorizer.fit_transform(corpus)
# similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])[0]
# matches['match_score'] = similarity_scores

# # Rank the relevant grants based on their match score
# matches = matches.sort_values('match_score', ascending=False)

# # Display the top 5 relevant grants to the user
# print(matches.head(5))



import csv
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_grants_from_csv(file_name):
    grant_data = []

    with open(file_name, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grant_data.append(row)

    return grant_data

def recommend_grants(user_description, grant_data, top_n=5):
    grant_descriptions = [grant["description"] for grant in grant_data]
    grant_descriptions.insert(0, user_description)

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(grant_descriptions)

    cosine_sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:])

    recommended_grants_indices = cosine_sim.argsort()[0][-top_n:]
    recommended_grants_scores = sorted(cosine_sim[0], reverse=True)[:top_n]
    recommended_grants = [grant_data[i] for i in recommended_grants_indices[::-1]]

    return recommended_grants, recommended_grants_scores

if __name__ == "__main__":
    grant_data = read_grants_from_csv("grants.csv")

    user_project_description = input("Please enter your project description: ")
    top_n = 5  # Number of grants to recommend

    recommended_grants, recommended_grants_scores = recommend_grants(user_project_description, grant_data, top_n)

    print("\nTop", top_n, "recommended grants:")
    for i, (grant, score) in enumerate(zip(recommended_grants, recommended_grants_scores)):
        print("\n{}. {}\nScore: {:.2%}\nDetails link: {}\nFoundation: {}\nGrant prize: {}\nTags: {}".format(
            i+1, grant["grant_name"], score, grant["details_link"], grant["foundation_name"], grant["grant_prize"], grant["tags"]))
