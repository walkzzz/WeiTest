"""Image Search Engine - template-based image recognition using OpenCV"""

from typing import List, Optional, Tuple
from dataclasses import dataclass
import cv2
import numpy as np
import pyautogui
from PIL import Image
import time


@dataclass
class Point:
    """屏幕坐标点"""

    x: int
    y: int


@dataclass
class Rect:
    """屏幕矩形区域"""

    left: int
    top: int
    width: int
    height: int

    def to_tuple(self) -> Tuple[int, int, int, int]:
        """转换为元组 (left, top, width, height)"""
        return (self.left, self.top, self.width, self.height)


class ImageSearchEngine:
    """
    图像搜索引擎 - 基于模板匹配的图像识别

    使用 OpenCV 的模板匹配功能在屏幕上查找图像

    Example:
        >>> engine = ImageSearchEngine(confidence=0.9)
        >>> point = engine.find("images/submit_btn.png")
        >>> if point:
        ...     pyautogui.click(point.x, point.y)
    """

    def __init__(self, confidence: float = 0.9) -> None:
        """
        初始化图像搜索引擎

        Args:
            confidence: 匹配置信度阈值 (0-1)，默认 0.9
        """
        self.confidence = confidence

    def find(
        self, template_path: str, region: Optional[Rect] = None, timeout: int = 10
    ) -> Optional[Point]:
        """
        查找图像位置

        Args:
            template_path: 模板图像路径
            region: 搜索区域（可选）
            timeout: 超时时间（秒）

        Returns:
            Point: 找到的图像中心点，未找到返回 None
        """
        start_time = time.time()

        while time.time() - start_time < timeout:
            result = self._match_template(template_path, region)
            if result:
                return result
            time.sleep(0.5)

        return None

    def find_all(
        self,
        template_path: str,
        region: Optional[Rect] = None,
        min_confidence: Optional[float] = None,
    ) -> List[Point]:
        """
        查找所有匹配的图像位置

        Args:
            template_path: 模板图像路径
            region: 搜索区域（可选）
            min_confidence: 最小置信度（可选，默认使用实例的 confidence）

        Returns:
            List[Point]: 所有匹配的中心点列表
        """
        try:
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                raise FileNotFoundError(f"无法读取模板图像：{template_path}")

            screenshot = pyautogui.screenshot()
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 裁剪区域
            if region:
                screenshot_np = screenshot_np[
                    region.top : region.top + region.height,
                    region.left : region.left + region.width,
                ]

            # 模板匹配
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
            threshold = min_confidence or self.confidence

            points = []
            while True:
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
                if max_val >= threshold:
                    # 计算中心点
                    h, w = template.shape[:2]
                    center_x = max_loc[0] + w // 2
                    center_y = max_loc[1] + h // 2

                    # 如果指定了区域，需要转换坐标
                    if region:
                        center_x += region.left
                        center_y += region.top

                    points.append(Point(center_x, center_y))

                    # 消除已匹配区域
                    top = max(0, max_loc[1] - h // 2)
                    left = max(0, max_loc[0] - w // 2)
                    bottom = min(result.shape[0], max_loc[1] + h // 2)
                    right = min(result.shape[1], max_loc[0] + w // 2)
                    result[top:bottom, left:right] = 0
                else:
                    break

            return points
        except Exception as e:
            print(f"图像匹配失败：{e}")
            return []

    def click(
        self, template_path: str, button: str = "left", clicks: int = 1, interval: float = 0.1
    ) -> bool:
        """
        找到图像并点击

        Args:
            template_path: 模板图像路径
            button: 鼠标按钮 ('left', 'right', 'middle')
            clicks: 点击次数
            interval: 点击间隔

        Returns:
            bool: 是否成功点击
        """
        point = self.find(template_path)
        if point:
            pyautogui.click(x=point.x, y=point.y, button=button, clicks=clicks, interval=interval)
            return True
        return False

    def _match_template(self, template_path: str, region: Optional[Rect] = None) -> Optional[Point]:
        """执行模板匹配"""
        try:
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                return None

            screenshot = pyautogui.screenshot()
            screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

            # 裁剪区域
            if region:
                screenshot_np = screenshot_np[
                    region.top : region.top + region.height,
                    region.left : region.left + region.width,
                ]

            # 模板匹配
            result = cv2.matchTemplate(screenshot_np, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

            if max_val >= self.confidence:
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2

                # 如果指定了区域，需要转换坐标
                if region:
                    center_x += region.left
                    center_y += region.top

                return Point(center_x, center_y)

            return None
        except Exception as e:
            print(f"模板匹配异常：{e}")
            return None
