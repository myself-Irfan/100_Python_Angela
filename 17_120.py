import requests
from html import unescape


class Question:
    def __init__(self, text: str, answer: str):
        self._text = text
        self._answer = answer

    @property
    def text(self):
        return self._text

    @property
    def answer(self):
        return self._answer


class QuizBrain:
    def __init__(self, q_bank):
        self._q_no = 0
        self._q_li = q_bank
        self._score = 0

    @property
    def q_no(self):
        return self._q_no

    @property
    def q_li(self):
        return self._q_li

    @property
    def score(self):
        return self._score

    def q_left(self) -> bool:
        """
        checks if obj attrb q_no has exceeded own attr q_li len
        :return: bool
        """
        return self._q_no < len(self._q_li)

    def check_ans(self, cur_ans, u_in) -> bool:
        if u_in == cur_ans or cur_ans.startswith(u_in):
            self._score += 1
            return True
        print(f'Incorrect. Correct answer is: {cur_ans}')
        return False

    def nxt_q(self):
        cur_q_obj = self._q_li[self._q_no]
        self._q_no += 1
        u_in = input(f'Q.{self._q_no}: {cur_q_obj.text}(True/False)?: ').capitalize()
        return self.check_ans(cur_q_obj.answer, u_in)


def fetch_qdata(amt: int):
    url = f'https://opentdb.com/api.php?amount={amt}&category=18&type=boolean'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Will raise an HTTPError if the response was unsuccessful
        resp_json = response.json().get('results', [])
        if not resp_json:
            raise ValueError("No data received from the API.")
        return [{'text': unescape(resp.get('question')), 'answer': resp.get('correct_answer')} for resp in resp_json]
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return []


def main():
    question_data = fetch_qdata(10)

    q_bank = [Question(q.get("text"), q.get("answer")) for q in question_data]

    i_qb = QuizBrain(q_bank)

    while i_qb.q_left():
        if not i_qb.nxt_q():
            break

    print(f'Your score: {i_qb.score}')


if __name__ == '__main__':
    main()
