def korean_format_number(n: int) -> str:
    """정수를 한글 형식으로 포맷팅된 문자열로 변환합니다.

    인수:
        n (int): 포맷팅할 정수입니다.

    반환값:
        str: 정수의 한글 형식으로 포맷팅된 문자열입니다.

    예시:
        >>> korean_format_number(12345)
        '1만 2345'

        >>> korean_format_number(27439263548400)
        '27조 4392억 6354만 8400'

    참고:
        이 함수는 정수를 1만 단위로 나누어 한글 형식으로 포맷팅된 문자열로 변환합니다. 사용되는 단위는 "만", "억", "조", "경"입니다.
    """
    """Converts an integer into a Korean formatted string representation.

    Args:
        n (int): The integer to be formatted.

    Returns:
        str: The Korean formatted string representation of the integer.

    Example:
        >>> korean_format_number(12345)
        '1만 2345'

        >>> korean_format_number(27439263548400)
        '27조 4392억 6354만 8400'

    Note:
        This function converts an integer into a Korean formatted string representation by dividing the number into units of 10,000 and appending the corresponding unit name. The units used are "만" (10,000), "억" (100 million), "조" (1 trillion), and "경" (10 quadrillion).
    """

    units = ["", "만", "억", "조", "경"]
    result = []
    unit_index = 0

    while n > 0:
        # 10000으로 나눈 나머지를 구하여 현재 단위의 숫자를 얻습니다.
        part = n % 10000
        if part > 0:  # 현재 단위의 값이 0이 아닌 경우에만 결과에 추가합니다.
            result.insert(0, f"{part}{units[unit_index]}")
        n //= 10000  # 다음 단위로 넘어갑니다.
        unit_index += 1

    return " ".join(result) if result else "0"
