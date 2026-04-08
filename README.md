# AI-SW 개발 워크스테이션 구축

## 1. 프로젝트 개요

본 과제의 목표는 macOS(iMac) 환경에서 터미널 기본 조작, 파일 권한, Docker 설치 및 운영, Dockerfile 기반 커스텀 이미지 제작, 포트 매핑, 바인드 마운트와 볼륨 영속성, Git/GitHub 연동까지 하나의 개발 워크스테이션 구축 흐름으로 직접 수행하고 증명하는 것이다.

이번 수행에서는 다음을 확인하였다.

- 터미널 기본 명령어와 권한 변경 실습
- Docker 설치 및 기본 동작 확인
- `docker run hello-world` 실행 성공
- Ubuntu 컨테이너 실행 및 내부 명령 수행
- NGINX 기반 커스텀 이미지 빌드 및 웹 서버 실행
- 포트 매핑을 통한 브라우저 접속 확인
- 바인드 마운트 실시간 반영 확인
- Docker Volume 영속성 검증
- Git 설정 및 로컬 저장소 초기화
- Docker Compose 기반 단일/멀티 컨테이너 실행
- Compose 운영 명령어(`up`, `down`, `ps`, `logs`) 실습
- 환경 변수 주입을 통한 설정 변경 학습
- GitHub SSH 키 인증 방식 이해

---

## 2. 실행 환경

- OS: macOS (iMac)
- Shell: zsh
- Container Runtime: OrbStack
- Docker Version: 28.5.2
- Docker Compose Version: v2.40.3
- Git: 로컬 저장소 초기화 및 커밋 수행

### 점검 명령

```bash
docker --version
docker info
git --version
```

### 확인 요약

- Docker CLI 정상 동작
- Docker Engine(OrbStack) 정상 구동
- Compose 플러그인 사용 가능
- Git 로컬 저장소 관리 가능

---

## 3. 수행 항목 체크리스트

| 항목 | 수행 여부 | 비고 |
|---|---|---|
| 터미널 기본 명령 실습 | 완료 | `pwd`, `ls -la`, `cd`, `touch`, `mkdir`, `cp`, `mv`, `rm` |
| 파일/디렉토리 권한 변경 | 완료 | `chmod 644`, `chmod 755` |
| Docker 설치 점검 | 완료 | `docker --version`, `docker info` |
| Docker 기본 운영 명령 | 완료 | `docker ps`, `docker ps -a`, `docker logs` 확인 |
| hello-world 실행 | 완료 | 실행 로그 포함 |
| Ubuntu 컨테이너 실행 | 완료 | 내부 진입 및 기본 명령 수행 |
| Dockerfile 커스텀 이미지 | 완료 | `my-nginx` 빌드 및 실행 |
| 포트 매핑 접속 증거 | 완료 | `8080`에서 확인 |
| 바인드 마운트 반영 | 완료 | `8081`에서 실시간 반영 확인 |
| Docker 볼륨 영속성 | 완료 | `8082`에서 삭제 전/후 비교 |
| Git 설정 | 완료 | `git config --list`, `git init`, `git commit` |
| GitHub/VSCode 연동 증거 | 실행해서 보여주기 가능 |  
| Docker Compose 단일 실행 | 완료 | `docker compose up -d` 확인 |
| Docker Compose 멀티 컨테이너 | 완료 | 보조 서비스 포함 실행 확인 |
| Compose 운영 명령어 | 완료 | `up`, `down`, `ps`, `logs` 실습 |
| 환경 변수 활용 | 설명 포함 | 실행화면 보이기 가능 |
| GitHub SSH 키 설정 | 설명 포함 | 등록되어있는거 깃허브에서 확인 가능|

> **주의:** 현재 대화와 업로드 자료 기준으로 작성했다. GitHub/VSCode 로그인 연동 캡처, `docker stats`, Ubuntu 내부 실행 로그, 환경 변수 적용 로그, SSH 연결 테스트 로그가 필요하다면 마지막에 추가하면 된다.

---

## 4. 프로젝트 디렉토리 구조와 설계 기준

### 4-1. 디렉토리 구조 예시

```text
ia-codyssey/
├── Dockerfile
├── README.md
├── compose.yaml
├── app/
│   └── index.html
└── README/
    └── (캡처 이미지들)
```

### 4-2. 어떤 기준으로 이렇게 구성했는가

이번 디렉토리 구성 기준은 아래 4가지였다.

1. **역할 분리**
   - 루트에는 `Dockerfile`, `compose.yaml`, `README.md`처럼 실행과 문서의 기준 파일을 둔다.
   - `app/`에는 NGINX가 서빙할 웹 파일을 둔다.
   - `README/`에는 문서용 증빙 이미지만 둔다.

2. **재현 가능성**
   - 다른 사람이 저장소를 열어도 “어느 폴더에서 어떤 명령을 실행해야 하는지” 바로 알 수 있게 하였다.
   - 예를 들어 프로젝트 루트에서 `docker build -t my-nginx .`를 실행하면 빌드가 가능하다.

3. **수정 편의성**
   - 바인드 마운트 실습 시 `app/index.html`만 수정하면 바로 컨테이너 반영 여부를 확인할 수 있도록 했다.
   - Compose 실습 시 `compose.yaml`과 `.env`만 수정하면 설정 변경 여부를 확인할 수 있도록 했다.

4. **제출 정리성**
   - README 본문, 실행 파일, Compose 설정, 캡처 증빙을 섞지 않고 분리하여 채점자가 구조를 이해하기 쉽게 구성하였다.

### 4-3. 왜 이런 구조가 좋은가

이 구조는 “문서”, “실행 코드”, “설정 파일”, “캡처 증빙”이 서로 섞이지 않으므로 관리가 쉽다. 또한 Docker 실습에서는 현재 작업 디렉토리가 매우 중요하므로, 폴더 역할을 명확히 나누면 빌드 경로 오류나 잘못된 파일 복사 문제를 줄일 수 있다.

---

## 5. 기본 터미널 명령어 및 파일 조작 실습

### 5-1. 작업 폴더 생성과 이동

```bash
cd Desktop
mkdir ai-sw-workstation
cd ai-sw-workstation
pwd
ls -la
```

### 5-2. 실습한 명령

- `pwd` : 현재 위치 확인
- `ls`, `ls -la`, `ls -1` : 파일 목록 확인
- `touch` : 빈 파일 생성
- `mkdir` : 디렉토리 생성
- `cp` : 파일 복사
- `mv` : 파일 이동/이름 변경
- `rm` : 파일 삭제
- `chmod` : 권한 변경

### 관련 로그

```bash
user@macbook Desktop % mkdir ai-sw-workstation
user@macbook Desktop % cd ai-sw-workstation
user@macbook ai-sw-workstation % pwd
~/Desktop/ai-sw-workstation
user@macbook ai-sw-workstation % touch README.md
user@macbook ai-sw-workstation % mkdir practice
user@macbook ai-sw-workstation % touch test.txt
user@macbook ai-sw-workstation % cp test.txt copy.txt
user@macbook ai-sw-workstation % mv copy.txt moved.txt
user@macbook ai-sw-workstation % rm moved.txt
user@macbook ai-sw-workstation % chmod 644 test.txt
user@macbook ai-sw-workstation % chmod 755 practice
```

### 5-3. 실수와 오류 관찰

```bash
user@macbook ai-sw-workstation % pwn
zsh: command not found: pwn

user@macbook ai-sw-workstation % ls-la
zsh: command not found: ls-la

user@macbook ai-sw-workstation % mv copy.txt moved.txt
mv: copy.txt: No such file or directory
```

이 과정을 통해 쉘은 명령어와 옵션을 공백 단위로 구분하므로, `ls-la`처럼 붙여 쓰면 다른 명령어로 인식된다는 점을 확인하였다.

---

## 6. 파일 권한 실습과 권한 숫자 표기 해석

리눅스/유닉스 계열 운영체제(macOS 포함)에서는 모든 파일과 디렉토리에 대해 “누가 읽을 수 있는지, 누가 수정할 수 있는지, 누가 실행하거나 접근할 수 있는지”를 권한(permission)으로 관리한다. 즉, 권한은 특정 파일이나 폴더를 사용자별로 어디까지 사용할 수 있는지 정하는 규칙이다.

### 6-1. 권한 의미

- `r` : read, 읽기
- `w` : write, 쓰기
- `x` : execute, 실행

#### 파일에서의 권한 의미
- `r` : 파일 내용을 읽을 수 있음
- `w` : 파일 내용을 수정할 수 있음
- `x` : 파일을 프로그램처럼 실행할 수 있음

#### 디렉토리에서의 권한 의미
- `r` : 디렉토리 안의 목록을 볼 수 있음
- `w` : 디렉토리 안에 파일을 생성, 삭제, 이름 변경할 수 있음
- `x` : 디렉토리 내부로 들어가거나 내부 파일에 접근할 수 있음

### 6-2. 755, 644는 어떻게 해석되는가

권한 숫자는 **소유자(owner) / 그룹(group) / 기타 사용자(others)** 순서이며, 각 숫자는 아래 값의 합으로 계산한다.


기본 개념 -2진수 비트 개념.
 
- 'r = 100'
- 'w = 010'
- 'x = 001'

- `r = 4`
- `w = 2`
- `x = 1`

예를 들어,

- `rwx = 4 + 2 + 1 = 7`
- `rw- = 4 + 2 + 0 = 6`
- `r-x = 4 + 0 + 1 = 5`
- `r-- = 4 + 0 + 0 = 4`

따라서 다음과 같이 해석할 수 있다.

- `755 = 7 / 5 / 5 = rwx / r-x / r-x`
- `644 = 6 / 4 / 4 = rw- / r-- / r--`

### 6-3. 왜 `test.txt`에는 644가 적절한가

`test.txt`는 실행이 목적이 아닌 일반 텍스트 파일이다. 따라서 이 파일은 “읽기”와 “수정”이 중요하지, “실행”이 필요하지 않다.

### 6-4. 왜 `practice` 디렉토리에는 755가 적절한가

디렉토리는 내부로 들어가고, 내부 목록을 보고, 내부 파일에 접근해야 한다. 이때 디렉토리에서는 `x` 권한이 매우 중요하다.

### 6-5. 실습 로그가 의미하는 바

```bash
user@macbook ai-sw-workstation % chmod 644 test.txt
user@macbook ai-sw-workstation % chmod 755 practice
```

### 6-6. `ls -l`로 보면 어떻게 보이는가

```bash
-rw-r--r--  1 user  staff   0 Apr  5  test.txt
drwxr-xr-x  1 user  staff   0 Apr  5  practice
```

### 6-7. 왜 파일 1개와 디렉토리 1개를 따로 실습하는가

같은 `chmod` 명령을 써도 파일과 디렉토리에서 `x`의 의미가 다르기 때문이다.

- 파일에서 `x`는 “실행 가능”
- 디렉토리에서 `x`는 “내부 진입 및 접근 가능”

---

## 7. 절대 경로와 상대 경로의 차이

### 7-1. 절대 경로

절대 경로는 루트 또는 홈 기준으로 파일의 전체 위치를 끝까지 적는 방식이다.

예:
```bash
~/Desktop/ai-sw-workstation/web/index.html
```

### 7-2. 상대 경로

상대 경로는 현재 작업 디렉토리를 기준으로 적는 방식이다.

.    현재 폴더
..   상위 폴더
~    내 홈폴더

예:
```bash
./web/index.html
./README/1000013376.jpg
```

### 7-3. 어떤 상황에서 무엇을 선택했는가

- **바인드 마운트 실행 시**: 절대 경로 또는 홈 기준 경로 사용
- **README 이미지 연결 시**: 상대 경로 사용
- **현재 폴더에서 Docker 이미지 빌드 시**: 상대 경로인 `.` 사용

즉, 시스템이 현재 위치와 무관하게 정확한 경로를 알아야 하면 절대 경로가 유리하고, 프로젝트 내부 참조나 문서 링크는 상대 경로가 더 관리하기 쉽다.

---

## 8. Docker 설치 및 기본 점검

### 8-1. 점검 명령

```bash
docker --version
docker info
```

### 8-2. 확인 내용

- Docker CLI 정상 동작
- buildx, compose 플러그인 사용 가능
- OrbStack 기반으로 Docker Engine 구동 중

### 관련 로그

```bash
user@macbook ai-sw-workstation % docker --version
Docker version 28.5.2, build ecc6942
```

---

## 9. `docker run hello-world` 실행 확인

Docker가 정상적으로 설치되어 있고, Docker Hub에서 이미지를 내려받아 컨테이너를 실행할 수 있는지 확인하기 위해 `hello-world` 이미지를 실행하였다.

### 실행 명령

```bash
docker run hello-world
```

### 관련 로그

```bash
user@macbook ~ % docker run hello-world
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
4f55086f7dd0: Pull complete
Digest: sha256:452a468a4bf985040037cb6d5392410206e47db9bf5b7278d281f94d1c2d0931
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.
```

### 평가 및 해석

이 로그를 통해 아래를 확인할 수 있다.

- Docker 클라이언트가 Docker 데몬과 정상적으로 통신하였다.
- 로컬에 이미지가 없었기 때문에 Docker Hub에서 `hello-world` 이미지를 내려받았다.
- 이미지를 기반으로 새 컨테이너를 생성하고 실행하였다.
- 실행 결과가 정상적으로 터미널에 출력되었다.

---

## 10. Docker 기본 운영 명령과 관찰 내용

### 10-1. 대표 운영 명령

```bash
docker images
docker ps
docker ps -a
docker logs my-web
docker stats
```

### 10-2. 실제 확인된 일부 로그

```bash
user@macbook web % docker ps
CONTAINER ID   IMAGE      COMMAND                   CREATED          STATUS         PORTS                                     NAMES
0bcb3989c52a   my-nginx   "/docker-entrypoint.…"   10 seconds ago   Up 7 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web
```

### 10-3. 운영 명령이 필요한 이유

- `docker images` : 어떤 이미지가 준비되어 있는지 확인
- `docker ps`, `docker ps -a` : 현재 실행 중/종료된 컨테이너 확인
- `docker logs` : 컨테이너가 왜 실패했는지 추적
- `docker stats` : CPU/메모리 사용량 등 자원 상태 확인

즉, Docker는 “실행만 하는 도구”가 아니라 “상태를 관찰하고 문제를 진단하는 운영 도구”이기도 하다.

---

## 11. Ubuntu 컨테이너 실행과 attach/exec 관찰

### 11-1. 목적

`hello-world`는 아주 짧게 실행되고 종료되는 테스트 이미지다. 반면 Ubuntu 컨테이너는 사용자가 직접 내부 셸에 들어가 명령을 실행하면서 컨테이너 구조를 관찰할 수 있다.

### 11-2. 예시 명령

```bash
docker run -it ubuntu bash
ls
echo "ubuntu container test"
exit
```

### 11-3. attach / exec 차이 정리

- `docker run -it ubuntu bash`
  - 새 컨테이너를 만들고 바로 내부 셸에 진입한다.
- `docker attach <container>`
  - 이미 실행 중인 컨테이너의 기본 프로세스에 다시 붙는다.
- `docker exec -it <container> bash`
  - 실행 중인 컨테이너 안에 새로운 셸 프로세스를 추가로 실행한다.

### 11-4. 관찰 포인트

- 기본 프로세스가 종료되면 컨테이너도 같이 종료될 수 있다.
- `exec`는 이미 실행 중인 컨테이너를 유지한 채 별도의 작업을 추가하기에 유리하다.
- `attach`는 기존 프로세스 자체에 연결되므로 조작에 주의가 필요하다.

---

## 12. 기존 베이스 이미지를 활용한 커스텀 이미지 제작

이번 과제에서는 웹 서버 베이스 이미지 방식(A)을 선택하였다.

- 선택한 기존 베이스 이미지: `nginx:latest`
- 선택 이유: 별도 웹 서버 설치 없이 정적 HTML 배포 구조를 빠르게 실습할 수 있음

### 12-1. HTML 파일

이번 실습에서는 `app/index.html` 파일을 작성하여 NGINX 기본 페이지 대신 사용자 정의 페이지가 출력되도록 구성하였다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>🚀 Hello Docker</h1>
  <p>AI-SW 개발 워크스테이션 과제 페이지</p>
</body>
</html>
```

### 12-2. Dockerfile

```dockerfile
FROM nginx:latest
COPY app/index.html /usr/share/nginx/html/index.html
```

### 12-3. 빌드 및 실행 명령

```bash
docker build -t my-nginx .
docker run -d -p 8080:80 --name my-web my-nginx
docker ps
curl http://localhost:8080
docker exec -it my-web cat /usr/share/nginx/html/index.html
docker logs my-web
```

### 12-4. 결과 요약

- `my-nginx` 이미지 빌드 성공
- `my-web` 컨테이너 실행 성공
- 호스트 `8080` 포트를 통해 브라우저 또는 `curl`로 HTML 응답 확인
- `app/index.html`이 컨테이너 내부 `index.html`로 정상 복사됨

---

## 13. 이미지와 컨테이너의 차이: 빌드 / 실행 / 변경 관점

### 13-1. 이미지란 무엇인가

이미지는 컨테이너를 만들기 위한 설계도이자 실행 템플릿이다. `Dockerfile`을 바탕으로 `docker build`를 수행하면 이미지가 만들어진다.

### 13-2. 컨테이너란 무엇인가

컨테이너는 이미지를 기반으로 실제로 실행되는 인스턴스이다. `docker run` 명령을 통해 이미지가 실제 프로세스로 동작하기 시작하면 그것이 컨테이너이다.

### 13-3. 빌드 관점에서의 차이

- 이미지: `docker build`의 결과물
- 컨테이너: `docker run`의 결과물

### 13-4. 실행 관점에서의 차이

- 이미지는 혼자서는 동작하지 않는다.
- 컨테이너는 포트를 열고 프로세스를 실행하며, 로그를 남기고, 종료 상태를 가진다.

### 13-5. 변경 관점에서의 차이

- 이미지 변경:
  - `Dockerfile`이나 복사 대상 파일을 수정한 뒤 **재빌드**해야 반영된다.
- 컨테이너 변경:
  - 실행 중인 컨테이너 내부 파일을 직접 수정하면 즉시 바뀔 수 있다.
  - 하지만 컨테이너를 삭제하면 그 변경이 사라질 수 있다.

### 13-6. 비유

- 이미지 = 붕어빵 틀
- 컨테이너 = 실제로 구워진 붕어빵
- 볼륨 = 붕어빵을 따로 보관하는 상자

---

## 14. 포트 매핑이 필요한 이유와 내부 포트에 직접 접속할 수 없는 이유

NGINX는 컨테이너 내부에서 `80` 포트를 사용한다. 하지만 그 `80` 포트는 컨테이너 내부 네트워크에 존재하므로, 호스트의 브라우저가 직접 접근할 수 없다.

예:
```bash
docker run -d -p 8080:80 --name my-web my-nginx
```

의 의미는 다음과 같다.

- 호스트의 `8080` 포트로 들어온 요청을
- 컨테이너 내부의 `80` 포트로 전달한다.

즉, 포트 매핑은 **외부 접근 경로를 만들어 주는 다리** 역할을 한다.

### 왜 호스트 포트를 80이 아니라 8080, 8081, 8082, 8083으로 나눴는가

- `8080` : 기본 웹 서버 컨테이너
- `8081` : 바인드 마운트 실험
- `8082` : 볼륨 영속성 실험
- `8083` : Compose 보너스 과제

이렇게 나누면 어떤 접속 결과가 어떤 실험에 대응하는지 즉시 구분할 수 있고, 여러 컨테이너를 동시에 실행해도 충돌을 줄일 수 있다.

---

## 15. 포트/볼륨 설정을 재현 가능하게 정리한 방식

### 15-1. 포트 재현 표

| 용도 | 호스트 포트 | 컨테이너 포트 | 실행 명령 핵심 |
|---|---:|---:|---|
| 기본 웹 서버 | 8080 | 80 | `docker run -d -p 8080:80 --name my-web my-nginx` |
| 바인드 마운트 | 8081 | 80 | `docker run -d --name my-web-bind -p 8081:80 -v ... nginx` |
| 볼륨 영속성 | 8082 | 80 | `docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx` |
| Compose | 8083 | 80 | `docker compose up -d` |

### 15-2. 볼륨 재현 정보

- 볼륨 이름: `my-nginx-data`
- 연결 위치: `/usr/share/nginx/html`
- 검증 방법:
  1. 볼륨 연결 컨테이너 실행
  2. 컨테이너 내부에 `index.html` 작성
  3. 브라우저 또는 `curl`로 확인
  4. 컨테이너 삭제
  5. 같은 볼륨을 새 컨테이너에 재연결
  6. 이전 파일이 그대로 남아 있는지 확인

### 15-3. 왜 이렇게 정리했는가

- 포트는 실험마다 충돌 없이 독립적으로 검증하려고 고정 번호를 부여하였다.
- 볼륨은 이름과 마운트 위치를 문서화해, 다른 사람이 그대로 따라 해도 같은 결과를 낼 수 있게 했다.
- 결과적으로 이 문서는 “실행기록”이면서 동시에 “재현 절차서” 역할을 한다.

---

## 16. 바인드 마운트 실습

### 16-1. 실행 명령

```bash
docker rm -f my-web-bind
docker run -d --name my-web-bind -p 8081:80 -v $(pwd)/app:/usr/share/nginx/html nginx
docker ps
```

### 16-2. 수정 후 반영한 HTML

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>바인드 마운트 실시간 반영 성공</h1>
  <p>파일을 수정하면 컨테이너에 바로 반영됩니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
```

### 16-3. 결과

- `8081` 포트에서 컨테이너 실행 성공
- 로컬 `app/index.html`을 수정하자 컨테이너의 페이지도 즉시 변경됨
- 이미지 재빌드 없이 변경 사항이 반영되었다는 점에서 개발 중 수정 확인에 유리함

### 바인드 마운트가 필요한 이유

바인드 마운트는 호스트 파일을 직접 연결하기 때문에 HTML, CSS, 설정 파일 등을 수정하면서 매번 이미지를 다시 빌드하지 않아도 된다. 즉, **개발 중 빠른 수정-확인 반복**에 적합하다.

---

## 17. Docker Volume 영속성 실습

### 17-1. 볼륨 생성

```bash
docker volume create my-nginx-data
docker volume ls
```

### 17-2. 볼륨 연결 컨테이너 실행

```bash
docker rm -f my-web-volume
docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
docker ps
```

### 17-3. 컨테이너 내부에 HTML 작성

```bash
docker exec -it my-web-volume sh -c 'cat > /usr/share/nginx/html/index.html << "EOF"
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Docker Volume Test</title>
</head>
<body>
  <h1>볼륨 영속성 성공</h1>
  <p>컨테이너를 삭제해도 이 페이지는 남습니다.</p>
  <p>작성자: 최대한</p>
</body>
</html>
EOF'
```

### 17-4. 삭제 전/후 검증 순서

```bash
curl http://127.0.0.1:8082
docker rm -f my-web-volume
docker run -d --name my-web-volume2 -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
curl http://127.0.0.1:8082
```

### 17-5. 결과 해석

처음 컨테이너에서 작성한 `index.html`이 컨테이너 삭제 후에도 새 컨테이너에서 그대로 확인되었다면, 데이터가 컨테이너가 아니라 볼륨에 저장되었다는 뜻이다. 이것이 바로 영속성이다.

---

## 18. Git 설정 및 로컬 저장소 초기화

### 18-1. 사용자 정보 설정

```bash
git config --global user.name "최대한"
git config --global user.email "dahan9819@skuniv.ac.kr"
git config --global --list
```

### 18-2. 저장소 초기화 및 커밋

```bash
cd ~/Desktop/ai-sw-workstation
git init
git status
git add .
git commit -m "Initial commit"
```

### 18-3. Git과 GitHub의 차이

- **Git**: 내 컴퓨터에서 파일 변경 이력을 관리하는 도구
- **GitHub**: Git 저장소를 원격으로 올려 백업 및 협업하는 플랫폼

즉, Git은 **로컬 버전 관리**, GitHub는 **원격 협업 플랫폼**이라고 볼 수 있다.

---

## 19. Docker Compose 기초

Docker Compose는 여러 컨테이너의 실행 설정을 YAML 파일에 문서처럼 정리해 두고, `docker compose up` 명령 한 번으로 실행할 수 있게 해주는 도구이다.  
즉, 원래 터미널에서 길게 입력하던 `docker run` 옵션들을 파일에 적어 두고 재사용 가능하게 만드는 방식이라고 이해할 수 있다.

### 19-1. 단일 컨테이너 Compose 예시

```yaml
services:
  web:
    image: nginx:latest
    container_name: compose-nginx
    ports:
      - "8083:80"
    volumes:
      - ./app:/usr/share/nginx/html
```

### 19-2. 기본 구조 해석

- `services` : 실행할 컨테이너들의 묶음
- `web` : 서비스 이름
- `image` : 어떤 이미지로 만들지 지정
- `container_name` : 컨테이너 이름 지정
- `ports` : 내 컴퓨터 포트와 컨테이너 포트를 연결
- `volumes` : 로컬 `app` 폴더를 NGINX html 경로와 연결

즉, 위 설정은 `web`이라는 이름의 서비스를 `nginx:latest` 이미지로 만들고,  
호스트의 `8083` 포트를 컨테이너의 `80` 포트에 연결하며, 로컬 HTML 파일을 바로 반영하도록 구성한 것이다.

### 19-3. 실행 및 확인 명령

```bash
docker compose up -d
docker compose ps
curl localhost:8083
```

### 19-4. 왜 필요한가

기존에는 아래처럼 긴 실행 명령을 직접 입력해야 했다.

```bash
docker run -d -p 8083:80 -v $(pwd)/app:/usr/share/nginx/html nginx
```

하지만 Compose를 사용하면 이미지, 포트, 볼륨 같은 실행 조건을 파일로 남길 수 있다.  
즉, **명령어 한 줄짜리 실행이 문서화된 실행 설정으로 바뀌는 것**이 핵심이다.

### 19-5. 배움 포인트

- 실행 옵션을 파일로 남겨 재현성을 높일 수 있다.
- 같은 환경을 다시 쉽게 실행할 수 있다.
- 실행 방식 자체가 문서가 되므로 유지보수에 유리하다.

---

## 20. Docker Compose 멀티 컨테이너

Compose를 이용하여 웹 서버와 보조 서비스 2개 이상을 함께 실행하는 구조를 실습하였다.  
이번에는 NGINX 웹 서버와 간단한 echo 서비스를 함께 구성하여 멀티 컨테이너 환경을 확인하였다.

### 20-1. compose.yaml

```yaml
services:
  web:
    image: nginx:latest
    container_name: compose-nginx
    ports:
      - "8083:80"
    volumes:
      - ./app:/usr/share/nginx/html
    depends_on:
      - echo

  echo:
    image: hashicorp/http-echo
    container_name: compose-echo
    command: ["-text=hello from echo container"]
    ports:
      - "5678:5678"
```

### 20-2. 확인 방법

```bash
docker compose up -d
docker compose ps
curl localhost:8083
curl localhost:5678
```

- `8083`에서는 사용자 정의 HTML 페이지가 출력되었다.
- `5678`에서는 `hello from echo container` 응답이 확인되었다.

### 20-3. 이 구조의 의미

이 구조의 장점은 컨테이너를 역할별로 분리할 수 있다는 것이다.

- `web` : 화면 제공
- `echo` : 보조 응답 서비스 제공

즉, 하나의 컨테이너에 모든 기능을 몰아넣는 것이 아니라,  
**각 기능을 독립된 서비스로 나눠 구성하는 감각**을 익히는 것이 중요하다.

### 20-4. 컨테이너 간 네트워크 통신

Compose는 기본적으로 하나의 네트워크를 자동 생성하고, 같은 프로젝트 안의 서비스들이 그 네트워크에 함께 들어가도록 해준다.  
따라서 각 컨테이너는 IP 주소 대신 서비스 이름을 통해 서로를 찾을 수 있다.

### 20-5. 배움 포인트

- 하나의 애플리케이션이 여러 서비스로 분리될 수 있음을 이해하였다.
- Compose가 서비스 간 네트워크를 자동으로 구성함을 확인하였다.
- 멀티 컨테이너 구성을 실제로 실행하고 검증하였다.

---

## 21. Compose 운영 명령어 실습

Compose의 주요 운영 명령어를 사용하여 실행, 종료, 상태 확인, 로그 확인을 수행하였다.  
이 항목은 단순히 “컨테이너를 띄울 수 있다”보다 더 중요한데, 이유는 **지금 상태가 어떤지 확인하는 습관**이 훨씬 실무적이기 때문이다.

### 21-1. 사용 명령어

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

### 21-2. 각 명령의 의미

#### `docker compose up`
Compose 파일을 읽고 필요한 서비스들을 생성하고 실행한다.  
처음 시작할 때 쓰는 핵심 명령이다.

#### `docker compose down`
실행 중인 서비스와 관련 네트워크 등을 정리하면서 종료한다.  
즉, “실습이 끝났으니 깨끗하게 치운다”에 해당한다.

#### `docker compose ps`
현재 어떤 서비스가 떠 있는지, 어떤 포트가 연결되어 있는지 상태를 확인한다.  
이 명령은 “사이트가 왜 안 열리지?” 할 때 가장 먼저 확인하는 명령이라고 볼 수 있다.

#### `docker compose logs`
컨테이너 내부에서 나온 로그를 확인한다.  
즉, 웹 서버가 에러를 냈는지, DB가 정상 기동했는지, 환경 변수 적용이 됐는지 등을 파악하는 데 필수다.

### 21-3. 왜 중요한가

이 과제에서 진짜 배우는 것은 단순한 명령어 암기가 아니라 **운영 루틴**이다.  
문제가 생기면 보통 아래 순서로 확인하게 된다.

1. `docker compose up -d` 로 실행
2. `docker compose ps` 로 실행 상태 확인
3. 안 되면 `docker compose logs` 확인
4. 정리할 때 `docker compose down`

즉, **실행 → 상태 확인 → 로그 확인 → 종료** 흐름을 몸에 익히는 것이 핵심이다.

### 21-4. 배움 포인트

- Compose 환경을 운영 관점에서 관리하는 흐름을 익혔다.
- 실행 여부, 포트 상태, 에러 로그를 확인하는 습관을 배웠다.
- 상태 확인 루틴을 통해 문제 해결 능력을 높일 수 있음을 알게 되었다.

---

## 22. 환경 변수 활용

Dockerfile 또는 Compose 파일에서 환경 변수를 주입하여 포트나 실행 모드를 변경하는 실습을 수행하였다.  
이 단계의 핵심은 프로그램 코드를 직접 수정하지 않고도, **실행 시점의 설정만 바꾸는 방법**을 배우는 데 있다.

```

### 22-3. 왜 중요한가

환경 변수를 쓰는 이유는 **설정과 코드를 분리하기 위해서**다.

예를 들면:

- 개발 환경에선 `MODE=dev`
- 배포 환경에선 `MODE=prod`
- 포트도 상황에 따라 `8080`, `8081`, `3000` 등으로 바꿀 수 있음

즉, 코드는 그대로 두고 설정만 바꾸면 되기 때문에 훨씬 유연하다.

### 22-4. 설정과 코드의 분리

이 실습의 핵심은 프로그램 동작 조건을 코드 안에 박아두지 않고,  
실행 환경에서 바꿀 수 있게 만드는 것이다.

예를 들어 같은 이미지라도:

- 어떤 환경에서는 개발 모드로 실행하고
- 다른 환경에서는 배포 모드로 실행하고
- 또 다른 환경에서는 포트만 다르게 열 수 있다

이것이 실무에서 말하는 **환경별 설정 관리의 기초**다.

### 22-5. 배움 포인트

- 프로그램 동작 조건을 코드에 하드코딩하지 않고 관리할 수 있다.
- 실행 환경에 따라 다른 설정을 줄 수 있다.
- 같은 이미지라도 환경 변수만 다르게 주면 다른 방식으로 실행 가능하다.
- 설정과 코드의 분리 개념을 이해하였다.

---

## 23. GitHub SSH 키 설정

GitHub에 HTTPS 대신 SSH 방식으로 푸시할 수 있도록 SSH 키를 생성하고 등록하는 과정을 학습하였다.  
이 단계는 GitHub에 코드를 올릴 때 **인증 방식을 SSH로 바꾸는 작업**이라고 볼 수 있다.

### 23-1. 기본 흐름

1. 기존 키 확인
2. 새 SSH 키 생성
3. `ssh-agent`에 등록
4. GitHub 계정에 공개키 등록
5. 연결 테스트
6. 저장소 원격 주소를 HTTPS 대신 SSH 주소로 설정

### 23-2. 예시 명령

```bash
ssh-keygen -t ed25519 -C "dahan9819@skuniv.ac.kr"
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
pbcopy < ~/.ssh/id_ed25519.pub
ssh -T git@github.com
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
git push -u origin main
```

### 23-3. HTTPS와 SSH 차이

#### HTTPS
- 원격 주소가 보통 `https://...`
- 인증 시 토큰이나 자격 증명 필요
- 브라우저 로그인 흐름과 비슷해서 처음에는 익숙함

#### SSH
- 원격 주소가 보통 `git@github.com:...`
- 공개키/개인키 방식 사용
- 설정 후에는 반복 인증이 더 편하다

### 23-4. 왜 중요한가

SSH는 공개키/개인키 쌍을 사용해 인증한다.

- 공개키는 GitHub에 등록
- 개인키는 내 컴퓨터에 안전하게 보관

여기에 passphrase까지 걸면 개인키 유출 위험을 더 줄일 수 있다.  
즉, 이 과제의 핵심은 단순히 “푸시 성공”이 아니라,  
**더 자동화되고 안전한 인증 방식을 이해하고 세팅하는 것**이다.

### 23-5. 보안 습관과 연결되는 이유

이 항목에서 배우는 핵심은 다음과 같다.

- 인증 방식이 여러 가지 있다는 것
- 더 자동화되고 안전한 방식으로 개발 환경을 세팅할 수 있다는 것
- 개인키는 절대 공유하면 안 된다는 기본 보안 습관

즉, SSH 설정은 단순 연결 설정이 아니라 **개발자의 인증/보안 습관**과도 연결되는 중요한 실습이다.

### 23-6. 보안 주의사항

- 공개키는 GitHub에 등록해도 되지만,
- 개인키는 절대 외부에 공유하면 안 된다.
- 가능하면 passphrase를 설정하여 보안을 강화하는 것이 좋다.


## 24. 트러블슈팅 

### 트러블슈팅 1. VSCode 터미널이 아니라 macOS 기본 터미널을 사용해 작업 위치를 혼동함

- **문제**  
  처음에는 VSCode 내부 터미널에서 작업한다고 생각했지만, 실제로는 macOS 기본 터미널에서 명령어를 입력하고 있었다. 이 때문에 현재 어느 폴더에서 작업 중인지, 프로젝트 폴더 안에서 실행하고 있는지 혼동이 생겼다.

- **조치**  
  `pwd`, `ls`, `cd` 명령어를 사용해 현재 작업 디렉토리를 다시 확인하였다. 이후에는 반드시 프로젝트 폴더(`ia-codyssey`)로 이동한 뒤 Docker와 Git 명령어를 실행하도록 작업 순서를 정리하였다.

- **결과**  
  작업 위치를 명확히 파악한 뒤에는 파일 생성, Docker 실행, Git 저장 과정이 훨씬 안정적으로 진행되었고, 경로 관련 혼동도 줄어들었다.

- **배운 점**  
  터미널 종류 자체보다 더 중요한 것은 **현재 작업 디렉토리를 정확히 확인하는 습관**이라는 점을 배웠다. 같은 명령어라도 어느 위치에서 실행하느냐에 따라 결과가 달라질 수 있기 때문에, 실습 전 현재 경로를 먼저 확인하는 것이 중요하다.

---

### 트러블슈팅 2. 포트 매핑 과정에서 HTML 파일 경로를 Dockerfile에 올바르게 작성하지 못함

- **문제**  
  NGINX 기반 커스텀 이미지를 빌드하는 과정에서 HTML 파일이 컨테이너 내부에 정상적으로 복사되지 않아, 원하는 페이지가 뜨지 않거나 빌드가 실패하는 문제가 발생하였다.

- **조치**  
  처음에는 HTML 파일 경로를 정확히 반영하지 못했지만, 프로젝트 폴더 구조를 다시 확인한 뒤 Dockerfile에서 HTML 파일의 상대경로를 올바르게 수정하였다. 예를 들어 `app/index.html` 파일을 사용하므로 다음과 같이 작성하였다.

  ```dockerfile
  COPY app/index.html /usr/share/nginx/html/index.html
  
- **결과**  
Docker 이미지가 정상적으로 빌드되었고, 컨테이너 실행 후 브라우저와 curl localhost:8080 명령으로 원하는 HTML 페이지가 정상 출력되는 것을 확인하였다.

- **배운 점**  
Dockerfile의 COPY 명령은 단순히 파일 이름만 쓰는 것이 아니라 빌드 컨텍스트 기준 상대경로를 정확히 작성해야 한다는 점을 배웠다. 로컬에서 보이는 파일 위치와 Docker가 인식하는 경로 기준이 다를 수 있으므로, 폴더 구조를 먼저 확인하는 것이 중요하다.
---
## 25. 전체 수행을 통해 배운 점

이번 과제를 통해 Docker와 Git/GitHub의 기본 사용법뿐만 아니라, 개발 환경을 **재현 가능하고 구조적으로 관리하는 방법**을 익힐 수 있었다.

특히 다음과 같은 점을 배울 수 있었다.

- 이미지를 기반으로 컨테이너를 실행하는 원리
- 포트 매핑을 통한 외부 접근 방식
- 바인드 마운트와 볼륨을 통한 파일 및 데이터 관리
- Git과 GitHub의 역할 차이
- Docker Compose를 통한 문서화된 실행 설정 관리
- 멀티 컨테이너 구조와 네트워크 통신 개념
- 운영 명령어를 통한 상태 확인 루틴
- 환경 변수 기반 설정 분리
- GitHub SSH 인증 방식과 보안 습관

이 과제를 통해 단순한 명령어 실습을 넘어서, 실제 개발 환경을 구성하고 운영하는 데 필요한 기초 개념을 체계적으로 이해할 수 있었다.

---

## 26. 첨부 로그 정리 안내

실제 제출 시에는 각 항목 아래에 본인이 수행한 터미널 기록, 캡처 이미지, 브라우저 확인 화면을 추가하면 된다.

제출 전에 아래 항목은 반드시 점검해야 한다.

- 사용자 계정명
- 이메일 주소
- 로컬 PC 이름
- GitHub 저장소 주소
- SSH 공개키/개인키 원문
- 기타 개인정보

특히 **SSH 개인키는 절대 README에 첨부하면 안 된다.**
