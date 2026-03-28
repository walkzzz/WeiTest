"""Configuration Encryption - encrypts and decrypts sensitive configuration values"""

from typing import Optional
from cryptography.fernet import Fernet


class ConfigEncryption:
    """配置加密器"""

    def __init__(self, key: Optional[str] = None) -> None:
        """
        初始化加密器

        Args:
            key: 加密密钥 (可选，不提供则生成新密钥)
        """
        if key:
            self.key = key.encode()
        else:
            self.key = Fernet.generate_key()

        self.cipher = Fernet(self.key)

    def encrypt(self, value: str) -> str:
        """
        加密值

        Args:
            value: 要加密的值

        Returns:
            加密后的值 (带 ENC[] 标记)
        """
        encrypted = self.cipher.encrypt(value.encode())
        return f"ENC[{encrypted.decode()}]"

    def decrypt(self, encrypted_value: str) -> str:
        """
        解密值

        Args:
            encrypted_value: 加密的值 (格式：ENC[...])

        Returns:
            解密后的值
        """
        if not encrypted_value.startswith("ENC[") or not encrypted_value.endswith("]"):
            raise ValueError("无效的加密值格式")

        encrypted_data = encrypted_value[4:-1].encode()
        decrypted = self.cipher.decrypt(encrypted_data)
        return decrypted.decode()

    def is_encrypted(self, value: str) -> bool:
        """
        检查值是否已加密

        Args:
            value: 要检查的值

        Returns:
            bool: 是否已加密
        """
        return value.startswith("ENC[") and value.endswith("]")

    def save_key(self, key_path: str) -> None:
        """
        保存密钥到文件

        Args:
            key_path: 密钥文件路径
        """
        with open(key_path, "w") as f:
            f.write(self.key.decode())

    @classmethod
    def load_key(cls, key_path: str) -> "ConfigEncryption":
        """
        从文件加载密钥

        Args:
            key_path: 密钥文件路径

        Returns:
            ConfigEncryption 实例
        """
        with open(key_path, "r") as f:
            key = f.read().strip()
        return cls(key)
