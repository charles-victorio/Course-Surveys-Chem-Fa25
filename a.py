"""Chem surveys"""


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# only if running as file
dir_of_this_file = os.path.dirname(os.path.realpath(__file__))
if os.getcwd() != dir_of_this_file:
    os.chdir(dir_of_this_file)

dfs = {
    survey_fname.removesuffix('.csv'): pd.read_csv(f"raw_survey_responses/{survey_fname}", header=None)
    for survey_fname in os.listdir('raw_survey_responses')
}

# Turn spreadsheet format into tabular
for survey_name, df in dfs.items():
    # df = dfs['w3s1']
    questions = df.iloc[0]
    options = df.iloc[1]
    data = df.iloc[2:].reset_index(drop=True)
    question_starts = questions[questions.notna()].index.tolist()
    question_starts.append(len(df.columns))  # Add end marker

    # Turn one-hot encoding into a categorical variable
    result_dict = {}
    dense_cols = []
    for i in range(len(question_starts) - 1): # for i, (start_col, end_col) in enumerate(zip(question_starts, question_starts[1:]))
        start_col = question_starts[i]
        end_col = question_starts[i + 1]
        if end_col - start_col == 1: # This is not a one-hot encoding situation
            dense_cols.append(i)
            continue
        
        question_text = questions.iloc[start_col]
        question_cols = list(range(start_col, end_col)) # do I need list? can dataframe slicing work with ranges
        
        # Get the one-hot data
        onehot_data = data.iloc[:, question_cols]
        
        # Convert to categorical using the option labels
        option_labels = options.iloc[question_cols].tolist()
        categorical = onehot_data.apply(
            lambda row: option_labels[row.argmax()], axis=1
        )
        
        result_dict[question_text] = categorical

    final_df = pd.DataFrame(result_dict)
    for i in dense_cols:
        start_col = question_starts[i]
        question_text = questions.iloc[start_col]
        data_of_the_col = data.iloc[:, start_col]
        final_df.insert(i, question_text, data_of_the_col)
    # processed_dfs[survey_name] = final_df
    dfs[survey_name] = final_df

# normalize questions
# this might have to be bidirectional
# first one is canonical
normalized_questions = {
    'Participant ID': 'id',
    'Response Timestamp': 'timestamp',
    'Which course are you completing this survey for?': 'course',
    'What class are you completing this survey for?': 'course',
    'This is survey 2. Which class are you filling this survey out for?': 'course',
    'This is the third survey. What class are you taking this survey for?': 'course',
    "My instructor's name is:": 'instructor',
    "If you are taking a lab, you may have to fill this out for multiple courses--which may be confusing. To be sure that you selected the course you intended to select above, what is your instructor's last name for the above selected course?": 'instructor',
    "Did you attend the Chemistry peer learning in room MS3974 ?": "peer_learning",

    'I am comfortable asking questions in lecture or discussion sections.': 'asking_questions',
    'I am confident in applying mathematical skills to Chemistry problems.': "apply_math",
    'I believe I can improve my Chemistry skills with consistent effort.': 'improve_skills',
    'I believe I can manage my time effectively when studying for Chemistry exams.': 'manage_time',
    'I believe intelligence and ability in Chemistry can be developed over time.': 'develop_intelligence',
    'I believe my contributions in class are valued.': 'contributions_valued',
    'I believe my current study habits will help me perform well in this class.': 'study_habits',
    'I can be myself when interacting with classmates and faculty in Chemistry.': 'be_myself',
    'I can explain Chemistry concepts in my own words.': 'own_words',
    'I can manage my time effectively when studying for Chemistry exams.': 'manage_time',
    'I can motivate myself to keep studying even when the material is difficult.': 'motivate',
    'I expect to earn at least a B in this class.': 'at_least_b',
    'I expect to earn at least a C in this class (C or better).': 'at_least_c',
    'I expect to earn at least a C in this class.': 'at_least_c',
    'I expect to feel more confident in Chemistry by the end of this quarter.': 'confident', # expect vs reflect
    'I feel more confident in Chemistry now that we are at the end of this quarter.': 'confident',
    'I feel comfortable seeking help when I don’t understand a concept.': 'seek_help',
    'I feel comfortable working on group problems or labs with other students.': 'work_in_groups',
    'I feel confident in my ability to succeed in this Chemistry course.': 'succeed',
    'I feel confident tackling new or unfamiliar Chemistry problems.': 'unfamiliar',
    'I feel like I belong in this Chemistry class.': 'belong',
    'I feel prepared to handle the workload and expectations of this course.': 'workload', # feel vs was
    'I was prepared to handle the workload and expectations of this course.': 'workload',
    'I feel supported by the Department or program offering this course.': 'supported_department',
    'I feel supported by the department or program offering this course.': 'supported_department',
    'I have at least one person in this class I could study with outside of class.': 'study_buddy',
    'I know where to find academic help if I need it': 'find_help',
    'I know where to find academic help if I need it (e.g., office hours, tutoring, peer learning).': 'find_help',
    'I see challenges in Chemistry as opportunities to grow.': 'challenges_are_growth',
    'I see myself as part of the learning community in this course.': 'part_of_community',
    'I see myself continuing in Chemistry or a related field after this class.': 'continuing',
    'I see myself continuing in Chemistry or a related(STEM) field after this class.': 'continuing',
    'I understand the study strategies needed to perform well in college-level science classes.': 'understand_study_strats',
    'In reference to the above question regarding attending Chemistry peer learning: Why or why not?': 'why_peer_learning',
    'Mistakes in Chemistry are an important part of learning.': 'mistakes_are_learning',
    'My instructor(s) care about my learning and progress.': 'instructor_cares',
    'My peers in this course respect my ideas.': 'peers_respect',
    'This question is to check if you are actually reading the question. Select Strongly Disagree here.': 'attention_check',
    'What are you most nervous about as you begin this course?': 'nervous',
    'What usually helps you learn best when material feels confusing or challenging?': 'learn_best',
    'When I don’t do well on an exam, I reflect and adjust my study strategies.': 'reflect',
    'When I struggle with a Chemistry concept, I can usually find a way to understand it.': 'when_struggle_find_way',
    'When do you feel most “connected” or “disconnected” in Chemistry learning spaces?': 'when_connected',
}
# Create the reverse mapping (code -> canonical question)
# Takes the first occurrence of each code as the canonical version
code_to_canonical = {}
for question, code in normalized_questions.items():
    if code not in code_to_canonical:
        code_to_canonical[code] = question

for survey_name, df in dfs.items():
    dfs[survey_name] = df.rename(columns=normalized_questions)

for survey_name, df in dfs.items():
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    # if someone responded to the survey multiple times, only keep their earliest submission
    df = df.loc[df.groupby('id')['timestamp'].idxmin()]

# ------
# standardize teacher's name spelling

teachers = [
    'lavelle',
    'deweese',
    'scerri',
    'ngo',
    'riu',
    'ow',
    'deifel',
    'wu',
    'harran',
    'henary',
    'pham',
    'athavale',
    
    'soroush-pejrimovsky',
    'hung',
    'han',
    'balagtas',
    
    'no lab'
]
spellcheck = {
    'eric': 'wu',
    'ryu': 'riu', 'rui': 'riu', 'riyu': 'riu',
    'chao': 'ngo', 'chau': 'ngo', 'chai': 'ngo', 'ngi': 'ngo', 'ngu': 'ngo',
    'franklin': 'oh',
    'harren': 'harran', 'hartan': 'harran', 'haran': 'harran',
    'leville': 'lavelle', 'lavell': 'lavelle', 'levelle': 'lavelle', 'la elle': 'lavelle', 'lavelee': 'lavelle', 'lavalle': 'lavelle',
    'scherri': 'scerri', 'scerry': 'scerri', 'sceri': 'scerri',
    'hung': 'pham', 'huang': 'pham',
    'diefel': 'deifel',
    'dweese': 'deweese', 'dewiest': 'deweese',

    'have not taken lab': 'no lab', # there's more variations
    'no, i don\'t take a lab': 'no lab',
    'didnt take lab': 'no lab'
}

def get_teacher(survey_name):
    if pd.isna(survey_name):
        return survey_name
    
    survey_name = survey_name.lower()
    
    # probably terrible big O
    for teacher in teachers:
        if teacher in survey_name:
            return teacher
    for survey_wrong_name, survey_corrected_name in spellcheck.items():
        if survey_wrong_name in survey_name:
            return survey_corrected_name
    
    return survey_name

for survey_name, df in dfs.items():
    if 'instructor' not in df.columns:
        continue
    df['instructor'] = df['instructor'].apply(get_teacher)


for df in dfs.values():
    df.drop(columns=[
        "timestamp",
        # These two are temporary, so it's easier for me
        # "course",
        "instructor"
    ], inplace=True, errors='ignore') # ignore errors bc two dfs already don't have `instructor`

# Attention check
ppl_who_failed_attention_check = dfs['w3s1'][dfs['w3s1'].attention_check != "Strongly Disagree"].id.unique()
for survey_name, df in dfs.items():
    dfs[survey_name] = df[~df["id"].isin(ppl_who_failed_attention_check)]


# ------
# merge dfs (problematic)

# survey prefixes _s1, _s2, _s3 are only needed for timestamp, course, and instructor
w3 = dfs['w3s1'] \
    .merge(dfs['w3s2'], on='id', how='outer', suffixes=('_s1', '_s2')) \
    .merge(dfs['w3s3'], on='id', how='outer', suffixes=('', '_s3'))
w3.rename(columns={'course': 'course_s3'}, inplace=True)

# drop timestamp_s1, timestamp_s2 # previously dropped

w10 = dfs['w10s1'] \
    .merge(dfs['w10s3'], on='id', how='outer', suffixes=('', '_s3')) \
    .merge(dfs['w10s2'], on='id', how='outer', suffixes=('_s1', '_s2'))
w3.rename(columns={'course': 'course_s3'}, inplace=True)

mega = w3.merge(w10, on='id', how='outer', suffixes=('_w3', '_w10'))

# Save cleaned response level data
w3.to_parquet("cleaned_response_lvl_data/cleaned_pre.parquet")
w10.to_parquet("cleaned_response_lvl_data/cleaned_post.parquet")
mega.to_parquet("cleaned_response_lvl_data/cleaned_all.parquet")

for survey_name, df in dfs.items():
    df.to_parquet(f"cleaned_response_lvl_data/{survey_name}.parquet")

# -----
# responses to question percentage breakdowns
def summarize_question(series, output='str'):
    counts = series.value_counts()
    total = len(series)
    percentages = counts / total * 100
    
    agree = percentages.get('Strongly Agree', 0) + percentages.get('Slightly Agree', 0)
    disagree = percentages.get('Strongly Disagree', 0) + percentages.get('Slightly Disagree', 0)
    neutral = percentages.get('Neutral', 0)
    
    if output == 'str':
        return {
            'agree': f"{agree:.2f}%",
            'neutral': f"{neutral:.2f}%",
            'disagree': f"{disagree:.2f}%"
        }
    elif output == 'float':
        return {
            'agree': agree,
            'neutral': neutral,
            'disagree': disagree
        }
    elif output == '%agree':
        return agree

"""
for each survey
question, course, agree, disagree, neutral
"""

results = {}

for survey_name, df in dfs.items():
    results[survey_name] = {
        "question": [],
        "course": [],
        "agree": [],
        "neutral": [],
        "disagree": []
    }
    for course_name, course_data in df.groupby('course'):
        for question in course_data.columns:
            if 'Strongly Agree' not in df[question].unique(): # huge hack to get likert questions
                continue

            percentages = summarize_question(course_data[question])
            results[survey_name]["question"].append(question)
            results[survey_name]["course"].append(course_name)
            results[survey_name]["agree"].append(percentages["agree"])
            results[survey_name]["neutral"].append(percentages["neutral"])
            results[survey_name]["disagree"].append(percentages["disagree"])
        
    results[survey_name] = pd.DataFrame(results[survey_name])

# final format
for survey_name, df in results.items():
    melted = df.melt(id_vars=['question', 'course'],
                                value_vars=['agree', 'neutral', 'disagree'],
                                var_name='response_type',
                                value_name='percentage')
    pivoted = melted.pivot_table(index=['question', 'response_type'],
                                columns='course',
                                values='percentage',
                                aggfunc='first')

    pivoted = pivoted.reset_index()
    pivoted['question'] = pivoted['question'].replace(code_to_canonical)
    pivoted = pivoted.set_index(['question', 'response_type'])

    pivoted.to_csv(f'nice_breakdowns/{survey_name}.csv')


# average likert
for survey_name, df in results.items():
    agree = results[survey_name]['agree'].str.rstrip('%').astype(float) / 100
    neutral = results[survey_name]['neutral'].str.rstrip('%').astype(float) / 100
    disagree = results[survey_name]['disagree'].str.rstrip('%').astype(float) / 100
    df['avg'] = agree * 1 + neutral * 0 + disagree * -1

common_cols = set(w3.columns.tolist()) & set(w10.columns.tolist())
# common_courses = # not CL, BL, C

w3s3 = results['w3s3']
w10s3 = results['w10s3']
before_confidence = w3s3.loc[w3s3.question == 'confident']#[['course', 'avg']]
after_confidence = w10s3.loc[w10s3.question == 'confident']#[['course', 'avg']]
before_vs_after_confidence = before_confidence.merge(after_confidence, on='course', how='inner', suffixes=('_before', '_after'))

# plot

df = before_vs_after_confidence
df['delta_avg'] = df.avg_after - df.avg_before

# Convert percentage strings to floats
for col in ['agree_before', 'neutral_before', 'disagree_before', 
            'agree_after', 'neutral_after', 'disagree_after']:
    df[col] = df[col].str.rstrip('%').astype(float)

# Set up the plot
fig, ax = plt.subplots(figsize=(14, 8))

# Get courses
courses = df['course'].tolist()
x = np.arange(len(courses))
width = 0.35

# Colors
colors_agree = '#2ecc71'  # green
colors_neutral = '#95a5a6'  # gray
colors_disagree = '#e74c3c'  # red

# Before bars
before_disagree = ax.bar(x - width/2, df['disagree_before'], width, 
                         label='Disagree (Before)', color=colors_disagree, alpha=0.7)
before_neutral = ax.bar(x - width/2, df['neutral_before'], width, 
                        bottom=df['disagree_before'],
                        label='Neutral (Before)', color=colors_neutral, alpha=0.7)
before_agree = ax.bar(x - width/2, df['agree_before'], width,
                      bottom=df['disagree_before'] + df['neutral_before'],
                      label='Agree (Before)', color=colors_agree, alpha=0.7)

# After bars
after_disagree = ax.bar(x + width/2, df['disagree_after'], width,
                        label='Disagree (After)', color=colors_disagree)
after_neutral = ax.bar(x + width/2, df['neutral_after'], width,
                       bottom=df['disagree_after'],
                       label='Neutral (After)', color=colors_neutral)
after_agree = ax.bar(x + width/2, df['agree_after'], width,
                     bottom=df['disagree_after'] + df['neutral_after'],
                     label='Agree (After)', color=colors_agree)

# Add delta labels above each bar pair
for i, (idx, row) in enumerate(df.iterrows()):
    delta = row['delta_avg']
    # Position label above the taller bar
    y_pos = 105  # Just above 100%
    
    # Color code: green for positive, red for negative
    color = '#2ecc71' if delta >= 0 else '#e74c3c'
    sign = '+' if delta >= 0 else ''
    
    ax.text(x[i], y_pos, f'{sign}{delta:.3f}', 
            ha='center', va='bottom', fontsize=9, 
            fontweight='bold', color=color)

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor='#2ecc71', label='Agree'),
    Patch(facecolor='#95a5a6', label='Neutral'),
    Patch(facecolor='#e74c3c', label='Disagree')
]
ax.legend(handles=legend_elements, loc='center right', title='Response Type')

# Customize

ax.set_ylabel('Percentage (%)', fontsize=12)
ax.set_xlabel('Course', fontsize=12)
ax.set_title('Student Confidence: Before vs After Survey (Δ Avg shown above)', 
             fontsize=14, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(courses, rotation=45, ha='right')
ax.set_ylim(0, 115)  # Extended to fit labels
ax.grid(axis='y', alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('pic2.png')




fig, ax = plt.subplots(figsize=(10, 8))

x = [0, 1]
x_labels = ['"I expect to feel more confident in Chemistry\nby the end of this quarter."', '"I feel more confident in Chemistry\nnow that we are at the end of this quarter."']

deltas = df['delta_agree'].values
cmap = LinearSegmentedColormap.from_list('redgreen', ['#e74c3c', '#2ecc71'])

# Sort by agree_after to group nearby labels
df_sorted = df.sort_values('agree_after')

# Plot and add labels with manual spacing
min_spacing = 3  # Minimum percentage points between labels
last_y = -100  # Start very low

for idx, row in df_sorted.iterrows():
    y = [row['agree_before'], row['agree_after']]
    delta = row['delta_agree']
    
    norm_delta = (delta - deltas.min()) / (deltas.max() - deltas.min())
    color = cmap(norm_delta)
    
    ax.plot(x, y, marker='o', linewidth=2.5, markersize=8, 
            color=color, alpha=0.8)
    
    # Adjust label position if too close to previous
    label_y = row['agree_after']
    if label_y - last_y < min_spacing:
        label_y = last_y + min_spacing
    
    ax.text(1.02, label_y, row['course'], 
            va='center', fontsize=9, color=color, fontweight='bold')
    
    last_y = label_y

ax.set_xticks(x)
ax.set_xticklabels(x_labels, fontsize=15)
ax.set_ylabel('Percent Agreeing (%)', fontsize=12)
# ax.set_xlabel('Survey Time', fontsize=12)
# ax.set_title('Change in Student Confidence: Before vs After', fontsize=14, fontweight='bold')
ax.set_xlim(-0.1, 1.3)
# ax.set_ylim(0, 105)
ax.set_ylim(40, 105)
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig("pic8.png")


# ---
# Agreement rates by question, course, and pre/post

AGREE_VALUES = {'Strongly Agree', 'Slightly Agree'}
YES_VALUES = {'Yes'}

def get_likert_cols(df):
    return [col for col in df.columns if df[col].isin(AGREE_VALUES).any()]

def get_yes_no_cols(df):
    return [col for col in df.columns if df[col].isin(YES_VALUES).any() and col not in get_likert_cols(df)]

def pct_agree(x):
    positive = AGREE_VALUES | YES_VALUES
    return x.isin(positive).sum() / x.notna().sum() * 100

records = []
for survey_name, df in dfs.items():
    time = 'w3' if survey_name.startswith('w3') else 'w10'
    likert_cols = get_likert_cols(df)
    yes_no_cols = get_yes_no_cols(df)
    all_cols = likert_cols + yes_no_cols
    
    melted = (
        df[['course'] + all_cols]
        .melt(id_vars='course', var_name='question', value_name='response')
    )
    
    result = (
        melted
        .groupby(['course', 'question'])['response']
        .agg(
            pct_agree=pct_agree,
            n=lambda x: x.notna().sum()
        )
        .reset_index()
        .assign(time=time)
    )
    records.append(result)

results = pd.concat(records, ignore_index=True)
results.to_csv("nice_breakdowns/agreement_rates.csv")


# ---
# Attention check sensitivity analysis
base = pd.read_csv("nice_breakdowns/agreement_rates_no_attn_check.csv").drop(columns=["Unnamed: 0"])
clean = pd.read_csv("nice_breakdowns/agreement_rates.csv").drop(columns=["Unnamed: 0"])

merged = base.merge(clean, on=["course", "question", "time"], suffixes=("_base", "_clean"))
merged["diff"] = merged["pct_agree_clean"] - merged["pct_agree_base"]

big_movers = merged[(abs(merged["diff"]) > 2) & (merged["n_base"] >= 30)]
merged.sort_values("diff", key=abs, ascending=False).to_csv("nice_breakdowns/attention_check_analysis.csv")

# Attention check failures did not contribute largely to the data (< 5pp across all question x course x pre/post permutations).


# Qualitative questions

# nervous: What are you most nervous about as you begin this course?
# when_connected: When do you feel most “connected” or “disconnected” in Chemistry learning spaces?
# learn_best: What usually helps you learn best when material feels confusing or challenging?
# why_peer_learning: In reference to the above question regarding attending Chemistry peer learning: Why or why not? [The above question: Did you attend the Chemistry peer learning in room MS3974?]


nervous = dfs['w3s1'].nervous.value_counts()
when_connected = dfs['w3s2'].when_connected.value_counts()
learn_best = dfs['w3s3'].learn_best.value_counts()
why_peer_learning = dfs['w10s1'].why_peer_learning.value_counts()

# tagged_responses
qs = {
    "nerv": pd.read_csv("tagged_qualitative/nervous.csv"),
    "conn": pd.read_csv("tagged_qualitative/when_connected.csv"),
    "learn": pd.read_csv("tagged_qualitative/learn_best.csv"),
    "peerl": pd.read_csv("tagged_qualitative/why_peer_learning.csv"),
}

tag_counts = {}

for q_name, df in qs.items():
    qs[q_name]["tags"] = df["tags"].str.split("+")
    df_exploded = df.explode("tags")
    tag_counts[q_name] = df_exploded.groupby("tags")["count"].sum().sort_values(ascending=False)


# only things left to do for fa25 chem surveys
# translate why_peer_learning codes
# make tag definitions expandable
# expand Connected in X Disconnected in Y
# pick notable quotes