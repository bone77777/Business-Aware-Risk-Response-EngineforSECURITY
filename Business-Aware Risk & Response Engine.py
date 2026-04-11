import math

class ResponseAction:
    def __init__(self, name, mitigation_rate, availability_cost, operational_cost):
        self.name = name
        self.mitigation_rate = mitigation_rate  # 脅威を抑える力 (0.0 - 1.0)
        self.availability_cost = availability_cost  # 可用性へのダメージ (0.0 - 1.0)
        self.operational_cost = operational_cost  # 運用負荷・人件費など

class BusinessAwareSOC:
    def __init__(self):
        # 1. アセットとコンテキストの定義
        self.asset_database = {
            "192.168.10.44": {
                "name": "Accounting_PC",
                "base_value": 70,
                "is_closing_period": True  # 決算期フラグ
            }
        }

    def get_dynamic_asset_value(self, ip):
        asset = self.asset_database.get(ip)
        value = asset["base_value"]
        # コンテキスト（決算期など）による価値の動的引き上げ
        if asset.get("is_closing_period"):
            value *= 1.5  # 決算期は価値が1.5倍に跳ね上がる
        return min(value, 100)

    def calculate_rori(self, risk_ignored, action, mitigation_cost):
        """
        RORI = (回避されたリスク - 対策コスト) / 対策コスト
        ※簡易モデルとして、(リスク減少分 - 業務停止コスト) を計算
        """
        mitigated_risk = risk_ignored * action.mitigation_rate
        # 業務停止コスト = アセット価値 × 可用性へのダメージ
        business_loss = self.get_dynamic_asset_value("192.168.10.44") * action.availability_cost
        
        net_benefit = mitigated_risk - (business_loss + mitigation_cost + action.operational_cost)
        return net_benefit

    def multi_objective_optimization(self, threat_prob, degradation, ip):
        # 1. インパクト計算: I = AssetValue * Degradation
        asset_value = self.get_dynamic_asset_value(ip)
        impact = asset_value * degradation
        risk_ignored = threat_prob * impact
        
        print(f"--- 分析開始 ---")
        print(f"アセット価値: {asset_value:.1f} | 未対策時のリスク: {risk_ignored:.1f}")

        # 2. 対策候補の定義
        actions = [
            ResponseAction("Full_Isolate", 0.99, 1.0, 20),   # 全遮断: 防御最強、可用性崩壊
            ResponseAction("Throttling", 0.60, 0.2, 5),    # 帯域制限: 防御そこそこ、可用性維持
            ResponseAction("Logging_Only", 0.05, 0.0, 1),   # 監視のみ: 防御ほぼなし、可用性完全
        ]

        best_action = None
        max_utility = -float('inf')

        # 3. 多目的最適化 (Security vs Availability vs Cost)
        print("\n[RORI評価]")
        for action in actions:
            # ユーティリティ算出 (RORIをベースに最適解を探索)
            utility = self.calculate_rori(risk_ignored, action, mitigation_cost=10)
            print(f"- {action.name:15}: 期待利益(Utility) = {utility:.2f}")

            if utility > max_utility:
                max_utility = utility
                best_action = action

        return best_action

# --- 実行シミュレーション ---
soc = BusinessAwareSOC()

# 深夜の大量通信シナリオ
# 脅威の確率 P=0.87, 被害度(情報漏洩の深刻度) Degradation=0.8
best_choice = soc.multi_objective_optimization(threat_prob=0.87, degradation=0.8, ip="192.168.10.44")

print(f"\n【最終意思決定】")
print(f"採用アクション: {best_choice.name}")