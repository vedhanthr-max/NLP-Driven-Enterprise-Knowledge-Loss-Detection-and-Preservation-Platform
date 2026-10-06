from typing import Any, Optional, Dict
from fastapi import HTTPException, status

class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Any] = None,
        suggestions: Optional[list] = None
    ):
        self.error_code = error_code
        self.message = message
        self.details = details
        self.suggestions = suggestions or []
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": details,
                "suggestions": self.suggestions
            }
        )

# Authentication Errors
class AuthException(AppException):
    def __init__(self, error_code: str, message: str, status_code: int = status.HTTP_401_UNAUTHORIZED, details: Any = None):
        super().__init__(status_code=status_code, error_code=error_code, message=message, details=details)

class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(error_code="ERR-AUTH-002", message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class TokenExpiredException(AuthException):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(error_code="ERR-AUTH-005", message=message, status_code=status.HTTP_401_UNAUTHORIZED)

class InvalidTokenException(AuthException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(error_code="ERR-AUTH-006", message=message, status_code=status.HTTP_401_UNAUTHORIZED)

# Document Errors
class DocumentNotFoundException(AppException):
    def __init__(self, document_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="ERR-DOC-001",
            message="Document not found",
            details={"document_id": document_id}
        )

class InvalidFileFormatException(AppException):
    def __init__(self, received_format: str, allowed_formats: list):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error_code="ERR-DOC-002",
            message="Invalid file format",
            details={"received_format": received_format, "allowed_formats": allowed_formats},
            suggestions=["Convert document to PDF, DOCX, or TXT format"]
        )

class FileTooLargeException(AppException):
    def __init__(self, size_bytes: int, max_bytes: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            error_code="ERR-DOC-003",
            message="File size exceeds maximum allowed limit (50 MB)",
            details={"file_size": size_bytes, "max_size": max_bytes}
        )

# Knowledge Errors
class KnowledgeNotFoundException(AppException):
    def __init__(self, knowledge_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="ERR-KNOW-001",
            message="Knowledge item not found",
            details={"knowledge_id": knowledge_id}
        )

# Risk Errors
class RiskCalculationException(AppException):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error_code="ERR-RISK-001",
            message=message,
            details=details
        )

# Permission Errors
class PermissionDeniedException(AppException):
    def __init__(self, message: str = "Insufficient permissions to perform this action"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="ERR-PERM-001",
            message=message
        )
