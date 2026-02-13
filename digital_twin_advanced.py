#!/usr/bin/env python3
"""
數位孿生進階分析 - 特殊關注項目整合
"""

import os
import json
import random
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List
from enum import Enum

CONFIG = {
    'data_file': '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring/data/behavior_twin_monthly.jsonl',
    'events_file': '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring/data/events.jsonl',
    'num_agents': 500,
}

class Group(Enum):
    FRESHMAN = "新鮮人"
    FINTECH = "FinTech家庭"

class Region(Enum):
    TAIPEI = "台北"
    TAINAN = "台南"

EVENT_TYPES = [
    "電價調漲", "限時加倍", "霜冰淇淋買一送一", 
    "點數折抵電費", "聯名換購", "複合店擴大"
]

@dataclass
class AdvancedPersona:
    persona_id: str
    group: str
    region: str
    points_sensitivity: float
    sudden_switch_trigger: float
    points_linkage_ability: float
    mrt_constraint: float
    parking_importance: float
    compound_preference: float
    age: int
    monthly_budget: float
    digital_adoption: float
    brand_loyalty: Dict[str, float]
    
    def to_dict(self):
        return asdict(self)

def log(msg: str):
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

def generate_personas(num_per_group: int = 500) -> List[AdvancedPersona]:
    log("生成進階 Persona...")
    personas = []
    
    for group in [Group.FRESHMAN.value, Group.FINTECH.value]:
        for i in range(num_per_group):
            for region in [Region.TAIPEI.value, Region.TAINAN.value]:
                params = {
                    Group.FRESHMAN.value: {
                        'points_sensitivity': (0.3, 0.5), 'sudden_switch_trigger': (0.6, 0.9),
                        'points_linkage_ability': (0.2, 0.4), 'monthly_budget': (5000, 15000),
                        'digital_adoption': (0.8, 0.98)
                    },
                    Group.FINTECH.value: {
                        'points_sensitivity': (0.7, 0.95), 'sudden_switch_trigger': (0.2, 0.4),
                        'points_linkage_ability': (0.7, 0.95), 'monthly_budget': (15000, 40000),
                        'digital_adoption': (0.5, 0.8)
                    }
                }[group]
                
                p = AdvancedPersona(
                    persona_id=f"ADV_{group[:2]}_{region[:2]}_{i+1:04d}",
                    group=group, region=region,
                    points_sensitivity=random.uniform(*params['points_sensitivity']),
                    sudden_switch_trigger=random.uniform(*params['sudden_switch_trigger']),
                    points_linkage_ability=random.uniform(*params['points_linkage_ability']),
                    mrt_constraint=random.uniform(0.5, 0.9) if region == Region.TAIPEI.value else random.uniform(0.1, 0.4),
                    parking_importance=random.uniform(0.2, 0.5) if region == Region.TAIPEI.value else random.uniform(0.6, 0.95),
                    compound_preference=random.uniform(0.4, 0.8),
                    age=random.randint(22, 50),
                    monthly_budget=random.uniform(*params['monthly_budget']),
                    digital_adoption=random.uniform(*params['digital_adoption']),
                    brand_loyalty={
                        '7-11': random.uniform(0.3, 0.7),
                        'FamilyMart': random.uniform(0.3, 0.7),
                        'Other': random.uniform(0.1, 0.3)
                    }
                )
                personas.append(p)
    
    log(f"生成 {len(personas)} 個 Persona")
    return personas

def simulate_event(personas: List[AdvancedPersona], event: str = None) -> Dict:
    if not event:
        event = random.choice(EVENT_TYPES)
    
    log(f"模擬事件：{event}")
    
    results = {}
    sudden_count = 0
    
    for group in [Group.FRESHMAN.value, Group.FINTECH.value]:
        for region in [Region.TAIPEI.value, Region.TAINAN.value]:
            filtered = [p for p in personas if p.group == group and p.region == region]
            if not filtered:
                continue
            
            total_7 = total_fm = 0
            for p in filtered:
                base_7 = p.brand_loyalty['7-11']
                base_fm = p.brand_loyalty['FamilyMart']
                
                # 事件影響
                if event == "限時加倍":
                    if group == Group.FRESHMAN.value:
                        base_7 *= 1.25
                        base_fm *= 1.30
                        if p.sudden_switch_trigger > 0.6:
                            sudden_count += 1
                    else:
                        base_7 *= 1.10
                        base_fm *= 1.10
                
                elif event == "霜冰淇淋買一送一":
                    base_fm *= 1.35
                
                elif event == "點數折抵電費":
                    if group == Group.FINTECH.value:
                        base_7 *= 1.40
                
                elif event == "電價調漲":
                    if group == Group.FRESHMAN.value:
                        base_7 *= 0.85
                        base_fm *= 0.85
                    else:
                        base_7 *= 1.05
                
                elif event == "聯名換購":
                    base_fm *= 1.35
                    if group == Group.FRESHMAN.value and p.sudden_switch_trigger > 0.5:
                        sudden_count += 1
                
                elif event == "複合店擴大":
                    if region == Region.TAINAN.value and p.compound_preference > 0.6:
                        base_7 *= 1.30
                
                total_7 += base_7
                total_fm += base_fm
            
            total = total_7 + total_fm + len(filtered) * 0.3
            results[f"{group}_{region}"] = {
                'group': group, 'region': region,
                '7-11': round(total_7 / total * 100, 1),
                'FamilyMart': round(total_fm / total * 100, 1),
                'Other': round(0.3 / (total_7/total + total_fm/total + 0.3) * 100, 1)
            }
    
    insights = []
    if sudden_count > 0:
        insights.append(f"突發轉向：{sudden_count} 人")
    
    if event == "限時加倍":
        insights.append("新鮮人瘋限時活動")
    elif event == "霜冰淇淋買一送一":
        insights.append("全家霜冰淇淋強勢吸客")
    elif event == "點數折抵電費":
        insights.append("FinTech 家庭首選 7-11")
    elif event == "電價調漲":
        insights.append("外食預算緊縮")
    
    return {'event': event, 'results': results, 'insights': insights}

def save_result(result: Dict):
    with open(CONFIG['data_file'], 'a', encoding='utf-8') as f:
        f.write(json.dumps({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **result
        }, ensure_ascii=False) + '\n')

def run(event: str = None):
    print("="*60)
    print("🌐 數位孿生進階分析 - 特殊關注項目")
    print("="*60)
    
    os.makedirs(os.path.dirname(CONFIG['data_file']), exist_ok=True)
    
    personas = generate_personas(CONFIG['num_agents'])
    result = simulate_event(personas, event)
    save_result(result)
    
    print(f"\n📢 事件：{result['event']}")
    print("\n📊 模擬結果：")
    
    for key, data in result['results'].items():
        print(f"\n{data['group']} / {data['region']}:")
        print(f"  7-11: {data['7-11']}%")
        print(f"  全家: {data['FamilyMart']}%")
    
    if result['insights']:
        print(f"\n💡 洞察：")
        for i in result['insights']:
            print(f"  - {i}")
    
    print(f"\n📁 數據已保存: {CONFIG['data_file']}")

if __name__ == '__main__':
    import sys
    event = sys.argv[1] if len(sys.argv) > 1 else None
    run(event)
