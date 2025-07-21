from datetime import datetime, timedelta

def make_daily_report_prompt(date_string: str, contexts: str) -> str:
    selected_date = datetime.strptime(date_string, '%Y-%m-%d').date()
    day = selected_date.weekday()
    weekdayKor = "월" if day == 0 else "화" if day == 1 else "수" if day == 2 else "목" if day == 3 else "금" if day == 4 else "토" if day == 5 else "일" if day == 6 else "월"
    
    # 한국어 날짜 형식으로 변환
    korean_date = f"{selected_date.year}년 {selected_date.month:02d}월 {selected_date.day:02d}일"

    lastDate = selected_date
    if(day==0 or day==5 or day==6):
        diff_to_friday = (day - 4 + 7) % 7
        lastDate = lastDate - timedelta(days=diff_to_friday)

    prompt = f"""
    💡 역할: 당신은 금융 시장을 분석하는 전문가입니다. 제공된 데이터를 기반으로 객관적이고 명확한 방식으로 증시 요약을 작성하세요.

    📌 **증시 요약**
    다음의 데이터를 활용하여 "Fingoo 증시 요약"을 작성하세요. 제공된 데이터는 미국 증시 관련 뉴스 및 분석 자료입니다.

    ### 🔥 **보고서 작성 템플릿**:
    【Fingoo 증시 요약 ｜{korean_date} ({weekdayKor}요일)】 

    📌 **1. 핵심 요점** ( ~ {date_string} 기준)
    - 주요 증시 변동 사항 (지수 상승/하락, 주요 원인)을 한 문장으로 요약하여 개조식으로 작성하세요.
    - 시장 참여자들의 반응을 한 줄씩 정리하세요.
    - 시장에 영향을 줄 수 있는 주요 인물의 발언 및 관련 뉴스를 포함하세요.

    📌 **2. 증시 마감 요약** ( ~ {lastDate} 기준)
    - 주요 지수 마감 수치 및 변동률 (S&P500, 나스닥100, 다우, 러셀2000 등)
    - 해당 변동에 대한 실제 요인 설명

    📌 **3. 경제 데이터 & 시장 반응** ( ~ {date_string} 기준)
    - 미국 경제 데이터 발표 내용 및 시장 반응 (국채 수익률, 외환, 금, 원유 등 포함)
    - 전문가의 반응 (기관, 이름, 코멘트 포함)

    📌 **4. 개별 기업 뉴스** ( ~ {lastDate} 기준)
    - 주가 변동이 있었던 기업, 주요 이슈 및 발언 포함

    📌 **5. 금일 주요 일정** ( ~ {date_string} 기준)
    - ★★★ 이상 일정만 추출하여 정리

    ⚠ 가장 처음에 와야 할 글자는 "【Fingoo 증시 요약 ｜{korean_date} ({weekdayKor}요일)】" 이어야 합니다.
    ⚠ 반드시 주어진 데이터만을 사용하여 작성하세요. 추가적인 가정이나 창작은 하지 마세요.  
    ⚠ 정보의 출처를 절대 기입하지 마세요.  

    ⚠ 본 Fingoo 증시 레포트는 공신력 있는 자료를 기반으로 하여 Fingoo 인공지능(AI) 기술을 사용하여 생성되었습니다."를 마지막에 출력해줘.

    contexts : 
    {contexts}

    """

    return prompt

def make_weekly_report_prompt(end_date:str, news_contexts:str, market_contexts:str) -> str:
    start_date = datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(days=6)
    prompt = f"""
    역할: 당신은 금융 시장을 분석하는 전문가입니다. 제공된 데이터를 기반으로 객관적이고 명확한 방식으로 주간 증시 요약을 작성하세요.

    📌 **주간 증시 요약**
    다음의 데이터를 활용하여 "Fingoo 주간 증시 요약"을 작성하세요. 제공된 데이터는 {start_date} ~ {end_date} 기간 동안의 미국 증시 관련 뉴스 및 분석 자료입니다.

    📌 **보고서 기간**: {start_date} ~ {end_date}

    ...

    ⚠ **반드시 주어진 데이터만을 사용하여 작성하세요. 추가적인 가정이나 창작은 하지 마세요.**  
    ⚠ **정보의 정확성을 유지하며, 지나치게 극적인 표현은 피하세요.**  
    ⚠ **정보의 출처를 절대 기입하지 마세요.**  

    " ⚠ 본 Fingoo 주간 증시 레포트는 공신력 있는 자료를 기반으로 Fingoo AI 기술을 사용하여 생성되었습니다."를 마지막에 출력해 주세요.

    위 포멧에 맞춰서 {start_date} ~ {end_date} 기간의 아래 'context' 데이터를 참고하여 주간 시황을 작성하세요.
    시황 데이터 context: {market_contexts}
    뉴스 context: {news_contexts}
    """

    return prompt


def make_weekly_report_dates(end_date:str) -> list[str]:
    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()
    current_date = end_date_obj - timedelta(days=6)

    datesToFetch = []

    while(current_date <= end_date_obj):
        datesToFetch.append(current_date.isoformat())
        current_date += timedelta(days=1)

    return datesToFetch