#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
주피터 노트북 생성 스크립트
"""

import nbformat as nbf
from pathlib import Path

def create_social_vulnerability_notebook():
    """사회취약지수 분석 주피터 노트북 생성"""
    
    # 새 노트북 생성
    nb = nbf.v4.new_notebook()
    
    # 셀들을 저장할 리스트
    cells = []
    
    # 1. 마크다운 셀 - 제목
    cells.append(nbf.v4.new_markdown_cell("""# 사회취약지수 분석 및 지도 시각화

이 노트북에서는 한국의 지역별 사회취약지수를 분석하고 지도로 시각화합니다.

## 분석 목표
- 자연재해 위험도와 노후주택 현황을 종합한 사회취약지수 계산
- 지역별 취약성 비교 및 시각화
- 인터랙티브 지도 생성"""))
    
    # 2. 코드 셀 - 라이브러리 임포트
    cells.append(nbf.v4.new_code_cell("""# 필요한 라이브러리 임포트
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium import plugins
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False

# 시각화 스타일 설정
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("라이브러리 임포트 완료!")"""))
    
    # 3. 마크다운 셀 - 섹션 제목
    cells.append(nbf.v4.new_markdown_cell("## 1. 데이터 로드 및 전처리"))
    
    # 4. 코드 셀 - 데이터 로드
    cells.append(nbf.v4.new_code_cell("""# 데이터 로드
df = pd.read_csv('../data/processed/processed_data.csv')
print("데이터 형태:", df.shape)
print("\\n데이터 미리보기:")
df.head()"""))
    
    # 5. 코드 셀 - 데이터 정보 확인
    cells.append(nbf.v4.new_code_cell("""# 데이터 정보 확인
print("데이터 정보:")
print(df.info())
print("\\n기술통계:")
print(df.describe())"""))
    
    # 6. 코드 셀 - 결측치 처리
    cells.append(nbf.v4.new_code_cell("""# 결측치 확인 및 처리
print("결측치 확인:")
print(df.isnull().sum())

# 대전광역시의 low_risk 결측치를 0으로 처리
df['low_risk'] = df['low_risk'].fillna(0)
print("\\n결측치 처리 후:")
print(df.isnull().sum())"""))
    
    # 7. 마크다운 셀 - 섹션 제목
    cells.append(nbf.v4.new_markdown_cell("## 2. 사회취약지수 계산"))
    
    # 8. 코드 셀 - 취약지수 계산
    cells.append(nbf.v4.new_code_cell("""# 사회취약지수 계산
# 위험도와 노후주택비율을 고려한 종합 취약지수
df['vulnerability_index'] = (
    df['total_risk'] * 0.4 +  # 전체 위험도 (40%)
    df['high_risk'] * 0.3 +   # 고위험도 (30%)
    df['aged_housing_ratio'] * 0.3  # 노후주택비율 (30%)
)

# 취약지수 정규화 (0-100 스케일)
df['vulnerability_normalized'] = (
    (df['vulnerability_index'] - df['vulnerability_index'].min()) / 
    (df['vulnerability_index'].max() - df['vulnerability_index'].min()) * 100
)

print("사회취약지수 계산 완료")
print("\\n취약지수 상위 5개 지역:")
print(df.nlargest(5, 'vulnerability_normalized')[['region', 'vulnerability_normalized', 'total_risk', 'aged_housing_ratio']])"""))
    
    # 9. 코드 셀 - 등급별 분류
    cells.append(nbf.v4.new_code_cell("""# 취약지수 등급별 분류
def classify_vulnerability(score):
    if score >= 70:
        return '매우 높음'
    elif score >= 50:
        return '높음'
    elif score >= 30:
        return '보통'
    else:
        return '낮음'

df['vulnerability_level'] = df['vulnerability_normalized'].apply(classify_vulnerability)

# 등급별 분포 확인
level_counts = df['vulnerability_level'].value_counts()
print("등급별 분포:")
print(level_counts)

print("\\n등급별 지역 분포:")
for level in ['매우 높음', '높음', '보통', '낮음']:
    regions = df[df['vulnerability_level'] == level]['region'].tolist()
    print(f"{level}: {', '.join(regions)}")"""))
    
    # 10. 마크다운 셀 - 섹션 제목
    cells.append(nbf.v4.new_markdown_cell("## 3. 데이터 시각화"))
    
    # 11. 코드 셀 - 시각화
    cells.append(nbf.v4.new_code_cell("""# 취약지수 분포 시각화
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 1. 취약지수 분포 히스토그램
axes[0, 0].hist(df['vulnerability_normalized'], bins=8, alpha=0.7, color='skyblue', edgecolor='black')
axes[0, 0].set_title('사회취약지수 분포', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('취약지수')
axes[0, 0].set_ylabel('지역 수')
axes[0, 0].grid(True, alpha=0.3)

# 2. 취약지수 상위 10개 지역
top_10 = df.nlargest(10, 'vulnerability_normalized')
axes[0, 1].barh(top_10['region'], top_10['vulnerability_normalized'], color='coral')
axes[0, 1].set_title('취약지수 상위 10개 지역', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('취약지수')

# 3. 위험도 vs 노후주택비율 산점도
scatter = axes[1, 0].scatter(df['total_risk'], df['aged_housing_ratio'], 
                            c=df['vulnerability_normalized'], s=100, alpha=0.7, cmap='viridis')
axes[1, 0].set_title('위험도 vs 노후주택비율', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('전체 위험도')
axes[1, 0].set_ylabel('노후주택비율 (%)')
plt.colorbar(scatter, ax=axes[1, 0], label='취약지수')

# 4. 지역별 취약지수 비교
df_sorted = df.sort_values('vulnerability_normalized', ascending=True)
colors = ['red' if x > 70 else 'orange' if x > 50 else 'yellow' if x > 30 else 'green' 
          for x in df_sorted['vulnerability_normalized']]
axes[1, 1].barh(df_sorted['region'], df_sorted['vulnerability_normalized'], 
                color=colors)
axes[1, 1].set_title('지역별 사회취약지수', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('취약지수')

plt.tight_layout()
plt.show()"""))
    
    # 12. 코드 셀 - 상관관계 분석
    cells.append(nbf.v4.new_code_cell("""# 상관관계 분석
correlation_vars = ['total_risk', 'high_risk', 'medium_risk', 'low_risk', 
                   'aged_housing_ratio', 'vulnerability_normalized']
correlation_matrix = df[correlation_vars].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, linewidths=0.5, cbar_kws={'shrink': 0.8})
plt.title('변수 간 상관관계 분석', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.show()"""))
    
    # 13. 코드 셀 - 파이차트
    cells.append(nbf.v4.new_code_cell("""# 등급별 분포 파이차트
level_counts = df['vulnerability_level'].value_counts()

plt.figure(figsize=(10, 6))
colors = ['red', 'orange', 'yellow', 'green']
plt.pie(level_counts.values, labels=level_counts.index, autopct='%1.1f%%', 
        colors=colors, startangle=90)
plt.title('사회취약지수 등급별 분포', fontsize=16, fontweight='bold')
plt.axis('equal')
plt.show()"""))
    
    # 14. 마크다운 셀 - 섹션 제목
    cells.append(nbf.v4.new_markdown_cell("## 4. 인터랙티브 지도 생성"))
    
    # 15. 코드 셀 - 지도 생성
    cells.append(nbf.v4.new_code_cell("""# 한국 지도 시각화를 위한 지역명 매핑
region_mapping = {
    '서울특별시': 'Seoul',
    '부산광역시': 'Busan',
    '대구광역시': 'Daegu',
    '인천광역시': 'Incheon',
    '광주광역시': 'Gwangju',
    '대전광역시': 'Daejeon',
    '울산광역시': 'Ulsan',
    '세종특별자치시': 'Sejong',
    '경기도': 'Gyeonggi-do',
    '강원도': 'Gangwon-do',
    '충청북도': 'Chungcheongbuk-do',
    '충청남도': 'Chungcheongnam-do',
    '전라북도': 'Jeollabuk-do',
    '전라남도': 'Jeollanam-do',
    '경상북도': 'Gyeongsangbuk-do',
    '경상남도': 'Gyeongsangnam-do',
    '제주특별자치도': 'Jeju-do'
}

# 지역명 매핑 추가
df['region_eng'] = df['region'].map(region_mapping)

# 한국 중심 좌표
korea_center = [36.5, 127.5]

# 지도 생성
m = folium.Map(location=korea_center, zoom_start=7, tiles='OpenStreetMap')

print("지도 생성 중...")"""))
    
    # 16. 코드 셀 - 마커 추가
    cells.append(nbf.v4.new_code_cell("""# 지역별 좌표 정의
region_coords = {
    'Seoul': [37.5665, 126.9780],
    'Busan': [35.1796, 129.0756],
    'Daegu': [35.8714, 128.6014],
    'Incheon': [37.4563, 126.7052],
    'Gwangju': [35.1595, 126.8526],
    'Daejeon': [36.3504, 127.3845],
    'Ulsan': [35.5384, 129.3114],
    'Sejong': [36.4870, 127.2820],
    'Gyeonggi-do': [37.4138, 127.5183],
    'Gangwon-do': [37.8228, 128.1555],
    'Chungcheongbuk-do': [36.8, 127.7],
    'Chungcheongnam-do': [36.5184, 126.8000],
    'Jeollabuk-do': [35.7175, 127.1530],
    'Jeollanam-do': [34.8679, 126.9910],
    'Gyeongsangbuk-do': [36.4919, 128.8889],
    'Gyeongsangnam-do': [35.4606, 128.2132],
    'Jeju-do': [33.4996, 126.5312]
}

# 각 지역에 원형 마커 추가
for idx, row in df.iterrows():
    # 취약지수에 따른 색상 결정
    if row['vulnerability_normalized'] > 70:
        color = 'red'
    elif row['vulnerability_normalized'] > 50:
        color = 'orange'
    elif row['vulnerability_normalized'] > 30:
        color = 'yellow'
    else:
        color = 'green'
    
    if row['region_eng'] in region_coords:
        coords = region_coords[row['region_eng']]
        
        # 팝업 정보
        popup_text = f\"\"\"
        <b>{row['region']}</b><br>
        취약지수: {row['vulnerability_normalized']:.1f}<br>
        전체 위험도: {row['total_risk']}<br>
        고위험도: {row['high_risk']}<br>
        노후주택비율: {row['aged_housing_ratio']:.1f}%<br>
        총 주택수: {row['total_housing_count']:,}개
        \"\"\"
        
        # 원형 마커 추가
        folium.CircleMarker(
            location=coords,
            radius=row['vulnerability_normalized']/5,  # 취약지수에 따른 크기
            popup=folium.Popup(popup_text, max_width=300),
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.7,
            weight=2
        ).add_to(m)

print("마커 추가 완료!")"""))
    
    # 17. 코드 셀 - 범례 및 저장
    cells.append(nbf.v4.new_code_cell("""# 범례 추가
legend_html = \"\"\"
<div style=\"position: fixed; 
            bottom: 50px; left: 50px; width: 200px; height: 120px; 
            background-color: white; border:2px solid grey; z-index:9999; 
            font-size:14px; padding: 10px\">
            <p><b>사회취약지수</b></p>
            <p><span style=\"color:red;\">●</span> 높음 (70+)</p>
            <p><span style=\"color:orange;\">●</span> 중간 (50-70)</p>
            <p><span style=\"color:yellow;\">●</span> 낮음 (30-50)</p>
            <p><span style=\"color:green;\">●</span> 매우 낮음 (<30)</p>
</div>
\"\"\"
m.get_root().html.add_child(folium.Element(legend_html))

# 지도 저장
results_dir = Path('../results')
results_dir.mkdir(exist_ok=True)
m.save(results_dir / 'vulnerability_map_interactive.html')
print("인터랙티브 지도가 '../results/vulnerability_map_interactive.html'에 저장되었습니다.")

# 지도 표시 (노트북에서)
m"""))
    
    # 18. 마크다운 셀 - 섹션 제목
    cells.append(nbf.v4.new_markdown_cell("## 5. 분석 결과 요약"))
    
    # 19. 코드 셀 - 결과 요약
    cells.append(nbf.v4.new_code_cell("""# 분석 결과 요약
print("=== 사회취약지수 분석 결과 요약 ===\\n")

print(f"1. 전체 지역 수: {len(df)}개")
print(f"2. 평균 취약지수: {df['vulnerability_normalized'].mean():.1f}")
print(f"3. 최고 취약지수: {df['vulnerability_normalized'].max():.1f} ({df.loc[df['vulnerability_normalized'].idxmax(), 'region']})")
print(f"4. 최저 취약지수: {df['vulnerability_normalized'].min():.1f} ({df.loc[df['vulnerability_normalized'].idxmin(), 'region']})")

print("\\n5. 취약지수 상위 5개 지역:")
top_5 = df.nlargest(5, 'vulnerability_normalized')
for idx, row in top_5.iterrows():
    print(f"   {row['region']}: {row['vulnerability_normalized']:.1f}")

print("\\n6. 주요 발견사항:")
print("   - 경상북도가 가장 높은 취약지수를 보임")
print("   - 세종특별자치시가 가장 낮은 취약지수를 보임")
print("   - 위험도와 노후주택비율이 취약지수에 큰 영향을 미침")"""))
    
    # 20. 코드 셀 - 결과 저장
    cells.append(nbf.v4.new_code_cell("""# 결과를 CSV로 저장
result_df = df[['region', 'vulnerability_normalized', 'vulnerability_level', 
                'total_risk', 'high_risk', 'aged_housing_ratio']].copy()
result_df = result_df.sort_values('vulnerability_normalized', ascending=False)

# 결과 디렉토리 생성
results_dir = Path('../results')
results_dir.mkdir(exist_ok=True)

result_df.to_csv(results_dir / 'social_vulnerability_analysis.csv', index=False, encoding='utf-8-sig')
print("분석 결과가 '../results/social_vulnerability_analysis.csv'에 저장되었습니다.")

# 최종 결과 테이블 표시
print("\\n최종 분석 결과:")
result_df"""))
    
    # 21. 마크다운 셀 - 정책적 시사점
    cells.append(nbf.v4.new_markdown_cell("""## 6. 정책적 시사점

### 우선 지원 대상 지역
1. **경상북도**: 종합적인 취약성 대책 필요
2. **전라남도**: 노후주택 개선 및 재해 대응 강화
3. **경상남도**: 위험도 감소 및 주택 개선
4. **강원도**: 산간 지역 특성을 고려한 대책

### 예방적 조치 필요 지역
- **전라북도**: 취약지수 상승 방지
- **충청북도**: 지속적 모니터링 필요

### 모범 사례 지역
- **세종특별자치시**: 계획도시의 장점 활용
- **경기도**: 대도시권의 안정성 확보

## 결론
자연재해 위험도와 노후주택 현황을 종합적으로 분석한 결과, 경상북도를 중심으로 한 영남권과 전라권의 취약성이 높게 나타났습니다. 이 분석 결과는 지역별 맞춤형 재해 대응 정책 수립과 주택 개선 사업의 우선순위 결정에 활용할 수 있습니다."""))
    
    # 셀들을 노트북에 추가
    nb.cells = cells
    
    # 메타데이터 설정
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {
                "name": "ipython",
                "version": 3
            },
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.5"
        }
    }
    
    # 노트북 저장
    notebooks_dir = Path('notebooks')
    notebooks_dir.mkdir(exist_ok=True)
    
    notebook_path = notebooks_dir / '02_social_vulnerability_analysis.ipynb'
    nbf.write(nb, notebook_path)
    
    print(f"주피터 노트북이 생성되었습니다: {notebook_path}")
    return notebook_path

if __name__ == "__main__":
    create_social_vulnerability_notebook() 