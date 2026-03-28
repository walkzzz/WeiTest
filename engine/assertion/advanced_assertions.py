"""Advanced Assertions - enhanced assertion capabilities"""

from typing import Any, Optional, Callable, Union
import cv2
import numpy as np
from PIL import Image


class ImageAssertion:
    """
    图像对比断言

    用于验证 UI 元素或屏幕区域的图像匹配

    Example:
        >>> assertion = ImageAssertion("expected.png", confidence=0.95)
        >>> assertion.should_match()
        >>> assertion.should_not_match()
    """

    def __init__(
        self,
        expected_image_path: str,
        actual_image_path: Optional[str] = None,
        confidence: float = 0.95,
        tolerance: int = 10,
    ) -> None:
        """
        初始化图像断言

        Args:
            expected_image_path: 期望图像路径
            actual_image_path: 实际图像路径 (可选)
            confidence: 匹配置信度 (0-1)
            tolerance: 颜色容差 (0-255)
        """
        self.expected_path = expected_image_path
        self.actual_path = actual_image_path
        self.confidence = confidence
        self.tolerance = tolerance
        self._last_result: Optional[bool] = None

    def should_match(self, region: Optional[tuple] = None) -> "ImageAssertion":
        """
        验证图像匹配

        Args:
            region: 可选的屏幕区域 (x, y, width, height)

        Returns:
            self: 支持链式调用

        Raises:
            AssertionError: 图像不匹配时
        """
        import pyautogui

        # 截取屏幕或区域
        if region:
            screenshot = pyautogui.screenshot(region=region)
        else:
            screenshot = pyautogui.screenshot()

        # 转换为 OpenCV 格式
        screenshot_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        expected = cv2.imread(self.expected_path, cv2.IMREAD_COLOR)

        if expected is None:
            raise FileNotFoundError(f"期望图像不存在：{self.expected_path}")

        # 模板匹配
        result = cv2.matchTemplate(screenshot_np, expected, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        self._last_result = max_val >= self.confidence

        if not self._last_result:
            raise AssertionError(f"图像不匹配 - 置信度：{max_val:.2f} (期望：{self.confidence})")

        return self

    def should_not_match(self) -> "ImageAssertion":
        """
        验证图像不匹配

        Returns:
            self: 支持链式调用

        Raises:
            AssertionError: 图像匹配时
        """
        try:
            self.should_match()
            raise AssertionError("图像不应该匹配")
        except AssertionError as e:
            if "图像不匹配" in str(e):
                # 符合预期
                return self
            else:
                raise

    def should_be_similar(self, threshold: float = 0.8) -> "ImageAssertion":
        """
        验证图像相似 (使用结构相似性 SSIM)

        Args:
            threshold: 相似度阈值

        Returns:
            self: 支持链式调用
        """
        try:
            from skimage.metrics import structural_similarity as ssim
        except ImportError:
            raise ImportError("请安装 scikit-image: pip install scikit-image")

        expected = cv2.imread(self.expected_path)
        actual = cv2.imread(self.actual_path)

        if expected is None or actual is None:
            raise FileNotFoundError("图像文件不存在")

        # 转换为灰度图
        expected_gray = cv2.cvtColor(expected, cv2.COLOR_BGR2GRAY)
        actual_gray = cv2.cvtColor(actual, cv2.COLOR_BGR2GRAY)

        # 计算 SSIM
        score, _ = ssim(expected_gray, actual_gray, full=True)

        self._last_result = score >= threshold

        if not self._last_result:
            raise AssertionError(f"图像相似度不足 - SSIM: {score:.2f} (期望：{threshold})")

        return self

    @property
    def last_result(self) -> Optional[bool]:
        """获取最后一次断言结果"""
        return self._last_result


class PropertyAssertion:
    """
    属性断言

    用于验证 UI 元素的属性

    Example:
        >>> assertion = PropertyAssertion(element)
        >>> assertion.has_property("AutomationId", "btn_submit")
        >>> assertion.has_style("color", "red")
    """

    def __init__(self, element: Any, description: str = "") -> None:
        """
        初始化属性断言

        Args:
            element: UI 元素
            description: 元素描述
        """
        self.element = element
        self.description = description
        self._last_result: Optional[bool] = None

    def has_property(self, name: str, expected_value: Any) -> "PropertyAssertion":
        """
        验证属性值

        Args:
            name: 属性名
            expected_value: 期望值

        Returns:
            self: 支持链式调用

        Raises:
            AssertionError: 属性值不匹配时
        """
        try:
            actual_value = getattr(self.element, name, None)

            self._last_result = actual_value == expected_value

            if not self._last_result:
                raise AssertionError(
                    f"属性 '{name}' 不匹配 - 实际：{actual_value}, 期望：{expected_value}"
                )
        except Exception as e:
            raise AssertionError(f"获取属性失败：{name} - {str(e)}")

        return self

    def has_attribute(self, name: str, expected_value: str) -> "PropertyAssertion":
        """
        验证自动化属性

        Args:
            name: 属性名
            expected_value: 期望值

        Returns:
            self: 支持链式调用
        """
        try:
            element_info = self.element.get_element_info()
            actual_value = getattr(element_info, name, None)

            self._last_result = actual_value == expected_value

            if not self._last_result:
                raise AssertionError(
                    f"属性 '{name}' 不匹配 - 实际：{actual_value}, 期望：{expected_value}"
                )
        except Exception as e:
            raise AssertionError(f"获取属性失败：{name} - {str(e)}")

        return self

    def has_style(self, property_name: str, expected_value: str) -> "PropertyAssertion":
        """
        验证样式属性

        Args:
            property_name: 样式属性名
            expected_value: 期望值

        Returns:
            self: 支持链式调用
        """
        try:
            actual_value = self.element.get_style(property_name)

            self._last_result = expected_value in str(actual_value)

            if not self._last_result:
                raise AssertionError(
                    f"样式 '{property_name}' 不匹配 - 实际：{actual_value}, 期望包含：{expected_value}"
                )
        except Exception as e:
            raise AssertionError(f"获取样式失败：{property_name} - {str(e)}")

        return self

    def is_visible(self) -> "PropertyAssertion":
        """
        验证元素可见

        Returns:
            self: 支持链式调用
        """
        self._last_result = self.element.is_visible()

        if not self._last_result:
            raise AssertionError("元素不可见")

        return self

    def is_enabled(self) -> "PropertyAssertion":
        """
        验证元素可用

        Returns:
            self: 支持链式调用
        """
        self._last_result = self.element.is_enabled()

        if not self._last_result:
            raise AssertionError("元素不可用")

        return self

    def has_text(self, expected_text: str) -> "PropertyAssertion":
        """
        验证文本内容

        Args:
            expected_text: 期望文本

        Returns:
            self: 支持链式调用
        """
        actual_text = self.element.window_text()

        self._last_result = actual_text == expected_text

        if not self._last_result:
            raise AssertionError(f"文本不匹配 - 实际：{actual_text}, 期望：{expected_text}")

        return self

    def contains_text(self, expected_text: str) -> "PropertyAssertion":
        """
        验证文本包含

        Args:
            expected_text: 期望包含的文本

        Returns:
            self: 支持链式调用
        """
        actual_text = self.element.window_text()

        self._last_result = expected_text in actual_text

        if not self._last_result:
            raise AssertionError(f"文本不包含 '{expected_text}' - 实际：{actual_text}")

        return self


class CustomAssertion:
    """
    自定义断言

    通过谓词函数自定义断言逻辑

    Example:
        >>> assertion = CustomAssertion(
        ...     lambda: page.element("btn").is_enabled(),
        ...     "按钮应该可用"
        ... )
        >>> assertion.should_be_true()
    """

    def __init__(self, predicate: Callable[[], bool], description: str = "") -> None:
        """
        初始化自定义断言

        Args:
            predicate: 谓词函数 (返回 bool)
            description: 断言描述
        """
        self.predicate = predicate
        self.description = description
        self._last_result: Optional[bool] = None

    def should_be_true(self) -> "CustomAssertion":
        """
        验证条件为真

        Returns:
            self: 支持链式调用

        Raises:
            AssertionError: 条件为假时
        """
        result = self.predicate()
        self._last_result = result

        if not result:
            raise AssertionError(
                f"断言失败：{self.description}" if self.description else "断言失败"
            )

        return self

    def should_be_false(self) -> "CustomAssertion":
        """
        验证条件为假

        Returns:
            self: 支持链式调用

        Raises:
            AssertionError: 条件为真时
        """
        result = self.predicate()
        self._last_result = not result

        if result:
            raise AssertionError(
                f"断言失败：{self.description} (应该为假)" if self.description else "断言失败"
            )

        return self

    def should_equal(self, expected: Any) -> "CustomAssertion":
        """
        验证等于期望值

        Args:
            expected: 期望值

        Returns:
            self: 支持链式调用
        """
        actual = self.predicate()
        self._last_result = actual == expected

        if not self._last_result:
            raise AssertionError(f"值不匹配 - 实际：{actual}, 期望：{expected}")

        return self


# ========== 便捷函数 ==========


def assert_image(expected_path: str, confidence: float = 0.95) -> ImageAssertion:
    """创建图像断言"""
    return ImageAssertion(expected_path, confidence=confidence)


def assert_property(element: Any) -> PropertyAssertion:
    """创建属性断言"""
    return PropertyAssertion(element)


def assert_custom(predicate: Callable[[], bool], description: str = "") -> CustomAssertion:
    """创建自定义断言"""
    return CustomAssertion(predicate, description)
