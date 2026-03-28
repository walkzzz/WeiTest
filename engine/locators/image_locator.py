"""Image Locator - locate elements by image template matching with full type annotations"""

import os
from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class ImageLocator:
    """
    图像定位器

    使用模板匹配定位 UI 元素

    Example:
        >>> locator = ImageLocator("buttons/login.png", threshold=0.9)
        >>> page.click(locator)

        >>> locator = ImageLocator("icons/save.png", timeout=10)
        >>> page.wait_element(locator)
    """

    template_path: str  # 模板图片路径
    threshold: float = 0.8  # 匹配阈值 (0-1)
    timeout: int = 10  # 超时时间
    description: str = ""  # 元素描述

    def __post_init__(self) -> None:
        """验证模板路径"""
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"模板图片不存在：{self.template_path}")
        if not 0 <= self.threshold <= 1:
            raise ValueError(f"阈值必须在 0-1 之间：{self.threshold}")
        if self.timeout < 0:
            raise ValueError(f"超时时间不能为负数：{self.timeout}")

    def locate(self, region: Optional[Tuple[int, int, int, int]] = None) -> Tuple[int, int]:
        """
        定位图像

        Args:
            region: 搜索区域 (x, y, width, height)

        Returns:
            (x, y) 中心点坐标

        Raises:
            ValueError: 未找到图像时
            ImportError: 未安装 pyautogui 时
        """
        try:
            import pyautogui
        except ImportError:
            raise ImportError("请安装 pyautogui: pip install pyautogui")

        location = pyautogui.locateOnScreen(
            self.template_path, confidence=self.threshold, region=region
        )

        if location is None:
            raise ValueError(f"未找到图像：{self.template_path}")

        center = pyautogui.center(location)
        return (center.x, center.y)

    def locate_all(
        self, region: Optional[Tuple[int, int, int, int]] = None
    ) -> List[Tuple[int, int]]:
        """
        定位所有匹配的图像

        Args:
            region: 搜索区域

        Returns:
            所有匹配位置列表
        """
        try:
            import pyautogui
        except ImportError:
            raise ImportError("请安装 pyautogui: pip install pyautogui")

        locations = pyautogui.locateAllOnScreen(
            self.template_path, confidence=self.threshold, region=region
        )

        return [(pyautogui.center(loc).x, pyautogui.center(loc).y) for loc in locations]

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "template_path": self.template_path,
            "threshold": self.threshold,
            "timeout": self.timeout,
            "description": self.description,
        }

    @classmethod
    def from_yaml(cls, data: Dict[str, Any]) -> "ImageLocator":
        """
        从 YAML 数据创建图像定位器

        Args:
            data: YAML 中定义的图像信息

        Returns:
            ImageLocator 实例
        """
        return cls(
            template_path=data["template_path"],
            threshold=data.get("threshold", 0.8),
            timeout=data.get("timeout", 10),
            description=data.get("description", ""),
        )
