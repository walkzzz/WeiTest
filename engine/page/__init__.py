"""Page module - PageObject pattern implementation"""

from engine.page.base_page import BasePage
from engine.page.yaml_page import YamlPage

__all__ = [
    "BasePage",
    "YamlPage",
]
