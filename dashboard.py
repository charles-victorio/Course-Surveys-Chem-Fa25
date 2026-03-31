import base64

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import pandas as pd
import numpy as np

question_to_code = {
    'I am comfortable asking questions in lecture or discussion sections.': 'asking_questions',
    'I am confident in applying mathematical skills to Chemistry problems.': 'apply_math',
    'I believe I can improve my Chemistry skills with consistent effort.': 'improve_skills',
    'I believe I can manage my time effectively when studying for Chemistry exams.': 'manage_time',
    'I believe intelligence and ability in Chemistry can be developed over time.': 'develop_intelligence',
    'I believe my contributions in class are valued.': 'contributions_valued',
    'I believe my current study habits will help me perform well in this class.': 'study_habits',
    'I can be myself when interacting with classmates and faculty in Chemistry.': 'be_myself',
    'I can explain Chemistry concepts in my own words.': 'own_words',
    'I can motivate myself to keep studying even when the material is difficult.': 'motivate',
    'I expect to earn at least a B in this class. [Asked in pre-survey only.]': 'at_least_b',
    'I expect to earn at least a C in this class (C or better).': 'at_least_c',
    'I expect to feel more confident [post test: I feel more confident] in Chemistry by the end of this quarter.': 'confident',
    'I feel comfortable seeking help when I don’t understand a concept.': 'seek_help',
    'I feel comfortable working on group problems or labs with other students.': 'work_in_groups',
    'I feel confident in my ability to succeed in this Chemistry course. [Asked in pre-survey only.]': 'succeed',
    'I feel confident tackling new or unfamiliar Chemistry problems.': 'unfamiliar',
    'I feel like I belong in this Chemistry class.': 'belong',
    'I feel prepared [post test: I was prepared] to handle the workload and expectations of this course.': 'workload',
    'I feel supported by the Department or program offering this course.': 'supported_department',
    'I have at least one person in this class I could study with outside of class.': 'study_buddy',
    'I know where to find academic help if I need it.': 'find_help',
    'I see challenges in Chemistry as opportunities to grow.': 'challenges_are_growth',
    'I see myself as part of the learning community in this course.': 'part_of_community',
    'I see myself continuing in Chemistry or a related field after this class.': 'continuing',
    'I understand the study strategies needed to perform well in college-level science classes.': 'understand_study_strats',
    # 'In reference to the above question regarding attending Chemistry peer learning: Why or why not?': 'why_peer_learning',
    'Mistakes in Chemistry are an important part of learning.': 'mistakes_are_learning',
    'My instructor(s) care about my learning and progress.': 'instructor_cares',
    'My peers in this course respect my ideas.': 'peers_respect',
    # 'This question is to check if you are actually reading the question. Select Strongly Disagree here. [Asked in pre-survey only.]': 'attention_check',
    # 'What are you most nervous about as you begin this course?': 'nervous',
    # 'What usually helps you learn best when material feels confusing or challenging?': 'learn_best',
    'When I don’t do well on an exam, I reflect and adjust my study strategies.': 'reflect',
    'When I struggle with a Chemistry concept, I can usually find a way to understand it.': 'when_struggle_find_way',
    # 'When do you feel most “connected” or “disconnected” in Chemistry learning spaces?': 'when_connected'
    'Did you attend the Chemistry peer learning in room MS3974 ?': 'peer_learning',
 }

st.set_page_config(page_title="Survey Dashboard", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 2rem; }
    h1 { font-size: 1.4rem; font-weight: 600; }
    .stSelectbox label { font-size: 0.85rem; color: #666; }
</style>
""", unsafe_allow_html=True)

# ── Constants ────────────────────────────────────────────────────────────────
N_THRESHOLD = 30
COLOR_PRE    = "#7BA7D4"   # blue
COLOR_POST   = "#5B4DA8"   # purple
COLOR_SUPPRESSED = "#CCCCCC"
ARROW_COLOR  = "#AAAAAA"

# ── Load data ────────────────────────────────────────────────────────────────
# Replace this with your real `results` DataFrame (output of the pipeline).
# Expected columns: time, course, question, pct_agree, n
@st.cache_data
def load_data():
    return pd.read_csv("nice_breakdowns/agreement_rates.csv")

results = load_data()

# ── Mobile warning ───────────────────────────────────────────────────────────

def mobile_warning():
    components.html("""
    <style>
    .mobile-warn {
    display: none;
    background: #ff4500;
    color: #fff;
    padding: 8px 12px;
    border-radius: 4px;
    font-family: sans-serif;
    font-size: 13px;
    }
    @media (max-width: 600px) {
    .mobile-warn { display: block; }
    }
    </style>
    <div class="mobile-warn">
    📊 This website is optimized for desktop. Some charts may be hard to read on mobile.
    </div>
    """, height=80)


# Overview Chart
# --------------

def Overview():
    def make_overview_chart(results):
        code_to_question = {v: k for k, v in question_to_code.items()}
        
        # aggregate across all courses, only n >= 30 for both
        pre  = results[results["time"] == "w3"].rename(columns={"pct_agree":"pre_pct","n":"pre_n"})
        post = results[results["time"] == "w10"].rename(columns={"pct_agree":"post_pct","n":"post_n"})
        
        merged = pre.merge(post, on=["question","course"], how="outer")
        valid = merged[
            (merged["pre_n"].fillna(0) >= N_THRESHOLD) &
            (merged["post_n"].fillna(0) >= N_THRESHOLD)
        ]
        
        agg = (
            valid.groupby("question")
            .agg(pre_pct=("pre_pct","mean"), post_pct=("post_pct","mean"))
            .assign(change=lambda d: d["post_pct"] - d["pre_pct"])
            .sort_values("change")
            .reset_index()
        )
        agg["label"] = agg["question"].map(code_to_question)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=agg["change"],
            y=agg["label"],
            orientation="h",
            marker_color=["#2e7d32" if v >= 0 else "#c62828" for v in agg["change"]],
            hovertemplate="<b>%{y}</b><br>Change: %{x:.1f}pp<extra></extra>",
        ))
        fig.update_layout(
            xaxis=dict(
                title="percentage point change (pre → post)",
                ticksuffix="pp",
                zeroline=True, zerolinecolor="black", zerolinewidth=1.5,
                showgrid=True, gridcolor="#f0f0f0",
            ),
            yaxis=dict(showgrid=False, tickfont=dict(color="black")),
            height=max(400, len(agg) * 30 + 80),
            margin=dict(l=300, r=40, t=60, b=50),
            plot_bgcolor="white",
            paper_bgcolor="white",
        )
        return fig

    st.write("")
    mobile_warning()
    st.header("How did responses change?")
    st.caption("Percent agree by question (pre → post change). Averaged across all courses with n ≥ 30 for both surveys.")
    st.plotly_chart(make_overview_chart(results), use_container_width=True)

# Question Charts
# --------------

def Quantitative_Responses():
    st.text("") # spacing

    # Question Selector
    questions = list(question_to_code.keys())

    if "q_idx" not in st.session_state:
        st.session_state.q_idx = int(st.query_params.get("q", 0))
        st.session_state._q_widget = questions[st.session_state.q_idx]

    def prev_q():
        st.session_state.q_idx = (st.session_state.q_idx - 1) % len(questions)
        st.session_state._q_widget = questions[st.session_state.q_idx]
        st.query_params["q"] = st.session_state.q_idx
    
    def next_q():
        st.session_state.q_idx = (st.session_state.q_idx + 1) % len(questions)
        st.session_state._q_widget = questions[st.session_state.q_idx]
        st.query_params["q"] = st.session_state.q_idx

    def on_q_change():
        st.session_state.q_idx = questions.index(st.session_state._q_widget)
        st.query_params["q"] = st.session_state.q_idx
    
    


    flex = st.container(horizontal=True)
    flex.button("‹", on_click=prev_q)
    flex.button("›", on_click=next_q)


    # ── Sidebar filters ──────────────────────────────────────────────────────────
    st.sidebar.title("Filters")

    st.sidebar.selectbox("Question (drag to expand sidebar)", list(question_to_code.keys()), key="_q_widget", on_change=on_q_change)
    selected_question = questions[st.session_state.q_idx]
    selected_question_code = question_to_code[selected_question]

    sort_by = st.sidebar.radio(
        "Sort courses by",
        ["Alphabetical", "Pre → Post change", "Pre % agree", "Post % agree"],
        index=0,
    )

    show_low_n = st.sidebar.checkbox("Show low-n results (n < 30)", value=True)

    # ── Filter & pivot ───────────────────────────────────────────────────────────
    df = results[
        results["question"] == selected_question_code
    ].copy()

    pre  = df[df["time"] == "w3" ][["course","pct_agree","n"]].rename(
        columns={"pct_agree":"pre_pct","n":"pre_n"})
    post = df[df["time"] == "w10"][["course","pct_agree","n"]].rename(
        columns={"pct_agree":"post_pct","n":"post_n"})

    merged = pre.merge(post, on="course", how="outer")

    # ── Sort ─────────────────────────────────────────────────────────────────────
    if sort_by == "Pre → Post change":
        merged["_sort"] = merged["post_pct"].fillna(0) - merged["pre_pct"].fillna(0)
    elif sort_by == "Pre % agree":
        merged["_sort"] = merged["pre_pct"].fillna(0)
    elif sort_by == "Post % agree":
        merged["_sort"] = merged["post_pct"].fillna(0)
    else:
        merged["_sort"] = merged["course"].apply(lambda x: x)

    # Push low-n values to the bottom
    if sort_by == "Pre % agree":
        low_n = merged["pre_n"].fillna(0) < N_THRESHOLD
    elif sort_by == "Post % agree":
        low_n = merged["post_n"].fillna(0) < N_THRESHOLD
    elif sort_by == "Pre → Post change":
        low_n = (merged["pre_n"].fillna(0) < N_THRESHOLD) | (merged["post_n"].fillna(0) < N_THRESHOLD)
    else: # alphabetical -> low-n doesnt matter
        low_n = pd.Series(False, index=merged.index)
    merged.loc[low_n, "_sort"] = -np.inf
    merged["_low_n"] = low_n.astype(int)  # 1 = low-n, 0 = ok

    merged = merged.sort_values(["_low_n", "_sort"], ascending=False)
    courses_ordered = merged["course"].tolist()

    # ── Build Plotly figure ──────────────────────────────────────────────────────
    fig = go.Figure()

    # Add an invisible dummy trace for each course so they're always on the y axis.
    # Otherwise, courses with low-n for both pre and post would be hidden when "Show low-n results" is checked 
    for i, course in enumerate(courses_ordered):
        fig.add_trace(go.Scatter(
            x=[0], y=[i],
            mode="none",
            showlegend=False,
            hoverinfo="skip",
        ))

    for _, row in merged.iterrows():
        course = row["course"]
        y = courses_ordered.index(course)

        pre_ok  = pd.notna(row.get("pre_pct"))  and row.get("pre_n",  0) >= N_THRESHOLD
        post_ok = pd.notna(row.get("post_pct")) and row.get("post_n", 0) >= N_THRESHOLD
        pre_sup  = pd.notna(row.get("pre_pct"))  and row.get("pre_n",  0) < N_THRESHOLD
        post_sup = pd.notna(row.get("post_pct")) and row.get("post_n", 0) < N_THRESHOLD

        def dot(x, color, symbol, label, n, suppressed=False):
            opacity = 0.3 if suppressed else 1.0
            marker_color = COLOR_SUPPRESSED if suppressed else color
            hover = f"<b>{label}</b><br>% agree: {x:.1f}%<br>n = {n}"
            if suppressed:
                hover += f"<br><i>suppressed (n < {N_THRESHOLD})</i>"
            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                mode="markers+text",
                marker=dict(size=14, color=marker_color, opacity=opacity, symbol=symbol,
                            line=dict(width=1.5, color=marker_color)),
                text=[f"n={int(n)}"] if suppressed else [""],
                textposition="top center",
                textfont=dict(size=9, color="#999"),
                hovertemplate=hover + "<extra></extra>",
                showlegend=False,
            ))

        # Arrow between pre and post (only if both exist)
        if pd.notna(row.get("pre_pct")) and pd.notna(row.get("post_pct")):
            both_ok = (row.get("pre_n", 0) >= N_THRESHOLD and
                    row.get("post_n", 0) >= N_THRESHOLD)
            if show_low_n or both_ok:
                arrow_opacity = 0.6 if both_ok else 0.2
                fig.add_annotation(
                    x=row["post_pct"], y=y,
                    ax=row["pre_pct"], ay=y,
                    xref="x", yref="y", axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2, arrowsize=1, arrowwidth=1.5,
                    arrowcolor=ARROW_COLOR,
                    opacity=arrow_opacity,
                )

        # Pre dot
        if pre_ok:
            dot(row["pre_pct"], COLOR_PRE, "diamond", "Pre", row["pre_n"])
        elif pre_sup and show_low_n:
            dot(row["pre_pct"], COLOR_PRE, "diamond", "Pre", row["pre_n"], suppressed=True)

        # Post dot
        if post_ok:
            dot(row["post_pct"], COLOR_POST, "circle", "Post", row["post_n"])
        elif post_sup and show_low_n:
            dot(row["post_pct"], COLOR_POST, "circle", "Post", row["post_n"], suppressed=True)

    # Legend traces
    for label, color, symbol in [("Pre (Week 3)", COLOR_PRE, "diamond"), ("Post (Week 10)", COLOR_POST, "circle")]:
        fig.add_trace(go.Scatter(
            x=[None], y=[None], mode="markers",
            marker=dict(size=10, color=color, symbol=symbol),
            name=label, showlegend=True,
        ))

    fig.update_layout(
        xaxis=dict(title="% agree", range=[-2, 102], ticksuffix="%",
                showgrid=True, gridcolor="#f0f0f0", zeroline=False),
        yaxis=dict(
            tickmode="array",
            tickvals=list(range(len(courses_ordered))),
            ticktext=courses_ordered,
            tickfont=dict(color="black"),
            showgrid=False,
        ),
        height=max(400, len(courses_ordered) * 40 + 80),
        margin=dict(l=120, r=40, t=60, b=50),
        plot_bgcolor="white",
        paper_bgcolor="white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        hoverlabel=dict(bgcolor="white", font_size=12),
        # title=dict(
        #     text=selected_question,
        #     font=dict(size=30),
        #     x=0.5,
        #     xanchor="center"
        # ),
    )

    # st.write("")
    mobile_warning()
    st.header(selected_question)
    st.plotly_chart(fig, use_container_width=True)

    # ── Summary stats below chart ────────────────────────────────────────────────
    st.divider()
    col1, col2, col3 = st.columns(3)

    valid = merged[
        (merged["pre_n"].fillna(0) >= N_THRESHOLD) &
        (merged["post_n"].fillna(0) >= N_THRESHOLD)
    ].copy()
    valid["change"] = valid["post_pct"] - valid["pre_pct"]

    with col1:
        st.metric("Courses with enough respondents¹", len(valid))
    with col2:
        if len(valid):
            st.metric("Pre-Survey Average¹",  f'{valid["pre_pct"].mean():.1f}%')
    with col3:
        if len(valid):
            st.metric("Post-Survey Average¹", f'{valid["post_pct"].mean():.1f}%',
                    delta=f'{valid["change"].mean():.1f}pp')
            
    st.caption("¹: Only includes courses with n ≥ 30 responses for both the Pre and Post survey.")


def Qualitative_Responses():
    # ── Load Data ─────────────────────────────────────────────────────────────────

    @st.cache_data
    def load_data():
        qs = {
            "nervous":          pd.read_csv("tagged_qualitative/nervous.csv"),
            "when_connected":   pd.read_csv("tagged_qualitative/when_connected.csv"),
            "learn_best":       pd.read_csv("tagged_qualitative/learn_best.csv"),
            "why_peer_learning":pd.read_csv("tagged_qualitative/why_peer_learning.csv"),
        }
        codebooks = {
            "nervous":          pd.read_csv("codebooks2/nervous.csv"),
            "when_connected":   pd.read_csv("codebooks2/when_connected.csv"),
            "learn_best":       pd.read_csv("codebooks2/learn_best.csv"),
            "why_peer_learning":pd.read_csv("codebooks2/why_peer_learning.csv"),
        }

        tag_counts = {}
        for q_name, df in qs.items():
            qs[q_name]["tags"] = df["tags"].str.split("+")
            df_exploded = df.explode("tags")
            tag_counts[q_name] = (
                df_exploded.groupby("tags")["count"].sum().sort_values(ascending=False)
            )

        return qs, codebooks, tag_counts


    QUESTION_LABELS = {
        "nervous":           "What are you most nervous about as you begin this course?",
        "when_connected":    'When do you feel most "connected" or "disconnected" in Chemistry learning spaces?',
        "learn_best":        "What usually helps you learn best when material feels confusing or challenging?",
        "why_peer_learning": "Why did/didn't you attend the Chemistry peer learning in room MS3974?",
    }

    FLAIR_COLORS = {
        "nervous":           ("#ff4500", "#ff450022"),
        "when_connected":    ("#0dd3bb", "#0dd3bb22"),
        "learn_best":        ("#46d160", "#46d16022"),
        "why_peer_learning": ("#ffd635", "#ffd63522"),
    }

    POST_SCORES = {
        "nervous": 0,
        "when_connected": 0,
        "learn_best": 0,
        "why_peer_learning": 0,
    }

    # ── Session state ─────────────────────────────────────────────────────────────
    
    if "page" not in st.session_state:
        st.session_state.page = "list"
    if "selected_q" not in st.session_state:
        st.session_state.selected_q = "nervous"

    # ── CSS ──────────────────────────────────────────────────────────────────────

    CSS = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400&display=swap');
    :root {
    --bg:      #1a1a1b;
    --surface: #272729;
    --border:  #343536;
    --text:    #d7dadc;
    --muted:   #818384;
    --orange:  #ff4500;
    --blue:    #0079d3;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { background: var(--bg); color: var(--text);
        font-family: 'IBM Plex Sans', sans-serif; }

    .wrap { max-width: 740px; margin: 0 auto; padding: 16px 0 40px; }

    /* topbar */
    .topbar { display:flex; align-items:center; gap:12px;
            padding:10px 12px; background:var(--surface);
            border:1px solid var(--border); border-radius:4px; margin-bottom:16px; }
    .topbar-logo { font-size:22px; font-weight:700; color:var(--orange); }
    .topbar-sub  { font-size:14px; font-weight:600; }
    .topbar-nav  { margin-left:auto; display:flex; gap:16px;
                font-size:13px; color:var(--muted); }

    /* ── Post list card ── */
    .post-row { background:var(--surface); border:1px solid var(--border);
                border-radius:4px; display:flex; margin-bottom:6px; }
    .vote-col { background:#1e1e1f; display:flex; flex-direction:column;
                align-items:center; padding:8px 6px; gap:3px;
                min-width:44px; border-radius:4px 0 0 4px; }
    .vote-up   { color:var(--orange); font-size:16px; }
    .vote-down { font-size:16px; color:var(--muted); }
    .vote-count{ font-weight:700; font-size:13px; }
    .post-summary { padding:10px 14px; flex:1; }
    .post-meta { font-size:12px; color:var(--muted); margin-bottom:4px; }
    .post-meta a { color:var(--blue); text-decoration:none; }
    .flair { display:inline-block; font-size:11px; font-weight:600;
            padding:2px 8px; border-radius:12px; margin-bottom:5px; }
    .post-title { font-size:16px; font-weight:700; color:var(--text);
                line-height:1.3; margin-bottom:8px; }
    .post-preview { font-size:13px; color:var(--muted); line-height:1.5; margin-bottom:8px; }
    .post-footer { display:flex; gap:4px; flex-wrap:wrap; }
    .post-action { font-size:12px; font-weight:700; color:var(--muted); padding:5px 8px; border-radius:2px; }
    
    /* ── Thread ── */
    .thread-post { background:var(--surface); border:1px solid var(--border);
                border-radius:4px; display:flex; margin-bottom:10px; overflow:hidden; }
    .thread-vote-col { background:#1e1e1f; display:flex; flex-direction:column;
                    align-items:center; padding:8px 6px; gap:4px; min-width:44px; }
    .thread-body  { padding:10px 14px; flex:1; }
    .thread-title { font-size:18px; font-weight:700; color:var(--text);
                    line-height:1.3; margin-bottom:10px; }

    .filter-bar { background:var(--surface); border:1px solid var(--border);
                border-radius:4px; padding:8px 12px; display:flex; align-items:center;
                gap:6px; flex-wrap:wrap; font-size:13px; margin-bottom:10px; }
    .filter-label { font-weight:600; color:var(--text); margin-right:4px; white-space:nowrap; }
    .filter-btn { padding:4px 10px; border-radius:20px; font-weight:600;
                background:transparent; border:1px solid var(--border);
                color:var(--muted); cursor:pointer; font-family:inherit;
                font-size:12px; transition:background .1s, color .1s; }
    .filter-btn:hover { background:var(--border); color:var(--text); }
    .filter-btn.active { background:var(--orange); border-color:var(--orange); color:#fff; }
                    
    .comments-wrap { background:var(--surface); border:1px solid var(--border);
                    border-radius:4px; padding:12px 16px; }
    .comment { padding:10px 0 4px 12px; margin-top:8px; }
    .comment-meta { font-size:12px; color:var(--muted); margin-bottom:5px;
                    display:flex; align-items:center; gap:6px; flex-wrap:wrap; }
    .comment-author { font-weight:700; font-size:13px; color:var(--text); }
    .comment-score  { color:var(--orange); font-weight:700; font-size:12px; }
    .theme-badge    { font-size:10px; font-weight:700; padding:1px 6px; border-radius:2px;
                    letter-spacing:.4px; font-family:'IBM Plex Mono',monospace; }
    .comment-body   { font-size:14px; line-height:1.6; color:#c8cbcf; margin-bottom:5px; }
    .comment-desc   { font-size:12px; color:var(--muted); font-style:italic; margin-bottom:4px; }
    .comment-actions { display:flex; gap:4px; flex-wrap:wrap; }
    .action { font-size:12px; font-weight:700; color:var(--muted); padding:4px 6px; border-radius:2px; }
    </style>
    """

    # ── Helpers ──────────────────────────────────────────────────────────────────

    def fmt_score(n):
        n = int(n)
        return f"{n/1000:.1f}k" if n >= 1000 else str(n)
    
    def render_comment(row, upvotes, border_color):
        username  = str(row.get("usernames", "anonymous")).strip()
        comment   = str(row.get("comments", "")).strip()
        primary   = str(row.get("primary_category", "")).strip()

        score_html  = f'<span class="comment-score">▲ {fmt_score(upvotes)}</span>' if upvotes else ""
        theme_html  = (f'<span class="theme-badge" style="background:{border_color}22;color:{border_color}">'
                    f'{primary}</span>') if primary else ""
        body        = comment if comment and comment != "nan" else "<em>No comment recorded.</em>"

        # Gold logic
        if username == 'LightYagami':
            file_ = open("gold_256.png", "rb")
            contents = file_.read()
            data_url = base64.b64encode(contents).decode("utf-8")
            file_.close()
            gold_html = f'<img src="data:image/gif;base64,{data_url}" alt="bruintalk gold" height="14px">'
        else:
            gold_html = ''

        return f"""
        <div class="comment" style="border-left:2px solid {border_color}" data-category="{primary}">
        <div class="comment-meta">
            <span class="comment-author">u/{username}</span>
            {theme_html}{score_html}{gold_html}
        </div>
        <div class="comment-body">{body}</div>
        <div class="comment-actions">
            <span class="action">▲ Upvote</span>
            <span class="action">▼ Downvote</span>
            <span class="action">💬 Reply</span>
            <span class="action">Share</span>
        </div>
        </div>
        """


    def render_post(q_key, codebook_df, tag_counts):
        question    = QUESTION_LABELS[q_key]
        total_votes = int(tag_counts.sum()) if len(tag_counts) else 0
        num_comments= len(codebook_df)

        # Build comments sorted by upvotes (match theme_id → tag → count)
        # tag_counts index is tag strings; theme_id in codebook starts with category prefix.
        # We match on theme_id stripped to tag key where possible, else 0.
        def get_upvotes(row):
            theme_id = str(row.get("secondary_category", "")).strip().lower()
            if "peer learning" in question: print(tag_counts)
            # try direct match first
            if theme_id in tag_counts.index:
                return int(tag_counts[theme_id])
            # try matching any tag that appears in theme_id
            for tag, count in tag_counts.items():
                if tag.lower() in theme_id or theme_id in tag.lower():
                    return int(count)
            return 0

        codebook_df = codebook_df.copy()
        codebook_df["_upvotes"] = codebook_df.apply(get_upvotes, axis=1)
        codebook_df = codebook_df.sort_values("_upvotes", ascending=False)

        border_colors = ["#ff4500", "#0dd3bb", "#46d160", "#ffd635", "#e4abff"]
        comments_html = "".join(
            render_comment(row, row["_upvotes"], border_colors[i % len(border_colors)])
            for i, row in codebook_df.iterrows()
        )

        # collect unique primary categories for this question, in upvote order
        categories = codebook_df.drop_duplicates("primary_category") \
                                .sort_values("_upvotes", ascending=False)["primary_category"] \
                                .dropna().tolist()
        categories = [c for c in categories if str(c) != "nan"]

        filter_btns = "".join(
            f'<button class="filter-btn" onclick="filterBy(this, \'{c}\')">{c}</button>'
            for c in categories
        )

        return f"""
        <div class="thread-post">
        <div class="thread-vote-col">
            <div class="vote-up">▲</div>
            <div class="vote-count">{fmt_score(total_votes)}</div>
            <div class="vote-down" style="color:var(--muted)">▼</div>
        </div>
        <div class="thread-body">
            <div class="post-meta">
            <a href="" onclick="return false;">r/ChemistryStudents</a> &nbsp;·&nbsp; Posted by <a href="" onclick="return false;">u/BritneyRobinson</a>
            </div>
            <span class="flair">Survey Question</span>
            <div class="post-title">{question}</div>
            <div class="post-footer">
            <span class="post-action">💬 {num_comments} Themes</span>
            <span class="post-action">🔗 Share</span>
            <span class="post-action">⭐ Save</span>
            </div>
        </div>
        </div>

        <div class="filter-bar">
            <span class="filter-label">Filter:</span>
            <button class="filter-btn active" onclick="filterBy(this, null)">All</button>
            {filter_btns}
        </div>

        <div class="comments-wrap">
        {comments_html}
        </div>
        """


    # # ── Main ──────────────────────────────────────────────────────────────────────

    try:
        qs, codebooks, tag_counts = load_data()
    except Exception as e:
        st.error(f"Could not load data: {e}")
        st.stop()

    st.write("")
    mobile_warning()
    with st.expander("ℹ️ How to read this page"):
        st.markdown("""
        This page displays student responses to open-ended survey questions, organized like a Reddit thread.
        Reddit is a popular social media platform where people post and comment. Here, each survey question
        is a "post," and each response theme is a "comment." The responses shown are representative quotes
        drawn from real student answers, which were read, tagged, and grouped by theme. The **upvote count (▲)**
        next to each response shows how many students expressed that same sentiment. Comments are sorted from
        most to least common, so the themes at the top reflect what the most students said.
        """)
    
    st.markdown(
        "<p style='font-size:13px;color:#818384;margin:8px 0 4px'>Click a question to open the thread:</p>",
        unsafe_allow_html=True,
    )

    cols = st.columns(len(QUESTION_LABELS))
    for col, (q_key, question) in zip(cols, QUESTION_LABELS.items()):
        flair_color, flair_bg = FLAIR_COLORS[q_key]
        label = question# [:42] + "…"
        if col.button(label, key=f"nav_{q_key}", use_container_width=True):
            st.session_state.page = "thread"
            st.session_state.selected_q = q_key
            st.rerun()


    if not st.session_state.selected_q:
        st.warning("Select at least one question in the sidebar.")
        st.stop()

    posts_html = render_post(st.session_state.selected_q, codebooks[st.session_state.selected_q], tag_counts[st.session_state.selected_q])

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="utf-8"></head>
    <body>
    {CSS}
    <div class="wrap">
    <div class="topbar">
        <div class="topbar-logo">bruintalk</div>
        <div class="topbar-sub">r/ChemistryStudents</div>
        <div class="topbar-nav">
        <span>Hot</span><span>New</span><span>Top</span><span>Rising</span>
        </div>
    </div>
    {posts_html}
    </div>""" + \
    """<script>
    function filterBy(btn, category) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    document.querySelectorAll('.comment').forEach(el => {
        console.log(el);
        if (!category || el.dataset.category === category) {
        el.style.display = '';
        } else {
        el.style.display = 'none';
        }
    });
    }
    </script>
    </body>
    </html>
    """

    # Estimate height: ~300px per post header + ~120px per comment
    estimated_height = 300 + 120 * len(codebooks[st.session_state.selected_q])

    components.html(full_html, height=min(estimated_height, 8000), scrolling=True)




pg = st.navigation([Overview, Quantitative_Responses, Qualitative_Responses])
pg.run()