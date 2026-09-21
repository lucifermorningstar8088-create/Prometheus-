from .core.models import ToolResult
class RecoveryEngine:
    def __init__(self,max_attempts=2):self.max_attempts=max_attempts
    def should_retry(self,attempt,result):return (not result.ok) and attempt<self.max_attempts
