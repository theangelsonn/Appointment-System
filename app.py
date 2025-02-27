"""
應用程式的入口點
用於啟動 Flask 網頁應用程式
"""

from app import create_app


# 創建 Flask 應用程式實例
app = create_app()

# 當直接執行此檔案時才會運行
if __name__ == "__main__":
    # 以除錯模式啟動應用程式
    # debug=True 表示：
    # 1. 程式碼修改後自動重新載入
    # 2. 顯示詳細的錯誤訊息
    # 3. 提供互動式除錯器
    app.run(debug=True)
