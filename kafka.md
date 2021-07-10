# Kafka
본 문서는 데브원영DVWY 님의 [아파치 카프카 유튜브 강의](https://www.youtube.com/watch?v=waw0XXNX-uQ&list=PL3Re5Ri5rZmkY46j6WcJXQYRlDRZSUQ1j)를 듣고 정리한 내용이다.


## 1. 아파치 카프카 개요 및 설명

데이터를 전송하는 line이 복잡해져 유지보수가 어려워지는 문제를 해결하기 위해 링크드인에서 내부적으로 개발한 오픈소스이다.

<img src="https://user-images.githubusercontent.com/55284181/125155149-e9e04600-e198-11eb-98de-bc6dd1eb5505.jpg" width="500">

- **Source Application**은 Apache kafka에 데이터를 전송한다.
- **Target Application**은 Apache kafka에서 데이터를 가져온다.

<img src="https://user-images.githubusercontent.com/55284181/123792333-7712d780-d91b-11eb-8810-f12d2a4b828d.PNG" width="500">

- Kafka에는 각종 데이터를 담는 **토픽(topic)** 이 있다.
- **Producer**는 토픽에 데이터를 넣는 역할을 하고, **Consumer**는 토픽에서 데이터를 가져가는 역할을 한다.
- **Producer**와 **Consumer**는 라이브러리로 되어 있어서 application에서 구현이 가능하다.

<img src="https://user-images.githubusercontent.com/55284181/123792328-75e1aa80-d91b-11eb-9150-8c114724f3c4.PNG" width="500">

- Kafka 특징
    - Kafka는 **고가용성(fault tolerant)** 으로서 서버가 이슈가 생기거나, 갑작스럽게 랙(전원이) 내려간다던가 하는 상황에서도 데이터를 **손실 없이 복구**할 수 있다.
    - **낮은 지연(latency)** 와 **높은 처리량(Throughput)** 을 통해 많은 양의 데이터를 효과적으로 처리할 수 있다.



## 2. 카프카 토픽 (Topic)

- **토픽 (Topic)** : 카프카에서 다양한 데이터를 저장하는 공간. 파일시스템의 폴더와 유사한 성질을 가진다.
- 각각의 토픽은 이름을 지정할 수 있으며, 무슨 데이터를 담는지 명확하게 명시하면 유지보수 시 편리하게 관리할 수 있다.

    <img src="https://user-images.githubusercontent.com/55284181/123793157-61ea7880-d91c-11eb-9f51-c6bcc5fba1f4.PNG" width="500">

- 하나의 **토픽**은 여러개의 **파티션**으로 구성되어 있고, 하나의 파티션은 **큐**와 같은 역할을 한다.
- **producer**는 파티션에 데이터를 차례로 쌓고, 토픽에 **consumer**가 붙게 되면 데이터를 가장 오래된 순서대로 가져간다.
- 더이상 데이터가 들어오지 않으면 consumer는 또 다른 데이터가 들어올 때까지 기다린다.
- consumer가 토픽 내부의 파티션에서 데이터를 가져가더라도 데이터는 삭제되지 않는다.
    
    <img src="https://user-images.githubusercontent.com/55284181/125155151-ec42a000-e198-11eb-8a0e-e9a78b76aa0d.jpg" width="500">

- consumer 그룹이 다르고, auto.offset.reset = earliest 세팅되어 있을 때 토픽에 새로운 consumer가 붙게 되면 다시 0번부터 가져가서 사용할 수 있게 된다.
- 이처럼 사용될 경우 동일 데이터에 대해 두번 처리할 수 있다.

    <img src="https://user-images.githubusercontent.com/55284181/125155153-ecdb3680-e198-11eb-8b3e-8a5b9c1bcab2.jpg" width="500">

- 파티션이 여러개일 경우 데이터가 토픽에 들어갈 때 어느 파티션에 들어갈지 결정하기 위한 key를 지정할 수 있다.
    1. key가 null인 경우 기본 파티셔너 설정을 사용한다면 round-robin으로 데이터가 들어갈 파티션이 지정된다.
    2. key가 있고, 기본 파티셔너를 사용할 경우 키의 해시값을 구하고 특정 파티션에 할당된다.

    <img src="https://user-images.githubusercontent.com/55284181/125155154-ed73cd00-e198-11eb-81df-01288aa82a12.jpg" width="500">

- 파티션 수를 늘릴 수는 있지만, 줄일 수는 없다.
- 파티션 수가 많아지면 consumer 수가 많아져 데이터 처리를 분산시킬 수 있다.
- 파티션의 데이터(record)가 삭제되는 타이밍은 옵션에 따라 달라진다.
    - log.retention.ms : 레코드가 저장되는 최대 시간
    - log.retention.byte : 저장되는 레코드의 최대 크기

    <img src="https://user-images.githubusercontent.com/55284181/125155155-ed73cd00-e198-11eb-8e04-a7fea89cd70f.jpg" width="500">
