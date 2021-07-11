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



## 3. Elasticsearch 시스템 구조

### 3-1. 클러스터 구성

Elasticsearch의 노드들은 클라이언트와의 통신을 위한 http 포트(9200~9299), 노드 간의 데이터 교환을 위한 tcp 포트 (9300~9399) 총 2개의 네트워크 통신을 열어두고 있다.

#### 여러 서버에 하나의 클러스터로 실행

- 3개의 다른 물리 서버에서 각각 1개 씩의 노드 실행
    
    <img width="640" alt="cluster1" src="https://user-images.githubusercontent.com/55284181/123535978-97e3fd00-d762-11eb-9e1e-0275c7cabde5.png">

- 서버1 에서 두개의 노드를 실행하고, 서버2 에서 한개의 노드를 실행
    
    <img width="640" alt="cluster2" src="https://user-images.githubusercontent.com/55284181/123536001-bf3aca00-d762-11eb-9b61-afef9e2aa5dc.png">

#### 하나의 서버에서 여러 클러스터 실행

- 하나의 물리 서버에서 서로 다른 두 개의 클러스터 실행
    
    ![cluster3](https://user-images.githubusercontent.com/55284181/123536068-fc9f5780-d762-11eb-8a00-58d644486018.png)

node-1과 node-2는 하나의 클러스터로 묶여있기 때문에 데이터 교환이 일어난다.
하지만 node-3은 클러스터가 다르기 때문에 node-1, node-2와 같은 클러스터로 바인딩 되지 않는다. node-1, node-2에 입력된 데이터를 node-3 에서 읽을 수 없다.

#### 디스커버리 (Discovery)

노드가 처음 실행 될 때 같은 서버의 다른 노드들을 찾아 하나의 클러스터로 바인딩 하는 과정

<img width="640" alt="discovery" src="https://user-images.githubusercontent.com/55284181/123536210-e776f880-d763-11eb-814f-553c1dc81a86.png">


### 3-2. 인덱스와 샤드 - Index & Sards

- **색인 (indexing)** : 데이터를 Elasticsearch에 저장하는 행위
- **도큐먼트 (document)** : 단일 데이터 단위
- **인덱스 (Index)** : 도큐먼트를 모아놓은 집합
- **샤드 (shard)** : 인덱스가 분리되는 단위. 각 노드에 분산되어 저장됨.

#### 프라이머리 샤드(Primary Shard) 와 복제본(Replica)

- 클러스터에 노드를 추가하게 되면 샤드들이 각 노드들로 분산되고 디폴트로 1개의 복제본을 생성한다.
    - 프라이머리 샤드 : 처음 생성된 샤드
    - 리플리카 : 복제본

    ex) 한 인덱스가 5개의 샤드로 구성되어 있고, 한 클러스터가 4개의 노드로 구성되어 있다고 가정한다. 각각 5개의 프라이머리 샤드와 복제본, 총 10개의 샤드들이 4개의 노드에 골고루 분배되어 저장된다.

    <img width="640" alt="shard" src="https://user-images.githubusercontent.com/55284181/123536324-99aec000-d764-11eb-88b2-aee46301171d.png">

- 같은 샤드와 복제본은 동일한 데이터를 담고 있으며 반드시 서로 다른 노드에 저장된다.

    ex) Node-3 노드가 시스템 다운이나 네트워크 단절등으로 사라지면 이 클러스터는 Node-3 에 있던 0번과 4번 샤드들을 유실하게 된다. 클러스터는 유실된 노드가 복구 되기를 기다리다가 타임아웃이 지나면 Elasticsearch는 0번, 4번 샤드들의 복제를 시작한다.

    ![shard2](https://user-images.githubusercontent.com/55284181/123536523-ad0e5b00-d765-11eb-8650-dbec7ccc7672.png)

#### 샤드 개수 설정

- 프라이머리 샤드 수는 인덱스를 처음 생성할 때 지정하며, 인덱스를 재색인 하지 않는 이상 바꿀 수 없다. 복제본의 개수는 나중에 변경이 가능하다.

    ex) 4개의 노드를 가진 클러스터에 프라이머리 샤드 5개, 복제본 1개인 books 인덱스, 그리고 프라이머리 샤드 3개 복제본 0개인 magazines 인덱스가 있을 때 전체 샤드 배치

    ![shard3](https://user-images.githubusercontent.com/55284181/123536675-c5cb4080-d766-11eb-90a8-d13a263f1f0f.png)

#### 샤드의 크기가 어떻게 성능에 영향을 미치나요?
- 용어 정리
    - 리프레쉬(refresh) 작업 : 데이터를 샤드에 입력할 때, Elasticsearch는 주기적으로 디스크에 불변의 루씬 **세그먼트** 형태로 저장(publish)하며, 이 작업 이후에 조회가 가능해진다.

    - 병합(merging) 작업 : 세그먼트의 개수가 많아지면, 주기적으로 더 큰 세그먼트로 병합된다. 병합 작업은 리소스에 무척 민감하며, 특히 디스크 I/O에 큰 영향을 받는다.

    - 큰 샤드는 클러스터 장애가 발생했을 때 복구 능력에 좋지 않은 영향을 끼친다. 샤드 크기는 최대 **50GB**를 넘지 않는 것이 좋다.

- 인덱스 보관 주기
    - 데이터 보관 주기를 관리하기 위하여 **시간 기반 인덱스**를 사용하는 것이 좋다.


### 3-3. 마스터 노드와 데이터 노드 - Master & Data Nodes

#### 마스터 노드 (Master Node)

인덱스의 메타 데이터, 샤드의 위치와 같은 클러스터 상태(Cluster Status) 정보를 관리한다.

기본적으로는 모든 노드가 마스터 노드로 선출될 수 있는 **마스터 후보 노드 (master eligible node)** 이다.

클러스터가 커져서 노드와 샤드들의 개수가 많아지게 되면, 마스터 노드의 역할을 수행 할 후보 노드들만 따로 설정해서 유지하는 것이 전체 클러스터 성능에 도움이 될 수 있다.

#### 데이터 노드 (Data Node)

실제로 색인된 데이터를 저장하고 있는 노드이다.

- 마스터 역할만 실행하는 노드
```
node.master: true
node.data: false
```

- 데이터 처리 역할만 실행하는 노드
```
node.master: false
node.data: true
```

#### Split Brain

네트워크 단절로 마스터 후보 노드가 분리되면 각자의 클러스터에서 데이터 변경이 이루어질 수 있다.
나중에 네트워크가 복구되고 하나의 클러스터로 다시 합쳐지게 되면, 데이터 정합성에 문제가 생기고 데이터 무결성이 유지될 수 없게 된다.
이러한 문제를 **Split Brain** 이라고 한다.

- Split Brain을 방지하기 위해 최소 마스터 후보 노드의 수를 ```(전체 마스터 후보 노드 / 2) + 1``` 개로 설정해야 한다.

- 클러스터 분리 시 마스터 노드가 절반 이상인 클러스터만 생존한다.
    
    ex) 아래의 경우 데이터는 node-4, node-5의 데이터만 사용이 가능하고 node-6은 네트워크가 복구될 때까지 동작하지 않고 노드가 분리되기 이전 상태 그대로 유지된다.

    ![split_brain](https://user-images.githubusercontent.com/55284181/123544798-e0fe7600-d78f-11eb-8d23-379410ff7f8c.png)



---
#### 참조 URL
- <https://17billion.github.io/elastic/2017/06/30/elastic_stack_overview.html>
- <https://www.elastic.co/kr/blog/how-many-shards-should-i-have-in-my-elasticsearch-cluster>
