# Docker
Docker는 애플리케이션을 신속하게 구축, 테스트 및 배포할 수 있는 소프트웨어 플랫폼이다.


## 도커 명령어

#### 컨테이너 관련 명령어
- container 조회
    ```shell
    docker ps -a
    ```
- container 접속
    ```shell
    docker exec -it [CONTAINER ID] /bin/bash
    ```
- container 접속 종료
    ```shell
    exit
    ```
- 실행중인 container 종료
    ```shell
    docker stop [CONTAINER ID]
    ```
- 종료된 container 삭제
    ```shell
    docker rm [CONTAINER ID]
    ```
- 현재 실행중인 모든 container 종료
    ```shell
    docker stop $(docker ps -q -f status=running)
    ```
- 종료된 모든 container 삭제
    ```shell
    docker rm $(docker ps -q -f status=exited)
    ```

#### 이미지 관련 명령어
- image 조회
    ```shell
    docker images -a
    ```
- image 정보 출력
    ```shell
    docker inspect [IMAGE ID]
    ```
- image 삭제
    ```shell
    docker rmi [IMAGE ID]
    ```
- 모든 image 삭제 (주의, 다 날라감)
    ```shell
    docker rmi $(docker images -q)
    ```

#### 볼륨 관련 명령어
- volume 조회
    ```shell
    docker volume ls
    ```
- volume 삭제
    ```shell
    docker volume rm [VOLUME NAME]
    ```
- 모든 volume 삭제
    ```shell
    docker volume rm $(docker volume ls -qf dangling=true)
    ```
    
#### 네트워크 관련 명령어
- network 리스트 조회
    ```shell
    docker network ls
    ```
- network 조회
    ```shell
    docker network inspect [NETWORK NAME]
    ```
- network disconnect
    ```shell
    docker network disconnect [NETWORK NAME] [CONTAINER NAME]
    ```
		
---
##### reference
- [docker 자주 사용하는 명령어 정리](http://home.zany.kr:9003/board/bView.asp?bCode=13&aCode=14169)
- [docker container에 접속하기](https://bluese05.tistory.com/21)
- [Docker volume 개념 및 MySql을 Docker상에서 운용하는 방법](https://joonhwan.github.io/2018-11-14-fix-mysql-volume-share-issue/)
- [docker volume 삭제](https://m.blog.naver.com/PostView.naver?isHttpsRedirect=true&blogId=bokmail83&logNo=221871848032)
- [Docker로 MySQL 컨테이너 만들기](https://velog.io/@wimes/Docker%EB%A1%9C-MySQL-%EC%BB%A8%ED%85%8C%EC%9D%B4%EB%84%88-%EB%A7%8C%EB%93%A4%EA%B8%B0)