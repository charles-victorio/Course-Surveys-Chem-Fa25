import base64

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

st.set_page_config(page_title="Survey Responses", layout="wide")

# ── Load Data ─────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    qs = {
        "nervous":          pd.read_csv("tagged_qualitative/deepseek_tagged_nervous.csv"),
        "when_connected":   pd.read_csv("tagged_qualitative/deepseek_tagged_when_connected.csv"),
        "learn_best":       pd.read_csv("tagged_qualitative/deepseek_tagged_learn_best.csv"),
        "why_peer_learning":pd.read_csv("tagged_qualitative/deepseek_tagged_why_peer_learning.csv"),
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