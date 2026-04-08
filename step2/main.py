import json
from pathlib import Path


STATE_FILE = Path("state.json")


class Quiz:
    def __init__(self, question, choices, answer, hint=""):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self):
        print("\n" + "-" * 50)
        print(f"문제: {self.question}")
        for i, choice in enumerate(self.choices, start=1):
            print(f"{i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            question=data["question"],
            choices=data["choices"],
            answer=data["answer"],
            hint=data.get("hint", "")
        )


class ScoreManager:
    def __init__(self, best_score=0, history=None):
        self.best_score = best_score
        self.history = history if history is not None else []

    def update_score(self, score, total):
        record = {
            "score": score,
            "total": total
        }
        self.history.append(record)

        if score > self.best_score:
            self.best_score = score
            return True
        return False

    def to_dict(self):
        return {
            "best_score": self.best_score,
            "history": self.history
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            best_score=data.get("best_score", 0),
            history=data.get("history", [])
        )


class QuizGame:
    def __init__(self):
        self.state_file = STATE_FILE
        self.game_title = "나라와 수도 맞추기 퀴즈"
        self.quizzes = []
        self.score_manager = ScoreManager()
        self.load_state()

    def get_default_quizzes(self):
        return [
            Quiz(
                "대한민국의 수도는 어디일까요?",
                ["서울", "부산", "인천", "대전"],
                1,
                "한강이 흐르는 도시예요."
            ),
            Quiz(
                "일본의 수도는 어디일까요?",
                ["오사카", "교토", "도쿄", "삿포로"],
                3,
                "일본에서 가장 대표적인 대도시예요."
            ),
            Quiz(
                "중국의 수도는 어디일까요?",
                ["상하이", "베이징", "광저우", "선전"],
                2,
                "자금성이 있는 도시예요."
            ),
            Quiz(
                "미국의 수도는 어디일까요?",
                ["뉴욕", "로스앤젤레스", "워싱턴 D.C.", "시카고"],
                3,
                "백악관이 있는 도시예요."
            ),
            Quiz(
                "프랑스의 수도는 어디일까요?",
                ["파리", "리옹", "마르세유", "니스"],
                1,
                "에펠탑으로 유명해요."
            ),
            Quiz(
                "영국의 수도는 어디일까요?",
                ["맨체스터", "리버풀", "런던", "옥스퍼드"],
                3,
                "빅벤이 있는 도시예요."
            ),
        ]

    def build_default_state(self):
        return {
            "game": {
                "title": self.game_title,
                "version": 1
            },
            "score": {
                "best_score": 0,
                "history": []
            },
            "quiz_data": [
                quiz.to_dict() for quiz in self.get_default_quizzes()
            ]
        }

    def save_state(self):
        data = {
            "game": {
                "title": self.game_title,
                "version": 1
            },
            "score": self.score_manager.to_dict(),
            "quiz_data": [quiz.to_dict() for quiz in self.quizzes]
        }

        try:
            with open(self.state_file, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as e:
            print(f"\n[저장 오류] 파일 저장 중 문제가 발생했습니다: {e}")

    def load_state(self):
        if not self.state_file.exists():
            print("[안내] state.json 파일이 없어 기본 퀴즈로 시작합니다.")
            default_data = self.build_default_state()
            self.quizzes = [Quiz.from_dict(q) for q in default_data["quiz_data"]]
            self.score_manager = ScoreManager.from_dict(default_data["score"])
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("JSON 최상위 구조가 딕셔너리가 아닙니다.")

            if "score" not in data or "quiz_data" not in data:
                raise ValueError("필수 키(score, quiz_data)가 없습니다.")

            if not isinstance(data["quiz_data"], list):
                raise ValueError("quiz_data가 리스트 형식이 아닙니다.")

            self.quizzes = [Quiz.from_dict(q) for q in data["quiz_data"]]
            self.score_manager = ScoreManager.from_dict(data["score"])

            if not self.quizzes:
                print("[안내] 저장된 퀴즈가 없어 기본 퀴즈를 복구합니다.")
                self.quizzes = self.get_default_quizzes()
                self.save_state()

        except (json.JSONDecodeError, ValueError, KeyError, TypeError) as e:
            print(f"[복구 안내] state.json 파일이 손상되었거나 형식이 올바르지 않습니다: {e}")
            print("[복구 안내] 기본 퀴즈 데이터로 초기화합니다.")
            default_data = self.build_default_state()
            self.quizzes = [Quiz.from_dict(q) for q in default_data["quiz_data"]]
            self.score_manager = ScoreManager.from_dict(default_data["score"])
            self.save_state()
        except OSError as e:
            print(f"[파일 오류] 파일을 읽는 중 문제가 발생했습니다: {e}")
            print("[안내] 기본 퀴즈 데이터로 시작합니다.")
            default_data = self.build_default_state()
            self.quizzes = [Quiz.from_dict(q) for q in default_data["quiz_data"]]
            self.score_manager = ScoreManager.from_dict(default_data["score"])

    def get_int_input(self, prompt, min_value=None, max_value=None):
        while True:
            try:
                raw = input(prompt).strip()

                if raw == "":
                    print("입력이 비어 있습니다. 다시 입력해주세요.")
                    continue

                value = int(raw)

                if min_value is not None and value < min_value:
                    print(f"{min_value} 이상 입력해주세요.")
                    continue

                if max_value is not None and value > max_value:
                    print(f"{max_value} 이하 입력해주세요.")
                    continue

                return value

            except ValueError:
                print("숫자로 입력해주세요.")
            except KeyboardInterrupt:
                print("\n[안내] Ctrl+C가 입력되어 저장 후 종료합니다.")
                self.save_state()
                raise SystemExit
            except EOFError:
                print("\n[안내] 입력이 종료되어 저장 후 종료합니다.")
                self.save_state()
                raise SystemExit

    def get_non_empty_input(self, prompt):
        while True:
            try:
                value = input(prompt).strip()
                if value == "":
                    print("빈 입력은 허용되지 않습니다. 다시 입력해주세요.")
                    continue
                return value
            except KeyboardInterrupt:
                print("\n[안내] Ctrl+C가 입력되어 저장 후 종료합니다.")
                self.save_state()
                raise SystemExit
            except EOFError:
                print("\n[안내] 입력이 종료되어 저장 후 종료합니다.")
                self.save_state()
                raise SystemExit

    def show_menu(self):
        print("\n" + "=" * 50)
        print(f"      🎯 {self.game_title} 🎯")
        print("=" * 50)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 점수 확인")
        print("5. 종료")
        print("=" * 50)

    def play_quiz(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quizzes)}문제)")
        correct_count = 0

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {index}]")
            quiz.display()
            answer = self.get_int_input("정답 번호를 입력하세요 (1-4): ", 1, 4)

            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print(f"❌ 오답입니다! 정답은 {quiz.answer}번입니다.")

        print("\n" + "=" * 50)
        print(f"결과: {len(self.quizzes)}문제 중 {correct_count}문제 정답!")
        print(f"점수: {correct_count}점")
        is_new_best = self.score_manager.update_score(correct_count, len(self.quizzes))

        if is_new_best:
            print("🎉 새로운 최고 점수입니다!")
        else:
            print(f"현재 최고 점수: {self.score_manager.best_score}점")

        print("=" * 50)
        self.save_state()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self.get_non_empty_input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choice = self.get_non_empty_input(f"선택지 {i}: ")
            choices.append(choice)

        answer = self.get_int_input("정답 번호를 입력하세요 (1-4): ", 1, 4)
        hint = self.get_non_empty_input("힌트(짧게) 입력하세요: ")

        new_quiz = Quiz(question, choices, answer, hint)
        self.quizzes.append(new_quiz)
        self.save_state()

        print("✅ 퀴즈가 추가되었습니다.")

    def list_quizzes(self):
        if not self.quizzes:
            print("\n등록된 퀴즈가 없습니다.")
            return

        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("-" * 50)
        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"[{index}] {quiz.question}")
        print("-" * 50)

    def show_score(self):
        print("\n🏆 점수 확인")
        print("-" * 50)
        print(f"최고 점수: {self.score_manager.best_score}점")

        if not self.score_manager.history:
            print("아직 플레이 기록이 없습니다.")
        else:
            print("플레이 기록:")
            for idx, record in enumerate(self.score_manager.history, start=1):
                print(f"{idx}. {record['total']}문제 중 {record['score']}점")
        print("-" * 50)

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_int_input("메뉴 번호를 선택하세요: ", 1, 5)

            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
            elif choice == 4:
                self.show_score()
            elif choice == 5:
                self.save_state()
                print("\n프로그램을 종료합니다. 데이터를 저장했습니다.")
                break


if __name__ == "__main__":
    try:
        game = QuizGame()
        game.run()
    except KeyboardInterrupt:
        print("\n[안내] 프로그램이 중단되어 저장 후 종료합니다.")
        try:
            game.save_state()
        except Exception:
            pass
    except EOFError:
        print("\n[안내] 입력 종료가 감지되어 저장 후 종료합니다.")
        try:
            game.save_state()
        except Exception:
            pass