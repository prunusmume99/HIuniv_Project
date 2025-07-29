# 📓 Jupyter Notebooks 폴더

## 📋 폴더 개요
이 폴더는 사회취약지수 분석을 위한 Jupyter Notebook 파일들을 포함합니다.

## 📁 파일 목록

### 1. `01_social_vulnerability_analysis.ipynb`
- **파일 크기**: 18KB (511 lines)
- **생성일**: 2025-07-29
- **설명**: 사회취약지수 분석 및 지도 시각화를 위한 메인 분석 노트북

#### 📊 분석 내용
1. **데이터 로드 및 전처리**
   - `processed_data.csv` 파일 로딩
   - 데이터 정보 확인 및 기술통계
   - 결측치 처리 (대전광역시 low_risk → 0)

2. **사회취약지수 계산**
   - 가중치 기반 취약지수 계산:
     - 전체 위험도 (40%)
     - 고위험도 (30%)
     - 노후주택비율 (30%)
   - 0-100 스케일로 정규화
   - 등급별 분류 (매우 높음/높음/보통/낮음)

3. **데이터 시각화**
   - 취약지수 분포 히스토그램
   - 상위 10개 지역 비교 차트
   - 위험도 vs 노후주택비율 산점도
   - 지역별 취약지수 비교 차트
   - 변수 간 상관관계 히트맵
   - 등급별 분포 파이차트

4. **인터랙티브 지도 생성**
   - Folium을 사용한 한국 지도 시각화
   - 지역별 원형 마커 (색상 및 크기로 취약도 표현)
   - 상세 정보 팝업
   - 범례 포함

5. **결과 요약 및 저장**
   - 분석 결과 요약
   - CSV 파일로 결과 저장
   - HTML 지도 파일 저장

#### 🛠️ 사용된 라이브러리
- **pandas**: 데이터 처리 및 분석
- **numpy**: 수치 계산
- **matplotlib**: 기본 시각화
- **seaborn**: 고급 시각화
- **folium**: 인터랙티브 지도 생성
- **pathlib**: 파일 경로 관리

#### 🎯 실행 방법
```bash
# Jupyter Notebook 실행
jupyter notebook notebooks/01_social_vulnerability_analysis.ipynb

# 또는 Jupyter Lab 사용
jupyter lab notebooks/01_social_vulnerability_analysis.ipynb
```

#### 📈 주요 결과
- **가장 취약한 지역**: 경상북도 (취약지수: 100.0)
- **가장 안전한 지역**: 세종특별자치시 (취약지수: 0.0)
- **취약지수 상위 5개 지역**: 경상북도, 전라남도, 경상남도, 강원도, 전라북도

#### 💾 생성되는 결과물
- `results/social_vulnerability_analysis.csv`: 분석 결과 데이터
- `results/vulnerability_map_interactive.html`: 인터랙티브 지도

## 🔧 노트북 실행 환경

### 필수 라이브러리
```python
# requirements.txt에 포함된 라이브러리들
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
folium>=0.14.0
jupyter>=1.0.0
```

### 한글 폰트 설정
```python
# 노트북 내에서 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
```

## 🚨 주의사항

1. **파일 경로**: 노트북은 `../data/processed/processed_data.csv` 경로에서 데이터를 로드합니다.
2. **결과 저장**: 분석 결과는 `../results/` 폴더에 저장됩니다.
3. **한글 폰트**: `data/NanumGothic.ttf` 폰트 파일이 필요합니다.
4. **인터넷 연결**: Folium 지도 시각화를 위해 인터넷 연결이 필요합니다.

## 📞 문제 해결

### 일반적인 오류
1. **FileNotFoundError**: 데이터 파일 경로 확인
2. **한글 깨짐**: 폰트 설정 확인
3. **지도 로딩 실패**: 인터넷 연결 확인

### 해결 방법
```python
# 경로 문제 해결
import os
print("현재 작업 디렉토리:", os.getcwd())

# 폰트 문제 해결
import matplotlib.font_manager as fm
print("사용 가능한 폰트:", [f.name for f in fm.fontManager.ttflist if 'Nanum' in f.name])
```

---
**마지막 업데이트**: 2025-07-29  
**노트북 버전**: 1.0 