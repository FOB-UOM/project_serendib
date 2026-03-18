"""Full Streamlit platform app for Project Serendib v2."""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st
from persistence import (
    connect,
    db_stats,
    init_db,
    insert_public_submission,
    list_public_submissions,
)

st.set_page_config(page_title="Project Serendib v2 Platform", page_icon="🌱", layout="wide")

REPO_ROOT = Path(__file__).resolve().parents[1]
PUBLIC_TASKS_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "public_tasks.json"
PUBLIC_SUBMISSIONS_PATH = REPO_ROOT / "shared" / "argilla" / "infra" / "public_submissions.json"
DB_CONN = connect()
init_db(DB_CONN)

PILLARS: dict[str, list[str]] = {
    "pillar-education-human-development": [
        "teacher-empowerment",
        "philosophy-psychology-personality",
        "art-literature-culture",
    ],
    "pillar-economy-enterprise": [
        "business-sme-bpm",
        "finance-financial-literacy",
        "political-economy",
    ],
    "pillar-society-environment": [
        "sociology-social-dynamics",
        "sustainability-climate",
    ],
}


@st.cache_data
def load_route_ocr():
    router_path = REPO_ROOT / "shared" / "ocr-pipeline" / "hybrid_router.py"
    spec = importlib.util.spec_from_file_location("hybrid_router", router_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load shared OCR router.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.route_ocr


@st.cache_resource
def load_gamification_module():
    module_path = REPO_ROOT / "shared" / "scripts" / "gamification.py"
    spec = importlib.util.spec_from_file_location("gamification", module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load gamification module.")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def list_non_placeholder_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    return [item for item in path.iterdir() if item.name != ".gitkeep"]


def count_pillar_files() -> int:
    total = 0
    for pillar, subpillars in PILLARS.items():
        for subpillar in subpillars:
            total += len(list_non_placeholder_files(REPO_ROOT / pillar / subpillar))
    return total


def load_json_list(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        return []
    return payload


def save_json_list(path: Path, payload: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


st.title("Project Serendib v2")
st.caption("Sovereign Sinhala Data Ecosystem")
language = st.sidebar.selectbox("Language", ["English", "සිංහල"], index=0)
high_contrast = st.sidebar.checkbox("High contrast mode", value=False)
if high_contrast:
    st.markdown(
        """
<style>
:root { color-scheme: light; }
.block-container { background-color: #ffffff; color: #111111; }
</style>
""",
        unsafe_allow_html=True,
    )

if language == "සිංහල":
    st.write("මෙය දිගුකාලීන පීඨ මූලික ව්‍යාපෘතියකි.")
else:
    st.write("This is a quiet, long-term faculty seed project.")

with st.sidebar:
    st.header("Platform Navigation")
    section = st.radio(
        "Go to",
        [
            "Overview",
            "Pillar Explorer",
            "OCR Workbench",
            "Public Task Studio",
            "Operations Dashboard",
            "Accounts & Badges",
            "Contribution Desk",
            "Roadmap",
        ],
    )
    st.markdown("---")
    st.markdown("**Core Links**")
    st.markdown("- `PROPOSAL-v2.md`")
    st.markdown("- `CONTRIBUTING.md`")
    st.markdown("- `shared/argilla/`")

if section == "Overview":
    st.subheader("Nationally Aligned 3-Pillar Architecture")
    col1, col2, col3 = st.columns(3)
    col1.metric("Main Pillars", len(PILLARS))
    col2.metric("Visible Sub-pillars", sum(len(v) for v in PILLARS.values()))
    col3.metric("Current content files", count_pillar_files())

    st.markdown("### Pillars")
    for pillar_name, subpillars in PILLARS.items():
        st.markdown(f"- **{pillar_name}**")
        for subpillar in subpillars:
            st.markdown(f"  - `{subpillar}/`")

    st.info("Use the Pillar Explorer to inspect each sub-pillar and start contributing.")

elif section == "Pillar Explorer":
    st.subheader("Pillar Explorer")
    selected_pillar = st.selectbox("Select pillar", list(PILLARS))
    selected_subpillar = st.selectbox("Select sub-pillar", PILLARS[selected_pillar])

    target_path = REPO_ROOT / selected_pillar / selected_subpillar
    st.code(str(target_path))

    files = list_non_placeholder_files(target_path)
    if files:
        st.success(f"Found {len(files)} file(s) in this sub-pillar.")
        for file_path in sorted(files):
            st.write(f"- {file_path.name}")
    else:
        st.warning("This sub-pillar is currently empty (template-ready).")
        st.caption("Create a README or dataset file here to begin.")

elif section == "OCR Workbench":
    st.subheader("Shared OCR Workbench")
    st.write("Signature shared layer: `shared/ocr-pipeline/`")

    route_ocr = load_route_ocr()

    document_name = st.text_input(
        "Document name",
        value="handwritten_scan_page_01.jpg",
        help="Try names like handwritten_scan_page_01.jpg or clean_document.png",
    )
    mode = st.selectbox("Routing mode", ["auto", "tesseract", "qwen2_vl"])
    if st.button("Route OCR", type="primary"):
        engine = route_ocr(document_name, mode)
        st.success(f"Selected OCR engine: {engine}")

    st.markdown("### Improvement Loop")
    st.markdown(
        """
1. Put incoming samples in `shared/ocr-pipeline/incoming/`
2. Route via CLI (`shared/ocr-pipeline/cli.py`)
3. Send uncertain outputs to Argilla
4. Feed corrections into the next quality cycle
"""
    )

elif section == "Public Task Studio":
    st.subheader("Public Task Studio (No GitHub Needed)")
    st.caption("For school students, teachers, and citizens to contribute directly.")

    tasks = load_json_list(PUBLIC_TASKS_PATH)
    submissions = list_public_submissions(DB_CONN)

    if not tasks:
        st.warning("No public tasks are currently configured.")
    else:
        task_labels = [f"{task['task_id']} — {task['title']}" for task in tasks]
        selected_label = st.selectbox("Choose a task", task_labels)
        selected_task = tasks[task_labels.index(selected_label)]

        st.markdown(f"**Pillar path:** `{selected_task['pillar']}`")
        st.markdown(f"**Prompt:** {selected_task['prompt']}")
        st.markdown(f"**Difficulty:** `{selected_task['difficulty']}`")

        contributor_name = st.text_input("Your name (optional)", value="")
        response_text = st.text_area("Your contribution", height=180)
        self_rating = st.slider("How confident are you?", min_value=1, max_value=5, value=3)

        if st.button("Submit contribution", type="primary"):
            cleaned = response_text.strip()
            if not cleaned:
                st.error("Please enter your contribution before submitting.")
            else:
                submission = {
                    "task_id": selected_task["task_id"],
                    "response_text": cleaned,
                    "contributor_name": contributor_name.strip() or "Anonymous",
                    "self_rating": self_rating,
                    "submitted_at": datetime.now(timezone.utc).isoformat(),
                }
                submission_id = insert_public_submission(DB_CONN, submission)
                submission["id"] = submission_id
                st.success("Thank you! Your contribution has been recorded.")

    st.markdown("#### Recent Public Contributions")
    if not submissions:
        st.info("No submissions yet.")
    else:
        recent_rows = []
        for item in reversed(submissions[-10:]):
            recent_rows.append(
                {
                    "task_id": item["task_id"],
                    "contributor": item.get("contributor_name", "Anonymous"),
                    "rating": item.get("self_rating", 3),
                    "submitted_at": item.get("submitted_at", "-"),
                    "status": item.get("status", "pending"),
                }
            )
        st.table(recent_rows)

elif section == "Operations Dashboard":
    st.subheader("Operations Dashboard")
    stats_payload = db_stats(DB_CONN)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Users", stats_payload["users"])
    c2.metric("Events", stats_payload["events"])
    c3.metric("Pending moderation", stats_payload["pending_submissions"])
    c4.metric("Approved submissions", stats_payload["approved_submissions"])

    denom = stats_payload["approved_submissions"] + stats_payload["rejected_submissions"]
    quality_score = stats_payload["approved_submissions"] / denom if denom else 0.0
    st.metric("Moderation quality score", f"{quality_score:.2%}")

    st.markdown("#### Pillar dataset growth (seed + exported records)")
    growth_rows = []
    for path in sorted(REPO_ROOT.glob("pillar-*/**/*.jsonl")):
        count = sum(1 for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip())
        growth_rows.append({"path": str(path.relative_to(REPO_ROOT)), "records": count})
    if growth_rows:
        st.table(growth_rows)
    else:
        st.info("No JSONL records found yet.")

elif section == "Accounts & Badges":
    st.subheader("Contributor Accounts + Gamification")
    st.caption("Backed by `shared/argilla/infra/state.json` and shared scripts.")

    gm = load_gamification_module()
    state_path = REPO_ROOT / "shared" / "argilla" / "infra" / "state.json"
    state = gm.load_state(state_path)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Register Contributor")
        username = st.text_input("Username", value="")
        display_name = st.text_input("Display name", value="")
        if st.button("Create account"):
            if not username.strip():
                st.error("Username is required.")
            else:
                try:
                    gm.register_user(state, username.strip(), display_name.strip() or None)
                    gm.save_state(state_path, state)
                    st.success(f"Account created: {username.strip()}")
                except ValueError as exc:
                    st.error(str(exc))

    with c2:
        st.markdown("#### Record Contribution Event")
        event_user = st.text_input("Contributor username", value="")
        event_type = st.selectbox("Event type", ["verify", "curate", "evaluate", "maintain"])
        units = st.number_input("Units", min_value=1, value=1, step=1)
        if st.button("Record event"):
            if not event_user.strip():
                st.error("Contributor username is required.")
            else:
                try:
                    event = gm.record_event(state, event_user.strip(), event_type, int(units))
                    gm.save_state(state_path, state)
                    st.success(
                        f"Recorded {event['event_type']} x{event['units']} "
                        f"(+{event['points_gained']} points)"
                    )
                except ValueError as exc:
                    st.error(str(exc))

    st.markdown("#### Leaderboard")
    leaders = gm.leaderboard(state, top_n=20)
    if not leaders:
        st.info("No contributors yet. Register the first account to begin.")
    else:
        rows = []
        for rank, user in enumerate(leaders, start=1):
            rows.append(
                {
                    "rank": rank,
                    "username": user["username"],
                    "display_name": user.get("display_name", user["username"]),
                    "points": user["points"],
                    "badges": ", ".join(user.get("badges", [])) or "-",
                }
            )
        st.table(rows)

    st.markdown("#### Argilla Integration Notes")
    st.markdown(
        """
- Use Argilla-native auth/RBAC for production access control.
- Keep tokens in environment variables (never commit secrets).
- Ingest verified Argilla records as `verify/curate/evaluate` events.
"""
    )

elif section == "Contribution Desk":
    st.subheader("Contribution Desk")
    st.markdown("### Where to contribute")
    st.markdown(
        """
- Pillar-specific work: contribute inside the most relevant sub-pillar
- Cross-pillar tools: `shared/scripts/`
- OCR improvements: `shared/ocr-pipeline/`
- Student tasks: `.github/ISSUE_TEMPLATE/student-task.md`
"""
    )
    st.markdown("### Student contribution checklist")
    st.markdown(
        """
- [ ] Pick the correct pillar/sub-pillar
- [ ] Add source/reference where relevant
- [ ] Avoid private or sensitive data
- [ ] Run lint/tests before PR
"""
    )

elif section == "Roadmap":
    st.subheader("Architectural Next Steps")
    st.caption("Detailed plan: `docs/EXECUTION-ROADMAP-v2.md`")
    st.markdown(
        """
1. **Data contracts**: define per-pillar schemas and metadata standards.
2. **Automated ingestion**: connect OCR + Argilla + workflows into a clean data loop.
3. **Quality scoring**: add measurable quality gates for provenance, safety, and coverage.
4. **Contributor operations**: establish student onboarding cycles and release cadence.
5. **Public delivery**: publish periodic snapshots/releases for transparent reuse.
"""
    )
    st.success("The platform is modular; new pillars can be added via `future-pillars-template/`.")
