
from fastapi import security, Depends, HTTPException  # type: ignore
from secrets import compare_digest

# THE SECURITY COMPONENT OF THE APP.
# REFERENCE: https://fastapi.tiangolo.com/tutorial/security/get-current-user/#get-the-user


# IMPROVEMENT:


# class Authenticator:
#     """FastAPI API key authenticator."""

#     def __init__(self, api_key: str):
#         self.api_key = api_key
#         self.header_scheme = security.APIKeyHeader(name="X-API-Key", auto_error=False)
#         # Build once, not on every call
#         self._dependency = self._build_dependency()

#     def _build_dependency(self):
#         api_key = self.api_key
#         header_scheme = self.header_scheme

#         async def verify(key: str = Depends(header_scheme)):
#             if not key or not compare_digest(key, api_key):
#                 raise HTTPException(status_code=401, detail="Invalid API key")
#             return key  # meaningful return

#         return Depends(verify)

#     def __call__(self) -> Depends:
#         return self._dependency

class Authenticator:
    """My FastAPI authenticator"""

    def __init__(self, api_key:str):
        self.header_scheme = security.APIKeyHeader(name="X-API-Key", auto_error=False)
        self.api_key = api_key
        self._dependency = self._build_dependency()
    
    def __call__(self) -> Depends:
        """Returns the dependency OBJECT (fastapi.Depends)."""
        async def verify_key(key: str = Depends(self.header_scheme)):
            if not key or not compare_digest(key, self.api_key):
                raise HTTPException(status_code=401, detail="Invalid API key")  # This is a CRITICAL line which protects my endpoint. Without it, access is granted REGARDLESS of return value.
            return True  # this return value is meaningless in this context
        
        return Depends(verify_key)
