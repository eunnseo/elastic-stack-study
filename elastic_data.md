# Elastic Stack
본 문서는 [Elastic 가이드북](https://esbook.kimjmin.net/) 자료를 공부한 뒤 정리한 내용이다.


## 4. Elasticsearch 데이터 처리

### 4-1. REST API

- 데이터 처리
    - 입력 : ```PUT http://user.com/kim -d {"name":"kim", "age":38, "gender":"m"}```

    - 조회 : ```GET http://user.com/kim```

    - 삭제 : ```DELETE http://user.com/kim```

- 유닉스 기반 운영체제에서는 **curl** 명령어로 간편하게 REST API 사용이 가능하다.

- Kibana Dev Tools
    - ```bin/kibana```를 실행시키면 디폴트로 같은 호스트위 **localhost:9200**에서 실행중인 elasticsearch와 통신하며 실행된다.

    - 기본적으로 Kibana는 5601 포트에서 실행된다.

    ![kibana_dev_tools](https://user-images.githubusercontent.com/55284181/123591966-9af4f100-d827-11eb-8c96-9b3dbb6e0cf5.png)

### 4-1. CRUD - 입력, 조회, 수정, 삭제

- Elasticsearch에서는 단일 도큐먼트별로 고유한 URL을 갖는다.

- 도큐먼트에 접근하는 URL : ```http://<호스트>:<포트>/<인덱스>/_doc/<도큐먼트 id>```

#### 입력 (PUT)

- **PUT** 메서드로 데이터를 입력하낟.

- my_index/_doc/1 최초 입력
    ```javascript
    // request
    PUT my_index/_doc/1
    {
        "name":"Jongmin Kim",
        "message":"안녕하세요 Elasticsearch"
    }

    // response
    {
        ...
        "result" : "created"
        ...
    }
    ```
    
- my_index/_doc/1 재입력

    - **_doc**을 사용하여 동일한 URL에 다른 내용의 도큐먼트를 재입력하게 되면 기존 도큐먼트는 삭제되고 새로운 도큐먼트로 덮어씌워지게 된다.

    ```javascript
    // request
    PUT my_index/_doc/1
    {
        "name":"Jongmin Kim",
        "message":"안녕하세요 Kibana"
    }

    // response
    {
        ...
        "result" : "updated"
        ...
    }
    ```

- _doc 대신 _create 로 새 도큐먼트 입력

    - **_create**을 사용하면 기존 도큐먼트가 덮어씌워지는 것을 방지하고 새로운 도큐먼트의 입력만 허용하는 것이 가능하다.

    - 입력하려는 도큐먼트 id에 이미 데이터가 있는 경우 입력 오류가 발생한다.

    ```javascript
    // request
    PUT my_index/_create/1
    {
        "name":"Jongmin Kim",
        "message":"안녕하세요 Elasticsearch"
    }

    // response
    {
        ...
        "error"
        ...
    }
    ```

#### 조회 (GET)

- **GET** 메서드로 가져올 도큐먼트의 URL을 입력하면 도큐먼트의 내용을 가져온다.

- my_index/_doc/1 도큐먼트 조회

    - 문서의 내용은 **_source** 항목에 나타난다.

    ```javascript
    // request
    GET my_index/_doc/1

    // response
    {
        "_index" : "my_index",
        "_type" : "_doc",
        "_id" : "1",
        "_version" : 4,
        "_seq_no" : 3,
        "_primary_term" : 1,
        "found" : true,
        "_source" : {
            "name" : "Jongmin Kim",
            "message" : "안녕하세요 Kibana"
        }
    }
    ```

#### 삭제 (DELETE)

- **DELETE** 메서드를 이용해서 도큐먼트 또는 인덱스 단위의 삭제가 가능하다.

- my_index/_doc/1 도큐먼트 삭제

    - 도큐먼트 내용은 삭제되었지만 인덱스는 남아있는 상태가 된다.

    ```javascript
    // request
    DELETE my_index/_doc/1

    // response
    {
        ...
        "result" : "deleted"
        ...
    }
    ```

    - 인덱스는 있으나 도큐먼트가 없을 때 도큐먼트를 GET해서 가져오려고 하면 도큐먼트를 못 찾았다는 ```"found" : false``` 응답을 받는다.

- my_index 인덱스 전체 삭제

    - 전체 인덱스가 삭제된다.

    ```javascript
    // request
    DELETE my_index

    // response
    {
        ...
        "acknowledged" : true
        ...
    }
    ```

    - 삭제된 인덱스 또는 처음부터 없는 인덱스의 도큐먼트를 조회하려고 하면 ```"type" : "index_not_found_exception" , "status" : 404``` 오류가 리턴된다.

#### 수정 (POST)

- **POST** 메서드는 PUT 메서드와 유사하게 데이터 입력에 사용이 가능하다.

- POST 명령으로 my_index/_doc 도큐먼트 입력

    - ```<인덱스>/_doc``` 까지만 입력하게 되면 자동으로 임의의 도큐먼트id 가 생성된다.

    ```javascript
    // request
    POST my_index/_doc
    {
        "name":"Jongmin Kim",
        "message":"안녕하세요 Elasticsearch"
    }

    // response
    {
        ...
        "_id" : "ZuFv12wBspWtEG13dOut",
        "result" : "created"
        ...
    }
    ```

#### _update

- ```POST <인덱스>/_update/<도큐먼트 id>``` 명령을 이용해 원하는 필드의 내용만 업데이트가 가능하다.

- my_index/_update/1 도큐먼트의 message 필드 업데이트

    - _update API 를 사용해서 단일 필드만 수정하는 경우에도 실제로 내부에서는 도큐먼트 전체 내용을 가져와서 _doc 에서 지정한 내용을 변경한 새 도큐먼트를 만든 뒤 전체 내용을 다시 PUT 으로 입력하는 작업을 진행한다.

    ```javascript
    // request
    POST my_index/_update/1
    {
        "doc": {
            "message":"안녕하세요 Kibana"
        }
    }

    // response
    {
        ...
        "_version" : 2,
        "result" : "updated"
        ...
    }
    ```


### 4-3. 벌크 API

- 여러 명령을 배치로 수행하기 위해서 **_bulk API**의 사용이 가능하다.

- _bulk API로 **index, create, update, delete**의 동작이 가능하다.

    <img width="640" alt="bulk" src="https://user-images.githubusercontent.com/55284181/123597974-f8d90700-d82e-11eb-9584-2774691479e1.png">


- 벌크 명령을 json 파일로 저장하고 **curl** 명령으로 실행시킬 수 있다.

- 다음 명령으로 bulk.json 파일에 있는 내용들을 _bulk 명령으로 실행 가능하다.

    ```shell
    curl -XPOST "http://localhost:9200/_bulk" -H 'Content-Type: application/json' --data-binary @bulk.json
    ```


### 4-4. 검색 API

- 검색은 **인덱스 단위**로 이루어진다.

- ```GET <인덱스명>/_search``` 형식으로 사용하며 쿼리를 입력하지 않으면 전체 도큐먼트를 찾는 **match_all** 검색을 한다.

#### URI 검색

- _search 뒤에 q 파라미터를 사용해서 검색어를 입력하는 방식이다.

    형식 : ```GET test/_search?q=<검색어>```

    - URI 검색으로 test 인덱스에서 검색어 "value" 검색

        ```javascript
        // request
        GET test/_search?q=value

        // response
        {
            ...
            "hits" : {
                "total" : {
                    "value" : 2,
                    "relation" : "eq"
                },
                "max_score" : 0.105360515,
                "hits" : [
                    {
                        "_index" : "test",
                        "_type" : "_doc",
                        "_id" : "3",
                        "_score" : 0.105360515,
                        "_source" : {
                            "field" : "value three"
                        }
                    },
                    {
                        "_index" : "test",
                        "_type" : "_doc",
                        "_id" : "1",
                        "_score" : 0.105360515,
                        "_source" : {
                            "field" : "value two"
                        }
                    }
                ]
            }
        }
        ```

    - **hits.total.value** : 검색 결과 전체에 해당되는 문서의 개수 표시

    - **hits:[ ]** : 가장 **정확도(relevancy)**가 높은 문서 10개 표시

- 여러 가지 검색어를 **AND, OR, NOT** 조건으로 검색이 가능하다.

    형식 : ```GET test/_search?q=<검색어> <조건> <검색어>```

- 검색어 value 을 field 필드에서 찾고 싶으면 ```<필드명>:<검색어>``` 형태로 검색이 가능하다.

    형식 : ```GET test/_search?q=<필드명>:<검색어>```

#### 데이터 본문 (Data Body) 검색

- 검색 쿼리를 데이터 본문으로 입력하는 방식이다.

- **match 쿼리**를 사용하여 "field" 필드에서 검색어 "value" 검색

- query 지정자로 시작 -> match 쿼리 지정 -> <필드명>:<검색어> 방식으로 입력

    ```javascript
    GET test/_search
    {
        "query": {
            "match": {
                "field": "value"
            }
        }
    }
    ```

#### 멀티테넌시 (Multitenancy)

- 여러 개의 인덱스를 한꺼번에 묶어서 검색하는 방식이다.

- 예를 들어, logs-2018-01, logs-2018-02 … 와 같이 날짜별로 저장된 인덱스들이 있다면 이 인덱스들을 모두 ```logs-*/_search``` 명령으로 한꺼번에 검색이 가능하다.

    ```javascript
    // 쉼표로 나열해서 여러 인덱스 검색
    GET logs-2018-01,2018-02,2018-03/_search

    // 와일드카드 * 를 이용해서 여러 인덱스 검색
    GET logs-2018-*/_search
    ```

- **_all**은 시스템 사용을 위한 인덱스 같은 곳의 데이터까지 접근하여 불필요한 작업 부하를 초래하므로 _all 은 되도록 사용하지 않는 것이 좋다.





## 6. 데이터 색인과 텍스트 분석

### 6-1. 역 인덱스 - Inverted Index

- **역 인덱스**는 책의 맨 뒤에 있는 주요 키워드에 대한 내용이 몇 페이지에 있는지 볼 수 있는 찾아보기 페이지에 비유할 수 있습니다.

- Elasticsearch에서는 추출된 각 키워드를 **텀(term)** 이라고 부른다.

- 역 인덱스를 데이터가 저장되는 과정에서 만들기 때문에 Elasticsearch는 데이터를 입력할 때 저장이 아닌 **색인**을 한다고 표현한다.

    <img width="640" alt="inverted_index" src="https://user-images.githubusercontent.com/55284181/123575354-848d6c00-d80c-11eb-83a9-691ae64c1730.png">

### 6-2. 텍스트 분석 - Text Analysis

- Elasticsearch에 저장되는 도큐먼트는 모든 **문자열(text)** 필드 별로 역 인덱스를 생성한다.

- **텍스트 분석 (Text Analysis)** : 문자열 필드가 저장될 때 데이터에서 검색어 토큰을 저장하기 위해 거치는 여러 단계의 처리 과정

- **애널라이저 (Analyzer)** : 텍스트 분석을 처리하는 기능. 캐릭터 필터 (0~3개) -> 토크나이저 (1개) -> 토큰필터 (0~n개)

    <img width="640" alt="analyzer" src="https://user-images.githubusercontent.com/55284181/123585803-c0c9c800-d81e-11eb-8889-4e986d79b90b.png">

    1. **캐릭터 필터 (Character Filter)** : 텍스트 데이터가 입력되면 가장 먼저 필요에 따라 전체 문장에서 특정 문자를 대치하거나 제거하는 과정을 담당하는 기능

    2. **토크나이저 (Tokenizer)** : 문장에 속한 단어들을 텀 단위로 하나씩 분리해 내는 처리 과정을 담당하는 기능

    3. **토큰 필터 (Token Filter)** : 분리된 텀 들을 하나씩 가공하는 과정을 담당하는 기능
        - ```lowercase``` 토큰 필터를 이용하여 대문자를 모두 소문자로 바꿔준다. 이렇게 하면 대소문자 구별 없이 검색이 가능하게 된다.
        - ```stop``` 토큰 필터를 이용하면 텀 중에서 검색어로서의 가치가 없는 단어들인 **불용어(stopword)**를 검색어 토큰에서 제외시킨다.
        - 영어에서는 ```snowball  ``` 토큰 필터를 이용하여 문법상 변형된 단어를 일반적으로 검색에 쓰이는 기본 형태로 변환하여 검색이 가능하게 한다.
        - ```synonym``` 토큰 필터를 사용하여 동의어를 추가해줄 수 있다.

