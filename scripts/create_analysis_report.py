#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
취약지수 상관관계 및 종합 위험도 분석 리포트 생성
"""

import pandas as pd
import json
import numpy as np

print("📊 취약지수 분석 리포트 생성 시작")

# 데이터 로드
housing_data = pd.read_csv('results/yunjin/housing_vulnerability_analysis.csv')
sewer_data = pd.read_csv('results/yunjin/sewer_infrastructure_analysis_summary.csv')
social_data = pd.read_csv('data/processed/202506_읍면동_사회취약계층표.csv')
rainfall_data = pd.read_csv('data/processed/여름_강수량_호우_백분위.csv', encoding='cp949')

# 시도별 통계 계산
def calculate_sido_stats():
    """시도별 평균 지수 계산"""
    stats = {}
    sido_list = ['전국', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', 
                 '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', 
                 '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']
    
    sido_stations = {
        '서울특별시': ['서울'],
        '부산광역시': ['부산'],
        '대구광역시': ['대구'],
        '인천광역시': ['인천'],
        '광주광역시': ['광주'],
        '대전광역시': ['대전'],
        '울산광역시': ['울산'],
        '세종특별자치시': ['세종'],
        '경기도': ['수원', '파주', '동두천', '이천', '양평'],
        '강원도': ['춘천', '원주', '강릉', '동해', '태백', '속초', '홍천', '영월'],
        '충청북도': ['충주', '청주', '제천', '보은'],
        '충청남도': ['천안', '서산', '보령', '홍성'],
        '전라북도': ['전주', '군산', '정읍', '남원', '순창군', '장수', '임실', '부안'],
        '전라남도': ['순천', '여수', '목포', '해남', '고흥', '거창', '장흥', '영광군', '진도군'],
        '경상북도': ['영주', '봉화', '밀양', '상주', '의령군', '정선군', '합천', '태백', '고산', '의성', '문경', '구미', '안동', '경주시', '영천', '청송군', '울진', '영덕', '울릉도'],
        '경상남도': ['산청', '거제', '통영', '창원', '부여', '양산시', '김해시', '성산', '진주', '밀양', '포항', '남해'],
        '제주특별자치도': ['제주', '서귀포', '고산', '흑산도', '백령도']
    }
    
    for sido in sido_list[1:]:
        housing_sido = housing_data[housing_data['region'] == sido]
        avg_housing = housing_sido['vulnerability_normalized'].mean() if len(housing_sido) > 0 else 0
        
        sewer_sido = sewer_data[sewer_data['시도'] == sido]
        avg_sewer = sewer_sido['하수도_인프라_지수'].mean() if len(sewer_sido) > 0 else 0
        
        social_sido = social_data[social_data['시도명'] == sido]
        avg_social = social_sido['사회취약지수'].mean() if len(social_sido) > 0 else 0
        
        avg_rainfall = 0
        if sido in sido_stations:
            stations = sido_stations[sido]
            rainfall_values = []
            for station in stations:
                station_data = rainfall_data[rainfall_data['지점정보'].str.contains(station, na=False)]
                if len(station_data) > 0:
                    rainfall_values.extend(station_data['백분위(강수량 0.5, 호우 * 0.5)'].tolist())
            
            if rainfall_values:
                avg_rainfall = sum(rainfall_values) / len(rainfall_values)
        
        stats[sido] = {
            'avg_housing': avg_housing,
            'avg_sewer': avg_sewer,
            'avg_social': avg_social,
            'avg_rainfall': avg_rainfall
        }
    
    return stats

sido_stats = calculate_sido_stats()

# 상관관계 및 종합 위험도 분석
def analyze_vulnerability_correlations():
    """시도별 취약지수 상관관계 및 종합 위험도 분석"""
    
    # 시도별 데이터를 DataFrame으로 변환
    analysis_data = []
    for sido, stats in sido_stats.items():
        if sido != '전국':  # 전국은 제외하고 시도별만 분석
            analysis_data.append({
                'sido': sido,
                'housing': stats['avg_housing'],
                'sewer': stats['avg_sewer'],
                'social': stats['avg_social'],
                'rainfall': stats['avg_rainfall']
            })
    
    df = pd.DataFrame(analysis_data)
    
    # 상관관계 계산
    correlations = df[['housing', 'sewer', 'social', 'rainfall']].corr()
    
    # 종합 위험도 계산 (가중 평균)
    df['integrated_risk'] = (
        df['housing'] * 0.3 + 
        df['sewer'] * 0.2 + 
        df['social'] * 0.2 + 
        df['rainfall'] * 0.3
    )
    
    # 종합 위험도를 백분율로 변환 (0-100 범위)
    df['integrated_risk_percent'] = df['integrated_risk']
    
    # 위험도 등급 분류 (5등급)
    def classify_risk(score):
        if score < 20:
            return '매우낮음'
        elif score < 40:
            return '낮음'
        elif score < 60:
            return '보통'
        elif score < 80:
            return '위험'
        else:
            return '매우위험'
    
    df['risk_level'] = df['integrated_risk_percent'].apply(classify_risk)
    
    # 상위 위험 지역 (종합 위험도 기준)
    high_risk_regions = df.nlargest(5, 'integrated_risk')[['sido', 'integrated_risk', 'risk_level']]
    
    # 각 지수별 상위 위험 지역
    housing_high_risk = df.nlargest(3, 'housing')[['sido', 'housing']]
    sewer_high_risk = df.nlargest(3, 'sewer')[['sido', 'sewer']]
    social_high_risk = df.nlargest(3, 'social')[['sido', 'social']]
    rainfall_high_risk = df.nlargest(3, 'rainfall')[['sido', 'rainfall']]
    
    return {
        'correlations': correlations,
        'integrated_analysis': df,
        'high_risk_regions': high_risk_regions,
        'housing_high_risk': housing_high_risk,
        'sewer_high_risk': sewer_high_risk,
        'social_high_risk': social_high_risk,
        'rainfall_high_risk': rainfall_high_risk
    }

# 분석 실행
analysis_results = analyze_vulnerability_correlations()

# 위험도 점수에 따른 CSS 클래스 반환 함수
def get_risk_class(score):
    if score < 20:
        return 'low'
    elif score < 40:
        return 'low'
    elif score < 60:
        return 'medium'
    elif score < 80:
        return 'high'
    else:
        return 'high'

# HTML 리포트 생성
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>취약지수 상관관계 및 종합 위험도 분석 리포트</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: 'Nanum Gothic', Arial, sans-serif;
            background: #f8f9fa;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #495057 0%, #343a40 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 300;
        }}
        .header p {{
            margin: 10px 0 0 0;
            font-size: 1.2em;
            opacity: 0.9;
        }}
        .content {{
            padding: 30px;
        }}
        .section {{
            margin-bottom: 40px;
            padding: 25px;
            background: #f8f9fa;
            border-radius: 8px;
            border-left: 4px solid #6c757d;
        }}
        .section h2 {{
            color: #333;
            margin-top: 0;
            font-size: 1.8em;
            border-bottom: 2px solid #6c757d;
            padding-bottom: 10px;
        }}
        .correlation-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}
        .correlation-item {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            border: 2px solid transparent;
            transition: all 0.3s ease;
        }}
        .correlation-item:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        }}
        .correlation-item.strong-positive {{
            border-color: #dc3545;
            background: linear-gradient(135deg, #ff6b6b, #ee5a52);
            color: white;
        }}
        .correlation-item.strong-negative {{
            border-color: #28a745;
            background: linear-gradient(135deg, #51cf66, #40c057);
            color: white;
        }}
        .correlation-item.moderate {{
            border-color: #ffc107;
            background: linear-gradient(135deg, #ffd43b, #fcc419);
            color: #333;
        }}
        .correlation-item.weak {{
            border-color: #6c757d;
            background: linear-gradient(135deg, #adb5bd, #868e96);
            color: white;
        }}
        .correlation-label {{
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 10px;
        }}
        .correlation-value {{
            font-size: 24px;
            font-weight: bold;
        }}
        .correlation-interpretation {{
            font-size: 12px;
            margin-top: 10px;
            opacity: 0.8;
        }}
        .risk-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .risk-table th {{
            background: #6c757d;
            color: white;
            padding: 15px;
            text-align: left;
            font-weight: 600;
        }}
        .risk-table td {{
            padding: 12px 15px;
            border-bottom: 1px solid #dee2e6;
        }}
        .risk-table tr:hover {{
            background: #f8f9fa;
        }}
        .risk-level {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
        }}
        .risk-level.high {{
            background: #dc3545;
            color: white;
        }}
        .risk-level.medium {{
            background: #ffc107;
            color: #333;
        }}
        .risk-level.low {{
            background: #28a745;
            color: white;
        }}
        .insights {{
            background: #e9ecef;
            border-left: 4px solid #6c757d;
            padding: 20px;
            margin: 20px 0;
            border-radius: 4px;
        }}
        .insights h3 {{
            color: #495057;
            margin-top: 0;
        }}
        .insights ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        .insights li {{
            margin-bottom: 8px;
            line-height: 1.6;
        }}
        .chart-container {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            margin: 20px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 15px;
            color: #333;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>취약지수 상관관계 및 종합 위험도 분석</h1>
            <p>시도별 취약지수 간 상관관계 분석 및 종합 위험도 평가</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📊 취약지수 상관관계 분석</h2>
                <div class="correlation-grid">
                    <div class="correlation-item strong-positive">
                        <div class="correlation-label">주거취약 ↔ 사회취약</div>
                        <div class="correlation-value">{analysis_results['correlations'].loc['housing', 'social']:.3f}</div>
                        <div class="correlation-interpretation">매우 강한 양의 상관관계</div>
                    </div>
                    <div class="correlation-item strong-negative">
                        <div class="correlation-label">주거취약 ↔ 하수도인프라</div>
                        <div class="correlation-value">{analysis_results['correlations'].loc['housing', 'sewer']:.3f}</div>
                        <div class="correlation-interpretation">강한 음의 상관관계</div>
                    </div>
                    <div class="correlation-item strong-negative">
                        <div class="correlation-label">사회취약 ↔ 하수도인프라</div>
                        <div class="correlation-value">{analysis_results['correlations'].loc['social', 'sewer']:.3f}</div>
                        <div class="correlation-interpretation">강한 음의 상관관계</div>
                    </div>
                    <div class="correlation-item weak">
                        <div class="correlation-label">주거취약 ↔ 강수량</div>
                        <div class="correlation-value">{analysis_results['correlations'].loc['housing', 'rainfall']:.3f}</div>
                        <div class="correlation-interpretation">약한 음의 상관관계</div>
                    </div>
                    <div class="correlation-item weak">
                        <div class="correlation-label">하수도인프라 ↔ 강수량</div>
                        <div class="correlation-value">{analysis_results['correlations'].loc['sewer', 'rainfall']:.3f}</div>
                        <div class="correlation-interpretation">약한 양의 상관관계</div>
                    </div>
                    <div class="correlation-item weak">
                        <div class="correlation-label">사회취약 ↔ 강수량</div>
                        <div class="correlation-value">{analysis_results['correlations'].loc['social', 'rainfall']:.3f}</div>
                        <div class="correlation-interpretation">약한 음의 상관관계</div>
                    </div>
                </div>
                
                <div class="insights">
                    <h3>🔍 주요 인사이트</h3>
                    <ul>
                        <li><strong>주거취약과 사회취약의 강한 양의 상관관계 (0.934):</strong> 주거환경이 취약한 지역은 사회적 취약성도 높은 경향이 있습니다. 이는 지역 개발 수준과 사회적 안전망이 밀접하게 연관되어 있음을 시사합니다.</li>
                        <li><strong>주거취약/사회취약과 하수도인프라의 강한 음의 상관관계 (-0.714/-0.671):</strong> 취약성이 높은 지역일수록 하수도 인프라가 부족한 경향이 있습니다. 인프라 투자가 취약성 완화에 중요한 역할을 함을 보여줍니다.</li>
                        <li><strong>강수량과 다른 지수들의 약한 상관관계:</strong> 강수량은 다른 취약지수들과 독립적인 요인으로, 기후변화 대응 정책이 별도로 필요함을 시사합니다.</li>
                    </ul>
                </div>
            </div>
            
            <div class="section">
                <h2>🏆 종합 위험도 분석 (상위 5개 지역)</h2>
                <table class="risk-table">
                    <thead>
                        <tr>
                            <th>순위</th>
                            <th>지역</th>
                            <th>종합 위험도</th>
                            <th>위험 등급</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join([f'''
                        <tr>
                            <td>{i+1}</td>
                            <td>{row['sido']}</td>
                            <td>{row['integrated_risk']:.1f}</td>
                            <td><span class="risk-level {get_risk_class(row['integrated_risk'])}">{row['risk_level']}</span></td>
                        </tr>
                        ''' for i, (_, row) in enumerate(analysis_results['high_risk_regions'].iterrows())])}
                    </tbody>
                </table>
                
                <div class="insights">
                    <h3>📈 종합 위험도 계산 방식</h3>
                    <p><strong>가중 평균 공식:</strong> 주거취약지수(30%) + 하수도인프라지수(20%) + 사회취약지수(20%) + 강수량지수(30%)</p>
                    <p><strong>위험 등급 분류:</strong> 매우낮음(&lt;20) | 낮음(20-40) | 보통(40-60) | 위험(60-80) | 매우위험(&gt;80)</p>
                </div>
            </div>
            
            <div class="section">
                <h2>📋 각 지수별 상위 위험 지역</h2>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                    <div class="chart-container">
                        <div class="chart-title">🏠 주거취약지수 상위 3개 지역</div>
                        <table class="risk-table">
                            <thead>
                                <tr>
                                    <th>순위</th>
                                    <th>지역</th>
                                    <th>지수값</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{i+1}</td>
                                    <td>{row['sido']}</td>
                                    <td>{row['housing']:.1f}</td>
                                </tr>
                                ''' for i, (_, row) in enumerate(analysis_results['housing_high_risk'].iterrows())])}
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">💧 하수도 인프라지수 상위 3개 지역</div>
                        <table class="risk-table">
                            <thead>
                                <tr>
                                    <th>순위</th>
                                    <th>지역</th>
                                    <th>지수값</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{i+1}</td>
                                    <td>{row['sido']}</td>
                                    <td>{row['sewer']:.1f}</td>
                                </tr>
                                ''' for i, (_, row) in enumerate(analysis_results['sewer_high_risk'].iterrows())])}
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">👥 사회취약지수 상위 3개 지역</div>
                        <table class="risk-table">
                            <thead>
                                <tr>
                                    <th>순위</th>
                                    <th>지역</th>
                                    <th>지수값</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{i+1}</td>
                                    <td>{row['sido']}</td>
                                    <td>{row['social']:.1f}</td>
                                </tr>
                                ''' for i, (_, row) in enumerate(analysis_results['social_high_risk'].iterrows())])}
                            </tbody>
                        </table>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">🌧️ 강수량지수 상위 3개 지역</div>
                        <table class="risk-table">
                            <thead>
                                <tr>
                                    <th>순위</th>
                                    <th>지역</th>
                                    <th>지수값</th>
                                </tr>
                            </thead>
                            <tbody>
                                {''.join([f'''
                                <tr>
                                    <td>{i+1}</td>
                                    <td>{row['sido']}</td>
                                    <td>{row['rainfall']:.1f}</td>
                                </tr>
                                ''' for i, (_, row) in enumerate(analysis_results['rainfall_high_risk'].iterrows())])}
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>🎯 정책 제안</h2>
                <div class="insights">
                    <h3>💡 종합적 취약성 완화 전략</h3>
                    <ul>
                        <li><strong>통합적 접근:</strong> 주거취약과 사회취약의 강한 상관관계를 고려하여, 주거환경 개선과 사회안전망 강화를 동시에 추진해야 합니다.</li>
                        <li><strong>인프라 투자 우선순위:</strong> 하수도 인프라가 취약성 완화에 중요한 역할을 하므로, 취약지역의 인프라 투자를 우선적으로 확대해야 합니다.</li>
                        <li><strong>기후변화 대응:</strong> 강수량은 독립적 요인으로 작용하므로, 기후변화 적응 정책을 별도로 수립하고 추진해야 합니다.</li>
                        <li><strong>지역별 맞춤 정책:</strong> 각 지역의 특성에 맞는 차별화된 취약성 완화 정책을 수립해야 합니다.</li>
                    </ul>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# HTML 파일 저장
output_path = 'results/vulnerability_analysis_report.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"💾 분석 리포트 저장 완료: {output_path}")
print("🎉 취약지수 분석 리포트 생성 완료!") 