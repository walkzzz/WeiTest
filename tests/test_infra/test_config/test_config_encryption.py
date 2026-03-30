"""配置加密完整测试"""

import pytest
from pathlib import Path
from infra.config.config_encryption import ConfigEncryption


class TestConfigEncryption:
    """配置加密测试"""

    @pytest.fixture
    def encryption(self):
        """创建加密器实例"""
        return ConfigEncryption()

    def test_encrypt(self, encryption):
        """测试加密"""
        secret = "password123"
        encrypted = encryption.encrypt(secret)
        assert encrypted.startswith("ENC[")
        assert encrypted.endswith("]")

    def test_decrypt(self, encryption):
        """测试解密"""
        secret = "password123"
        encrypted = encryption.encrypt(secret)
        decrypted = encryption.decrypt(encrypted)
        assert decrypted == secret

    def test_is_encrypted_true(self, encryption):
        """测试检查已加密"""
        encrypted = encryption.encrypt("secret")
        assert encryption.is_encrypted(encrypted) is True

    def test_is_encrypted_false(self, encryption):
        """测试检查未加密"""
        assert encryption.is_encrypted("plain") is False

    def test_save_key(self, encryption, tmp_path):
        """测试保存密钥"""
        key_file = tmp_path / "test.key"
        encryption.save_key(str(key_file))
        assert key_file.exists()

    def test_load_key(self, encryption, tmp_path):
        """测试加载密钥"""
        key_file = tmp_path / "test.key"
        encryption.save_key(str(key_file))
        
        loaded = ConfigEncryption.load_key(str(key_file))
        assert loaded is not None

    def test_decrypt_invalid_format(self, encryption):
        """测试解密无效格式"""
        with pytest.raises(ValueError):
            encryption.decrypt("invalid")
