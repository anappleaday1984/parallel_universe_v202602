#!/usr/bin/env python3
"""
數位孿生日間情報分析系統
Digital Twin Daily Intelligence Analysis

根據每日網路動態分析兩類人消費習性變化
輸出 JSON 格式報告
"""

import os
import json
import random
from datetime import datetime
from typing import Dict, List, Any

CONFIG = {
    'output_file': '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring/data/daily_intel_report.jsonl',
    'promo_file': '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring/data/promotions_20260214.json',
    'log_file': '/Users/the_mini_bot/.openclaw/workspace/logs/digital_twin_intel.log',
}

# ============ Persona 定義 ============

PERSONAS = {
    'Fresh_Grad': {
        'name': '社會新鮮人',
        'age': '22-25歲',
        'status': '單身，租屋族',
        'core_needs': 'CP值、社交熱點、數位便利',
        'points_view': '生活小確幸',
        'characteristics': {
            'price_sensitivity': 0.8,
            'surprise_seeking': 0.85,
            'digital_adoption': 0.95,
            'efficiency_need': 0.4,
            'family_oriented': 0.1
        }
    },
    'FinTech_Family': {
        'name': 'FinTech 菁英家庭',
        'age': '35-45歲',
        'status': '雙薪家庭，二子',
        'core_needs': '品質安全、大量採買效率、集團點數理財',
        'points_view': '家庭資產管理',
        'characteristics': {
            'price_sensitivity': 0.5,
            'surprise_seeking': 0.3,
            'digital_adoption': 0.7,
            'efficiency_need': 0.9,
            'family_oriented': 0.95
        }
    }
}

# ============ 地域參數 ============

REGIONS = {
    'Taipei': {
        'name': '台北',
        'characteristics': '高密度門市、捷運生活圈、高外送依賴',
        'store_density': 1.5,
        'mrt_coverage': 0.9,
        'delivery_dependence': 0.85
    },
    'Tainan': {
        'name': '台南',
        'characteristics': '大型複合店、跨品牌生活圈、連鎖與地方小吃取捨',
        'store_density': 0.6,
        'mrt_coverage': 0.1,
        'delivery_dependence': 0.4
    }
}

# ============ 事件影響權重 ============

EVENT_IMPACTS = {
    '電價調漲': {
        'fresh_grad': {'budget_impact': -0.15, 'shift': '外食減少'},
        'fintech': {'budget_impact': -0.05, 'shift': '開源節流'}
    },
    '限時加倍': {
        'fresh_grad': {'budget_impact': 0.10, 'shift': '瘋搶限時'},
        'fintech': {'budget_impact': 0.05, 'shift': '穩定參與'}
    },
    '霜冰淇淋買一送一': {
        'fresh_grad': {'budget_impact': 0.15, 'shift': '打卡分享'},
        'fintech': {'budget_impact': 0.08, 'shift': '家庭嘗鮮'}
    },
    '點數折抵電費': {
        'fresh_grad': {'budget_impact': 0.05, 'shift': '被動參與'},
        'fintech': {'budget_impact': 0.20, 'shift': '主動理財'}
    },
    '聯名換購': {
        'fresh_grad': {'budget_impact': 0.20, 'shift': '蒐集慾望'},
        'fintech': {'budget_impact': 0.10, 'shift': '理性評估'}
    },
    '複合店擴大': {
        'fresh_grad': {'budget_impact': 0.05, 'shift': '新奇體驗'},
        'fintech': {'budget_impact': 0.15, 'shift': '效率提升'}
    }
}

# ============ 數據獲取 ============

def fetch_daily_promotions() -> Dict:
    """獲取今日促銷資訊"""
    promo_file = CONFIG['promo_file']
    
    if os.path.exists(promo_file):
        try:
            with open(promo_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except:
            pass
    
    return {'promotions': [], 'events': []}

def fetch_recent_events() -> List[str]:
    """獲取近期事件"""
    events_file = '/Users/the_mini_bot/.openclaw/workspace/digital_twin/monitoring/data/events.jsonl'
    
    events = []
    if os.path.exists(events_file):
        try:
            with open(events_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        events.append(json.loads(line).get('event', ''))
        except:
            pass
    
    return events[-5:] if events else []

# ============ 核心分析 ============

def analyze_incentive_match(intelligence: Dict) -> Dict:
    """誘因匹配分析"""
    
    active_events = intelligence.get('events', [])
    
    # 計算影響權重
    fresh_grad_impact = 0
    fintech_impact = 0
    
    for event in active_events:
        if event in EVENT_IMPACTS:
            fresh_grad_impact += EVENT_IMPACTS[event]['fresh_grad']['budget_impact']
            fintech_impact += EVENT_IMPACTS[event]['fintech']['budget_impact']
    
    return {
        'fresh_grad_total_impact': round(fresh_grad_impact, 3),
        'fintech_total_impact': round(fintech_impact, 3),
        'dominant_group': 'Fresh_Grad' if abs(fresh_grad_impact) > abs(fintech_impact) else 'FinTech_Family'
    }

def simulate_regional_behavior(intelligence: Dict, region: str, persona: str) -> Dict:
    """模擬地域行為"""
    
    region_data = REGIONS[region]
    persona_data = PERSONAS[persona]
    chars = persona_data['characteristics']
    
    # 基礎忠誠度
    base_loyalty_7 = random.uniform(0.25, 0.45)
    base_loyalty_fm = random.uniform(0.25, 0.45)
    
    # 事件影響
    event_impact = 0
    shift_reason = "無特殊變化"
    
    active_events = intelligence.get('events', [])
    for event in active_events:
        if event in EVENT_IMPACTS:
            impact = EVENT_IMPACTS[event]
            if persona == 'Fresh_Grad':
                event_impact += impact['fresh_grad']['budget_impact']
                shift_reason = impact['fresh_grad']['shift']
            else:
                event_impact += impact['fintech']['budget_impact']
                shift_reason = impact['fintech']['shift']
    
    # 地域調整
    if region == 'Taipei':
        # 台北：高效率需求
        if chars['efficiency_need'] > 0.7:
            base_loyalty_7 *= 1.1
        # 捷運制約
        base_loyalty_7 *= (1 + region_data['mrt_coverage'] * 0.1)
    else:
        # 台南：複合店偏好
        if chars['family_oriented'] > 0.7:
            base_loyalty_7 *= 1.15
        # 跨品牌容忍
        base_loyalty_fm *= 1.1
    
    # 應用事件影響
    base_loyalty_7 *= (1 + event_impact)
    base_loyalty_fm *= (1 + event_impact * 0.8)
    
    # 正規化
    total = base_loyalty_7 + base_loyalty_fm + 0.2
    loyalty_7 = round(base_loyalty_7 / total, 3)
    loyalty_fm = round(base_loyalty_fm / total, 3)
    
    # 行為描述
    if persona == 'Fresh_Grad':
        if event_impact > 0.1:
            activity = f"受 {shift_reason} 影響，消費意願提升"
        elif event_impact < -0.1:
            activity = f"受 {shift_reason} 影響，消費緊縮"
        else:
            activity = "維持正常消費節奏，關注數位優惠"
    else:
        if event_impact > 0.15:
            activity = f"受 {shift_reason} 影響，積極參與點數理財"
        elif event_impact < -0.1:
            activity = f"受 {shift_reason} 影響，優化家庭支出"
        else:
            activity = "維持效率導向採買，重視品質與折扣"
    
    return {
        'activity': activity,
        'loyalty_7_11': loyalty_7,
        'loyalty_Family': loyalty_fm,
        'trigger': shift_reason
    }

def detect_anomalies(behavior_data: Dict) -> str:
    """異常檢測"""
    
    anomalies = []
    
    # 檢測異常品牌轉移
    for region, data in behavior_data.items():
        fg = data.get('Fresh_Grad', {})
        ff = data.get('FinTech_Family', {})
        
        fg_diff = fg.get('loyalty_7_11', 0) - fg.get('loyalty_Family', 0)
        ff_diff = ff.get('loyalty_7_11', 0) - ff.get('loyalty_Family', 0)
        
        # 顯著轉移
        if abs(fg_diff) > 0.15:
            anomalies.append(f"{region} 新鮮人品牌偏好的顯著變化 (差異: {fg_diff:.2f})")
        if abs(ff_diff) > 0.15:
            anomalies.append(f"{region} FinTech 家庭品牌偏好的顯著變化 (差異: {ff_diff:.2f})")
    
    # 檢測異常行為
    for region, data in behavior_data.items():
        fg = data.get('Fresh_Grad', {})
        if '瘋搶' in fg.get('activity', '') or '打卡' in fg.get('activity', ''):
            anomalies.append(f"{region} 新鮮人出現社交驅動消費行為")
    
    if not anomalies:
        return "無異常行為觀測，群體行為符合預期模型"
    
    return " | ".join(anomalies)

# ============ 主程式 ============

def run():
    """主程式"""
    print("="*60)
    print("📰 數位孿生日間情報分析")
    print("="*60)
    
    # 1. 獲取數據
    print("\n1️⃣ 獲取今日情報...")
    promotions = fetch_daily_promotions()
    recent_events = fetch_recent_events()
    
    intelligence = {
        'promotions': promotions.get('promotions', [])[:5],
        'events': recent_events
    }
    
    # 生成情報摘要
    if recent_events:
        intel_summary = f"今日監測到 {len(recent_events)} 個相關事件：{', '.join(recent_events)}"
    else:
        intel_summary = "今日無重大事件，維持基準消費行為"
    
    print(f"   事件：{intel_summary}")
    
    # 2. 誘因匹配分析
    print("\n2️⃣ 誘因匹配分析...")
    incentive = analyze_incentive_match(intelligence)
    print(f"   主要受影響群體：{incentive['dominant_group']}")
    
    # 3. 模擬行為
    print("\n3️⃣ 模擬地域行為...")
    behavior_report = {}
    
    for region in ['Taipei', 'Tainan']:
        behavior_report[region] = {}
        
        for persona in ['Fresh_Grad', 'FinTech_Family']:
            result = simulate_regional_behavior(intelligence, region, persona)
            behavior_report[region][persona] = result
            
            print(f"   {region} {persona}: 7-11={result['loyalty_7_11']:.1%}, 全家={result['loyalty_Family']:.1%}")
    
    # 4. 異常檢測
    print("\n4️⃣ 異常檢測...")
    anomalies = detect_anomalies(behavior_report)
    print(f"   {anomalies}")
    
    # 5. 生成報告
    print("\n5️⃣ 生成報告...")
    
    report = {
        'date': datetime.now().strftime('%Y-%m-%d'),
        'daily_intelligence_summary': intel_summary,
        'behavioral_twin_report': behavior_report,
        'anomaly_detection': anomalies,
        'incentive_analysis': incentive,
        'metadata': {
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'personas': list(PERSONAS.keys()),
            'regions': list(REGIONS.keys())
        }
    }
    
    # 6. 保存報告
    os.makedirs(os.path.dirname(CONFIG['output_file']), exist_ok=True)
    with open(CONFIG['output_file'], 'a', encoding='utf-8') as f:
        f.write(json.dumps(report, ensure_ascii=False) + '\n')
    
    print(f"\n✅ 報告已保存: {CONFIG['output_file']}")
    
    # 7. 顯示 JSON 輸出
    print("\n" + "="*60)
    print("📄 JSON 輸出")
    print("="*60)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    
    return report

if __name__ == '__main__':
    run()
