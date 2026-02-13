#!/usr/bin/env python3
"""
數位孿生月度追蹤系統 - 整合群體分析
Digital Twin Monthly Tracking System with Multi-Group Analysis

功能：
1. 群體 A (新鮮人)：體驗、驚喜、數位遊戲化
2. 群體 B (FinTech 家庭)：效率、信賴、資產管理
3. 地域變數：台北 vs 台南
4. JSONL 格式持久化儲存
5. 每日 02:00 自動執行
"""

import os
import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Any
from enum import Enum

# ============ 配置 ============

CONFIG = {
    'output_folder': '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring',
    'data_file': '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring/data/behavior_twin_monthly.jsonl',
    'log_file': '/Users/the_mini_bot/.openclaw/workspace/logs/digital_twin_monthly.log',
    'num_agents_per_group': 500,  # 每群體人數
    'simulation_days': 1,  # 每日模擬
}

# ============ 群體定義 ============

class Group(Enum):
    FRESHMAN = "新鮮人"      # 體驗、驚喜、數位遊戲化
    FINTECH = "FinTech家庭"  # 效率、信賴、資產管理

class Region(Enum):
    TAIPEI = "台北"  # 快節奏、高密度
    TAINAN = "台南"  # 大型複合店、跨品牌生活圈

# ============ Persona ============

@dataclass
class Persona:
    """消費者人格"""
    persona_id: str
    group: str           # 新鮮人 / FinTech家庭
    region: str          # 台北 / 台南
    age: int
    digital_gamification: float  # 數位遊戲化偏好
    efficiency_seeking: float   # 效率追求
    trust_requirement: float     # 信賴需求
    experience_seeking: float   # 體驗追求
    surprise_preference: float  # 驚喜偏好
    asset_management: float     # 資產管理意識
    brand_loyalty: Dict[str, float]  # 各品牌忠誠度
    monthly_spending: float
    
    def to_dict(self):
        return {
            'persona_id': self.persona_id,
            'group': self.group,
            'region': self.region,
            'age': self.age,
            'digital_gamification': self.digital_gamification,
            'efficiency_seeking': self.efficiency_seeking,
            'trust_requirement': self.trust_requirement,
            'experience_seeking': self.experience_seeking,
            'surprise_preference': self.surprise_preference,
            'asset_management': self.asset_management,
            'brand_loyalty': self.brand_loyalty,
            'monthly_spending': self.monthly_spending
        }

# ============ 群體行為參數 ============

GROUP_PARAMS = {
    Group.FRESHMAN.value: {
        'digital_gamification': (0.7, 0.95),    # 高遊戲化偏好
        'experience_seeking': (0.7, 0.95),       # 高體驗追求
        'surprise_preference': (0.6, 0.90),     # 高驚喜偏好
        'efficiency_seeking': (0.3, 0.60),      # 中低效率追求
        'trust_requirement': (0.4, 0.70),       # 中信賴需求
        'asset_management': (0.2, 0.50),         # 低資產管理
        'monthly_spending': (5000, 15000),       # 月消費
    },
    Group.FINTECH.value: {
        'digital_gamification': (0.3, 0.60),     # 中低遊戲化
        'experience_seeking': (0.3, 0.60),       # 中體驗追求
        'surprise_preference': (0.2, 0.50),     # 低驚喜偏好
        'efficiency_seeking': (0.7, 0.95),       # 高效率追求
        'trust_requirement': (0.7, 0.95),        # 高信賴需求
        'asset_management': (0.7, 0.95),         # 高資產管理
        'monthly_spending': (15000, 40000),     # 月消費
    }
}

REGION_PARAMS = {
    Region.TAIPEI.value: {
        'speed_factor': 1.3,        # 快節奏
        'density_factor': 1.5,      # 高密度
        'digital_adoption': 1.2,    # 高數位採用
        'cross_brand_tolerance': 0.6  # 低跨品牌容忍
    },
    Region.TAINAN.value: {
        'speed_factor': 0.8,        # 慢節奏
        'density_factor': 0.7,      # 低密度
        'digital_adoption': 0.9,    # 中數位採用
        'cross_brand_tolerance': 1.2  # 高跨品牌容忍
    }
}

# ============ 品牌偏好權重 ============

BRAND_WEIGHTS = {
    '7-11': {
        Group.FRESHMAN.value: 0.35,
        Group.FINTECH.value: 0.42
    },
    'FamilyMart': {
        Group.FRESHMAN.value: 0.40,
        Group.FINTECH.value: 0.35
    },
    'Other': {
        Group.FRESHMAN.value: 0.25,
        Group.FINTECH.value: 0.23
    }
}

# ============ 數據結構 ============

@dataclass
class DailyBehaviorRecord:
    """每日行為記錄"""
    timestamp: str
    group: str
    region: str
    total_personas: int
    brand_distribution: Dict[str, int]
    brand_percentages: Dict[str, float]
    avg_satisfaction: float
    digital_adoption_rate: float
    gamification_engagement: float
    efficiency_score: float
    key_insights: List[str]
    
    def to_dict(self):
        return asdict(self)

# ============ 核心功能 ============

def log(message: str):
    """日誌"""
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{ts}] {message}")
    try:
        os.makedirs(os.path.dirname(CONFIG['log_file']), exist_ok=True)
        with open(CONFIG['log_file'], 'a', encoding='utf-8') as f:
            f.write(f"[{ts}] {message}\n")
    except:
        pass

def generate_personas(num_per_group: int = 500) -> List[Persona]:
    """生成兩群體 Persona"""
    log("生成多群體 Persona...")
    
    personas = []
    
    for group in [Group.FRESHMAN.value, Group.FINTECH.value]:
        params = GROUP_PARAMS[group]
        
        for i in range(num_per_group):
            for region in [Region.TAIPEI.value, Region.TAINAN.value]:
                rparams = REGION_PARAMS[region]
                
                # 基礎參數
                digital_gam = random.uniform(*params['digital_gamification'])
                experience = random.uniform(*params['experience_seeking'])
                surprise = random.uniform(*params['surprise_preference'])
                efficiency = random.uniform(*params['efficiency_seeking'])
                trust = random.uniform(*params['trust_requirement'])
                asset_mgmt = random.uniform(*params['asset_management'])
                spending = random.uniform(*params['monthly_spending'])
                
                # 地域調整
                if region == Region.TAIPEI.value:
                    efficiency *= rparams['speed_factor']
                    digital_gam *= rparams['digital_adoption']
                else:
                    experience *= rparams['cross_brand_tolerance']
                    trust *= 1.1
                
                # 品牌忠誠度
                base_weights = BRAND_WEIGHTS
                brand_loyalty = {
                    '7-11': random.uniform(0.3, 0.8) * base_weights['7-11'].get(group, 0.5),
                    'FamilyMart': random.uniform(0.3, 0.8) * base_weights['FamilyMart'].get(group, 0.5),
                    'Other': random.uniform(0.1, 0.4)
                }
                
                p = Persona(
                    persona_id=f"{group[:2]}_{region[:2]}_{i+1:04d}",
                    group=group,
                    region=region,
                    age=random.randint(20, 45),
                    digital_gamification=min(1.0, digital_gam),
                    efficiency_seeking=min(1.0, efficiency),
                    trust_requirement=min(1.0, trust),
                    experience_seeking=min(1.0, experience),
                    surprise_preference=min(1.0, surprise),
                    asset_management=min(1.0, asset_mgmt),
                    brand_loyalty=brand_loyalty,
                    monthly_spending=spending
                )
                personas.append(p)
    
    log(f"生成 {len(personas)} 個 Persona 完成")
    return personas

def simulate_daily_behavior(personas: List[Persona], 
                           promotions: Dict = None) -> List[DailyBehaviorRecord]:
    """模擬每日行為"""
    log("模擬每日行為偏移...")
    
    records = []
    
    for group in [Group.FRESHMAN.value, Group.FINTECH.value]:
        for region in [Region.TAIPEI.value, Region.TAINAN.value]:
            # 篩選當前群體+地域
            group_personas = [p for p in personas if p.group == group and p.region == region]
            
            if not group_personas:
                continue
            
            # 計算品牌分布
            brand_dist = {'7-11': 0, 'FamilyMart': 0, 'Other': 0}
            
            for p in group_personas:
                # 根據促銷調整選擇
                promo_multiplier = 1.0
                if promotions:
                    promo_multiplier = 1.0 + (promotions.get('discount', 0) * 0.1)
                
                # 選擇品牌
                weights = [
                    p.brand_loyalty['7-11'] * promo_multiplier,
                    p.brand_loyalty['FamilyMart'] * promo_multiplier,
                    p.brand_loyalty['Other']
                ]
                
                choice = random.choices(['7-11', 'FamilyMart', 'Other'], weights=weights)[0]
                brand_dist[choice] += 1
            
            # 計算指標
            total = len(group_personas)
            brand_pct = {k: round(v/total*100, 1) for k, v in brand_dist.items()}
            
            # 滿意度
            avg_satis = sum(p.trust_requirement * 0.3 + p.experience_seeking * 0.3 + 
                          p.efficiency_seeking * 0.2 + p.digital_gamification * 0.2 
                          for p in group_personas) / total
            
            # 數位採用率
            digital_rate = sum(p.digital_gamification for p in group_personas) / total
            
            # 遊戲化參與度
            gamification = sum(p.digital_gamification for p in group_personas) / total
            
            # 效率分數
            efficiency = sum(p.efficiency_seeking for p in group_personas) / total
            
            # 生成洞察
            insights = []
            top_brand = max(brand_dist, key=brand_dist.get)
            insights.append(f"{region} {group} 最偏好 {top_brand} ({brand_pct[top_brand]}%)")
            
            if digital_rate > 0.6:
                insights.append("數位採用率高，適合推廣 App")
            if efficiency > 0.6:
                insights.append("效率導向，優化結帳流程")
            if avg_satis > 0.7:
                insights.append("整體滿意度佳")
            
            record = DailyBehaviorRecord(
                timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                group=group,
                region=region,
                total_personas=total,
                brand_distribution=brand_dist,
                brand_percentages=brand_pct,
                avg_satisfaction=round(avg_satis, 3),
                digital_adoption_rate=round(digital_rate, 3),
                gamification_engagement=round(gamification, 3),
                efficiency_score=round(efficiency, 3),
                key_insights=insights
            )
            
            records.append(record)
    
    log(f"生成 {len(records)} 筆每日記錄")
    return records

def save_to_jsonl(records: List[DailyBehaviorRecord]):
    """保存到 JSONL 檔案"""
    log("保存到 JSONL...")
    
    with open(CONFIG['data_file'], 'a', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record.to_dict(), ensure_ascii=False) + '\n')
    
    log(f"已追加 {len(records)} 筆記錄到 {CONFIG['data_file']}")

def fetch_daily_promotions() -> Dict:
    """抓取當日促銷資訊"""
    log("抓取當日促銷資訊...")
    
    # 模擬促銷數據（實際可接入 RSS/API）
    promotions = {
        '7-11': {
            'discount': random.uniform(0.05, 0.20),
            'promo_type': random.choice(['咖啡優惠', '點數加倍', '新品上架']),
            'digital_game': random.random() > 0.5
        },
        'FamilyMart': {
            'discount': random.uniform(0.05, 0.25),
            'promo_type': random.choice(['冰淇淋特價', '聯名商品', '會員日']),
            'digital_game': random.random() > 0.3
        }
    }
    
    return promotions

def generate_summary(records: List[DailyBehaviorRecord]) -> str:
    """生成當日摘要"""
    
    summary = f"""# 📊 數位孿生日報
**時間**：{datetime.now().strftime('%Y-%m-%d')}

## 群體分析

"""
    
    for record in records:
        summary += f"""### {record.group} / {record.region}

| 指標 | 數據 |
|------|------|
| 人數 | {record.total_personas} |
| 7-11 偏好 | {record.brand_percentages.get('7-11', 0)}% |
| 全家偏好 | {record.brand_percentages.get('FamilyMart', 0)}% |
| 數位採用率 | {record.digital_adoption_rate*100:.1f}% |
| 遊戲化參與 | {record.gamification_engagement*100:.1f}% |
| 效率分數 | {record.efficiency_score*100:.1f}% |

"""
    
    return summary

# ============ 分析功能 ============

def analyze_trend(days: int = 3) -> Dict:
    """分析近期趨勢"""
    log(f"分析過去 {days} 天趨勢...")
    
    if not os.path.exists(CONFIG['data_file']):
        return {"error": "無歷史數據"}
    
    records = []
    with open(CONFIG['data_file'], 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    
    # 取得最近 N 天的記錄
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    recent = [r for r in records if r['timestamp'][:10] >= cutoff]
    
    if not recent:
        return {"error": f"過去 {days} 天無數據"}
    
    # 按群體+地域分析
    analysis = {}
    for record in recent:
        key = f"{record['group']}_{record['region']}"
        if key not in analysis:
            analysis[key] = {
                'group': record['group'],
                'region': record['region'],
                'samples': [],
                'brand_trend': {'7-11': [], 'FamilyMart': []}
            }
        
        analysis[key]['samples'].append(record['avg_satisfaction'])
        analysis[key]['brand_trend']['7-11'].append(record['brand_percentages'].get('7-11', 0))
        analysis[key]['brand_trend']['FamilyMart'].append(record['brand_percentages'].get('FamilyMart', 0))
    
    # 計算趨勢
    result = {}
    for key, data in analysis.items():
        result[key] = {
            'avg_satisfaction': sum(data['samples']) / len(data['samples']),
            '7-11_avg': sum(data['brand_trend']['7-11']) / len(data['brand_trend']['7-11']),
            'FamilyMart_avg': sum(data['brand_trend']['FamilyMart']) / len(data['brand_trend']['FamilyMart']),
            'brand_shift': (sum(data['brand_trend']['FamilyMart']) / len(data['brand_trend']['FamilyMart'])) - 
                          (sum(data['brand_trend']['7-11']) / len(data['brand_trend']['7-11']))
        }
    
    return result

# ============ 主程式 ============

def run():
    """主程式"""
    print("="*60)
    print("📊 數位孿生月度追蹤系統")
    print("="*60)
    
    # 1. 抓取促銷
    promotions = fetch_daily_promotions()
    
    # 2. 生成 Persona
    personas = generate_personas(CONFIG['num_agents_per_group'])
    
    # 3. 模擬行為
    records = simulate_daily_behavior(personas, promotions)
    
    # 4. 保存到 JSONL
    save_to_jsonl(records)
    
    # 5. 生成摘要
    summary = generate_summary(records)
    
    # 顯示摘要
    print(f"\n{'='*60}")
    print("📊 當日摘要")
    print("="*60)
    
    for record in records:
        print(f"\n{record.group} / {record.region}:")
        print(f"  7-11: {record.brand_percentages.get('7-11', 0)}%")
        print(f"  全家: {record.brand_percentages.get('FamilyMart', 0)}%")
        print(f"  滿意度: {record.avg_satisfaction*100:.1f}%")
        print(f"  數位採用: {record.digital_adoption_rate*100:.1f}%")
    
    print(f"\n📁 數據已保存: {CONFIG['data_file']}")
    
    return records, summary

if __name__ == '__main__':
    run()
