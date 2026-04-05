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
| Docker 기본 운영 명령 | 부분 완료 | `docker ps`, `docker ps -a`, `docker logs` 기록 있음 |
| hello-world 실행 | 완료 | 실행 로그 포함 |
| Ubuntu 컨테이너 실행 | 설명 포함 | 제출 전 실제 로그 추가 권장 |
| Dockerfile 커스텀 이미지 | 완료 | `my-nginx` 빌드 및 실행 |
| 포트 매핑 접속 증거 | 완료 | `8080`, `8081`, `8082`, `8083` 사용 |
| 바인드 마운트 반영 | 완료 | 실시간 반영 설명 및 캡처 포함 |
| Docker 볼륨 영속성 | 완료 | 삭제 전/후 비교 기록 |
| Git 설정 | 완료 | `git config --list`, `git init`, `git commit` |
| GitHub/VSCode 연동 증거 | 보완 필요 | 제출 전 로그인/연동 캡처 추가 권장 |
| Docker Compose 보너스 | 완료 | 단일/멀티 컨테이너 실행 기록 |
| 환경 변수 활용 | 설명 포함 | 제출 전 실제 적용 로그 추가 권장 |
| GitHub SSH 키 설정 | 설명 포함 | 제출 전 실제 키 등록/테스트 로그 추가 권장 |

> **주의:** 현재 대화와 업로드 자료 기준으로 작성했다. GitHub/VSCode 로그인 연동 캡처, `docker stats`, Ubuntu 내부 실행 로그, 환경 변수 적용 로그, SSH 연결 테스트 로그가 필요하다면 마지막에 추가하면 된다.

---

## 4. 프로젝트 디렉토리 구조와 설계 기준

### 4-1. 디렉토리 구조 예시

```text
ai-sw-workstation/
├── README.md
├── web/
│   ├── Dockerfile
│   └── index.html
├── bonus-compose/
│   ├── compose.yaml
│   └── .env
└── README/
    ├── 1000013376.jpg
    ├── 1000013377.jpg
    ├── 1000013378.jpg
    └── 1000013379.jpg
```

### 4-2. 어떤 기준으로 이렇게 구성했는가

이번 디렉토리 구성 기준은 아래 4가지였다.

1. **역할 분리**
   - `web/`에는 웹 서버 실행에 필요한 파일만 둔다.
   - `bonus-compose/`에는 Compose 실습 파일만 둔다.
   - `README/`에는 문서용 증빙 이미지만 둔다.

2. **재현 가능성**
   - 다른 사람이 저장소를 열어도 “어느 폴더에서 어떤 명령을 실행해야 하는지” 바로 알 수 있게 하였다.
   - 예를 들어 `web/` 폴더에서 `docker build -t my-nginx .`를 실행하면 빌드가 가능하다.

3. **수정 편의성**
   - 바인드 마운트 실습 시 `web/index.html`만 수정하면 바로 컨테이너 반영 여부를 확인할 수 있도록 했다.
   - Compose 실습 시 `bonus-compose/compose.yaml`과 `.env`만 수정하면 설정 변경 여부를 확인할 수 있도록 했다.

4. **제출 정리성**
   - README 본문, 실행 파일, 보너스 과제, 이미지 캡처를 섞지 않고 분리하여 채점자가 구조를 이해하기 쉽게 구성하였다.

### 4-3. 왜 이런 구조가 좋은가

이 구조는 “문서”, “실행 코드”, “보너스 과제”, “캡처 증빙”이 서로 섞이지 않으므로 관리가 쉽다. 또한 Docker 실습에서는 현재 작업 디렉토리가 매우 중요하므로, 폴더 역할을 명확히 나누면 빌드 경로 오류나 잘못된 파일 복사 문제를 줄일 수 있다.

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

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>AI-SW Workstation</title>
</head>
<body>
  <h1>AI/SW 개발 워크스테이션 구축 성공</h1>
  <p>Docker NGINX 컨테이너 실행 확인</p>
  <p>작성자: 최대한</p>
</body>
</html>
```

### 12-2. Dockerfile

```dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
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
- 컨테이너 내부 `index.html`도 정상 교체됨

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
docker run -d --name my-web-bind -p 8081:80 -v ~/Desktop/ai-sw-workstation/web:/usr/share/nginx/html nginx
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
- 로컬 `web/index.html`을 수정하자 컨테이너의 페이지도 즉시 변경됨
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

### 19-1. 기본 구조 예시

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8083:80"
```

### 19-2. 왜 필요한가

기존에는 다음처럼 긴 실행 명령을 직접 입력해야 했다.

```bash
docker run -d -p 8083:80 nginx
```

하지만 Compose를 사용하면 이미지, 포트, 환경 변수, 볼륨 같은 설정을 파일로 남길 수 있다. 즉, 컨테이너 실행 명령이 **문서화된 실행 설정**으로 바뀌는 것이다.

### 19-3. 배움 포인트

- 실행 옵션을 파일로 남겨 재현성을 높일 수 있다.
- 팀원이나 다른 환경에서도 동일한 실행 조건을 공유할 수 있다.
- 실행 방식 자체가 문서가 되므로 유지보수에 유리하다.

---

## 20. Docker Compose 멀티 컨테이너

Compose를 이용하여 웹 서버와 보조 서비스 2개 이상을 함께 실행하는 구조를 학습하였다.

### 20-1. 예시 compose.yaml

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8083:80"

  db:
    image: postgres:latest
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: sampledb
```

### 20-2. 컨테이너 간 네트워크 통신

Compose는 기본적으로 프로젝트 내부 네트워크를 자동 생성한다. 같은 Compose 프로젝트 안의 서비스들은 서로를 **서비스 이름으로 찾을 수 있다.**

예를 들어:
- `web` 컨테이너는 `db`라는 이름으로 데이터베이스에 접근할 수 있다.
- IP 주소를 직접 외우지 않아도 된다.

이것이 바로 **서비스 디스커버리(service discovery)** 의 기초 개념이다.

### 20-3. 배움 포인트

- 하나의 애플리케이션이 여러 서비스로 분리될 수 있음을 이해하였다.
- Compose가 서비스 간 네트워크를 자동으로 구성함을 확인하였다.
- 컨테이너끼리 이름으로 통신 가능한 구조를 경험하였다.

---

## 21. Compose 운영 명령어 실습

### 21-1. 사용 명령어

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

### 21-2. 설명

- `up`: 서비스 생성 및 실행
- `ps`: 현재 실행 중인 서비스 상태 확인
- `logs`: 서비스 로그 확인
- `down`: 서비스 종료 및 정리

### 21-3. 왜 중요한가

컨테이너를 단순히 실행하는 것보다, 문제가 생겼을 때 상태를 확인하고 원인을 찾는 루틴을 익히는 것이 더 중요하다.

### 21-4. 상태 확인 루틴

1. `docker compose up -d` 로 실행
2. `docker compose ps` 로 실행 상태 확인
3. 문제가 있으면 `docker compose logs` 로 로그 확인
4. 실습 종료 후 `docker compose down` 으로 정리

---

## 22. 환경 변수 활용

Dockerfile 또는 Compose 파일에서 환경 변수를 주입하여 포트나 실행 모드를 변경하는 실습을 수행하였다.

### 22-1. 예시

```yaml
services:
  web:
    image: my-web
    environment:
      PORT: "8083"
      MODE: "dev"
```

또는 `.env` 파일:

```env
PORT=8083
MODE=dev
```

그리고 Compose 파일에서 다음처럼 사용할 수 있다.

```yaml
services:
  web:
    image: my-web
    ports:
      - "${PORT}:80"
    environment:
      MODE: ${MODE}
```

### 22-2. 왜 중요한가

환경 변수는 프로그램 코드를 직접 수정하지 않고도 실행 시점에 설정 값을 바꿀 수 있게 해주는 방법이다.

예를 들어:
- 개발 환경: `MODE=dev`
- 배포 환경: `MODE=prod`

처럼 같은 이미지라도 설정만 다르게 하여 다른 방식으로 실행할 수 있다.

### 22-3. 설정과 코드의 분리

이 실습의 핵심은 **코드와 설정을 분리하는 것**이다. 포트 번호, 모드, 데이터베이스 주소 같은 값을 코드 안에 하드코딩하지 않고 외부 설정으로 관리하면 훨씬 유연하고 유지보수하기 쉬워진다.

---

## 23. GitHub SSH 키 설정

GitHub에 HTTPS 대신 SSH 방식으로 푸시할 수 있도록 SSH 키를 생성하고 등록하는 과정을 학습하였다.

### 23-1. 기본 흐름

1. SSH 키 생성
2. 공개키를 GitHub에 등록
3. SSH 연결 테스트
4. 원격 저장소 주소를 SSH 방식으로 변경
5. push 동작 확인

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

### 23-3. 인증 방식 차이

- **HTTPS**
  - 주소 예: `https://github.com/user/repo.git`
  - 로그인 또는 토큰 기반 인증
- **SSH**
  - 주소 예: `git@github.com:user/repo.git`
  - 공개키/개인키 기반 인증

### 23-4. 왜 배우는가

SSH 방식은 한 번 세팅해 두면 반복 인증이 편하고, 개인키와 공개키를 분리해 관리하므로 보안 측면에서도 좋은 습관을 익힐 수 있다.

### 23-5. 보안 주의사항

- 공개키는 GitHub에 등록해도 되지만,
- 개인키는 절대 외부에 공유하면 안 된다.
- 가능하면 passphrase를 설정하여 보안을 강화하는 것이 좋다.

---

## 24. 트러블슈팅 예시 정리

### 트러블슈팅 1. 셸에 HTML을 직접 입력하다가 문법 충돌

#### 문제
터미널에 직접 HTML을 한 줄씩 입력하는 과정에서 `<`, `>`, 따옴표 등 특수문자가 셸 문법과 충돌할 수 있었다.

#### 조치
터미널에 직접 HTML을 한 줄씩 입력하는 대신, `nano` 편집기 또는 heredoc 문법을 사용하였다.

#### 결과
`index.html`을 정상적으로 작성할 수 있었고, NGINX 컨테이너에서 페이지가 정상 출력되었다.

#### 배운 점
셸은 일반 텍스트 입력기와 다르므로, HTML/스크립트 내용 중 특수문자는 셸 문법과 충돌할 수 있다. 따라서 파일 편집은 전용 편집기 또는 안전한 리다이렉션 문법을 사용하는 것이 좋다.

---

### 트러블슈팅 2. Docker Compose 포트 충돌

#### 문제
Compose 실행 시 `8081` 포트가 이미 사용 중이라 실행 실패할 수 있다.

#### 원인 가설
기존 바인드 마운트 실습 컨테이너 `my-web-bind`가 `8081` 포트를 점유하고 있을 가능성이 있다고 판단하였다.

#### 포트 충돌 원인 진단 순서
1. 에러 메시지에서 어떤 포트가 충돌했는지 확인
2. `docker ps`로 해당 포트를 점유 중인 컨테이너가 있는지 확인
3. 필요 시 `lsof -i :8081` 같은 명령으로 호스트 점유 여부 확인
4. 기존 컨테이너를 중지/삭제하거나 다른 포트로 변경
5. 재실행 후 `docker ps`로 매핑 결과 재확인

#### 조치
기존 실험을 유지하기 위해 `compose.yaml`의 호스트 포트를 `8083`으로 변경하였다.

#### 결과
Compose 실행이 정상 완료되었다.

#### 배운 점
포트 충돌은 단순 에러가 아니라 “호스트에서 하나의 포트는 동시에 하나의 서비스만 바인딩 가능하다”는 운영 개념과 연결된다. 따라서 실습별 포트 계획을 먼저 세우는 것이 중요하다.

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
