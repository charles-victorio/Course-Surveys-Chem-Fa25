import pandas as pd

fname = "qualitative_codebooks/deepseek_why_peer_learning_codebook.txt"
codebook = pd.read_csv(fname)

other_cols = [
    ["Clueless_Student", "I didn't know it existed."],
    ["UnawareOfThis", "I wasn't aware of this resource."],
    ["JustFoundOut", "I'm hearing about it for the first time."],
    ["ForgotAboutIt", "I knew about it but forgot."],
    ["NoTimeEver", "I didn't have time."],
    ["ScheduleClash", "I had a schedule conflict."],
    ["CommuterLife", "I couldn't make it work with my commute."],
    ["TooBusyQuarter", "My schedule was too busy."],
    ["DidntNeedIt", "I didn't feel like I needed it."],
    ["SoloLearner", "I prefer to study on my own."],
    ["AlreadyGotIt", "I already understood the material."],
    ["DoingAlright", "I was doing well without it."],
    ["NotNecessary", "I didn't think it was necessary."],
    ["OfficeHoursGang", "I used office hours instead."],
    ["StudyGroupSquad", "I studied with friends instead."],
    ["OtherTutoring", "I used other tutoring programs."],
    ["OnlineResources", "I used online resources instead."],
    ["ProfessorReview", "I went to professor review sessions."],
    ["AloneTime", "I prefer studying alone."],
    ["KnownFaces", "I prefer studying with people I know."],
    ["GroupDistraction", "I find group study distracting."],
    ["NotAFan", "I don't really like peer learning."],
    ["Anxiety_Alone", "I was nervous about going alone."],
    ["CantFindRoom", "I couldn't find the room."],
    ["NeverHeardAboutIt", "There weren't enough announcements about it."],
    ["ThoughtItWasFull", "I thought it was full or had to sign up."],
    ["NotForMe", "I thought it was only for certain programs."],
    ["DidntKnowWhatToExpect", "I wasn't sure how the sessions worked."],
    ["WouldntHelp", "I didn't think it would be helpful."],
    ["BeenBefore_NotHelpful", "I went before and it wasn't helpful."],
    ["BlindLeadingBlind", "I'm skeptical about students teaching."],
    ["TABetter", "I think TA or professor help is better."],
    ["WentThere", "I did attend the peer learning."],
    ["WentElsewhere", "I attended peer learning at another location."],
    ["WentToUA", "I attended UA sessions or step-ups instead."],
    ["ActuallyHelpful", "I found the sessions helpful."],
    ["NoResponse", ""],
    ["OtherCommitments", "I had work or other obligations."],
    ["PersonalIssues", "I had personal issues going on."],
    ["NeverMadeIt", "I was too lazy to go."],
    ["Miscellaneous", "Other reasons."]
]

codebook[["usernames", "comments"]] = pd.DataFrame(other_cols, columns=["username", "comment"])

codebook.to_csv("codebooks2/why_peer_learning.csv")

tagged_responses = pd.read_csv("tagged_qualitative/deepseek_tagged_why_peer_learning.csv")
tag_mapping = codebook.set_index("theme_id")["secondary_category"].to_dict()
tagged_responses["tags"] = tagged_responses["tags"].map(lambda tags: '+'.join([tag_mapping.get(tag, tags) for tag in tags.split("+")]))
tagged_responses.to_csv("tagged_qualitative/deepseek_tagged_why_peer_learning.csv")