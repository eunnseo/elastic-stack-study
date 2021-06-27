# Elastic Stack
본 문서는 [Elastic 가이드북](https://esbook.kimjmin.net/) 자료를 공부한 뒤 정리한 내용이다.


## 1. Elastic Stack 소개

- ELK Stack = Elasticsearch + Logstash + Kibana

- ELK Stack에 Beats가 포함되어 **Elastic Stack** 이란 이름으로 현재 서비스가 제공되고 있다.


### 1-1. Elasticsearch

모든 데이터를 색인하여 저장하고 검색, 집계 등을 수행하며 결과를 클라이언트 또는 다른 프로그램으로 전달하여 동작한다.
다양한 플러그인들을 사용해 손쉽게 기능의 확장이 가능하며 아마존 웹 서비스(AWS), 마이크로소프트 애저(MS Azure) 같은 클라우드 서비스 그리고 하둡(Hadoop) 플랫폼들과의 연동도 가능하다.

#### Elasticsearch의 특징
- 오픈소스 (open source) : Elastic 라이센스 + Apache 라이센스
- 실시간 분석 (real-time) : 클러스터가 실행되고 있는 동안 계속해서 데이터가 색인(indexing)되고, 동시에 실시간에 가까운 속도로 색인된 데이터의 검색, 집계가 가능하다.
- 전문 (full text) 검색 엔진 : 역파일 색인(inverted file index) 구조로 데이터를 저장하는 루씬을 사용하여 가공된 텍스트를 검색한다.
- RESTFul API : 모든 데이터 조회, 입력, 삭제를 http 프로토콜을 통해 Rest API로 처리한다.
- 멀티테넌시 (multitenancy) : 인덱스들을 별도의 커넥션 없이 하나의 질의로 묶어서 검색하고, 검색 결과들을 하나의 출력으로 도출할 수 있다.


### 1-2. Logstash

**입력** 기능에서 다양한 데이터 저장소로부터 데이터를 입력 받고, **필터** 기능을 통해 데이터를 확장, 변경, 필터링 및 삭제 등의 처리를 통해 가공한다. 그 후 **출력** 기능을 통해 다양한 데이터 저장소로 데이터를 전송한다.


### 1-3. Kibana

Elasticsearch를 시각화할 수 있는 도구이다.

- **Discover** : Elasticsearch에 색인된 소스 데이터들의 검색을 위한 메뉴
- **Visualize** : aggregation 집계 기능을 통해 조회된 데이터의 통계를 다양한 차트로 표현할 수 있는 패널을 만드는 메뉴
- **Dashboard** : Visualize 메뉴에서 만들어진 시각화 도구들을 조합해서 대시보드 화면을 만들고 저장, 불러오기 등을 할 수 있는 메뉴


### 1-4. Beats

- 데이터를 Logstash 또는 Elasticsearch로 전송하는 도구. Logshash보다 경량화된 서비스이다.
- Go 언어로 개발되었다.
- Packetbeat, Libbeat, Filebeat, Metricbeat, Winlogbeat, Auditbeat 등이 있다. 



## 2. Elasticsearch 시작하기

### 2-1. 데이터 색인

- **색인 (indexing)** : 데이터가 검색될 수 있는 구조로 변경하기 위해 원본 문서를 검색어 토큰들으로 변환하여 저장하는 일련의 과정

- **인덱스 (index, indices)** : 색인 과정을 거친 결과물, 또는 색인된 데이터가 저장되는 저장소. Elasticsearch에서 도큐먼트들의 논리적인 집합을 표한하는 단위

- **검색 (search)** : 인덱스에 들어있는 검색어 토큰들을 포함하고 있는 문서를 찾아가는 과정

- **질의 (query)** : 사용자가 원하는 문서를 찾거나 집계 결과를 출력하기 위해 검색 시 입력하는 검색어 또는 검색 조건

![data-indexing](https://user-images.githubusercontent.com/55284181/123533411-4763a400-d750-11eb-812e-9ce214b52c9d.png)



---
#### 참조 URL
- <https://17billion.github.io/elastic/2017/06/30/elastic_stack_overview.html>
