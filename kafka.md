# Apache Kafka
본 문서는 데브원영DVWY 님의 [아파치 카프카 유튜브 강의](https://www.youtube.com/watch?v=waw0XXNX-uQ&list=PL3Re5Ri5rZmkY46j6WcJXQYRlDRZSUQ1j)를 듣고 정리한 내용이다.


## 1. 아파치 카프카 개요 및 설명

데이터를 전송하는 line이 복잡해져 유지보수가 어려워지는 문제를 해결하기 위해 링크드인에서 내부적으로 개발한 오픈소스이다.

<img src="https://user-images.githubusercontent.com/55284181/123792333-7712d780-d91b-11eb-8810-f12d2a4b828d.PNG" width="600">

- **Source Application**은 Apache kafka에 데이터를 전송한다.
- **Target Application**은 Apache kafka에서 데이터를 가져온다.

<img src="https://user-images.githubusercontent.com/55284181/123792328-75e1aa80-d91b-11eb-9150-8c114724f3c4.PNG" width="600">

- Kafka에는 각종 데이터를 담는 **토픽(topic)** 이 있다.
- **Producer**는 토픽에 데이터를 넣는 역할을 하고, **Consumer**는 토픽에서 데이터를 가져가는 역할을 한다.
- Producer와 Consumer는 라이브러리로 되어 있어서 application에서 구현이 가능하다.


+ Kafka 특징
    - Kafka는 **고가용성(fault tolerant)** 으로서 서버가 이슈가 생기거나, 갑작스럽게 랙(전원이) 내려간다던가 하는 상황에서도 데이터를 손실 없이 복구할 수 있다.
    - **낮은 지연(latency)** 와 **높은 처리량(Throughput)** 을 통해 많은 양의 데이터를 효과적으로 처리할 수 있다.


### 카프카 메시지

카프카의 메시지는 Key(키) 와 Value(값) 으로 구성된다.

+ **Key(키)**
    - 메시지의 키는 **해당 메시지가 카프카 브로커 내부에 저장될 때, 토픽의 어느 파티션에 저장될지 결정할 때 사용**한다.
    - 프로듀서가 메시지를 브로커로 전달할 때, 프로듀서 내부의 파티셔너(Partitioner)가 저장 위치를 결정하는데, 이때 키의 값을 이용하여 연산하고 그 결과에 따라 저장되는 위치를 결정한다.

+ **Value(값)**
    - 메시지의 값은 **메시지가 전달하고자 하는 내용물**을 의미한다.
    - 문자열, json 등 다양한 타입의 값을 보내는 것이 가능하다.
    - 이는 브로커를 통해 메시지가 발행되거나 소비될 때, 메시지 전체가 **직렬화/역직렬화** 되기 때문이다.

- 메시지의 키와 값은 다양한 타입이 될 수 있지만, 특정한 구조인 **스키마(schema)** 를 가진다.
- 이는 Producer가 발행하고 Consumer가 소비할 때 메시지를 적절하게 처리하기 위해 필요하다.


### 카프카 브로커 (Kafka Broker)

<img src="https://user-images.githubusercontent.com/55284181/125157289-15692d80-e1a5-11eb-9b64-99aea8db175c.png" width="500">

- **카프카 브로커**는 **카프카가 설치되어 있는 서버 단위**를 의미한다.
- 일반적으로 '카프카'라고 불리는 시스템을 말한다.
- Producer와 Consumer 사이에서 메시지를 중계하는 역할을 한다.
- 보통 3개 이상의 브로커로 구성하여 사용하는 것을 권장한다.


### Zookeeper

<img src="https://user-images.githubusercontent.com/55284181/125167009-4400fb80-e1d9-11eb-95ea-103ad773dd02.png" width="500">

- 카프카를 구성할 때는 한 대 이상의 주키퍼로 구성된 주키퍼 클러스터와 한 대 이상의 브로커로 구성된 브로커(=카프카) 클러스터로 구성된다.
- **주키퍼(Zookeeper)** 는 **분산 시스템(카프카 브로커)의 여러 가지 메타 정보를 관리**하고, 필요시에는 분산 시스템의 마스터를 선출한다.
- 주키퍼는 디렉터리 형태로 데이터를 저장, 관리한다.



## 2. 카프카 토픽 (Topic)

**Topic**은 **카프카에서 다양한 데이터를 저장하는 공간**으로 파일시스템의 폴더와 유사한 성질을 가진다.
각각의 토픽은 이름을 지정할 수 있으며, 무슨 데이터를 담는지 명확하게 명시하면 유지보수 시 편리하게 관리할 수 있다.

<img src="https://user-images.githubusercontent.com/55284181/125155151-ec42a000-e198-11eb-8a0e-e9a78b76aa0d.jpg" width="600">

- 하나의 토픽은 여러개의 파티션으로 구성되어 있고, 하나의 파티션은 **큐**와 같은 역할을 한다.
- producer는 파티션에 데이터를 차례로 쌓고, 토픽에 consumer가 붙게 되면 데이터를 가장 오래된 순서대로 가져간다.
- 더이상 데이터가 들어오지 않으면 consumer는 또 다른 데이터가 들어올 때까지 기다린다.
- consumer가 토픽 내부의 파티션에서 데이터(record)를 가져가더라도 데이터는 삭제되지 않는다.


+ **토픽에 새로운 consumer가 붙게 되는 경우**

    <img src="https://user-images.githubusercontent.com/55284181/125155153-ecdb3680-e198-11eb-8b3e-8a5b9c1bcab2.jpg" width="600">

    - consumer 그룹이 다르고, auto.offset.reset = earliest 세팅되어 있을 때 토픽에 새로운 consumer가 붙게 되면 다시 0번부터 가져가서 사용할 수 있게 된다.
    - 이처럼 사용될 경우 동일 데이터에 대해 두번 처리할 수 있다.


+ **파티션이 여러개일 경우**

    <img src="https://user-images.githubusercontent.com/55284181/125155154-ed73cd00-e198-11eb-81df-01288aa82a12.jpg" width="600">

    - 데이터가 토픽에 들어갈 때 어느 파티션에 들어갈지 결정하기 위한 key를 지정할 수 있다.
        1. key가 null인 경우 기본 파티셔너 설정을 사용한다면 **round-robin**으로 데이터가 들어갈 파티션이 지정된다.
        2. key가 있고, 기본 파티셔너를 사용할 경우 키의 해시값을 구하고 특정 파티션에 할당된다.

    <img src="https://user-images.githubusercontent.com/55284181/125155155-ed73cd00-e198-11eb-8e04-a7fea89cd70f.jpg" width="600">

    - 파티션 수를 늘릴 수는 있지만, 줄일 수는 없다.
    - 파티션 수가 많아지면 consumer 수가 많아져 데이터 처리를 분산시킬 수 있다.
    - 파티션의 데이터(record)가 삭제되는 타이밍은 옵션에 따라 달라진다.
        - log.retention.ms : 레코드가 저장되는 최대 시간
        - log.retention.byte : 저장되는 레코드의 최대 크기



## 3. 카프카 Broker, Replication, ISR


### Replication과 ISR

<img src="https://user-images.githubusercontent.com/55284181/125170824-e0cc9480-e1eb-11eb-8ef6-888c5d53399b.jpg" width="600">

- **Replication**은 **partition의 복제**를 의미한다.
- Replication 수 = 원본 파티션 1개 + 복제본 파티션 수
- 브로커 개수에 따라서 Replication 수가 제한된다. (브로커 개수 >= replication 수)

<img src="https://user-images.githubusercontent.com/55284181/125170828-e2965800-e1eb-11eb-8be9-0e00da142531.jpg" width="600">

- **Leader partition** : 원본 파티션 1개
- **Follower partition** : 복제본 파티션 (replicated partition)
- **ISR (In Sync Replica)** : Leader partition + Follower partition

+ Replication을 사용하는 이유
    - Replication은 partition의 고가용성을 위해 사용된다.
    - Leader partition이 죽으면 Follower partition이 Leader partition 역할을 승계하게 된다.


### Replication과 ack옵션

Producer가 토픽의 파티션에 데이터를 전달할 때 전달받는 주체가 **Leader partition** 이다.

- ack옵션

    - ack = 0

        <img src="https://user-images.githubusercontent.com/55284181/125170903-49b40c80-e1ec-11eb-9e49-b283a2cb5707.jpg" width="600">

        - 프로듀서는 Leader partition에 데이터를 전송하고 응답값을 받지 않는다.
        - Leader partition에 데이터가 정상적으로 전송됐는지, 그리고 나머지 partition에 정상적으로 복제되었는지 알 수 없고 보장할 수 없다.
        - 속도는 빠르지만 데이터 유실 가능성이 있다.

    - ack = 1

        <img src="https://user-images.githubusercontent.com/55284181/125170906-4ae53980-e1ec-11eb-82bc-58768221a1f5.jpg" width="600">

        - Leader partition에 데이터를 전송하고, 데이터를 정상적으로 받았는지 응답값을 받는다.
        - 나머지 partition에 복제되었는지는 알 수 없다.
        - 데이터 유실 가능성이 있다.

    - ack = all

        <img src="https://user-images.githubusercontent.com/55284181/125170907-4b7dd000-e1ec-11eb-9de1-1a26f59ab3e7.jpg" width="600">

        - Leader partition에 데이터를 전송하고, 데이터를 정상적으로 받았는지 응답값을 받는다.
        - Follower partition에 복제가 잘 이루어졌는지 응답값을 받는다.
        - 데이터 유실은 없다.
        - 0, 1에 비해 확인 절차가 많기 때문에 속도가 현저히 느리다.


+ 적정 Replication 개수
    - Replication 개수가 많아지면 그만큼 브로커의 리소스 사용량도 늘어나게 된다.
    - 카프카에 들어오는 데이터량과 저장시간(retention date)를 고려하여 replication 개수를 정해야 한다.
    - 3개 이상의 브로커를 사용할 때 replication은 3으로 설정하는 것을 추천한다.



## 4. 카프카 Producer

**프로듀서(Producer)** 는 **데이터를 kafka topic에 생산하는 역할**을 한다. 카프카 클라이언트인 Consumer와 Producer를 사용하기 위해서는 아파치 카프카 라이브러리를 추가해야 한다.

- Producer 역할
    - Topic에 전송할 메시지를 생성한다.
    - 특정 Topic으로 데이터를 publish 한다.
    - kafka broker로 데이터를 전송할 때 전송 성공여부를 알 수 있고, 실패할 경우 재시도할 수 있다.


### Producer가 전송한 데이터의 흐름

+ **key = null이고, 파티션이 1개인 경우**

    <img src="https://user-images.githubusercontent.com/55284181/125167545-149fbe00-e1dc-11eb-8b48-5f8409fbccb7.jpg" width="600">

+ **key = null이고, 파티션이 2개인 경우**

    <img src="https://user-images.githubusercontent.com/55284181/125167546-15d0eb00-e1dc-11eb-8c5c-6c206a7699ed.jpg" width="600">

    - 데이터가 round-robin으로 2개의 파티션에 쌓이게 된다.

+ **key가 존재하고, 파티션이 2개인 경우**

    <img src="https://user-images.githubusercontent.com/55284181/125167547-16698180-e1dc-11eb-8370-9e2e9c453ae4.jpg" width="600">

    - "buy"라는 value의 key = 1, "review"라는 value의 key = 2
    - 카프카는 key를 특정한 hash값으로 변경시켜 파티션과 1대1 매칭을 시킨다.
    - 이는 각 파티션에 동일 key의 value만 쌓이도록 한다.

+ **key가 존재하고, 파티션이 3개인 경우**

    <img src="https://user-images.githubusercontent.com/55284181/125167549-17021800-e1dc-11eb-8d41-104ddb0c1855.jpg" width="600">

    - key와 파티션의 매칭이 깨지기 때문에 key와 파티션의 연결은 보장되지 않는다.



## 5. 카프카 Consumer

Consumer 는 **토픽의 파티션에 저장된 데이터를 가져오는 역할**을 한다. 이를 **폴링(polling)** 이라고 한다.

+ Consumer 역할
    - Topic의 partition 으로부터 데이터 polling
    - Partition offset 위치 기록 (commit)
    - Consumer가 여러개일 경우 Consumer group을 통해 병렬처리


### Producer에서 Consumer로 메시지 전달

- **offset**은 **파티션에 들어간 데이터가 가지는 파티션 내에서의 고유한 번호**이다.
- offset은 토픽별로, 파티션별로 별개로 지정된다.
- offset은 Consumer가 데이터를 어느 지점까지 읽었는지 확인하는 용도로 사용된다.

<img src="https://user-images.githubusercontent.com/55284181/125171961-f1800900-e1f1-11eb-8f8e-9c8bb941817a.jpg" width="600">

- Consumer가 데이터를 읽기 시작하면 offset을 **commit**하게 되는데, 이렇게 가져간 내용에 대한 정보는 카프카의 **__consumer_offset** 토픽에 저장한다.
- 중간에 Consumer가 실행이 중지되더라도, offset 정보가 저장되어있기 때문에 Consumer를 재실행하면 데이터의 처리 시점을 복구하여 데이터 처리를 할 수 있다.


### 1개 이상 Consumer로 이루어진 Consumer group

<img src="https://user-images.githubusercontent.com/55284181/125171962-f2189f80-e1f1-11eb-8e4f-d591fd46ef43.jpg" width="600">

- Consumer가 1개일 경우 2개의 파티션에서 데이터를 가져간다.
- Consumer가 2개일 경우 각 Consumer가 각각의 파티션을 할당하여 데이터를 가져가서 처리한다.
- Consumer가 3개 이상일 경우 더이상 할당될 파티션이 없어서 동작하지 않는다.


### 서로 다른 Consumer group

<img src="https://user-images.githubusercontent.com/55284181/125171963-f2b13600-e1f1-11eb-8262-0fa23e2641e1.jpg" width="600">

- 서로 다른 Consumer group에 속한 Consumer들은 다른 consumer group에 영향을 미치지 않는다.
- 이는 __consumer_offset 토픽에는 consumer group별로, 그리고 토픽별로 offset을 나누어 저장하기 때문이다.



## 6. 카프카 개발환경 구축 및 실행

#### Install
- Install jdk

    ```shell
    $ sudo apt install default-jdk
    ```

- Download latest Apache Kafka

    [official download website](https://kafka.apache.org/downloads)

    Please run commands according to your version
    ```shell
    $ wget https://mirror.navercorp.com/apache/kafka/2.8.0/kafka_2.13-2.8.0.tgz
    $ tar xzf kafka_2.13-2.8.0.tgz
    $ sudo mv kafka_2.13-2.8.0 /usr/local/
    ```

#### Run
- Run zookeeper

    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/zookeeper-server-start.sh config/zookeeper.properties
    ```

- Run Kafka

    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/kafka-server-start.sh config/server.properties
    ```

#### Kafka Topic
- Create Topic

    Topic named "bigdata" with 5 partitions and 1 replication
    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/kafka-topics.sh --create --bootstrap-server localhost:9092 --replication-factor 1 --partitions 5 --topic bigdata
    ```
    + --bootstrap-server : kafka 주소
    + --zookeeper : zookeeper 주소
    + --replication-factor : broker에 복사되는 개수 (안정성 증가) 단일서버라면 1개
    + --partitions : partition 개수
    + --topic : topic 이름

- Check Topic list

    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/kafka-topics.sh --list --bootstrap-server localhost:9092
    ```

- Check Topic details

    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/kafka-topics.sh --describe --bootstrap-server localhost:9092 --topic {topic name}
    ```

- Remove Topic

    Add the following to ```./config/server.properties```:
    ```shell
    delete.topic.enable = true
    ```
    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic {topic name}
    ```

#### Exercise
- Run python producing code

    ```shell
    $ python3 kafka_producer.py
    ```

- Check by kafka consumer

    ```shell
    $ cd /usr/local/kafka_2.13-2.8.0/
    $ ./bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic {topic name} --from-beginning
    ```
    + --from-beginning : 처음부터 소비하겠다는 옵션

- Run python consuming code

    ```shell
    $ python3 kafka_consumer.py
    ```




---
##### reference
- [카프카 메시지와 토픽과 파티션](https://always-kimkim.tistory.com/entry/kafka101-message-topic-partition)
- [카프카 브로커](https://always-kimkim.tistory.com/entry/kafka101-broker)
- [How to Install Apache Kafka on Ubuntu 20.04](https://tecadmin.net/how-to-install-apache-kafka-on-ubuntu-20-04/)
- [Kafka 따라해보기 - 1 (설치하기 및 실행하기)](https://hyanghope.tistory.com/548?category=1075240)
- [Kafka 따라해보기 - 2 (Python3로 간단히 code 짜보기)](https://hyanghope.tistory.com/549?category=1075240) - confluent_kafka 모듈 사용
- [Python으로 Kafka에 전송(Producer)하고 가져오기(consumer)](https://needjarvis.tistory.com/607) - kafka 모듈 사용
- [Topic 내의 message 지우는 방법](https://eyeballs.tistory.com/339)
