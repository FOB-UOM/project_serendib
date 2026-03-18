import importlib.util
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "shared" / "scripts" / "gamification.py"

spec = importlib.util.spec_from_file_location("gamification", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError("Unable to load gamification module")
gamification = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gamification
spec.loader.exec_module(gamification)


def test_register_user_and_record_event_awards_points_and_badges():
    state = gamification.default_state()
    gamification.register_user(state, "naveen", "Naveen")

    gamification.record_event(state, "naveen", "maintain", units=2)
    user = state["users"][0]

    assert user["points"] == 16
    assert "Bronze" in user["badges"]


def test_leaderboard_sorted_by_points_descending():
    state = gamification.default_state()
    gamification.register_user(state, "user_a")
    gamification.register_user(state, "user_b")

    gamification.record_event(state, "user_a", "verify", units=1)
    gamification.record_event(state, "user_b", "curate", units=1)

    ranking = gamification.leaderboard(state)
    assert ranking[0]["username"] == "user_b"
