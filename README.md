````markdown
# AI-SW 개발 워크스테이션 구축

## 1. 프로젝트 개요
본 과제에서는 macOS(iMac) 환경에서 터미널 기본 명령어를 익히고, Docker를 활용하여 AI/SW 개발 워크스테이션의 기초 실행 환경을 구성하였다. 또한 NGINX 기반 웹 서버 컨테이너 실행, 바인드 마운트 실습, Docker Volume 영속성 확인, Git 저장소 초기화 및 커밋까지 수행하였다. 추가로 보너스 과제로 Docker Compose를 이용한 단일 서비스 및 멀티 컨테이너 실행까지 확인하였다.

---

## 2. 실습 환경
- OS: macOS (iMac)
- Shell: zsh
- Docker Version: 28.5.2
- Docker Compose Version: v2.40.3
- Container Runtime: OrbStack
- Git: 로컬 저장소 초기화 후 커밋 수행

---

## 3. 프로젝트 폴더 생성 및 기본 터미널 명령어 실습

### 3-1. 작업 폴더 생성
Desktop 아래에 `ai-sw-workstation` 폴더를 만들고 이동하였다.

```bash
cd Desktop
mkdir ai-sw-workstation
cd ai-sw-workstation
pwd
ls -la
````

### 3-2. 기본 명령어 실습 내용

다음과 같은 기본 명령어를 실습하였다.

* `pwd` : 현재 경로 확인
* `ls`, `ls -la`, `ls -1` : 파일/폴더 목록 확인
* `touch` : 파일 생성
* `mkdir` : 폴더 생성
* `cp` : 파일 복사
* `mv` : 파일 이동/이름 변경
* `rm` : 파일 삭제
* `chmod` : 권한 변경

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

### 3-3. 실습 중 있었던 오류

명령어를 잘못 입력한 경우도 있었고, 이를 통해 정확한 명령어 형식의 중요성을 확인하였다.

예:

* `pwn` 입력 → `pwd`가 맞음
* `ls-la` 입력 → `ls -la`가 맞음
* 이미 이동된 파일을 다시 `mv`하려고 하여 에러 발생

### 관련 로그

```bash
user@macbook ai-sw-workstation % pwn
zsh: command not found: pwn

user@macbook ai-sw-workstation % ls-la
zsh: command not found: ls-la

user@macbook ai-sw-workstation % mv copy.txt moved.txt
mv: copy.txt: No such file or directory
```

---

## 4. Docker 설치 및 동작 확인

Docker가 정상적으로 설치되어 있는지 버전과 시스템 정보를 확인하였다.

```bash
docker --version
docker info
```

### 확인 내용

* Docker CLI 정상 동작
* buildx, compose 플러그인 사용 가능
* OrbStack 기반으로 Docker Engine 구동 중

### 관련 로그

```bash
user@macbook ai-sw-workstation % docker --version
Docker version 28.5.2, build ecc6942
```

---

## 5. Docker 이미지 빌드 및 NGINX 웹 서버 실행

### 5-1. `web` 폴더 및 HTML 파일 작성

NGINX 컨테이너에서 띄울 HTML 페이지를 작성하였다.

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

### 5-2. Dockerfile 작성

작성한 HTML 파일을 NGINX 기본 웹 루트에 복사하도록 Dockerfile을 작성하였다.

```dockerfile
FROM nginx:latest
COPY index.html /usr/share/nginx/html/index.html
```

### 5-3. 이미지 빌드 과정

처음에는 `docker build -t my-nginx`처럼 경로(`.`)를 빠뜨려 오류가 발생하였다. 이후 `docker build -t my-nginx .` 명령으로 정상 빌드하였다.

```bash
docker build -t my-nginx .
```

### 5-4. 컨테이너 실행

처음에는 `docker run -d 8080:80 --name my-web my-nginx`처럼 `-p` 옵션 없이 입력하여 오류가 났다. 이후 아래 명령으로 정상 실행하였다.

```bash
docker run -d -p 8080:80 --name my-web my-nginx
docker ps
curl http://localhost:8080
docker exec -it my-web cat /usr/share/nginx/html/index.html
docker logs my-web
```

### 결과

* `my-nginx` 이미지 생성 완료
* `my-web` 컨테이너를 통해 8080 포트에서 HTML 페이지 확인
* `curl`로 웹 페이지 응답 확인
* 컨테이너 내부의 `index.html`도 정상 반영됨 확인

### 관련 로그

```bash
user@macbook web % docker build -t my-nginx .
[+] Building 8.2s (7/7) FINISHED

user@macbook web % docker run -d -p 8080:80 --name my-web my-nginx
0bcb3989c52ae733dcb58e639c02dcd8251b45ffa0d6bd46ef811985b780a294

user@macbook web % docker ps
CONTAINER ID   IMAGE      COMMAND                   CREATED          STATUS         PORTS                                     NAMES
0bcb3989c52a   my-nginx   "/docker-entrypoint.…"   10 seconds ago   Up 7 seconds   0.0.0.0:8080->80/tcp, [::]:8080->80/tcp   my-web

user@macbook web % curl http://localhost:8080
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
### 관련 이미지
images/무제 폴더/1000013376.jpg


### 5-5. 실습 중 어려웠던 점

1. `docker build` 명령에서 마지막에 `.`을 빼먹어 빌드가 실패하였다.
2. `docker run` 실행 시 `-p` 옵션을 빠뜨려 잘못된 이미지명으로 인식되는 오류가 발생하였다.
3. 처음 HTML 작성 시 `<!DOCTYPE html>`을 터미널에 직접 잘못 입력해서 `zsh: event not found: DOCTYPE` 오류가 발생하였다. 이후 `nano` 또는 heredoc 문법을 올바르게 사용하여 해결하였다.

### 관련 로그

```bash
user@macbook web % docker build -t my-nginx
ERROR: docker: 'docker buildx build' requires 1 argument

user@macbook web % docker run -d 8080:80 --name my-web my-nginx
docker: Error response from daemon: pull access denied for 8080

zsh: event not found: DOCTYPE
```

---

## 6. 바인드 마운트 실습

### 6-1. 실행 명령

로컬 `web` 폴더를 컨테이너 내부 `/usr/share/nginx/html`에 연결하여 바인드 마운트 실습을 진행하였다.

```bash
docker rm -f my-web-bind
docker run -d --name my-web-bind -p 8081:80 -v ~/Desktop/ai-sw-workstation/web:/usr/share/nginx/html nginx
docker ps
```

### 6-2. HTML 수정 후 반영 확인

로컬의 `index.html` 파일 내용을 수정하여 컨테이너에 실시간으로 반영되는지 확인하였다.

수정 후 내용:

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

### 결과

* `8081` 포트에서 바인드 마운트 컨테이너 실행 성공
* 로컬 파일 수정 시 컨테이너 웹 페이지에도 즉시 반영됨을 확인

### 관련 로그

```bash
user@macbook ~ % docker run -d --name my-web-bind -p 8081:80 -v ~/Desktop/ai-sw-workstation/web:/usr/share/nginx/html nginx
a07f02f562f41ce291640b810e496059cafc56ef24b0f9a4e65f16f90084c700

user@macbook ~ % docker ps
CONTAINER ID   IMAGE     COMMAND                   CREATED          STATUS          PORTS                                     NAMES
a07f02f562f4   nginx     "/docker-entrypoint.…"   25 seconds ago   Up 24 seconds   0.0.0.0:8081->80/tcp, [::]:8081->80/tcp   my-web-bind
```

---
### 관련 이미지








## 7. Docker Volume 영속성 실습

### 7-1. Volume 생성

```bash
docker volume create my-nginx-data
docker volume ls
```

### 7-2. Volume 연결 컨테이너 실행

```bash
docker rm -f my-web-volume
docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
docker ps
```

### 7-3. 컨테이너 내부에 HTML 작성

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

### 7-4. 영속성 확인

```bash
curl http://127.0.0.1:8082
docker rm -f my-web-volume
docker run -d --name my-web-volume2 -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
curl http://127.0.0.1:8082
```

### 결과

* `my-nginx-data` 볼륨 생성 완료
* 8082 포트에서 웹 페이지 정상 확인
* 기존 컨테이너 삭제 후 새 컨테이너(`my-web-volume2`)를 실행해도 이전 HTML이 그대로 유지됨
* Docker Volume의 데이터 영속성을 확인함

### 관련 로그

```bash
user@macbook ~ % docker volume create my-nginx-data
my-nginx-data

user@macbook ~ % docker run -d --name my-web-volume -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
358e97c04a9e471688343147863b6f16baa97985a2ccdcc15221603a3f5bb268

user@macbook ~ % curl http://127.0.0.1:8082
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

user@macbook ~ % docker rm -f my-web-volume
my-web-volume

user@macbook ~ % docker run -d --name my-web-volume2 -p 8082:80 -v my-nginx-data:/usr/share/nginx/html nginx
e5a86b65b68c540674589508eef0d3d9b21473cbab032240ef7ae1e280b5ac98

user@macbook ~ % curl http://127.0.0.1:8082
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
```

---
### 관련 이미지










## 8. Git 저장소 초기화 및 커밋

### 8-1. Git 사용자 정보 설정

```bash
git config --global user.name "최대한"
git config --global user.email "user_email@example.com"
git config --global --list
```

### 8-2. 저장소 초기화 및 커밋

```bash
cd ~/Desktop/ai-sw-workstation
git init
git status
git add .
git commit -m "Initial commit: AI-SW workstation setup"
git branch -m main
git status
git branch
```

### 결과

* Git 저장소 초기화 완료
* 프로젝트 파일 전체 스테이징 후 초기 커밋 완료
* 기본 브랜치를 `master`에서 `main`으로 변경
* 작업 폴더가 깨끗한 상태 확인

### 관련 로그

```bash
user@macbook ~ % git config --global user.email "user_email@example.com"
user@macbook ~ % git config --global --list
user.name=최대한
user.email=user_email@example.com

user@macbook ~ % cd ~/Desktop/ai-sw-workstation
user@macbook ai-sw-workstation % git init
Initialized empty Git repository in ~/Desktop/ai-sw-workstation/.git/

user@macbook ai-sw-workstation % git add .
user@macbook ai-sw-workstation % git commit -m "Initial commit: AI-SW workstation setup"
[master (root-commit) 4655712] Initial commit: AI-SW workstation setup

user@macbook ai-sw-workstation % git branch -m main
user@macbook ai-sw-workstation % git status
On branch main
nothing to commit, working tree clean
```

---
### 관련 이미지





## 9. 보너스 과제: Docker Compose 실습

### 9-1. 단일 서비스 Compose 실행

`bonus-compose` 폴더에서 `compose.yaml` 파일을 작성하여 NGINX 컨테이너를 실행하였다.

초기 파일:

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8081:80"
```

### 9-2. 포트 충돌 문제 발생

기존에 `my-web-bind` 컨테이너가 `8081` 포트를 사용 중이어서 Compose 실행 시 포트 충돌이 발생하였다.

### 관련 로그

```bash
user@macbook bonus-compose % docker compose up -d
Error response from daemon: failed to set up container networking:
Bind for 0.0.0.0:8081 failed: port is already allocated
```

### 9-3. 포트 변경 후 해결

기존 바인드 마운트 컨테이너와 충돌하지 않도록 `8083` 포트로 수정 후 다시 실행하였다.

수정된 파일:

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8083:80"
```

실행 명령:

```bash
docker compose up -d
docker compose ps
docker compose down
```



### 관련 이미지





### 결과

* `8083` 포트로 단일 서비스 Compose 실행 성공
* `docker compose ps`로 실행 상태 확인
* `docker compose down`으로 정리 완료

### 관련 로그

```bash
user@macbook bonus-compose % docker compose up -d
[+] Running 1/1
✔ Container bonus-compose-web-1 Started

user@macbook bonus-compose % docker compose ps
NAME                  IMAGE          COMMAND                   SERVICE   CREATED        STATUS                  PORTS
bonus-compose-web-1   nginx:latest   "/docker-entrypoint.…"   web       1 second ago   Up Less than a second   0.0.0.0:8083->80/tcp, [::]:8083->80/tcp
```

---

## 10. 보너스 과제: 멀티 컨테이너 Compose 실행

### 10-1. `web` + `helper` 서비스 구성

보너스 과제로 NGINX 웹 서버와 Ubuntu 보조 컨테이너를 함께 실행하였다.

```yaml
services:
  web:
    image: nginx:latest
    ports:
      - "8083:80"

  helper:
    image: ubuntu:latest
    command: ["bash", "-c", "while true; do echo helper container is running; sleep 10; done"]
```

### 10-2. 실행 및 로그 확인

```bash
docker compose up -d
docker compose ps
docker compose logs
docker compose down
```

### 결과

* `web` 컨테이너와 `helper` 컨테이너가 동시에 실행됨
* 동일 Compose 네트워크(`bonus-compose_default`) 내에서 서비스가 관리됨
* `docker compose logs`에서 `helper container is running` 메시지 반복 출력 확인
* NGINX 컨테이너 로그도 정상 출력됨

### 관련 로그

```bash
user@macbook bonus-compose % docker compose up -d
[+] Running 3/3
✔ Network bonus-compose_default     Created
✔ Container bonus-compose-web-1     Started
✔ Container bonus-compose-helper-1  Started

user@macbook bonus-compose % docker compose ps
NAME                     IMAGE           COMMAND                   SERVICE   CREATED         STATUS         PORTS
bonus-compose-helper-1   ubuntu:latest   "bash -c 'while true…"   helper    9 seconds ago   Up 8 seconds
bonus-compose-web-1      nginx:latest    "/docker-entrypoint.…"   web       9 seconds ago   Up 8 seconds   0.0.0.0:8083->80/tcp, [::]:8083->80/tcp
```

---

### 관련 이미지




## 11. 전체 실행 포트 정리

* 기본 웹 서버 실행: `8080`
* 바인드 마운트 실습: `8081`
* Docker Volume 영속성 실습: `8082`
* Docker Compose 보너스 과제: `8083`

---

## 12. 수행 결과 요약

이번 과제를 통해 다음 항목을 수행하였다.

* 터미널 기본 명령어 실습
* Docker 설치 및 실행 환경 확인
* Dockerfile 기반 커스텀 NGINX 이미지 빌드
* `8080` 포트에서 웹 서버 컨테이너 실행
* 바인드 마운트 실습 및 실시간 반영 확인
* Docker Volume 영속성 확인
* Git 저장소 초기화 및 초기 커밋 수행
* Docker Compose 단일 서비스 실행
* Docker Compose 멀티 컨테이너 실행
* 포트 충돌 오류를 직접 해결하며 실습 문제 해결 경험 축적

---





