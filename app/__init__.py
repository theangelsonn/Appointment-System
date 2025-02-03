"""
Flask 應用程式的初始化檔案
負責創建和配置 Flask 應用程式實例
"""

from flask import Flask


def create_app():
    """
    創建並配置 Flask 應用程式

    處理流程：
    1. 創建 Flask 應用程式實例
    2. 設定應用程式密鑰
    3. 註冊路由藍圖

    返回：
    Flask: 配置完成的 Flask 應用程式實例
    """
    # 創建 Flask 應用程式實例
    app = Flask(__name__)

    # 設置密鑰，用於：
    # - Session 資料加密
    # - Flash 訊息加密
    # - CSRF 保護
    # 注意：在正式環境中應使用強密鑰並妥善保管
    app.secret_key = 'your secret key'

    # 註冊路由藍圖
    # 藍圖用於組織相關的路由和視圖函數
    from .controller.routes import main
    app.register_blueprint(main)

    return app
