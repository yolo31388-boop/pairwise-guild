
class Guild:
    def __init__(self, name):
        self.name = name
        self.members = {}
        self.warehouse = []
        self.warehouse_log = []
        self.announcements = []
        self.applications = []
        self.funds = 1000
        self.skills = {}
        self.archived = False

    def add_member(self, pid, role="member"):
        self.members[pid] = {"role": role, "contribution": 0}

    def warehouse_deposit(self, pid, item):
        self.warehouse.append(item)
        # BUG: 不记录日志

    def warehouse_withdraw(self, pid, item):
        if item in self.warehouse:
            self.warehouse.remove(item)
            # BUG: 不记录日志
            return item
        return None

    def has_permission(self, pid, action):
        # BUG: 硬编码权限
        role = self.members[pid]["role"]
        if action == "withdraw":
            return role in ["leader", "vice"]
        return True

    def leave_guild(self, pid):
        # BUG: 贡献清零
        del self.members[pid]

    def edit_announcement(self, pid, content):
        self.announcements.append(content)
        # BUG: 不记录编辑者

    def process_application(self, aid, accept):
        # BUG: 不超时
        for app in self.applications:
            if app["id"] == aid:
                if accept:
                    self.add_member(app["pid"])
                self.applications.remove(app)
                return True
        return False

    def use_funds(self, pid, amount):
        # BUG: 无审批
        self.funds -= amount
        return True
