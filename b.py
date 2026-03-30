import numpy as np
import pandas as pd

df = pd.read_parquet('cleaned_all.parquet')
predf = pd.read_parquet("cleaned_pre.parquet")
postdf = pd.read_parquet("cleaned_post.parquet")

# differenc responces btwn surveys, maybe ppl filled it out for multiple classes
print("Course consistency check:")
print((all_three['course_s1'] == all_three['course_s2']).sum(), "matches between s1 and s2")
print((all_three['course_s2'] == all_three['course']).sum(), "matches between s2 and s3")
print((all_three['course_s1'] == all_three['course']).sum(), "matches between s1 and s3")
print(((all_three['course_s1'] == all_three['course_s2']) & (all_three['course_s2'] == all_three['course'])).sum(), "matches between all 3")

# ---------------
# Venn diagram of respondents

from matplotlib_venn import venn3
from matplotlib_venn.layout.venn3 import DefaultLayoutAlgorithm
import matplotlib.pyplot as plt

# Get the counts for each region
# Format: (s1 only, s2 only, s1&s2 only, s3 only, s1&s3 only, s2&s3 only, all three)

s1_only = len(predf[predf['took_s1'] & ~predf['took_s2'] & ~predf['took_s3']])  # 0 (not in your data)
s2_only = len(predf[~predf['took_s1'] & predf['took_s2'] & ~predf['took_s3']])  # 16
s3_only = len(predf[~predf['took_s1'] & ~predf['took_s2'] & predf['took_s3']])  # 14

s1_s2_only = len(predf[predf['took_s1'] & predf['took_s2'] & ~predf['took_s3']])  # 20
s1_s3_only = len(predf[predf['took_s1'] & ~predf['took_s2'] & predf['took_s3']])  # 5
s2_s3_only = len(predf[~predf['took_s1'] & predf['took_s2'] & predf['took_s3']])  # 38

all_three = len(predf[predf['took_s1'] & predf['took_s2'] & predf['took_s3']])  # 1561

# Create Venn diagram
plt.figure(figsize=(10, 8))
venn3(subsets=(s1_only, s2_only, s1_s2_only, s3_only, s1_s3_only, s2_s3_only, all_three),
      set_labels=('Survey 1', 'Survey 2', 'Survey 3'),
      layout_algorithm=DefaultLayoutAlgorithm(fixed_subset_sizes=(1,1,1,1,1,1,1)))

plt.title('Student Participation Across 3 Pre-Surveys\n(n=1776)', fontsize=14)
plt.tight_layout()
plt.savefig('pic9.png')

# Or if you want percentages too
print(f"All 3 surveys: {all_three} ({all_three/len(predf)*100:.1f}%)")
print(f"Only S1 & S2: {s1_s2_only} ({s1_s2_only/len(predf)*100:.1f}%)")
print(f"Only S2 & S3: {s2_s3_only} ({s2_s3_only/len(predf)*100:.1f}%)")



# ---
# respondents in each survey in each course
course_table = pd.DataFrame({
    survey: dfs[survey]['course'].value_counts()
    for survey in ['w3s1', 'w3s2', 'w3s3', 'w10s1', 'w10s2', 'w10s3']
})

# Fill NaN with 0 for courses not in a particular survey
course_table = course_table.fillna(0).astype(int)

# Sort by total across all surveys
course_table['Total'] = course_table.sum(axis=1)
course_table = course_table.sort_values('Total', ascending=False)

# get average for each week
course_table['w3_avg'] = (course_table['w3s1'] + course_table['w3s2'] + course_table['w3s3']) / 3
course_table['w10_avg'] = (course_table['w10s1'] + course_table['w10s2'] + course_table['w10s3']) / 3

# Optional: nicer display
print(course_table.to_string())

# ----
# teachers for each course
courses = ['Chemistry 14A', 'Chemistry 14AE', 'Chemistry 14B', 'Chemistry 14BL', 'Chemistry 14C', 'Chemistry 14CL', 'Chemistry 14D', 'Chemistry 20A', 'Chemistry 30A', 'Chemistry 30AL', 'Chemistry 30B', 'Chemistry 30BL', 'Chemistry 30C', 'Chemistry 30CL']
for course in courses:
    print(f"========== {course} ==========")
    for survey_name, df in dfs.items():
        if 'instructor' not in df.columns:
            continue
        print(survey_name)
        print(df[df.course == course].instructor.value_counts())


# --------
# most mispelled teacher's names
# by percentage, exclude <10 respondents


# ------
# Ok now I want
# One course's responses to all questions | All courses' responses to one question
# % agree
# show w3 in one color, w10 in another color, arrow btwn them
# if question is only in one or the other, only show one dot (one color) and no arrow