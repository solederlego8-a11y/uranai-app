# -*- coding: utf-8 -*-
"""uranai パッケージ

11種の占術モジュール（命占10種＋姓名判断）を登録し、
まとめて実行して「今日の総合鑑定」を生成するエントリポイントを提供する。
"""
from __future__ import annotations

from datetime import date

from . import (
    aggregator,
    india_uranai,
    kyusei_kigaku,
    maya,
    sanmei,
    seimei,
    seiyo_uranai,
    shibi_tosuu,
    shichu_suimei,
    shukuyo,
    suuhi,
    tibet,
    utils,
)

# 表示順に並べたモジュール一覧（モジュール名, モジュール）
MODULES = [
    ("姓名判断", seimei),
    ("西洋占星術", seiyo_uranai),
    ("四柱推命", shichu_suimei),
    ("紫微斗数", shibi_tosuu),
    ("九星気学", kyusei_kigaku),
    ("算命学", sanmei),
    ("数秘術", suuhi),
    ("インド占星術", india_uranai),
    ("宿曜占星術", shukuyo),
    ("マヤ暦占い", maya),
    ("チベット占星術", tibet),
]

__all__ = ["MODULES", "run_all_modules", "build_report", "aggregator", "utils"]


def run_all_modules(user_data: dict) -> list:
    """11種すべての占術を実行する（個々の例外はデフォルト値で補完する）。"""
    return [aggregator.safe_calculate(module, name, user_data)
            for name, module in MODULES]


def build_report(user_data: dict) -> dict:
    """入力データから「今日の総合鑑定」一式を生成する。"""
    if not user_data.get("today"):
        user_data["today"] = date.today()
    results = run_all_modules(user_data)
    return aggregator.aggregate(results, user_data)
