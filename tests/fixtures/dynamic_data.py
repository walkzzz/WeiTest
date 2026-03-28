"""Dynamic Test Data Generation with Faker"""

import pytest
from typing import Dict, Any


@pytest.fixture
def fake_user_data():
    """生成虚拟用户数据"""
    try:
        from faker import Faker

        fake = Faker("zh_CN")

        return {
            "username": fake.user_name(),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "name": fake.name(),
            "address": fake.address(),
            "company": fake.company(),
            "password": fake.password(length=12),
        }
    except ImportError:
        # Faker 未安装时返回静态数据
        return {
            "username": "test_user",
            "email": "test@example.com",
            "phone": "13800138000",
            "name": "测试用户",
            "address": "测试地址",
            "company": "测试公司",
            "password": "TestPass123",
        }


@pytest.fixture
def fake_company_data():
    """生成虚拟公司数据"""
    try:
        from faker import Faker

        fake = Faker("zh_CN")

        return {
            "company_name": fake.company(),
            "tax_id": fake.tax_id(),
            "bank_account": fake.bank_country("CN"),
            "address": fake.address(),
            "phone": fake.phone_number(),
            "email": fake.company_email(),
        }
    except ImportError:
        return {
            "company_name": "测试公司",
            "tax_id": "91110000000000000X",
            "bank_account": "1234567890",
            "address": "测试地址",
            "phone": "010-88888888",
            "email": "info@test.com",
        }


@pytest.fixture
def fake_order_data():
    """生成虚拟订单数据"""
    try:
        from faker import Faker

        fake = Faker("zh_CN")

        return {
            "order_id": fake.uuid4(),
            "product_name": fake.catch_phrase(),
            "quantity": fake.random_int(min=1, max=100),
            "unit_price": fake.pyfloat(left_digits=3, right_digits=2, positive=True),
            "total_amount": fake.pyfloat(left_digits=4, right_digits=2, positive=True),
            "shipping_address": fake.address(),
        }
    except ImportError:
        return {
            "order_id": "ORD-001",
            "product_name": "测试商品",
            "quantity": 10,
            "unit_price": 99.99,
            "total_amount": 999.90,
            "shipping_address": "测试地址",
        }


@pytest.fixture
def fake_credit_card():
    """生成虚拟信用卡数据（仅用于测试）"""
    try:
        from faker import Faker

        fake = Faker()

        return {
            "card_number": fake.credit_card_number(),
            "expire_date": fake.credit_card_expire(),
            "security_code": fake.credit_card_security_code(),
            "card_holder": fake.name(),
        }
    except ImportError:
        return {
            "card_number": "4111111111111111",
            "expire_date": "12/25",
            "security_code": "123",
            "card_holder": "Test User",
        }


@pytest.fixture
def fake_browser_data():
    """生成虚拟浏览器数据"""
    try:
        from faker import Faker

        fake = Faker()

        return {
            "user_agent": fake.user_agent(),
            "ip_address": fake.ipv4(),
            "mac_address": fake.mac_address(),
            "chrome_version": fake.chrome(),
            "firefox_version": fake.firefox(),
        }
    except ImportError:
        return {
            "user_agent": "Mozilla/5.0",
            "ip_address": "192.168.1.1",
            "mac_address": "00:11:22:33:44:55",
            "chrome_version": "Chrome/120.0.0.0",
            "firefox_version": "Firefox/121.0",
        }


# ========== Data Template Engine ==========


class DataTemplate:
    """数据模板引擎"""

    def __init__(self):
        try:
            from faker import Faker

            self.fake = Faker("zh_CN")
            self.available = True
        except ImportError:
            self.available = False

    def generate(self, template: Dict[str, str]) -> Dict[str, Any]:
        """
        根据模板生成数据

        Args:
            template: 数据模板

        Returns:
            生成的数据

        示例:
            >>> template = {
            ...     "username": "user_name",
            ...     "email": "email",
            ...     "name": "name"
            ... }
            >>> dt = DataTemplate()
            >>> dt.generate(template)
            {'username': 'zhangsan', 'email': 'test@example.com', ...}
        """
        if not self.available:
            return template

        result = {}
        for key, faker_method in template.items():
            try:
                method = getattr(self.fake, faker_method)
                result[key] = method()
            except AttributeError:
                result[key] = faker_method  # 使用原值

        return result


# ========== Usage Example ==========


@pytest.fixture
def dynamic_test_data():
    """动态测试数据生成器"""
    return DataTemplate()


# ========== Example Usage ==========
"""
# 使用示例 1: 直接使用 fixture
def test_register_user(fake_user_data):
    page.type_text(username_input, fake_user_data["username"])
    page.type_text(email_input, fake_user_data["email"])

# 使用示例 2: 参数化测试
@pytest.mark.parametrize("user_type", ["admin", "user", "guest"])
def test_user_permissions(user_type, fake_user_data):
    fake_user_data["role"] = user_type
    # 测试逻辑

# 使用示例 3: 模板引擎
def test_dynamic_data(dynamic_test_data):
    template = {
        "username": "user_name",
        "email": "email",
        "phone": "phone_number"
    }
    data = dynamic_test_data.generate(template)
    # 使用 data
"""
