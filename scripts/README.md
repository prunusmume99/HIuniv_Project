# 🔧 Scripts

이 폴더는 프로젝트의 Python 스크립트들을 포함합니다.

## 📋 스크립트 목록

### 🗺️ **🆕 통합 지도 생성 스크립트**

#### 1. `create_fixed_integrated_map.py` (최신)
- **목적**: 통합 취약지수 지도 생성 (등급 매핑 수정 버전)
- **기능**:
  - **4개 레이어 시스템**: 주거취약지수, 수도인프라지수, 사회취약지수, 통합취약지수
  - **유연한 매핑 시스템**: 부분 단어 매칭, 시도명 정규화, 키워드 기반 매칭
  - **등급별 색상 시스템**: 각 지수별 등급에 따른 직관적인 색상 구분
  - **인터랙티브 기능**: 툴팁, 확대/축소, 레이어 컨트롤, 전체화면
  - **높은 매핑 성공률**: 94.3% 매핑 성공 (3295개 성공, 200개 실패)
- **특별 기능**:
  - **세종특별자치시 매핑**: "세종" 키워드로 자동 매핑
  - **부분 매칭**: "장안구" → "수원시 장안구" 등 유연한 매칭
  - **시도명 정규화**: "서울" → "서울특별시" 등 표준화
- **입력**: 
  - `data/processed/202506_읍면동_사회취약계층표.csv`
  - `results/yunjin/sewer_infrastructure_analysis_summary.csv`
  - `results/yunjin/housing_vulnerability_analysis.csv`
  - `data/raw/hangjeongdong_*.geojson` 파일들
- **출력**: `results/integrated_housing_sewer_social_map_fixed.html`

#### 2. `create_integrated_vulnerability_map.py` (이전 버전)
- **목적**: 통합 취약성 지도 시스템 생성
- **기능**:
  - **탭 형태 인터페이스**: 사회취약지수, 수도인프라지수, 주거취약지수를 한 페이지에서 확인
  - **등급별 색상 시스템**: 각 지수별 등급에 따른 직관적인 색상 구분
  - **최강화된 매핑**: 99-100% 매칭률로 정확한 지리적 데이터 연동
  - **인터랙티브 기능**: 툴팁, 확대/축소, 레이어 컨트롤 등
  - **모던한 디자인**: 그라데이션 헤더, 부드러운 탭 전환 애니메이션
- **입력**: 
  - `data/processed/202506_읍면동_사회취약계층표.csv`
  - `results/sewer_infrastructure_analysis_summary.csv`
  - `results/housing_vulnerability_analysis.csv`
  - `data/raw/*.geojson` 파일들
- **출력**: `results/integrated_vulnerability_map.html`

### 📊 **데이터 처리 스크립트**

#### 2. `preprocess_sewer_data.py`
- **목적**: 하수도 인프라 데이터 전처리
- **기능**:
  - 원시 하수도 데이터 로드 및 정리
  - 데이터 타입 변환 및 결측치 처리
  - 인구밀도 계산 및 정규화
  - 전처리된 데이터를 `data/processed/sewer_infrastructure_processed.csv`로 저장
- **입력**: `data/raw/Sewer_Coverage_Rate.csv`
- **출력**: `data/processed/sewer_infrastructure_processed.csv`

#### 3. `sewer_infrastructure_index.py`
- **목적**: 하수도 인프라 지수 계산
- **기능**:
  - 하수도 인프라 지수 계산 (가중치 기반)
  - 인프라 등급 분류
  - 결과를 `data/processed/sewer_infrastructure_analysis.csv`로 저장
- **입력**: `data/processed/sewer_infrastructure_processed.csv`
- **출력**: `data/processed/sewer_infrastructure_analysis.csv`

### 📓 **노트북 생성 스크립트**

#### 4. `create_housing_vulnerability_notebook.py`
- **목적**: 주거취약지수 분석 노트북 생성
- **기능**:
  - 주거취약지수 분석을 위한 Jupyter 노트북 자동 생성
  - 데이터 로드, 분석, 시각화 코드 포함
  - 결과를 `notebooks/01_housing_vulnerability_analysis.ipynb`로 저장
- **출력**: `notebooks/01_housing_vulnerability_analysis.ipynb`

#### 5. `create_sewer_infrastructure_notebook.py`
- **목적**: 하수도 인프라 분석 노트북 생성
- **기능**:
  - 하수도 인프라 분석을 위한 Jupyter 노트북 자동 생성
  - 데이터 전처리, 지수 계산, 시각화 코드 포함
  - 결과를 `notebooks/02_sewer_infrastructure_analysis.ipynb`로 저장
- **출력**: `notebooks/02_sewer_infrastructure_analysis.ipynb`

#### 6. `create_housing_vulnerability_map_notebook.py`
- **목적**: 주거취약지수 지도 시각화 노트북 생성
- **기능**:
  - 주거취약지수 지도 시각화를 위한 Jupyter 노트북 자동 생성
  - 최강화된 매칭 시스템 포함
  - Folium 기반 인터랙티브 지도 생성 코드
  - 결과를 `notebooks/04_housing_vulnerability_map_visualization.ipynb`로 저장
- **출력**: `notebooks/04_housing_vulnerability_map_visualization.ipynb`

#### 7. `create_sewer_map_visualization_notebook.py`
- **목적**: 하수도 인프라 지도 시각화 노트북 생성
- **기능**:
  - 하수도 인프라 지도 시각화를 위한 Jupyter 노트북 자동 생성
  - 최강화된 매칭 시스템 포함
  - Folium 기반 인터랙티브 지도 생성 코드
  - 결과를 `notebooks/03_sewer_infrastructure_map_visualization.ipynb`로 저장
- **출력**: `notebooks/03_sewer_infrastructure_map_visualization.ipynb`

## 🚀 사용 방법

### 환경 설정
```bash
# 필요한 패키지 설치
pip install -r ../requirements.txt

# Python 스크립트 실행
python scripts/[스크립트명].py
```

### 실행 순서
1. **데이터 전처리**: `preprocess_sewer_data.py`
2. **지수 계산**: `sewer_infrastructure_index.py`
3. **노트북 생성**: `create_*.py` 스크립트들
4. **분석 실행**: 생성된 노트북 실행
5. **🆕 통합 지도 생성**: `create_fixed_integrated_map.py` (최신)

### 개별 실행 예시
```bash
# 🆕 통합 취약지수 지도 생성 (최신)
python scripts/create_fixed_integrated_map.py

# 하수도 데이터 전처리
python scripts/preprocess_sewer_data.py

# 하수도 인프라 지수 계산
python scripts/sewer_infrastructure_index.py

# 주거취약지수 분석 노트북 생성
python scripts/create_housing_vulnerability_notebook.py

# 하수도 인프라 분석 노트북 생성
python scripts/create_sewer_infrastructure_notebook.py

# 주거취약지수 지도 시각화 노트북 생성
python scripts/create_housing_vulnerability_map_notebook.py

# 하수도 인프라 지도 시각화 노트북 생성
python scripts/create_sewer_map_visualization_notebook.py
```

## 🔧 주요 기능

### 🗺️ **🆕 통합 지도 시스템**
- **4개 레이어 시스템**: 주거취약지수, 수도인프라지수, 사회취약지수, 통합취약지수
- **유연한 매핑 시스템**: 부분 단어 매칭, 시도명 정규화, 키워드 기반 매칭
- **등급별 색상 시스템**: 각 지수별 등급에 따른 직관적인 색상 구분
- **인터랙티브 기능**: 툴팁, 확대/축소, 레이어 컨트롤, 전체화면
- **높은 매핑 성공률**: 94.3% 매핑 성공 (3295개 성공, 200개 실패)
- **특별 기능**: 세종특별자치시 매핑, 부분 매칭, 시도명 정규화

### 📊 **데이터 처리**
- 안전한 데이터 타입 변환
- 결측치 처리
- 정규화 및 표준화
- 인구밀도 계산

### 🎯 **지수 계산**
- 가중치 기반 복합 지수 계산
- 등급 분류 시스템
- 정규화 및 표준화

### 📓 **노트북 생성**
- 자동화된 Jupyter 노트북 생성
- 완전한 분석 워크플로우 포함
- 시각화 코드 자동 생성

### 🗺️ **지도 시각화**
- **유연한 매핑 시스템**: 6단계 매칭 전략 (정확한 매칭 → 부분 매칭 → 키워드 매칭)
- **Folium 기반 인터랙티브 지도**: 4개 레이어 시스템
- **색상별 등급 표시**: 각 지수별 고유 색상 팔레트
- **상세한 툴팁 정보**: 지수값, 등급, 라벨 표시
- **특별 매핑**: 세종특별자치시, 부분 단어 매칭, 시도명 정규화

## 📁 파일 구조
```
scripts/
├── create_fixed_integrated_map.py                # 🆕 통합 취약지수 지도 생성 (최신)
├── create_integrated_vulnerability_map.py        # 통합 취약성 지도 생성 (이전 버전)
├── preprocess_sewer_data.py                      # 하수도 데이터 전처리
├── sewer_infrastructure_index.py                 # 하수도 인프라 지수 계산
├── create_housing_vulnerability_notebook.py      # 주거취약지수 분석 노트북 생성
├── create_sewer_infrastructure_notebook.py       # 하수도 인프라 분석 노트북 생성
├── create_housing_vulnerability_map_notebook.py  # 주거취약지수 지도 시각화 노트북 생성
├── create_sewer_map_visualization_notebook.py    # 하수도 인프라 지도 시각화 노트북 생성
└── README.md                                     # 이 파일
```

## 🔗 관련 파일
- **데이터**: `../data/`
- **노트북**: `../notebooks/`
- **결과**: `../results/`
- **문서**: `../docs/`

## ⚠️ 주의사항

### 실행 전 확인사항
1. **Python 환경**: Python 3.8 이상 필요
2. **필수 패키지**: `requirements.txt`의 모든 패키지 설치
3. **데이터 파일**: 원시 데이터 파일들이 `data/raw/`에 존재하는지 확인
4. **경로 설정**: Windows 경로 형식 사용 (`C:\Users\...`)
5. **🆕 통합 지도**: 모든 개별 지도 파일들이 `results/`에 존재하는지 확인

### 오류 해결
```python
# 경로 문제 해결
import os
print("현재 작업 디렉토리:", os.getcwd())

# 파일 존재 여부 확인
file_path = "data/raw/Sewer_Coverage_Rate.csv"
print(f"파일 존재 여부: {os.path.exists(file_path)}")

# 패키지 설치 확인
try:
    import pandas as pd
    import folium
    print("필수 패키지 설치 완료")
except ImportError as e:
    print(f"패키지 설치 필요: {e}")

# 🆕 통합 지도 관련 파일 확인
integrated_files = [
    "results/korea_vulnerability_map.html",
    "results/sewer_infrastructure_map.html", 
    "results/housing_vulnerability_map.html"
]
for file in integrated_files:
    print(f"{file} 존재 여부: {os.path.exists(file)}")
```

## 🆕 최신 업데이트

### 통합 취약지수 지도 시스템 (2025-08-07)
- **새로운 기능**: 4개 레이어 통합 취약지수 지도 시스템
- **개선사항**: 유연한 매핑 시스템, 부분 단어 매칭, 시도명 정규화
- **특별 기능**: 세종특별자치시 매핑, 키워드 기반 매칭
- **성능**: 94.3% 매핑 성공률 달성 (3295개 성공, 200개 실패)
- **매핑 전략**: 6단계 매칭 (정확한 매칭 → 부분 매칭 → 키워드 매칭) 