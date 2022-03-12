# 네트워크 io 바운드
# cpu 연산이 아닌 input output에 의한 bound
# bound에 의해서 코드가 멈추는 현상 : 블로킹

import requests


def io_bound_func():
    result = requests.get("https://google.com")
    return result


if __name__ == "__main__":
    for i in range(10):
        result = io_bound_func()
    print(result)
