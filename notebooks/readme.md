# 📓 Jupyter Notebooks 폴더

## 📋 폴더 개요

이 폴더에는 **사회취약지수 산출**을 위한 전처리·지표 계산·시각화 과정을 담은 Jupyter Notebook이 포함되어 있습니다.  
행정동별(법정동코드) 인구 데이터를 정리한 뒤, 아동·고령·외국인·장애인 인구를 이용해 지수를 계산하고 Choropleth 지도까지 생성합니다.  
추가로, 지도 위에 붙는 **Top-10 패널**은 Chart.js 기반으로 현대적인 칩 스타일 시·도 버튼과 수평 막대그래프로 구성되어 있으며, 선택한 지역에 따라 실시간으로 업데이트됩니다.

## 📁 파일 목록

### 1. `사회취약계층.ipynb`

* **파일 크기**: **32 MB** (≈ 53 cells / 320 lines)  
* **생성일**: **2025-07-30**  
* **설명**: 법정동 → 행정동 코드 정규화, 취약계층 인구 집계, 사회취약지수 계산 및 지도 시각화를 수행하는 메인 노트북

#### 📊 분석 내용

1. **데이터 로드 & 정규화**
   * `KIKcd_H.20250714_processed.xlsx` 법정동 코드 → `cd`
   * KOSIS 주민등록인구 (`pop15`, `pop65`, `popFo`, `popDP`) 수집
   * `제1동` → `1동`, `1.2.3가` → `1·2·3가` 패턴 치환

2. **인구 테이블 병합 & 결측 보정**
   * 아동·고령·외국인·장애인 인구를 `total`에 `left join`
   * `총인구 == 0` 행 제거, 결측치 `0` 대체

3. **사회취약지수 계산 (주관 가중합)**
   * 가중치: 고령 0.35 · 아동 0.20 · 장애 0.20 · 외국인 0.25  
   * 각 변수 % 변환 후 가중합 → `vuln_raw`
   * Min-Max 정규화 → `vuln_pct` (0–100 스케일)

4. **데이터 시각화**
   * 취약지수 분포 히스토그램  
   * 상위 20개 동 막대그래프  
   * 변수 간 상관 히트맵  
   * **Folium Choropleth**: 전국 GeoJSON(시도별 파일 병합) 사용  
   * **Top-10 패널**: Chart.js 기반, 칩 스타일 시·도 버튼, active 표시, 수평 막대그래프 실시간 갱신 (기본 ‘전국’). 팝업 너비 확장(≈380px), 캔버스 너비 350으로 가독성 확보.

5. **결과 저장**
   * `results/maps/korea_vulnerability_map.html`

#### 🛠️ 사용된 라이브러리

* **pandas** ‒ 데이터 처리  
* **numpy** ‒ 수치 계산  
* **matplotlib / seaborn** ‒ 정적 시각화  
* **folium** ‒ 인터랙티브 지도  
* **json / glob** ‒ GeoJSON 병합  
* **re / pathlib** ‒ 문자열·경로 처리  
* **Chart.js** (HTML/JS 임베디드) ‒ Top-10 인터랙티브 바차트

#### 🎯 실행 방법

```bash
# Jupyter Notebook 실행
jupyter notebook notebooks/사회취약계층.ipynb

#### 📈 주요 결과

* **최고 취약 동**: ○○동 (취약지수 100)
* **최저 취약 동**: △△동 (취약지수 0)
* **상위 5개 시·도 평균**: 경북 > 전남 > 경남 > 강원 > 전북

#### 💾 생성되는 결과물

* `data/processed/사회취약지수표.csv`: 행정동별 지표
* `results/korea_vulnerability_map.html`: Choropleth 지도

## 🔧 노트북 실행 환경

### 필수 라이브러리

```python
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
folium>=0.14.0
jupyter>=1.0.0
```

### 한글 폰트 설정

```python
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.unicode_minus'] = False
```

## 🚨 주의사항

1. **파일 경로** : 상대 경로 기준 `../data/raw/` 등 확인
2. **GeoJSON 병합** : `data/raw/hangjeongdong_*.geojson` 모두 존재해야 함
3. **인터넷 연결** : Folium 타일 로딩에 필요
4. **폰트** : `ipynb 코드에 적힌 폰트` 제공 필수

## 📞 문제 해결

```python
import os, matplotlib.font_manager as fm
print("CWD:", os.getcwd())
print("Nanum 폰트:", [f.name for f in fm.fontManager.ttflist if 'Nanum' in f.name])
```

## 🚀 최신 업데이트 (2025-07-31)

* **사회취약지수 계산**: 장애인·아동·외국인 인구를 포함한 주관 가중합 지수 도출, Min-Max 정규화로 0–100 스케일 통일  
* **GeoJSON 자동 병합**: 시도별 GeoJSON을 하나의 전국 FeatureCollection으로 합쳐 Choropleth에 적용  
* **결측치 처리 로직 개선**: `총인구 == 0` 행 자동 제거, 누락값은 0으로 대체  
* **Top-10 패널 UI 개선**: Chart.js 기반 수평 막대그래프, 칩 스타일 시도 버튼 (active 강조), 팝업 너비 확장(380px) 및 캔버스 너비 350으로 가독성 향상  