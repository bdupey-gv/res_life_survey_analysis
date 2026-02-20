import pandas as pd                            # Importing the pandas library for working with datasets.
import matplotlib.pyplot as plt                # Importing the matplotlib library for creating visualizations. 
import seaborn as sns                          # Importing the seaborn library for creating statistical graphics.    
from wordcloud import WordCloud, STOPWORDS     # Importing the WordCloud library for generating word clouds.   
import numpy as np                             # Importing the numpy library for numerical operations.
from scipy import stats                        # Importing the stats module from scipy for statistical analysis.    
import statsmodels.api as sm                   # Importing the statsmodels library for statistical modeling and analysis.
sns.set_style("whitegrid")                     # Setting the style for seaborn plots to "whitegrid" for better aesthetics. 
from collections import Counter                # Importing the Counter class from the collections module for counting hashable objects, used for word frequency analysis.



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
plt.savefig("belonging_histogram.png", dpi=300, bbox_inches='tight')  
plt.show()
plt.close()



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
plt.savefig("housing_satisfaction_bar.png", dpi=300, bbox_inches='tight')  
plt.show()
plt.close()


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
plt.savefig("community_belonging_bar.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()



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
plt.savefig("safety_at_night_bar.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()



# Graph five, box plot - belonging by residence hall.
residence_hall_column = "Which Residence Hall did you live in during the fall semester?"

plt.figure()
sns.boxplot(data=df, x=residence_hall_column, y=belonging_column, color="pink")
plt.title("Sense of Belonging by Residence Hall")
plt.xlabel("Residence Hall")
plt.ylabel("Belonging Rating (1-10)")
plt.xticks(rotation = 45)
plt.savefig("belonging_by_hall_boxplot.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()



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
word_cloud = WordCloud(width = 800, height = 400, background_color = "white", stopwords=custom_stopwords, colormap = "pink").generate(text)

# Displays the word cloud.
plt.figure(figsize=(10,5))
plt.imshow(word_cloud, interpolation = 'bilinear')
plt.axis("off")
plt.title("Common Dislikes About Living on Campus")
plt.savefig("dislikes_wordcloud.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()


print("\n" + "="*50)
print("RESIDENCE LIFE SURVEY SUMMARY (2023-2024)")
print("="*50)



from collections import Counter

filtered_words = [
    word for word in text.lower().split()
    if word not in custom_stopwords and len(word) > 3
]

word_counts = Counter(filtered_words)

print("\n=== Top 10 Dislike Themes ===")
for word, count in word_counts.most_common(10):
    print(f"{word}: {count}")


# Column names used often.
belonging_column = "On a scale to 1-10 how would your rate your sense of belonging / connection to Grand View University"
residence_hall_column = "Which Residence Hall did you live in during the fall semester?"
athlete_column = "Do you participate on a Grand View Athletic Team?"
class_column = "What is your current class standing?"
community_column = "Please read the following statements regarding the community on campus and rate them. [I feel a strong sense of community among the people living in my residence hall]"
safety_column = "Please read the following statements regarding safety and rate them. [I feel safe walking alone on campus at night]"
ra_column = "Please read the following statements regarding your fall semester RA and rate them. [It is easy to get in contact with my RA]"
facilities_column = 'Please read the following statements regarding Residence Life Facilities & Services and rate them. [I feel satisfied with the cleanliness of my residence hall]'
dining_column = 'Please read the following statements regarding GV Dining and rate them. [I feel satisfied with the food quality on campus]'



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



# Map Linkert scale responses to numeric values for correlation analysis.
likert_map = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

likert_columns = [
    community_column,
    safety_column,
    ra_column,
    facilities_column,
    dining_column
]




# Convert Likert scale responses to numeric values for correlation analysis.
for col in likert_columns:
    df[col] = df[col].map(likert_map)

correlation_columns = likert_columns + [belonging_column]




# Filter students with low sense of belonging (5 or lower) and calculate the percentage.
low_belonging = df[df[belonging_column] <= 5]




# Calculate the percentage of students with low sense of belonging.
total_students = len(df)
percent_low = (len(low_belonging) / total_students) * 100
print(f"{percent_low:.1f}% of students report belonging 5 or lower.")




# Create and displays correlation heatmap.
sns.heatmap(df[correlation_columns].corr(), annot=True, cmap = "pink")
plt.title("Correlation Matrix")
plt.title("Correlation Matrix")
plt.savefig("correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.show()
plt.close()



# Runs Regression Analysis. 
X = df[[community_column, safety_column, ra_column, facilities_column, dining_column]]
X = sm.add_constant(X)
y = df[belonging_column]

model = sm.OLS(y, X, missing='drop').fit()
print("\n=== Key Predictors of Belonging ===")

coefficients = model.params.round(3)
pvalues = model.pvalues.round(3)

for var in coefficients.index[1:]: 
    print(f"{var[:40]}...")
    print(f"  Coefficient: {coefficients[var]}")
    print(f"  P-value: {pvalues[var]}\n")

print(f"Model R-squared: {model.rsquared:.3f}")



# Identifies at-risk groups based on low belonging.
print("\n=== Belonging by Residence Hall ===")
hall_means = df.groupby(residence_hall_column)[belonging_column].mean().round(2)
for hall, mean in hall_means.items():
    print(f"{hall}: {mean}")



# Converts likert to postive versus negative. 
positive = df[community_column].isin([4,5]).mean()*100
print(f"% Positive community perception: {positive:.1f}%")



# Creates a summary file with key findings.
summary_file = "res_life_survey_summary_23_24.txt"
with open(summary_file, "w") as f:
    f.write("RESIDENCE LIFE SURVEY SUMMARY (2023-2024)\n")
    f.write("="*50 + "\n\n")
    
    f.write("=== Top 10 Dislike Themes ===\n")
    for word, count in word_counts.most_common(10):
        f.write(f"{word}: {count}\n")
    
    f.write("\n=== Descriptive Statistics ===\n")
    f.write(f"Mean belonging: {df[belonging_column].mean():.2f}\n")
    f.write(f"Median belonging: {df[belonging_column].median():.2f}\n")
    f.write(f"Mode belonging: {df[belonging_column].mode()[0]:.2f}\n")
    f.write(f"Standard deviation belonging: {std_val:.2f}\n")
    f.write(f"Minimum belonging: {df[belonging_column].min():.2f}\n")
    f.write(f"Maximum belonging: {df[belonging_column].max():.2f}\n\n")
    
    f.write(f"{percent_low:.1f}% of students report belonging 5 or lower.\n\n")
    
    f.write("=== Key Predictors of Belonging ===\n")
    for var in coefficients.index[1:]: 
        f.write(f"{var[:40]}...\n")
        f.write(f"  Coefficient: {coefficients[var]}\n")
        f.write(f"  P-value: {pvalues[var]}\n\n")
    
    f.write(f"Model R-squared: {model.rsquared:.3f}\n\n")
    
    f.write("=== Belonging by Residence Hall ===\n")
    for hall, mean in hall_means.items():
        f.write(f"{hall}: {mean}\n")
    
    f.write(f"\n% Positive community perception: {positive:.1f}%\n")
print("Summary file created successfully.")