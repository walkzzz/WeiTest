"""Screenshot Manager - automatic screenshots on test failure"""

import os
from pathlib import Path
from datetime import datetime
from typing import Optional


class ScreenshotManager:
    """
    截图管理器
    
    负责测试失败时自动截图
    """
    
    def __init__(self, output_dir: str = "reports/screenshots"):
        """
        初始化截图管理器
        
        Args:
            output_dir: 截图输出目录
        """
        self.output_dir = Path(output_dir)
        self.screenshot_dir = self.output_dir  # 别名，为了兼容性
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """确保输出目录存在"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def take_screenshot(self, page, filename: Optional[str] = None) -> str:
        """
        拍摄截图
        
        Args:
            page: 页面对象
            filename: 文件名（可选，默认使用时间戳）
        
        Returns:
            截图文件路径
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
        
        filepath = self.output_dir / filename
        
        try:
            # 使用 page 的截图方法
            if hasattr(page, 'take_screenshot'):
                page.take_screenshot(str(filepath))
            else:
                # 备用方案：使用 pyautogui
                import pyautogui
                screenshot = pyautogui.screenshot()
                screenshot.save(str(filepath))
            
            return str(filepath)
        except Exception as e:
            raise RuntimeError(f"截图失败：{e}")
    
    def take_screenshot_on_failure(self, page, test_name: str) -> str:
        """
        测试失败时截图
        
        Args:
            page: 页面对象
            test_name: 测试名称
        
        Returns:
            截图文件路径
        """
        # 清理测试名称中的非法字符
        safe_name = test_name.replace("/", "_").replace("\\", "_").replace("::", "_")
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"failure_{safe_name}_{timestamp}.png"
        
        return self.take_screenshot(page, filename)
    
    def cleanup_old_screenshots(self, days: int = 7):
        """
        清理旧的截图
        
        Args:
            days: 保留天数
        """
        import time
        
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        for filepath in self.output_dir.glob("*.png"):
            if filepath.stat().st_mtime < cutoff_time:
                filepath.unlink()


# 便捷函数
def get_screenshot_manager(output_dir: str = "reports/screenshots") -> ScreenshotManager:
    """获取截图管理器实例"""
    return ScreenshotManager(output_dir)
