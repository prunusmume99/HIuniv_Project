#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
향상된 통합 취약지수 지도 생성
상위 10개 위험지역 그래프와 시도별 필터링 기능 포함
"""

import pandas as pd
import folium
import json
import numpy as np
from folium import plugins
import branca.colormap as cm
import os

print("🚀 향상된 통합 취약지수 지도 생성 시작")

# 데이터 로드
housing_data = pd.read_csv('results/yunjin/housing_vulnerability_analysis.csv')
sewer_data = pd.read_csv('results/yunjin/sewer_infrastructure_analysis_summary.csv')
social_data = pd.read_csv('data/processed/202506_읍면동_사회취약계층표.csv')
rainfall_data = pd.read_csv('data/processed/여름_강수량_호우_백분위.csv', encoding='cp949')

# GeoJSON 데이터 로드 및 통합
print("📁 GeoJSON 데이터 로드 중...")

# 모든 시도의 GeoJSON 파일 경로
geo_paths = {
    '서울': 'data/raw/hangjeongdong_서울특별시.geojson',
    '부산': 'data/raw/hangjeongdong_부산광역시.geojson',
    '대구': 'data/raw/hangjeongdong_대구광역시.geojson',
    '인천': 'data/raw/hangjeongdong_인천광역시.geojson',
    '광주': 'data/raw/hangjeongdong_광주광역시.geojson',
    '대전': 'data/raw/hangjeongdong_대전광역시.geojson',
    '울산': 'data/raw/hangjeongdong_울산광역시.geojson',
    '세종': 'data/raw/hangjeongdong_세종특별자치시.geojson',
    '경기': 'data/raw/hangjeongdong_경기도.geojson',
    '강원': 'data/raw/hangjeongdong_강원도.geojson',
    '충북': 'data/raw/hangjeongdong_충청북도.geojson',
    '충남': 'data/raw/hangjeongdong_충청남도.geojson',
    '전북': 'data/raw/hangjeongdong_전라북도.geojson',
    '전남': 'data/raw/hangjeongdong_전라남도.geojson',
    '경북': 'data/raw/hangjeongdong_경상북도.geojson',
    '경남': 'data/raw/hangjeongdong_경상남도.geojson',
    '제주': 'data/raw/hangjeongdong_제주특별자치도.geojson'
}

# GeoJSON 파일들 로드
geos = []
for sido, path in geo_paths.items():
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            geo_data = json.load(f)
            geos.append(geo_data)
            print(f"✅ {sido}: {len(geo_data['features'])}개 행정동")
    else:
        print(f"❌ {sido}: 파일 없음 ({path})")

# 모든 GeoJSON 병합
geo_all = {
    "type": "FeatureCollection",
    "features": [f for g in geos for f in g['features']]
}

print(f"✅ GeoJSON 로드 완료: {len(geo_all['features'])}개 행정동")

# 통합 취약도 계산을 위한 임시 데이터 생성
# 실제로는 기존 통합 지도 생성 스크립트의 로직을 사용해야 함
# 여기서는 간단한 예시로 임시 데이터 생성
for feat in geo_all['features']:
    # 임시로 랜덤 값 생성 (실제로는 기존 로직 사용)
    feat['properties']['통합취약도'] = np.random.uniform(20, 80)

# 상위 10개 데이터 추출
def get_top_10_data(data, value_col, name_col):
    """상위 10개 데이터 추출 (높은 값 순)"""
    sorted_data = data.sort_values(value_col, ascending=False).head(10)
    return [
        {'region': row[name_col], 'value': row[value_col]} 
        for _, row in sorted_data.iterrows()
    ]

def get_top_10_data_low(data, value_col, name_col):
    """상위 10개 데이터 추출 (낮은 값 순)"""
    sorted_data = data.sort_values(value_col, ascending=True).head(10)
    return [
        {'region': row[name_col], 'value': row[value_col]} 
        for _, row in sorted_data.iterrows()
    ]

def get_top_10_data_from_features(features, value_col, name_col):
    """GeoJSON features에서 상위 10개 데이터 추출"""
    data_list = []
    for feat in features:
        properties = feat['properties']
        if value_col in properties and name_col in properties:
            data_list.append({
                'region': properties[name_col],
                'value': properties[value_col]
            })
    
    # 값 기준으로 정렬 (높은 값이 위험)
    data_list.sort(key=lambda x: x['value'], reverse=True)
    return data_list[:10]

# 각 지수별 상위 10개
housing_top10 = get_top_10_data(housing_data, 'vulnerability_normalized', 'region')
# 수도인프라지수는 낮은 값이 취약하므로 별도 함수 사용
sewer_top10 = get_top_10_data_low(sewer_data, '하수도_인프라_지수', '행정구역명')
social_top10 = get_top_10_data(social_data, '사회취약지수', '읍면동명')
rainfall_top10 = get_top_10_data(rainfall_data, '백분위(강수량 0.5, 호우 * 0.5)', '지점정보')


# 시도 목록
sido_list = ['전국', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시', 
             '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', 
             '충청남도', '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']

# 시도별 통계 계산
def calculate_sido_stats():
    """시도별 평균 지수 계산"""
    stats = {}
    
    # 전국 평균
    stats['전국'] = {
        'avg_housing': housing_data['vulnerability_normalized'].mean(),
        'avg_sewer': sewer_data['하수도_인프라_지수'].mean(),
        'avg_social': social_data['사회취약지수'].mean(),
        'avg_rainfall': rainfall_data['백분위(강수량 0.5, 호우 * 0.5)'].mean()
    }
    
    # 시도별 평균 (주거취약지수는 시도별 데이터가 있으므로 그대로 사용)
    for sido in sido_list[1:]:  # 전국 제외
        # 주거취약지수
        housing_sido = housing_data[housing_data['region'] == sido]
        avg_housing = housing_sido['vulnerability_normalized'].mean() if len(housing_sido) > 0 else 0
        
        # 수도인프라지수
        sewer_sido = sewer_data[sewer_data['시도'] == sido]
        avg_sewer = sewer_sido['하수도_인프라_지수'].mean() if len(sewer_sido) > 0 else 0
        
        # 사회취약지수
        social_sido = social_data[social_data['시도명'] == sido]
        avg_social = social_sido['사회취약지수'].mean() if len(social_sido) > 0 else 0
        
        # 강수량지수 (시도별로 가장 가까운 지점 사용)
        rainfall_sido = rainfall_data[rainfall_data['지점정보'].str.contains(sido[:2], na=False)]
        avg_rainfall = rainfall_sido['백분위(강수량 0.5, 호우 * 0.5)'].mean() if len(rainfall_sido) > 0 else 0
        
        stats[sido] = {
            'avg_housing': avg_housing,
            'avg_sewer': avg_sewer,
            'avg_social': avg_social,
            'avg_rainfall': avg_rainfall
        }
    
    return stats

# 시도별 통계 데이터 생성
sido_stats = calculate_sido_stats()

# HTML 템플릿 생성
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>향상된 통합 취약지수 지도</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Nanum Gothic', Arial, sans-serif;
        }}
        .container {{
            display: flex;
            height: 100vh;
        }}
        .map-container {{
            flex: 1;
            position: relative;
        }}
        .sidebar {{
            width: 400px;
            background: #f8f9fa;
            border-left: 1px solid #dee2e6;
            overflow-y: auto;
            padding: 20px;
            max-height: 100vh;
        }}
        .chart-container {{
            margin-bottom: 30px;
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}
        .filter-section {{
            margin-bottom: 20px;
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .filter-title {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}
        .sido-buttons {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        .sido-btn {{
            padding: 5px 10px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
        }}
        .sido-btn:hover {{
            background: #f0f0f0;
        }}
        .sido-btn.active {{
            background: #007bff;
            color: white;
            border-color: #007bff;
        }}
        .stats-section {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 20px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stats-title {{
            font-size: 16px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
        }}
        .stat-item {{
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 4px;
        }}
        .stat-value {{
            font-size: 18px;
            font-weight: bold;
            color: #007bff;
        }}
        .stat-label {{
            font-size: 12px;
            color: #666;
        }}
        .tab-container {{
            margin-bottom: 20px;
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-height: 400px;
            overflow-y: auto;
        }}
        .tab-buttons {{
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
        }}
        .tab-btn {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            flex: 1;
        }}
        .tab-btn:hover {{
            background: #f0f0f0;
        }}
        .tab-btn.active {{
            background: #007bff;
            color: white;
            border-color: #007bff;
        }}
        .chart-content {{
            display: none;
        }}
        .chart-content.active {{
            display: block;
        }}
        .chart-content canvas {{
            max-height: 300px !important;
            height: 300px !important;
        }}
        .map-tab-container {{
            margin-bottom: 20px;
            background: white;
            border-radius: 8px;
            padding: 15px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .map-tab-buttons {{
            display: flex;
            gap: 5px;
            margin-bottom: 15px;
        }}
        .map-tab-btn {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            background: white;
            border-radius: 4px;
            cursor: pointer;
            font-size: 12px;
            flex: 1;
        }}
        .map-tab-btn:hover {{
            background: #f0f0f0;
        }}
        .map-tab-btn.active {{
            background: #007bff;
            color: white;
            border-color: #007bff;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="map-container" id="map">
            <iframe src="integrated_housing_sewer_social_map_fixed.html" width="100%" height="100%" frameborder="0"></iframe>
        </div>
        <div class="sidebar">
            <div class="filter-section">
                <div class="filter-title">지역 필터</div>
                <div class="sido-buttons" id="sidoButtons">
                    <!-- 시도 버튼들이 여기에 생성됩니다 -->
                </div>
            </div>
            
            <div class="stats-section">
                <div class="stats-title">현재 지역 통계</div>
                <div class="stats-grid" id="statsGrid">
                    <!-- 통계가 여기에 표시됩니다 -->
                </div>
            </div>
            
            <div class="tab-container">
                <div class="tab-buttons" id="tabButtons">
                    <!-- 탭 버튼들이 여기에 생성됩니다 -->
                </div>
                
                <div class="chart-content active" id="housingContent">
                    <div class="chart-title">주거취약지수 상위 10개 지역</div>
                    <canvas id="housingChart"></canvas>
                </div>
                
                <div class="chart-content" id="sewerContent">
                    <div class="chart-title">수도인프라지수 취약 상위 10개 지역</div>
                    <canvas id="sewerChart"></canvas>
                </div>
                
                <div class="chart-content" id="socialContent">
                    <div class="chart-title">사회취약지수 상위 10개 지역</div>
                    <canvas id="socialChart"></canvas>
                </div>
                
                <div class="chart-content" id="rainfallContent">
                    <div class="chart-title">강수량지수 상위 10개 지역</div>
                    <canvas id="rainfallChart"></canvas>
                </div>
            </div>
        </div>
    </div>

    <script>
        // top10Data 객체를 각 지수별로 따로 넣음
        const top10Data = {{
            housing: {json.dumps(housing_top10, ensure_ascii=False)},
            sewer: {json.dumps(sewer_top10, ensure_ascii=False)},
            social: {json.dumps(social_top10, ensure_ascii=False)},
            rainfall: {json.dumps(rainfall_top10, ensure_ascii=False)}
        }};
        const sidoList = {json.dumps(sido_list, ensure_ascii=False)};
        const sidoStats = {json.dumps(sido_stats, ensure_ascii=False)};
        
        // 현재 선택된 시도
        let currentSido = '전국';
        
        // 현재 선택된 탭
        let currentTab = 'housing';
        
        // 시도 버튼 생성
        function createSidoButtons() {{
            const container = document.getElementById('sidoButtons');
            container.innerHTML = '';
            
            sidoList.forEach(sido => {{
                const btn = document.createElement('button');
                btn.className = 'sido-btn' + (sido === currentSido ? ' active' : '');
                btn.textContent = sido;
                btn.onclick = () => filterBySido(sido);
                container.appendChild(btn);
            }});
        }}
        
        // 탭 버튼 생성
        function createTabButtons() {{
            const container = document.getElementById('tabButtons');
            container.innerHTML = '';
            
            const tabs = [
                {{id: 'housing', name: '주거취약', color: '#de2d26'}},
                {{id: 'sewer', name: '수도취약', color: '#31a354'}},
                {{id: 'social', name: '사회취약', color: '#c51b8a'}},
                {{id: 'rainfall', name: '강수량', color: '#1976d2'}}
            ];
            
            tabs.forEach(tab => {{
                const btn = document.createElement('button');
                btn.className = 'tab-btn' + (tab.id === currentTab ? ' active' : '');
                btn.textContent = tab.name;
                btn.onclick = () => switchTab(tab.id);
                container.appendChild(btn);
            }});
        }}
        
        // 탭 전환
        function switchTab(tabId) {{
            currentTab = tabId;
            createTabButtons();
            
            // 모든 차트 내용 숨기기
            document.querySelectorAll('.chart-content').forEach(content => {{
                content.classList.remove('active');
            }});
            
            // 선택된 탭 내용 보이기
            document.getElementById(tabId + 'Content').classList.add('active');
        }}
        
        // 시도별 필터링
        function filterBySido(sido) {{
            currentSido = sido;
            createSidoButtons();
            updateStats();
            console.log('필터링:', sido);
        }}
        
        // 통계 업데이트
        function updateStats() {{
            const stats = sidoStats[currentSido];
            const statsGrid = document.getElementById('statsGrid');
            statsGrid.innerHTML = `
                <div class="stat-item">
                    <div class="stat-value">${{stats.avg_housing.toFixed(1)}}</div>
                    <div class="stat-label">평균 주거취약지수</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${{stats.avg_sewer.toFixed(1)}}</div>
                    <div class="stat-label">평균 수도인프라지수</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${{stats.avg_social.toFixed(1)}}</div>
                    <div class="stat-label">평균 사회취약지수</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">${{stats.avg_rainfall.toFixed(1)}}</div>
                    <div class="stat-label">평균 강수량지수</div>
                </div>
            `;
        }}
        
        // 차트 생성 함수
        function createChart(canvasId, data, title, color) {{
            const ctx = document.getElementById(canvasId).getContext('2d');
            return new Chart(ctx, {{
                type: 'bar',
                data: {{
                    labels: data.map(item => item.region),
                    datasets: [{{
                        label: title,
                        data: data.map(item => item.value),
                        backgroundColor: color,
                        borderColor: color,
                        borderWidth: 1
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        y: {{
                            beginAtZero: true,
                            title: {{
                                display: true,
                                text: '지수값'
                            }}
                        }},
                        x: {{
                            ticks: {{
                                maxRotation: 45,
                                minRotation: 45
                            }}
                        }}
                    }},
                    plugins: {{
                        legend: {{
                            display: false
                        }}
                    }},
                    layout: {{
                        padding: {{
                            top: 10,
                            bottom: 10
                        }}
                    }}
                }}
            }});
        }}
        
        // 페이지 로드 시 초기화
        document.addEventListener('DOMContentLoaded', function() {{
            createSidoButtons();
            createTabButtons();
            updateStats();
            
            // 차트 생성
            createChart('housingChart', top10Data.housing, '주거취약지수', '#de2d26');
            createChart('sewerChart', top10Data.sewer, '수도인프라지수', '#31a354');
            createChart('socialChart', top10Data.social, '사회취약지수', '#c51b8a');
            createChart('rainfallChart', top10Data.rainfall, '강수량지수', '#1976d2');
        }});
    </script>
</body>
</html>
"""

# HTML 파일 저장
output_path = 'results/enhanced_vulnerability_map.html'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"💾 향상된 지도 저장 완료: {output_path}")
print("🎉 향상된 통합 취약지수 지도 생성 완료!") 