# -*- coding: utf-8 -*-
# Date:2025-01-24 11:54
import os
import json
import csv
from typing import List, Dict
from datetime import datetime


class NewsStorage:
    def __init__(self, output_dir: str = "data", output_format: str = "json"):
        """
        初始化存储器。

        :param output_dir: 输出文件存储目录，相对于项目根目录
        :param output_format: 输出文件格式，支持 "json" 或 "csv"
        """
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..")
        )
        self.output_dir = os.path.join(self.project_root, output_dir)
        self.output_format = output_format.lower()

    def save(self, news_data: List[Dict], source_name: str) -> str:
        """
        保存新闻数据到文件。

        :param news_data: 新闻数据，格式为 List[Dict]
        :param source_name: 新闻源名称（如 "cctv", "netease" 等）
        :return: 保存的文件路径
        """
        if not news_data:
            raise ValueError("新闻数据不能为空")

        # 按来源建立子目录
        sub_dir = os.path.join(self.output_dir, source_name)
        os.makedirs(sub_dir, exist_ok=True)

        # 生成文件名
        # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # filename = f"{source_name}_{timestamp}.{self.output_format}"
        filename = f"{source_name}.{self.output_format}"
        filepath = os.path.join(sub_dir, filename)

        # 保存数据
        if self.output_format == "json":
            self._save_as_json(news_data, filepath)
        elif self.output_format == "csv":
            self._save_as_csv(news_data, filepath)
        else:
            raise ValueError(f"不支持的输出格式: {self.output_format}")

        return filepath

    def _save_as_json(self, news_data: List[Dict], filepath: str):
        """将新闻数据保存为 JSON 文件。"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(news_data, f, ensure_ascii=False, indent=4)

    def _save_as_csv(self, news_data: List[Dict], filepath: str):
        """将新闻数据保存为 CSV 文件。"""
        if not news_data:
            return

        fieldnames = news_data[0].keys()

        with open(filepath, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(news_data)
