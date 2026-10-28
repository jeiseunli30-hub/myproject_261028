# AI 교육적 효과 인식 설문 App

이 앱은 Streamlit과 SQLite3를 기반으로 작성되었습니다.

## 실행 방법

1. 필요한 패키지 설치:
   ```bash
   pip install -r requirements.txt
   ```

2. 앱 실행:
   ```bash
   streamlit run app.py
   ```

## 게임 화면 개선 (2026-10-28)

- 블록리게임 / 테트리스게임 / pythonid 화면이 하나의 프레임 안에 잘리지 않고 표시되도록 수정
  (기존: 바깥 820px 안에 1800px iframe → 이중 스크롤·화면 잘림)
- 화면 높이 조절 슬라이더, "새 창에서 크게 열기" 버튼 추가
- 새 메뉴 "게임 함께보기": 블록리 + 테트리스를 좌우로 나란히 표시
