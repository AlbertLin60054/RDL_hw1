# 強化學習作業一 (RL HW1)

本專案使用 Python Flask 與前端 HTML/JavaScript 實作了一個強化的網格地圖開發 (Gridworld) 作業。專案目前完成的功能包含 **HW1-1 網格地圖開發** 與 **HW1-2 策略顯示與價值評估** 的完整流程。

## 專案結構
```text
RDL_Hw1/
├── app.py                # Flask 後端應用程式 (負責價值評估演算法的運算與伺服器架設)
├── README.md             # 本說明檔案
└── templates/
    └── index.html        # 前端 UI 介面展示與使用者網格互動的邏輯
```

## 功能完成事項摘要 (Completed Requirements)

### HW1-1: 網格地圖開發
1. **網格參數化生成**: 允許使用者自訂網格空間維度 $n$ (支援從 3 開始，符合介面樣式的 $n \times n$ 大小)。
2. **互動式網格設定**:
   - 第一次點擊：設定為 **起始點 (Start)**，顏色為綠色。
   - 第二次點擊：設定為 **終點 (Goal / End)**，顏色為紅色。
   - 後續點擊（最多可點 $n-2$ 次）：設定為 **障礙物 (Obstacle)**，顏色為灰色。
   - 前端設有限制機制，一但設定完整的地圖格數後將不再改變既有配置。

### HW1-2: 策略顯示與價值評估 (Policy Evaluation)
1. **策略產生 (Policy Generation)**: 
   - 當使用者點選完畢所有的格點後，會跳出「Evaluate Policy」按鈕。
   - 點擊按鈕會透過非同步請求給 Flask 後端，後端程式會對所有可行的網格 (非終端、非障礙物) 隨機指定一個固定的前往方向（`↑`、`↓`、`←`、`→`），形成一個**隨機確定性策略 (Deterministic Random Policy)**。
2. **策略評估 (Iterative Policy Evaluation)**:
   - 為了展現評估概念，環境使用以下參數：
     - **Discount Factor ($\gamma$)**: 0.9 (確保任意隨便瞎指的策略最後都能收斂出價值)
     - **Reward ($r$)**: 走一步為 -1。撞牆與撞障礙物皆為停留在原地並且 -1。
     - **Terminal Reward**: 走到終結點時即完成，終結點本身的預期價值 $V(s) = 0$。
   - 由於隨機生成的單向箭頭很容易卡入無限迴圈（撞牆出不去或是兩個格子互指互相彈開），而根據無窮等比極數收斂定理：$V = -1 / (1 - \gamma)$，因此你會觀察到大多數不能導向終點的格子會趨近於 **-10** 的精準數學價值。
3. **結果視覺化**:
   - 演算法收斂並回傳前端後，會動態在畫面下方展開兩個矩陣做對照：
     - **Value Matrix**: 顯示每一個格子計算出來的 $V(s)$ 值。
     - **Policy Matrix**: 顯示該格子對應指引方向的政策箭頭。

## 執行方式與 GitHub Pages 展示
本專案已經完全改寫為**純前端 (Static Frontend)** 應用程式，所有的 Policy Evaluation 運算邏輯皆直接由瀏覽器的 JavaScript 執行，因此再也不需要依賴 Flask 伺服器了！

👉 **您現在可以直接透過 GitHub Pages 在線上展示與操作此作業：**
[https://AlbertLin60054.github.io/RDL_hw1/](https://AlbertLin60054.github.io/RDL_hw1/)

*(備註：因已更新為靜態架構，若要在本機端測試，只需直接雙擊打開 `index.html` 檔案即可！)*
