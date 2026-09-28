
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from guild.system import Guild


def test_warehouse_logged():
    g = Guild("test")
    g.add_member("p1", "leader")
    g.warehouse_deposit("p1", "sword")
    g.warehouse_withdraw("p1", "sword")
    assert len(g.warehouse_log) == 2
    assert g.warehouse_log[0]["action"] == "deposit"


def test_permission_configurable():
    g = Guild("test")
    g.add_member("p1", "member")
    g.set_permission("member", "withdraw", False)
    assert g.has_permission("p1", "withdraw") == False


def test_leave_preserves_contribution():
    g = Guild("test")
    g.add_member("p1", "member")
    g.members["p1"]["contribution"] = 500
    g.leave_guild("p1")
    assert g.frozen_contributions.get("p1", 0) == 500


def test_announcement_editor_recorded():
    g = Guild("test")
    g.add_member("p1", "vice")
    g.edit_announcement("p1", "新公告")
    assert g.announcements[-1]["editor"] == "p1"


def test_application_timeout():
    g = Guild("test")
    g.applications.append({"id": "a1", "pid": "p2", "timestamp": 0})
    g.process_timeout(1000)
    assert len(g.applications) == 0


def test_funds_approval_required():
    g = Guild("test")
    g.add_member("p1", "vice")
    result = g.use_funds("p1", 500)
    assert result == False  # 需要审批
    assert g.funds == 1000


def test_funds_small_auto_approved():
    g = Guild("test")
    g.add_member("p1", "vice")
    result = g.use_funds("p1", 10)
    assert result == True
    assert g.funds == 990


def test_guild_dissolve_archive():
    g = Guild("test")
    g.skills["power"] = 5
    g.dissolve()
    assert g.archived == True
    assert g.archived_data["skills"]["power"] == 5


def test_rejoin_restores_contribution():
    g = Guild("test")
    g.add_member("p1", "member")
    g.members["p1"]["contribution"] = 500
    g.leave_guild("p1")
    g.add_member("p1", "member")
    assert g.members["p1"]["contribution"] == 500
