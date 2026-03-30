import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="r/Python • Reddit", layout="wide")

# ── Data ─────────────────────────────────────────────────────────────────────

POST = {
    "subreddit": "r/Python",
    "author": "throwaway_dev_42",
    "time": "6 hours ago",
    "title": "I accidentally rewrote our entire backend in a weekend and it's 10x faster",
    "body": (
        "So this started as me just trying to fix a single slow endpoint. "
        "48 hours later I had replaced our Flask monolith with FastAPI + async SQLAlchemy "
        "and our p99 latency dropped from 4200ms to 380ms. My manager doesn't know yet. "
        "The git diff is... substantial."
    ),
    "score": 14800,
    "awards": ["🏆", "🥇", "❤️"],
    "flair": "Discussion",
    "num_comments": 312,
}

COMMENTS = [
    {
        "author": "pythonista_pete",
        "time": "5 hours ago",
        "score": 4200,
        "text": "The best part of this story is 'my manager doesn't know yet'. Sir, they follow you on GitHub.",
        "replies": [
            {
                "author": "throwaway_dev_42",
                "time": "5 hours ago",
                "score": 2100,
                "text": "I set the repo to private at 3am. I'm not a monster.",
                "replies": [
                    {
                        "author": "git_blame_game",
                        "time": "4 hours ago",
                        "score": 891,
                        "text": "The commit timestamps are still going to betray you. 'feat: minor cleanup' at 2:47am on a Saturday.",
                        "replies": [],
                    }
                ],
            }
        ],
    },
    {
        "author": "async_await_anxiety",
        "time": "5 hours ago",
        "score": 3100,
        "text": (
            "FastAPI is genuinely one of the best decisions I've made in recent years. "
            "The automatic OpenAPI docs alone saved us dozens of hours of back-and-forth with the frontend team."
        ),
        "replies": [
            {
                "author": "django_die_hard",
                "time": "4 hours ago",
                "score": 720,
                "text": "Counterpoint: Django REST Framework + drf-spectacular gives you the same thing with 10 years of battle-testing behind it.",
                "replies": [
                    {
                        "author": "async_await_anxiety",
                        "time": "4 hours ago",
                        "score": 540,
                        "text": "Fair, but have you felt the async? Have you truly felt it?",
                        "replies": [],
                    }
                ],
            }
        ],
    },
    {
        "author": "senior_eng_seniority",
        "time": "4 hours ago",
        "score": 2800,
        "text": (
            "Genuine question: how did you handle the migration of in-flight requests, "
            "session state, and any background jobs that were tied to the old Flask request context? "
            "That's usually the part that turns a weekend rewrite into a 3-month project."
        ),
        "replies": [
            {
                "author": "throwaway_dev_42",
                "time": "4 hours ago",
                "score": 1500,
                "text": "We have no background jobs, no session state (JWT), and it's an internal tool with ~20 users. I chose my battlefield wisely.",
                "replies": [
                    {
                        "author": "senior_eng_seniority",
                        "time": "3 hours ago",
                        "score": 980,
                        "text": "Okay that's actually completely reasonable then. Carry on. 🫡",
                        "replies": [],
                    }
                ],
            }
        ],
    },
    {
        "author": "sqlalchemy_simp",
        "time": "3 hours ago",
        "score": 1200,
        "text": "Async SQLAlchemy 2.0 is so good it should be illegal. The `async with AsyncSession()` pattern is clean as hell.",
        "replies": [],
    },
    {
        "author": "rewrite_survivor",
        "time": "2 hours ago",
        "score": 654,
        "text": (
            "I once rewrote something over a weekend that took down prod for 6 hours on Monday. "
            "Not saying that'll happen to you. Just. Be careful out there."
        ),
        "replies": [
            {
                "author": "throwaway_dev_42",
                "time": "2 hours ago",
                "score": 412,
                "text": "I have a rollback plan. The rollback plan is to quit.",
                "replies": [],
            }
        ],
    },
]

# ── Helpers ──────────────────────────────────────────────────────────────────

def fmt_score(n: int) -> str:
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def render_comment(c: dict, depth: int = 0) -> str:
    indent = depth * 20
    border_colors = ["#ff4500", "#0dd3bb", "#46d160", "#ffd635", "#e4abff"]
    border = border_colors[depth % len(border_colors)]

    replies_html = "".join(render_comment(r, depth + 1) for r in c.get("replies", []))

    op_badge = (
        '<span class="op-badge">OP</span>' if c["author"] == POST["author"] else ""
    )

    return f"""
    <div class="comment" style="margin-left:{indent}px; border-left: 2px solid {border};">
      <div class="comment-meta">
        <span class="comment-author">{c['author']}</span>{op_badge}
        <span class="comment-score">▲ {fmt_score(c['score'])}</span>
        <span class="comment-time">• {c['time']}</span>
      </div>
      <div class="comment-body">{c['text']}</div>
      <div class="comment-actions">
        <span class="action">▲ Upvote</span>
        <span class="action">▼ Downvote</span>
        <span class="action">💬 Reply</span>
        <span class="action">Share</span>
        <span class="action">Report</span>
      </div>
      {replies_html}
    </div>
    """


# ── CSS ──────────────────────────────────────────────────────────────────────

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap');

:root {
  --bg:       #1a1a1b;
  --surface:  #272729;
  --border:   #343536;
  --text:     #d7dadc;
  --muted:    #818384;
  --orange:   #ff4500;
  --blue:     #0079d3;
  --green:    #46d160;
}

.reddit-wrap {
  font-family: 'IBM Plex Sans', sans-serif;
  background: var(--bg);
  color: var(--text);
  max-width: 740px;
  margin: 0 auto;
  padding: 16px 0 40px;
}

/* ── Top bar ── */
.topbar {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  padding: 10px 12px;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
}
.topbar-logo {
  font-size: 22px;
  font-weight: 700;
  color: var(--orange);
  letter-spacing: -0.5px;
}
.topbar-sub {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
}
.topbar-nav {
  margin-left: auto;
  display: flex;
  gap: 16px;
  font-size: 13px;
  color: var(--muted);
}
.topbar-nav span { cursor: pointer; }
.topbar-nav span:hover { color: var(--text); }

/* ── Post card ── */
.post-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  display: flex;
  gap: 0;
  margin-bottom: 10px;
  overflow: hidden;
}
.vote-col {
  background: #1e1e1f;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 6px;
  gap: 4px;
  min-width: 40px;
  font-size: 11px;
  color: var(--muted);
}
.vote-up   { color: var(--orange); font-size: 18px; cursor: pointer; }
.vote-down { font-size: 18px; cursor: pointer; }
.vote-count { font-weight: 700; font-size: 13px; color: var(--text); }
.post-body {
  padding: 10px 12px;
  flex: 1;
}
.post-meta {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 6px;
}
.post-meta a { color: var(--blue); text-decoration: none; }
.post-flair {
  display: inline-block;
  background: #0079d326;
  color: var(--blue);
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 12px;
  margin-right: 8px;
}
.post-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text);
  line-height: 1.3;
  margin: 6px 0 8px;
}
.post-text {
  font-size: 14px;
  color: #c8cbcf;
  line-height: 1.6;
  margin-bottom: 10px;
  padding: 10px 12px;
  background: #1e1e1f;
  border-radius: 4px;
}
.awards {
  display: inline-flex;
  gap: 4px;
  margin-right: 10px;
}
.award { font-size: 16px; }
.post-actions {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
.post-action {
  font-size: 12px;
  font-weight: 700;
  color: var(--muted);
  padding: 6px 8px;
  border-radius: 2px;
  cursor: pointer;
  white-space: nowrap;
}
.post-action:hover { background: var(--border); color: var(--text); }

/* ── Sort bar ── */
.sort-bar {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--muted);
  margin-bottom: 10px;
}
.sort-label { font-weight: 600; color: var(--text); }
.sort-btn {
  padding: 5px 10px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
}
.sort-btn.active { background: var(--border); color: var(--text); }
.sort-btn:hover  { background: var(--border); }

/* ── Comments ── */
.comments-wrap {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 12px 16px;
}
.comment {
  padding: 10px 0 4px 12px;
  margin-top: 8px;
}
.comment-meta {
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}
.comment-author {
  font-weight: 700;
  font-size: 13px;
  color: var(--text);
  cursor: pointer;
}
.comment-author:hover { text-decoration: underline; }
.comment-score  { color: var(--orange); font-weight: 700; font-size: 12px; }
.comment-time   { color: var(--muted); }
.op-badge {
  background: var(--blue);
  color: #fff;
  font-size: 10px;
  font-weight: 700;
  padding: 1px 5px;
  border-radius: 2px;
  letter-spacing: 0.5px;
}
.comment-body {
  font-size: 14px;
  line-height: 1.6;
  color: #c8cbcf;
  margin-bottom: 5px;
}
.comment-actions {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}
.action {
  font-size: 12px;
  font-weight: 700;
  color: var(--muted);
  padding: 4px 6px;
  border-radius: 2px;
  cursor: pointer;
}
.action:hover { background: var(--border); color: var(--text); }
</style>
"""

# ── Build HTML ────────────────────────────────────────────────────────────────

awards_html = "".join(f'<span class="award">{a}</span>' for a in POST["awards"])
comments_html = "".join(render_comment(c) for c in COMMENTS)

HTML = f"""
{CSS}
<div class="reddit-wrap">

  <!-- Top bar -->
  <div class="topbar">
    <div class="topbar-logo">reddit</div>
    <div class="topbar-sub">{POST['subreddit']}</div>
    <div class="topbar-nav">
      <span>Hot</span><span>New</span><span>Top</span><span>Rising</span>
    </div>
  </div>

  <!-- Post -->
  <div class="post-card">
    <div class="vote-col">
      <div class="vote-up">▲</div>
      <div class="vote-count">{fmt_score(POST['score'])}</div>
      <div class="vote-down">▼</div>
    </div>
    <div class="post-body">
      <div class="post-meta">
        <a href="#">{POST['subreddit']}</a> &nbsp;•&nbsp;
        Posted by <a href="#">u/{POST['author']}</a> &nbsp;{POST['time']}
      </div>
      <span class="post-flair">{POST['flair']}</span>
      <div class="post-title">{POST['title']}</div>
      <div class="post-text">{POST['body']}</div>
      <div style="display:flex;align-items:center;margin-bottom:8px;">
        <div class="awards">{awards_html}</div>
      </div>
      <div class="post-actions">
        <span class="post-action">💬 {POST['num_comments']} Comments</span>
        <span class="post-action">🔗 Share</span>
        <span class="post-action">⭐ Save</span>
        <span class="post-action">… More</span>
      </div>
    </div>
  </div>

  <!-- Sort bar -->
  <div class="sort-bar">
    <span class="sort-label">Sort by:</span>
    <span class="sort-btn active">Best</span>
    <span class="sort-btn">Top</span>
    <span class="sort-btn">New</span>
    <span class="sort-btn">Controversial</span>
  </div>

  <!-- Comments -->
  <div class="comments-wrap">
    {comments_html}
  </div>

</div>
"""

# ── Render ────────────────────────────────────────────────────────────────────

# Use components.html to render arbitrary HTML properly — st.markdown has
# a length limit and falls back to showing raw source for large HTML strings.
components.html(HTML, height=2400, scrolling=True)