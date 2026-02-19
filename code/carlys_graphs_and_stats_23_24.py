import pandas as pd                            # Importing the pandas library for working with datasets.
import matplotlib.pyplot as plt                # Importing the matplotlib library for creating visualizations. 
import seaborn as sns                          # Importing the seaborn library for creating statistical graphics.    
from wordcloud import WordCloud, STOPWORDS     # Importing the WordCloud library for generating word clouds.   
import numpy as np                             # Importing the numpy library for numerical operations.
from scipy import stats                        # Importing the stats module from scipy for statistical analysis.    
import statsmodels.api as sm                   # Importing the statsmodels library for statistical modeling and analysis.
sns.set_style("whitegrid")                     # Setting the style for seaborn plots to "whitegrid" for better aesthetics. 



# Loads the CSV File into a pandas DataFrame and prints all column names in the dataset.
df = pd.read_csv("code/data/23_24_survey.csv")
df.columns = df.columns.str.strip()  # Strips any leading or trailing whitespace from column names.



# Graph one, histogram - sense of belonging on a scale of 1-10.
belonging_column = "On a scale to 1-10 how would your rate your sense of belonging / connection to Grand View University"

plt.figure()
df[belonging_column].plot(
    kind = "hist", 
    bins = 10,
    color = "pink", 
    edgecolor = "black")
plt.title("Distribution of Sense of Belonging")
plt.xlabel("Belonging Rating (1-10)")
plt.ylabel("Number of Students")
plt.show()



# Graph two, bar chart - overall housing satisfaction.
satisfaction_column = "How would you rate your overall satisfaction in regards to living on campus?"

plt.figure()
df[satisfaction_column].value_counts().plot(
    kind = "bar",
    color = "pink",
    edgecolor = "black")
plt.title("Overall Housing Satisfaction")
plt.xlabel("Satisfaction Level")
plt.ylabel("Number of Students")
plt.xticks(rotation = 45)
plt.show()



# Graph three, stack bar chart - community belonging question (likert).
community_column = "Please read the following statements regarding the community on campus and rate them. [I feel a strong sense of community among the people living in my residence hall]"

plt.figure()
community_counts = df[community_column].value_counts().sort_index().plot(
    kind = "bar", 
    color = "pink", 
    edgecolor = "black")
plt.title("Sense of Community in Residence Halls")
plt.xlabel("Response (1-5)")
plt.ylabel("Number of Students")
plt.xticks(rotation = 45)
plt.show()



# Graph four, stacked bar chart - safety at night. 
safety_column = "Please read the following statements regarding safety and rate them. [I feel safe walking alone on campus at night]"

plt.figure()
df[safety_column].value_counts().sort_index().plot(
    kind = "bar", 
    color = "pink", 
    edgecolor = "black")
plt.title("Feeling Safe Walking Alone at Night")
plt.xlabel("Response (1-5)")
plt.ylabel("Number of Students")
plt.xticks(rotation = 45)
plt.show()



# Graph five, box plot - belonging by residence hall.
residence_hall_column = "Which Residence Hall did you live in during the fall semester?"

plt.figure()
sns.boxplot(data=df, x=residence_hall_column, y=belonging_column, color="pink")
plt.title("Sense of Belonging by Residence Hall")
plt.xlabel("Residence Hall")
plt.ylabel("Belonging Rating (1-10)")
plt.xticks(rotation = 45)
plt.show()



# Graph six, word cloud - disklikes about living on campus.
dislikes_column = "What do you dislike about living on campus?"

# Combine all text responses into one string.
text = " ".join(df[dislikes_column].dropna().astype(str))

# Define stopwords to exclude common words that don't add much meaning to the word cloud.
custom_stopwords = set(STOPWORDS)
custom_stopwords.update(["living", "campus", "like", "dislike", "people", "residence", 
                         "hall", "dorms", "dormitory", "options", "sometimes", "much", "lot", "really", 
                         "usually", "schedule", "yet", "room", "general", "ridiculous", "odd", "used", 
                         "random", "motivation", "many"])

# Generates the word cloud.
word_cloud = WordCloud(width = 800, height = 400, background_color = "white", stopwords=custom_stopwords).generate(text)

# Displays the word cloud.
plt.figure(figsize=(10,5))
plt.imshow(word_cloud, interpolation = 'bilinear')
plt.axis("off")
plt.title("Common Dislikes About Living on Campus")
plt.show()



# Column names used often.
belonging_column = "On a scale to 1-10 how would your rate your sense of belonging / connection to Grand View University"
residence_hall_column = "Which Residence Hall did you live in during the fall semester?"
athlete_column = "Do you participate on a Grand View Athletic Team?"
class_column = "What is your current class standing?"
community_column = "Please read the following statements regarding the community on campus and rate them. [I feel a strong sense of community among the people living in my residence hall]"
safety_column = "Please read the following statements regarding safety and rate them. [I feel safe walking alone on campus at night]"
ra_column = "Please read the following statements regarding your fall semester RA and rate them. [It is easy to get in contact with my RA]"
facilities_column = "Please read the following statements regarding the facilities and rate them. [The facilities in my residence hall are well-maintained]"
dining_column = "Please read the following statements regarding dining and rate them. [The dining options on campus are satisfactory]"

# Descriptitive statstics. 
print("\n=== Descriptive Statistics ===")
print("Mean belonging:", f"{df[belonging_column].mean():.2f}")
print("Median belonging:", f"{df[belonging_column].median():.2f}")
print("Mode belonging:", f"{df[belonging_column].mode()[0]:.2f}")

std_val = df[belonging_column].std()
print(f"Standard deviation belonging: {std_val:.2f}")
print("Minimum belonging:", f"{df[belonging_column].min():.2f}")
print("Maximum belonging:", f"{df[belonging_column].max():.2f}")
print("\n")