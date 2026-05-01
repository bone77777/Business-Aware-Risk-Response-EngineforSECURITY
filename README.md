# Business-Aware Risk Response Engine for SECURITY

セキュリティインシデント発生時に、**ビジネスコンテキストを考慮した最適な対応アクション**を自動選択するSOC（Security Operations Center）意思決定支援エンジンです。

---

## 概要

従来のSOCツールは「セキュリティ的に最強の対応」を選びがちですが、実際の運用では**業務継続性・コスト・リスク軽減効果のトレードオフ**が常に存在します。

このエンジンは以下を統合的に評価し、最適なインシデント対応アクションを選択します。

- アセットの動的価値（決算期・繁忙期などのビジネスコンテキスト反映）
- 対応アクションによる可用性へのダメージ
- 運用コスト・人件費
- RORI（Return on Response Investment）による定量評価

---

## デモ：深夜の大量通信シナリオ

```
--- 分析開始 ---
アセット価値: 100.0 | 未対策時のリスク: 69.6

[RORI評価]
- Full_Isolate    : 期待利益(Utility) = -11.56
- Throttling      : 期待利益(Utility) =  16.88   ← 最適解
- Logging_Only    : 期待利益(Utility) = -6.79

【最終意思決定】
採用アクション: Throttling
```

決算期中の経理PCへの不審な大量通信に対して、「全遮断（業務完全停止）」ではなく「帯域制限（業務継続しながら脅威を抑制）」を最適解として選択します。

---

## アーキテクチャ

```
BusinessAwareSOC
├── asset_database          # アセット情報・ビジネスコンテキスト定義
├── get_dynamic_asset_value # コンテキストに応じた動的価値計算
├── calculate_rori          # RORI（対応投資対効果）算出
└── multi_objective_optimization  # 多目的最適化・最終アクション決定

ResponseAction
├── mitigation_rate         # 脅威軽減率 (0.0〜1.0)
├── availability_cost       # 可用性へのダメージ (0.0〜1.0)
└── operational_cost        # 運用コスト
```

---

## 主要概念

### RORI（Return on Response Investment）

```
RORI = 回避されたリスク - (業務停止コスト + 対策コスト + 運用コスト)
```

セキュリティ対応の「費用対効果」を定量化します。RORIが最大のアクションを最適解として採用します。

### 動的アセット価値

アセットの価値はビジネスコンテキストによって変化します。

```python
# 決算期は価値が1.5倍に
if asset.get("is_closing_period"):
    value *= 1.5
```

「経理PCが決算期かどうか」によって、同じ脅威に対する最適対応が変わります。

### 対応アクション候補

| アクション | 脅威軽減率 | 可用性ダメージ | 運用コスト |
|---|---|---|---|
| Full_Isolate（全遮断） | 99% | 100%（業務停止） | 高 |
| Throttling（帯域制限） | 60% | 20%（一部影響） | 中 |
| Logging_Only（監視のみ） | 5% | 0%（影響なし） | 低 |

---

## 使い方

### 必要環境

- Python 3.8 以上
- 標準ライブラリのみ（追加インストール不要）

### 実行

```bash
python main.py
```

### カスタマイズ例

```python
# アセットを追加する
self.asset_database = {
    "192.168.10.44": {
        "name": "Accounting_PC",
        "base_value": 70,
        "is_closing_period": True
    },
    "192.168.10.10": {
        "name": "Web_Server",
        "base_value": 90,
        "is_closing_period": False
    }
}

# シナリオを変えて実行する
soc.multi_objective_optimization(
    threat_prob=0.5,   # 脅威確率
    degradation=0.6,   # 被害深刻度
    ip="192.168.10.10"
)
```

---

## 設計思想

> "セキュリティ的に最強の対応" と "ビジネス的に正しい対応" は、しばしば一致しない。

このエンジンは、その乖離を埋めるために設計されています。決算期の経理システムを全遮断することは「セキュリティ的には正しい」かもしれませんが、「ビジネス的には致命的」になりえます。Business-Aware Risk Response Engineは、そのトレードオフを定量的に扱います。

---

## 今後の拡張予定

- [ ] 複数アセットへの同時対応最適化
- [ ] 時系列でのビジネスコンテキスト自動切替（営業時間外・休日対応）
- [ ] SIEMログとの連携による脅威確率の自動推定
- [ ] Webダッシュボードでの可視化

---

## ライセンス

MIT License
