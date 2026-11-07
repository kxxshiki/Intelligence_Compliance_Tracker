from app.services.llm.base import LLMProvider


class FallbackProvider(LLMProvider):
    def generate_remediation(self, context: str) -> str:
        lower_context = context.lower()
        if "mfa" in lower_context:
            return "Enable MFA for the affected privileged account and re-validate access tokens and sign-in policies."
        if "branch protection" in lower_context or "direct push" in lower_context:
            return "Enable branch protection and block direct pushes to protected branches, then require pull request review before merge."
        if "disk encryption" in lower_context or "security logging" in lower_context:
            return "Turn on encryption and security logging for the affected system, and ensure the logs are retained for audit review."
        if "backup" in lower_context:
            return "Create a fresh backup and verify the most recent backup is within the required retention window."
        if "public access" in lower_context:
            return "Remove public bucket access, enforce private ACLs, and validate the bucket configuration against the public access rule."
        return "Review the evidence and remediate the failed control by applying the approved policy change and re-running compliance evaluation."
