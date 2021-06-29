# Kafka
본 문서는 데브원영DVWY 님의 [아파치 카프카 유튜브 강의](https://www.youtube.com/watch?v=waw0XXNX-uQ&list=PL3Re5Ri5rZmkY46j6WcJXQYRlDRZSUQ1j)를 듣고 정리한 내용이다.


## 1. 아파치 카프카

- **Source Application**은 Apache kafka에 데이터를 전송한다.

- **Target Application**은 Apache kafka에서 데이터를 가져온다.

![kafka1](https://user-images.githubusercontent.com/55284181/123792333-7712d780-d91b-11eb-8810-f12d2a4b828d.PNG)

- Kafka에는 각종 데이터를 담는 **토픽(topic)**이 있는데 이는 큐 역할을 한다.

- **Producer**와 **Consumer**는 라이브러리로 되어 있어서 application에서 구현이 가능하다.

![kafka2](https://user-images.githubusercontent.com/55284181/123792328-75e1aa80-d91b-11eb-9150-8c114724f3c4.PNG)

- Kafka 특징

    - Kafka는 **고가용성(fault tolerant)**으로서 서버가 이슈가 생기거나, 갑작스럽게 랙(전원이) 내려간다던가 하는 상황에서도 데이터를 **손실 없이 복구**할 수 있다.

    - **낮은 지연(latency)**와 **높은 처리량(Throughput)**을 통해 많은 양의 데이터를 효과적으로 처리할 수 있다.


## 2. 카프카 토픽 (Topic)

- **토픽 (Topic)** : 카프카에서 다양한 데이터를 저장하는 공간

- 각각의 토픽은 이름을 지정할 수 있으며, 무슨 데이터를 담는지 명확하게 명시하면 유지보수 시 편리하게 관리할 수 있다.

![topic1](https://user-images.githubusercontent.com/55284181/123793157-61ea7880-d91c-11eb-9f51-c6bcc5fba1f4.PNG)

- 하나의 토픽은 여러개의 **파티션**으로 구성되어 있고, 하나의 파티션은 **큐**와 같은 역할을 한다.

- producer는 파티션에 데이터를 차례로 추가하고, 토픽에 consumer가 붙게 되면 데이터를 가장 오래된 순서대로 가져간다.

- 더이상 데이터가 들어오지 않으면 consumer는 또 다른 데이터가 들어올때까지 기다린다.

- consumer가 토픽 내부의 파티션에서 데이터를 가져가더라도 데이터는 삭제되지 않는다.

![topic2](https://user-images.githubusercontent.com/55284181/123793154-60b94b80-d91c-11eb-89ba-4e952f6c1785.PNG)