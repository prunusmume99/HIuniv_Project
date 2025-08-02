# 📓 Notebooks

이 폴더는 프로젝트의 Jupyter 노트북들을 포함합니다.

## 📋 노트북 목록

### 🔍 **분석 노트북**

#### 1. `01_housing_vulnerability_analysis.ipynb`
- **목적**: 주거취약지수 분석 및 계산
- **기능**:
  - 노후주택비율 데이터 로드
  - 주거취약지수 정규화 계산
  - 취약등급 분류 (매우 높음, 높음, 보통, 낮음, 매우 낮음)
  - 결과를 `results/housing_vulnerability_analysis.csv`로 저장
- **입력**: `data/processed/processed_data.csv`
- **출력**: `results/housing_vulnerability_analysis.csv`

#### 2. `02_sewer_infrastructure_analysis.ipynb`
- **목적**: 하수도 인프라 분석 및 지수 계산
- **기능**:
  - 하수도 관련 데이터 로드 및 전처리
  - 하수도 인프라 지수 계산 (가중치 기반)
  - 인프라 등급 분류 (높음, 보통, 낮음, 매우 낮음)
  - 결과를 `data/processed/sewer_infrastructure_analysis.csv`로 저장
- **입력**: `data/raw/Sewer_Coverage_Rate.csv`
- **출력**: `data/processed/sewer_infrastructure_analysis.csv`

### 🗺️ **지도 시각화 노트북**

#### 3. `03_sewer_infrastructure_map_visualization.ipynb`
- **목적**: 하수도 인프라 지수를 지도에 시각화
- **기능**:
  - GeoJSON 파일과 하수도 인프라 데이터 매핑
  - 최강화된 매칭 시스템 (10단계 매칭 전략)
  - Folium을 사용한 인터랙티브 지도 생성
  - 색상별 인프라 등급 표시
  - 상세한 툴팁 정보 제공
- **입력**: 
  - `data/processed/sewer_infrastructure_analysis.csv`
  - `data/raw/*.geojson` 파일들
- **출력**: `results/sewer_infrastructure_map.html`

#### 4. `04_housing_vulnerability_map_visualization.ipynb`
- **목적**: 주거취약지수를 지도에 시각화
- **기능**:
  - GeoJSON 파일과 주거취약지수 데이터 매핑
  - 최강화된 매칭 시스템 (10단계 매칭 전략)
  - Folium을 사용한 인터랙티브 지도 생성
  - 색상별 취약등급 표시
  - 상세한 툴팁 정보 제공
- **입력**: 
  - `results/housing_vulnerability_analysis.csv`
  - `data/raw/*.geojson` 파일들
- **출력**: `results/housing_vulnerability_map.html`

## 🚀 사용 방법

### 환경 설정
```bash
# 필요한 패키지 설치
pip install -r ../requirements.txt

# Jupyter 노트북 실행
jupyter notebook
```

### 실행 순서
1. **데이터 분석**: `01_housing_vulnerability_analysis.ipynb` → `02_sewer_infrastructure_analysis.ipynb`
2. **지도 시각화**: `03_sewer_infrastructure_map_visualization.ipynb` → `04_housing_vulnerability_map_visualization.ipynb`

## 📊 주요 기능

### 🔧 **최강화된 매칭 시스템**
- 정확한 매칭
- 정규화된 매칭
- 접미사 제거 매칭
- 공백 제거 매칭
- 특수문자 제거 매칭
- 부분 매칭
- 유사도 기반 매칭
- 단어 기반 매칭
- 부분 문자열 매칭
- 평균값 폴백

### 🎨 **색상 체계**
- **하수도 인프라**: 빨강(매우 낮음) → 주황(낮음) → 노랑(보통) → 파랑(높음)
- **주거취약지수**: 빨강(매우 높음) → 주황(높음) → 노랑(보통) → 연두(낮음) → 파랑(매우 낮음)

### 📈 **데이터 처리**
- 안전한 데이터 타입 변환
- NaN 값 처리
- 정규화 및 표준화
- 등급 분류

## 📁 파일 구조
```
notebooks/
├── 01_housing_vulnerability_analysis.ipynb      # 주거취약지수 분석
├── 02_sewer_infrastructure_analysis.ipynb       # 하수도 인프라 분석
├── 03_sewer_infrastructure_map_visualization.ipynb  # 하수도 인프라 지도 시각화
├── 04_housing_vulnerability_map_visualization.ipynb # 주거취약지수 지도 시각화
└── README.md                                    # 이 파일
```

## 🔗 관련 파일
- **데이터**: `../data/`
- **결과**: `../results/`
- **스크립트**: `../scripts/`
- **문서**: `../docs/` 