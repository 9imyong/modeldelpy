from passlib.context import CryptContext

# bcrypt 해시 스키마 설정
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(plain_password: str) -> str:
    """
    평문 비밀번호를 bcrypt 해시로 변환하여 반환합니다.
    사용 예시:
        from app.utils.security import hash_password
        print(hash_password("my_secure_password"))
    """
    return pwd_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    평문 비밀번호와 저장된 해시를 비교하여 일치 여부를 반환합니다.
    """
    return pwd_context.verify(plain_password, hashed_password)