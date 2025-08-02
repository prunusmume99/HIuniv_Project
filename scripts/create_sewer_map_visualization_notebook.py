#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
수도 인프라 지수 지도 시각화 노트북 생성 스크립트

이 스크립트는 사회취약계층.ipynb를 참고하여 수도 인프라 지수를 바탕으로 한 지도 시각화 노트북을 생성합니다.
"""

import json
import os

def create_notebook():
    """노트북 파일 생성"""
    
    notebook_content = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "# 수도 인프라 지수 지도 시각화 노트북\n",
                    "\n",
                    "이 노트북은 하수도 인프라 지수를 바탕으로 전국 행정동 단위 지도 시각화를 수행합니다.\n",
                    "\n",
                    "## 목차\n",
                    "1. [라이브러리 임포트](#1-라이브러리-임포트)\n",
                    "2. [데이터 로드 및 전처리](#2-데이터-로드-및-전처리)\n",
                    "3. [하수도 인프라 지수 계산](#3-하수도-인프라-지수-계산)\n",
                    "4. [지도 데이터 준비](#4-지도-데이터-준비)\n",
                    "5. [지도 시각화](#5-지도-시각화)\n",
                    "6. [결과 저장](#6-결과-저장)"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 1. 라이브러리 임포트"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "import os\n",
                    "import numpy as np\n",
                    "import pandas as pd\n",
                    "import folium\n",
                    "import json\n",
                    "from sklearn.preprocessing import MinMaxScaler\n",
                    "import warnings\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "print(\"라이브러리 임포트 완료\")\n",
                    "print(f\"현재 작업 디렉토리: {os.getcwd()}\")\n",
                    "print(f\"Folium 버전: {folium.__version__}\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 2. 데이터 로드 및 전처리"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 하수도 인프라 데이터 로드\n",
                    "def load_sewer_data():\n",
                    "    \"\"\"하수도 인프라 데이터 로드\"\"\"\n",
                    "    # 상대 경로 사용 (사회취약계층.ipynb 방식)\n",
                    "    file_path = '../data/processed/sewer_infrastructure_processed.csv'\n",
                    "    \n",
                    "    if not os.path.exists(file_path):\n",
                    "        print(f\"데이터 파일을 찾을 수 없습니다: {file_path}\")\n",
                    "        print(\"절대 경로로 시도합니다...\")\n",
                    "        # 절대 경로로 재시도\n",
                    "        project_dir = r\"/Users/sullem/yj/HIuniv_Project\"\n",
                    "        file_path = os.path.join(project_dir, \"data\", \"processed\", \"sewer_infrastructure_processed.csv\")\n",
                    "        if not os.path.exists(file_path):\n",
                    "            print(f\"절대 경로에서도 파일을 찾을 수 없습니다: {file_path}\")\n",
                    "            return None\n",
                    "    \n",
                    "    df = pd.read_csv(file_path, encoding='utf-8')\n",
                    "    print(f\"하수도 인프라 데이터 로드 완료: {len(df)}개 행\")\n",
                    "    return df\n",
                    "\n",
                    "# 데이터 로드\n",
                    "sewer_df = load_sewer_data()\n",
                    "\n",
                    "if sewer_df is not None:\n",
                    "    print(\"\\n데이터 미리보기:\")\n",
                    "    display(sewer_df.head())\n",
                    "    \n",
                    "    print(\"\\n데이터 정보:\")\n",
                    "    print(sewer_df.info())\n",
                    "    \n",
                    "    print(\"\\n기본 통계:\")\n",
                    "    display(sewer_df.describe())\n",
                    "else:\n",
                    "    print(\"데이터 로드에 실패했습니다.\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 3. 하수도 인프라 지수 계산"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "def calculate_infrastructure_index(df):\n",
                    "    \"\"\"하수도 인프라 지수 계산\"\"\"\n",
                    "    # 가중치 설정\n",
                    "    weights = {\n",
                    "        '하수도설치율': 0.3,\n",
                    "        '공공하수처리구역 인구보급률': 0.3,\n",
                    "        '고도처리인구 보급률': 0.2,\n",
                    "        '인구밀도_정규화': 0.2\n",
                    "    }\n",
                    "    \n",
                    "    # 인구 밀도 정규화 (0-100 스케일)\n",
                    "    scaler = MinMaxScaler(feature_range=(0, 100))\n",
                    "    df['인구밀도_정규화'] = scaler.fit_transform(df[['인구밀도']])\n",
                    "    \n",
                    "    # 가중 평균으로 인프라 지수 계산\n",
                    "    df['하수도_인프라_지수'] = (\n",
                    "        df['하수도설치율'] * weights['하수도설치율'] +\n",
                    "        df['공공하수처리구역 인구보급률'] * weights['공공하수처리구역 인구보급률'] +\n",
                    "        df['고도처리인구 보급률'] * weights['고도처리인구 보급률'] +\n",
                    "        df['인구밀도_정규화'] * weights['인구밀도_정규화']\n",
                    "    )\n",
                    "    \n",
                    "    # 지수 등급 분류 (0-25, 25-50, 50-75, 75-100)\n",
                    "    bins = [0, 25, 50, 75, 100]\n",
                    "    df['인프라_등급'] = pd.cut(\n",
                    "        df['하수도_인프라_지수'],\n",
                    "        bins=bins,\n",
                    "        labels=[1, 2, 3, 4],\n",
                    "        include_lowest=True\n",
                    "    )\n",
                    "    \n",
                    "    return df\n",
                    "\n",
                    "if sewer_df is not None:\n",
                    "    # 하수도 인프라 지수 계산\n",
                    "    sewer_df = calculate_infrastructure_index(sewer_df)\n",
                    "    print(f\"하수도 인프라 지수 계산 완료\")\n",
                    "    print(f\"평균 인프라 지수: {sewer_df['하수도_인프라_지수'].mean():.2f}\")\n",
                    "    \n",
                    "    # 결과 확인\n",
                    "    print(\"\\n인프라 지수 분포:\")\n",
                    "    display(sewer_df[['하수도_인프라_지수', '인프라_등급']].describe())\n",
                    "    \n",
                    "    print(\"\\n등급별 분포:\")\n",
                    "    display(sewer_df['인프라_등급'].value_counts().sort_index())\n",
                    "else:\n",
                    "    print(\"데이터가 없어 인프라 지수를 계산할 수 없습니다.\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 4. 지도 데이터 준비"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# 시도별로 분리된 행정동 GeoJSON 파일 경로 정의 (사회취약계층.ipynb 방식)\n",
                    "paths = {\n",
                    "    '세종': '../data/raw/hangjeongdong_세종특별자치시.geojson',\n",
                    "    '경북': '../data/raw/hangjeongdong_경상북도.geojson',\n",
                    "    '강원': '../data/raw/hangjeongdong_강원도.geojson',\n",
                    "    '경기': '../data/raw/hangjeongdong_경기도.geojson',\n",
                    "    '경남': '../data/raw/hangjeongdong_경상남도.geojson',\n",
                    "    '광주': '../data/raw/hangjeongdong_광주광역시.geojson',\n",
                    "    '대전': '../data/raw/hangjeongdong_대전광역시.geojson',\n",
                    "    '대구': '../data/raw/hangjeongdong_대구광역시.geojson',\n",
                    "    '서울': '../data/raw/hangjeongdong_서울특별시.geojson',\n",
                    "    '부산': '../data/raw/hangjeongdong_부산광역시.geojson',\n",
                    "    '인천': '../data/raw/hangjeongdong_인천광역시.geojson',\n",
                    "    '울산': '../data/raw/hangjeongdong_울산광역시.geojson',\n",
                    "    '제주': '../data/raw/hangjeongdong_제주특별자치도.geojson',\n",
                    "    '전북': '../data/raw/hangjeongdong_전라북도.geojson',\n",
                    "    '전남': '../data/raw/hangjeongdong_전라남도.geojson',\n",
                    "    '충남': '../data/raw/hangjeongdong_충청남도.geojson',\n",
                    "    '충북': '../data/raw/hangjeongdong_충청북도.geojson',\n",
                    "}\n",
                    "\n",
                    "# 존재하는 파일만 필터링\n",
                    "existing_paths = {k: v for k, v in paths.items() if os.path.exists(v)}\n",
                    "print(f\"존재하는 GeoJSON 파일 수: {len(existing_paths)}/{len(paths)}\")\n",
                    "\n",
                    "if len(existing_paths) == 0:\n",
                    "    print(\"\\nGeoJSON 파일을 찾을 수 없습니다. 절대 경로로 재시도합니다...\")\n",
                    "    # 절대 경로로 재시도\n",
                    "    project_dir = r\"/Users/sullem/yj/HIuniv_Project\"\n",
                    "    paths = {\n",
                    "        '세종': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_세종특별자치시.geojson'),\n",
                    "        '경북': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_경상북도.geojson'),\n",
                    "        '강원': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_강원도.geojson'),\n",
                    "        '경기': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_경기도.geojson'),\n",
                    "        '경남': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_경상남도.geojson'),\n",
                    "        '광주': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_광주광역시.geojson'),\n",
                    "        '대전': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_대전광역시.geojson'),\n",
                    "        '대구': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_대구광역시.geojson'),\n",
                    "        '서울': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_서울특별시.geojson'),\n",
                    "        '부산': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_부산광역시.geojson'),\n",
                    "        '인천': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_인천광역시.geojson'),\n",
                    "        '울산': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_울산광역시.geojson'),\n",
                    "        '제주': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_제주특별자치도.geojson'),\n",
                    "        '전북': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_전라북도.geojson'),\n",
                    "        '전남': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_전라남도.geojson'),\n",
                    "        '충남': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_충청남도.geojson'),\n",
                    "        '충북': os.path.join(project_dir, 'data', 'raw', 'hangjeongdong_충청북도.geojson'),\n",
                    "    }\n",
                    "    existing_paths = {k: v for k, v in paths.items() if os.path.exists(v)}\n",
                    "    print(f\"절대 경로에서 존재하는 GeoJSON 파일 수: {len(existing_paths)}/{len(paths)}\")\n",
                    "\n",
                    "if len(existing_paths) > 0:\n",
                    "    # 각 파일을 열어 GeoJSON 객체로 로드 (사회취약계층.ipynb 방식)\n",
                    "    geos = []\n",
                    "    for sido, path in existing_paths.items():\n",
                    "        try:\n",
                    "            with open(path, 'r', encoding='utf-8') as f:\n",
                    "                geo = json.load(f)\n",
                    "                geos.append(geo)\n",
                    "                print(f\"{sido}: {len(geo['features'])}개 행정동\")\n",
                    "        except Exception as e:\n",
                    "            print(f\"{sido} 파일 로드 실패: {e}\")\n",
                    "    \n",
                    "    # 모든 feature를 하나의 FeatureCollection으로 합쳐 전국 단위 GeoJSON 생성\n",
                    "    geo_all = {\n",
                    "        \"type\": \"FeatureCollection\",\n",
                    "        \"features\": [f for g in geos for f in g['features']]\n",
                    "    }\n",
                    "    \n",
                    "    print(f\"\\n전국 행정동 수: {len(geo_all['features'])}\")\n",
                    "else:\n",
                    "    print(\"\\nGeoJSON 파일을 찾을 수 없습니다. 다른 방법으로 지도 데이터를 준비합니다.\")\n",
                    "    geo_all = None"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### 데이터 매핑 준비"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if geo_all is not None and sewer_df is not None:\n",
                    "    # 행정동 코드 → 이름 매핑 준비 (GeoJSON의 properties에서 가져옴)\n",
                    "    code2name = {str(f['properties']['adm_cd2']): f['properties']['adm_nm']\n",
                    "                 for f in geo_all['features']}\n",
                    "    \n",
                    "    # sewer_df에 행정동명 컬럼 추가 (매핑 실패하면 NaN)\n",
                    "    sewer_df['행정동명'] = sewer_df['행정동코드'].astype(str).map(code2name)\n",
                    "    \n",
                    "    # 매핑 결과 확인\n",
                    "    print(f\"매핑된 행정동 수: {sewer_df['행정동명'].notna().sum()}/{len(sewer_df)}\")\n",
                    "    \n",
                    "    # sewer_df를 dict 형태로 만들어 빠른 조회용 사전 생성\n",
                    "    data_dict = sewer_df.set_index('행정동코드').to_dict(orient='index')\n",
                    "    \n",
                    "    # 매핑되지 않은 feature에 들어갈 기본값\n",
                    "    empty = {\n",
                    "        '하수도설치율': 0, \n",
                    "        '공공하수처리구역 인구보급률': 0, \n",
                    "        '고도처리인구 보급률': 0, \n",
                    "        '인구밀도': 0,\n",
                    "        '하수도_인프라_지수': 0, \n",
                    "        '인프라_등급': 1\n",
                    "    }\n",
                    "    \n",
                    "    print(\"데이터 매핑 준비 완료\")\n",
                    "else:\n",
                    "    print(\"지도 데이터나 하수도 데이터가 없어 매핑을 건너뜁니다.\")\n",
                    "    data_dict = None"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 5. 지도 시각화"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if geo_all is not None and data_dict is not None:\n",
                    "    # 모든 GeoJSON feature에 sewer_df의 값을 주입하여 속성 보강\n",
                    "    for feat in geo_all['features']:\n",
                    "        c = str(feat['properties']['adm_cd2'])  # 행정동 코드 문자열화\n",
                    "        row = data_dict.get(c)\n",
                    "        if row:\n",
                    "            # 해당 코드가 sewer_df에 있으면 실제 값으로 덮어쓰기\n",
                    "            feat['properties'].update({\n",
                    "                '하수도설치율': row['하수도설치율'],\n",
                    "                '공공하수처리구역 인구보급률': row['공공하수처리구역 인구보급률'],\n",
                    "                '고도처리인구 보급률': row['고도처리인구 보급률'],\n",
                    "                '인구밀도': row['인구밀도'],\n",
                    "                '하수도_인프라_지수': row['하수도_인프라_지수'],\n",
                    "                '인프라_등급': row['인프라_등급'],\n",
                    "            })\n",
                    "        else:\n",
                    "            # 없으면 기본값 채우기\n",
                    "            feat['properties'].update(empty)\n",
                    "    \n",
                    "    print(\"GeoJSON 속성 병합 완료\")\n",
                    "else:\n",
                    "    print(\"지도 데이터나 매핑 데이터가 없어 속성 병합을 건너뜁니다.\")"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if geo_all is not None and sewer_df is not None:\n",
                    "    # 기본 지도 생성: 중앙 위치, 줌 레벨, 라이트한 타일, 축척 표시\n",
                    "    m = folium.Map(location=[36, 127], zoom_start=7,\n",
                    "                   tiles='cartodbpositron', control_scale=True)\n",
                    "    \n",
                    "    # 점수 구간 기준 설정: 0~25, 25~50, 50~75, 75~100\n",
                    "    bins = [0, 25, 50, 75, 100]\n",
                    "    \n",
                    "    # Choropleth 레이어 추가: 하수도 인프라 지수를 컬러로 시각화\n",
                    "    choropleth = folium.Choropleth(\n",
                    "        geo_data=geo_all,  # 병합된 전국 GeoJSON\n",
                    "        data=sewer_df,  # 데이터 프레임\n",
                    "        columns=('행정동코드', '하수도_인프라_지수'),  # 매핑 열\n",
                    "        key_on='feature.properties.adm_cd2',  # GeoJSON 측 속성 키\n",
                    "        fill_color='YlOrRd',  # 색상 팔레트 (노랑-주황-빨강)\n",
                    "        fill_opacity=0.85, line_opacity=0.3, line_weight=0.4,  # 스타일\n",
                    "        nan_fill_color='#f7f7f7',  # 결측 색\n",
                    "        bins=bins, highlight=True,  # 등급 구간 및 하이라이트 활성화\n",
                    "        name='하수도 인프라 지수'  # 레이어 이름 (레이어 컨트롤에 표시)\n",
                    "    ).add_to(m)\n",
                    "    \n",
                    "    # Tooltip 추가 (사회취약계층.ipynb 방식)\n",
                    "    # 각 feature에 tooltip 추가\n",
                    "    for feature in geo_all['features']:\n",
                    "        props = feature['properties']\n",
                    "        tooltip_text = f\"\"\"\n",
                    "        <b>{props.get('adm_nm', 'N/A')}</b><br>\n",
                    "        인프라 지수: {props.get('하수도_인프라_지수', 0):.2f}<br>\n",
                    "        등급: {props.get('인프라_등급', 1)}<br>\n",
                    "        하수도설치율: {props.get('하수도설치율', 0):.1f}%<br>\n",
                    "        공공하수처리구역: {props.get('공공하수처리구역 인구보급률', 0):.1f}%\n",
                    "        \"\"\"\n",
                    "        \n",
                    "        # GeoJSON feature에 tooltip 추가\n",
                    "        folium.GeoJson(\n",
                    "            feature,\n",
                    "            tooltip=folium.Tooltip(\n",
                    "                tooltip_text,\n",
                    "                style=\"background-color: rgba(255,255,255,0.9);\"\n",
                    "                       \"border:1px solid #999;border-radius:3px;\"\n",
                    "                       \"box-shadow:2px 2px 6px rgba(0,0,0,0.15);\"\n",
                    "                       \"font-size:12px;padding:4px;\"\n",
                    "            )\n",
                    "        ).add_to(m)\n",
                    "    \n",
                    "    # 레이어 컨트롤 추가\n",
                    "    folium.LayerControl(collapsed=False).add_to(m)\n",
                    "    \n",
                    "    print(\"지도 생성 완료!\")\n",
                    "    display(m)\n",
                    "else:\n",
                    "    print(\"지도 데이터나 하수도 데이터가 없어 지도를 생성할 수 없습니다.\")\n",
                    "    print(\"\\n대안: 구 단위 지도 시각화를 시도해보세요.\")\n",
                    "    print(\"1. SIG.geojson 파일이 있는지 확인\")\n",
                    "    print(\"2. geo/SIG.geojson 경로 확인\")\n",
                    "    print(\"3. 다른 지도 시각화 방법 사용\")"
                ]
            },
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "## 6. 결과 저장"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "if 'm' in locals():\n",
                    "    # 결과물을 HTML 파일로 저장\n",
                    "    # 상대 경로로 저장 시도\n",
                    "    map_file = '../results/sewer_infrastructure_emd_map.html'\n",
                    "    \n",
                    "    # 디렉토리가 없으면 생성\n",
                    "    os.makedirs(os.path.dirname(map_file), exist_ok=True)\n",
                    "    \n",
                    "    m.save(map_file)\n",
                    "    \n",
                    "    print(f\"지도 저장 완료: {map_file}\")\n",
                    "    \n",
                    "    # 분석 결과 요약\n",
                    "    if sewer_df is not None:\n",
                    "        print(\"\\n=== 분석 결과 요약 ===\")\n",
                    "        print(f\"전체 행정동 수: {len(sewer_df)}\")\n",
                    "        print(f\"평균 하수도 인프라 지수: {sewer_df['하수도_인프라_지수'].mean():.2f}\")\n",
                    "        print(f\"최고 하수도 인프라 지수: {sewer_df['하수도_인프라_지수'].max():.2f}\")\n",
                    "        print(f\"최저 하수도 인프라 지수: {sewer_df['하수도_인프라_지수'].min():.2f}\")\n",
                    "        \n",
                    "        print(\"\\n등급별 분포:\")\n",
                    "        grade_dist = sewer_df['인프라_등급'].value_counts().sort_index()\n",
                    "        for grade, count in grade_dist.items():\n",
                    "            percentage = (count / len(sewer_df)) * 100\n",
                    "            print(f\"등급 {grade}: {count}개 ({percentage:.1f}%)\")\n",
                    "        \n",
                    "        print(\"\\n상위 10개 행정동:\")\n",
                    "        top_10 = sewer_df.nlargest(10, '하수도_인프라_지수')[['시도', '행정구역명', '하수도_인프라_지수', '인프라_등급']]\n",
                    "        display(top_10)\n",
                    "        \n",
                    "        print(\"\\n하위 10개 행정동:\")\n",
                    "        bottom_10 = sewer_df.nsmallest(10, '하수도_인프라_지수')[['시도', '행정구역명', '하수도_인프라_지수', '인프라_등급']]\n",
                    "        display(bottom_10)\n",
                    "else:\n",
                    "    print(\"지도가 생성되지 않아 저장할 수 없습니다.\")"
                ]
            }
        ],
        "metadata": {
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
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook_content

def main():
    """메인 함수"""
    print("=== 수도 인프라 지수 지도 시각화 노트북 생성 ===")
    
    # 노트북 내용 생성
    notebook_content = create_notebook()
    
    # 노트북 파일 저장
    project_dir = r"/Users/sullem/yj/HIuniv_Project"
    notebook_file = os.path.join(project_dir, "notebooks", "04_sewer_infrastructure_map_visualization.ipynb")
    
    with open(notebook_file, 'w', encoding='utf-8') as f:
        json.dump(notebook_content, f, ensure_ascii=False, indent=1)
    
    print(f"노트북 파일 생성 완료: {notebook_file}")
    print("이제 주피터 노트북에서 파일을 열어서 실행할 수 있습니다!")

if __name__ == "__main__":
    main() 