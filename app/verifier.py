from .core.models import VerificationStatus,ToolResult
class Verifier:
    def verify(self,result:ToolResult):
        if not result.ok:return VerificationStatus.UNVERIFIED,[result.error or "tool failed"]
        if result.evidence.get("tested") is False:return VerificationStatus.PARTIAL,["No test command was discoverable"]
        return VerificationStatus.VERIFIED,["Tool completed successfully","Evidence captured"]
