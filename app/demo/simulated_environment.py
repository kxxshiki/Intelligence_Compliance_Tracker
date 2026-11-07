from __future__ import annotations

from copy import deepcopy


class SimulatedEnvironment:
    def __init__(self):
        self.users = {
            "admin@example.com": {"username": "admin", "mfa_enabled": False, "is_privileged": True, "authorized": True, "active": True, "days_since_last_login": 10},
            "inactive@example.com": {"username": "inactive", "mfa_enabled": True, "is_privileged": False, "authorized": True, "active": True, "days_since_last_login": 120},
            "analyst@example.com": {"username": "analyst", "mfa_enabled": True, "is_privileged": False, "authorized": True, "active": True, "days_since_last_login": 20},
        }
        self.repositories = {
            "payments-service": {"repository": "payments-service", "branch_protection": False, "allow_direct_push": True},
            "inventory-service": {"repository": "inventory-service", "branch_protection": True, "allow_direct_push": False},
        }
        self.servers = {
            "prod-server-01": {"server": "prod-server-01", "disk_encryption": False, "security_logging": True, "critical_patches_pending": 3},
            "staging-server-01": {"server": "staging-server-01", "disk_encryption": True, "security_logging": True, "critical_patches_pending": 0},
        }
        self.cloud_storage = {
            "customer-data-bucket": {"bucket": "customer-data-bucket", "public_access": True},
            "finance-archive-bucket": {"bucket": "finance-archive-bucket", "public_access": False},
        }
        self.backups = {
            "production-database": {"system": "production-database", "backup_age_hours": 48},
            "analytics-db": {"system": "analytics-db", "backup_age_hours": 10},
        }

    def collect_evidence(self):
        evidence = []
        for subject_id, item in self.users.items():
            evidence.append({"source_type": "USER", "source_name": "users", "asset_identifier": subject_id, "evidence_type": "USER_SECURITY_CONFIGURATION", "raw_data": {"username": item.get("username"), **item}})
        for _, item in self.repositories.items():
            evidence.append({"source_type": "REPOSITORY", "source_name": "repositories", "asset_identifier": item["repository"], "evidence_type": "REPOSITORY_CONFIGURATION", "raw_data": deepcopy(item)})
        for _, item in self.servers.items():
            evidence.append({"source_type": "SERVER", "source_name": "servers", "asset_identifier": item["server"], "evidence_type": "SERVER_CONFIGURATION", "raw_data": deepcopy(item)})
        for _, item in self.cloud_storage.items():
            evidence.append({"source_type": "CLOUD", "source_name": "cloud_storage", "asset_identifier": item["bucket"], "evidence_type": "CLOUD_CONFIGURATION", "raw_data": deepcopy(item)})
        for _, item in self.backups.items():
            evidence.append({"source_type": "BACKUP", "source_name": "backups", "asset_identifier": item["system"], "evidence_type": "BACKUP_CONFIGURATION", "raw_data": deepcopy(item)})
        return evidence

    def apply_action(self, action: str, asset_identifier: str):
        if action == "ENABLE_MFA":
            if asset_identifier in self.users:
                self.users[asset_identifier]["mfa_enabled"] = True
        elif action == "DISABLE_INACTIVE_ACCOUNT":
            for user in self.users.values():
                if user.get("days_since_last_login", 0) > 90:
                    user["active"] = False
        elif action == "AUTHORIZE_PRIVILEGED_USER":
            for user in self.users.values():
                if user.get("is_privileged"):
                    user["authorized"] = True
        elif action == "ENABLE_BRANCH_PROTECTION":
            for repo in self.repositories.values():
                repo["branch_protection"] = True
        elif action == "DISABLE_DIRECT_PUSH":
            for repo in self.repositories.values():
                repo["allow_direct_push"] = False
        elif action == "ENABLE_DISK_ENCRYPTION":
            for server in self.servers.values():
                server["disk_encryption"] = True
        elif action == "ENABLE_SECURITY_LOGGING":
            for server in self.servers.values():
                server["security_logging"] = True
        elif action == "INSTALL_CRITICAL_PATCHES":
            for server in self.servers.values():
                server["critical_patches_pending"] = 0
        elif action == "DISABLE_PUBLIC_ACCESS":
            for bucket in self.cloud_storage.values():
                bucket["public_access"] = False
        elif action == "CREATE_RECENT_BACKUP":
            for backup in self.backups.values():
                backup["backup_age_hours"] = 12

    def drift_example(self):
        self.users["admin@example.com"]["mfa_enabled"] = True
        self.users["inactive@example.com"]["active"] = False
        self.repositories["payments-service"]["branch_protection"] = True
        self.repositories["payments-service"]["allow_direct_push"] = False
        self.servers["prod-server-01"]["disk_encryption"] = True
        self.servers["prod-server-01"]["critical_patches_pending"] = 0
        self.cloud_storage["customer-data-bucket"]["public_access"] = False
        self.backups["production-database"]["backup_age_hours"] = 10
