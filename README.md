# Fitness Trainer App

一個基於 **Streamlit + MediaPipe Pose** 的 AI 健身教練 Web App。透過瀏覽器的鏡頭，
即時分析使用者動作，自動計算深蹲、二頭彎舉、腿部訓練的次數並給出姿勢建議；
同時提供營養標籤 OCR 識別 + AI 營養諮詢功能。

## 功能

| 模塊 | 路徑 | 說明 |
|---|---|---|
| 首頁 | `main.py` | 兩個入口：「Start」進入訓練頁，「Nutrition info」進入營養頁 |
| 訓練導航 | `pages/home.py` | 列出三種訓練：Squatting / Curls / Leg |
| 深蹲計數 + 姿勢糾正 | `pages/squat.py` `process_frame.py` | 用 `streamlit-webrtc` 串流鏡頭，MediaPipe 計算髖膝踝角度，搭配 state machine 計次 |
| 二頭彎舉 | `pages/curls.py` | 通過肘關節角度穿越閾值計次 |
| 腿部訓練 | `pages/leg.py` | 通過膝關節角度穿越閾值計次 |
| 營養標籤 OCR | `pages/ocr.py` | Tesseract 識別 Calories/Fat/Sodium/Sugars/Protein，並用 GPT 給建議 |

## 項目結構

```
fitness_app/
├── main.py                # Streamlit 首頁
├── pages/
│   ├── home.py            # 訓練選擇頁
│   ├── squat.py           # 深蹲計數（主要功能）
│   ├── curls.py           # 彎舉計數
│   ├── leg.py             # 腿部計數
│   └── ocr.py             # 營養標籤 OCR + GPT 諮詢
├── PoseModule.py          # MediaPipe Pose 通用封裝
├── process_frame.py       # 深蹲姿態 state machine
├── thresholds.py          # Beginner / Pro 兩套角度閾值
├── utils.py               # 角度計算、繪圖、landmark 工具
├── squat.py               # 根目錄舊版（建議使用 pages/squat.py）
├── requirements.txt
├── package.json
├── samples/               # 食品營養標籤樣本圖
├── test/                  # 早期測試腳本
└── .devcontainer/         # GitHub Codespaces / VS Code Dev Container 配置
```

## 環境與依賴

### Python 3.10 / 3.11

```bash
pip install -r requirements.txt
```

主要依賴：

- `streamlit`
- `streamlit-webrtc` — 瀏覽器內 WebRTC 鏡頭串流
- `mediapipe` — Pose 關節點檢測
- `opencv-python-headless` — 影像處理（headless 版本，無 GUI 依賴）
- `numpy`、`Pillow`
- `av`、`aiortc` — 視訊幀解碼
- `pytesseract` + [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- `openai>=0.27` — GPT 飲食建議（OCR 頁面使用）

### Tesseract

OCR 頁面寫死路徑：

```python
pytesseract.pytesseract.tesseract_cmd = r"/opt/homebrew/bin/tesseract"
```

macOS 用 `brew install tesseract` 安裝即可。其他系統需調整該路徑。

### OpenAI API Key

OCR 頁面的 GPT 功能需要 API Key。

建議先把 Key 寫到環境變數：

```bash
export OPENAI_API_KEY="sk-..."
```

然後修改 `pages/ocr.py` 內原本硬編碼 `openai.api_key` 的那一行，改成：

```python
import os
openai.api_key = os.environ["OPENAI_API_KEY"]
```

不要把金鑰硬編碼進原始碼，也不要再 push 到 GitHub。

## 啟動

```bash
streamlit run main.py
```

瀏覽器打開 [http://localhost:8501](http://localhost:8501)，允許鏡頭權限即可使用。

- `http://localhost:8501/home` 進入訓練頁
- `http://localhost:8501/ocr` 進入營養頁

> 部分頁面對圖片路徑寫死了 `/Users/pacoakm/Documents/AI/...`，
> 在其他機器上運行請改 `main.py` 與 `pages/home.py` 中的圖片路徑，
> 或把圖片放到對應位置。

## 深蹲計數原理（核心模塊）

`ProcessFrame` 結合 MediaPipe Pose 的 33 個關節點與 `thresholds.py` 的角度閾值，
維護一個狀態序列 `state_seq`：

- `s1`（站立 / NORMAL）
- `s2`（過渡 / TRANS）
- `s3`（到位 / PASS）

完整的 `s1 → s2 → s3 → s2 → s1` 計為一次有效深蹲。
`CNT_FRAME_THRESH=50` 表示同一狀態需連續 50 幀才確認，避免誤觸發。

即時反饋：

- `LOWER YOUR HIPS` — 髖部蹲得不夠深
- `BEND BACKWARDS` / `BEND FORWARD` — 上背姿態
- `KNEE FALLING OVER TOE` — 膝蓋超過腳尖
- `SQUAT TOO DEEP` — 蹲得過低傷膝
- `INACTIVE_THRESH=15s` — 鏡頭前 15 秒無人
- `OFFSET_THRESH=35°` — 人體相對鏡頭偏移過多

`thresholds.py` 提供 Beginner / Pro 兩套閾值。
Pro 模式對膝蓋角度與踝關節更嚴格。

## 開發容器

`.devcontainer/devcontainer.json` 配置好 Python 3.11 + Streamlit 8501 端口轉發，
適合在 GitHub Codespaces 或 VS Code Dev Containers 中一鍵啟動。

## 注意事項

- 鏡頭功能依賴瀏覽器 WebRTC，需要 HTTPS 或 localhost。
  Streamlit 本地開發已預設支援。
- OCR 結果依賴標籤圖清晰度。`samples/` 目錄提供幾張真實的食品標籤樣本可以測試。
- 該項目為實驗性 demo，深蹲計數和姿勢建議僅供參考，無法替代專業教練。
