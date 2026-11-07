from __future__ import annotations


class EvidenceNormalizer:
    def normalize(self, raw_data: dict) -> dict:
        raise NotImplementedError


class UserSecurityNormalizer(EvidenceNormalizer):
    def normalize(self, raw_data: dict) -> dict:
        username = raw_data.get("username") or raw_data.get("user") or raw_data.get("email") or "unknown-user"
        attrs = {key: value for key, value in raw_data.items() if key not in {"username", "user", "email"}}
        return {"subject_type": "USER", "subject_id": username, "attributes": attrs}


class RepositoryNormalizer(EvidenceNormalizer):
    def normalize(self, raw_data: dict) -> dict:
        name = raw_data.get("repository") or raw_data.get("name") or "unknown-repository"
        attrs = {key: value for key, value in raw_data.items() if key not in {"repository", "name"}}
        return {"subject_type": "REPOSITORY", "subject_id": name, "attributes": attrs}


class ServerNormalizer(EvidenceNormalizer):
    def normalize(self, raw_data: dict) -> dict:
        server = raw_data.get("server") or raw_data.get("hostname") or raw_data.get("system") or "unknown-server"
        attrs = {key: value for key, value in raw_data.items() if key not in {"server", "hostname", "system"}}
        return {"subject_type": "SERVER", "subject_id": server, "attributes": attrs}


class CloudNormalizer(EvidenceNormalizer):
    def normalize(self, raw_data: dict) -> dict:
        bucket = raw_data.get("bucket") or raw_data.get("storage") or raw_data.get("name") or "unknown-bucket"
        attrs = {key: value for key, value in raw_data.items() if key not in {"bucket", "storage", "name"}}
        return {"subject_type": "CLOUD", "subject_id": bucket, "attributes": attrs}


class BackupNormalizer(EvidenceNormalizer):
    def normalize(self, raw_data: dict) -> dict:
        system = raw_data.get("system") or raw_data.get("backup_name") or raw_data.get("name") or "unknown-backup"
        attrs = {key: value for key, value in raw_data.items() if key not in {"system", "backup_name", "name"}}
        return {"subject_type": "BACKUP", "subject_id": system, "attributes": attrs}


class NormalizationService:
    def __init__(self):
        self.strategies = {
            "USER_SECURITY_CONFIGURATION": UserSecurityNormalizer(),
            "REPOSITORY_CONFIGURATION": RepositoryNormalizer(),
            "SERVER_CONFIGURATION": ServerNormalizer(),
            "CLOUD_CONFIGURATION": CloudNormalizer(),
            "BACKUP_CONFIGURATION": BackupNormalizer(),
        }

    def normalize(self, evidence_type: str, raw_data: dict) -> dict:
        strategy = self.strategies.get(evidence_type)
        if strategy is None:
            return {"subject_type": "UNKNOWN", "subject_id": "unknown", "attributes": raw_data}
        return strategy.normalize(raw_data)

    def normalized_text(self, normalized: dict) -> str:
        return str({
            "subject_type": normalized.get("subject_type"),
            "subject_id": normalized.get("subject_id"),
            "attributes": normalized.get("attributes", {}),
        })
