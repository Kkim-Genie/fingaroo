from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import asyncio
from app.knowledge.application.daily_market_condition_service import DailyMarketConditionService
from app.knowledge.infra.repository.daily_market_condition_repo import DailyMarketConditionRepository
from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository
from app.knowledge.infra.repository.news_repo import NewsRepository

# 스케줄러 인스턴스 생성
scheduler = AsyncIOScheduler()
daily_market_condition_repo = DailyMarketConditionRepository()
news_repo = NewsRepository()
embeddings_repo = EmbeddingsRepository()
embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
daily_market_condition_service = DailyMarketConditionService(daily_market_condition_repo=daily_market_condition_repo, news_repo=news_repo, embeddings_service=embeddings_service)

# 스케줄링될 실제 작업 함수
def make_daily_report():
    print(f"[스케줄러] 시황 생성 시작! 현재 시간: {datetime.datetime.now()}")
    date_string = datetime.datetime.now().strftime("%Y-%m-%d")
    daily_market_condition_service.create(date_string)
    print(f"[스케줄러] 시황 생성 완료! 현재 시간: {datetime.datetime.now()}")

# 스케줄러 초기화 및 작업 추가 함수
def init_scheduler():
    """
    스케줄러를 초기화하고 필요한 작업을 추가합니다.
    """
    print("[스케줄러] 스케줄러 초기화 및 작업 추가 중...")

    # 예시: 매일 오후 4시 0분에 my_scheduled_task 실행
    scheduler.add_job(
        make_daily_report,
        CronTrigger(hour=16, minute=0), # 매일 오후 4시 (한국 시간 기준)
        id="make_daily_report",
        replace_existing=True,
        timezone="Asia/Seoul" # 시간대 명시 (매우 중요)
    )

    print("[스케줄러] 작업 추가 완료.")

# 스케줄러 시작 함수
def start_scheduler():
    """
    스케줄러를 시작합니다.
    """
    if not scheduler.running:
        scheduler.start()
        print("[스케줄러] 스케줄러 시작됨.")
    else:
        print("[스케줄러] 스케줄러가 이미 실행 중입니다.")

# 스케줄러 종료 함수
def shutdown_scheduler():
    """
    스케줄러를 종료합니다.
    """
    if scheduler.running:
        scheduler.shutdown()
        print("[스케줄러] 스케줄러 종료됨.")
    else:
        print("[스케줄러] 스케줄러가 이미 종료되어 있습니다.")

# 스케줄러에 현재 등록된 작업 목록을 보여주는 함수 (선택 사항)
def get_jobs():
    """
    현재 스케줄러에 등록된 모든 작업을 반환합니다.
    """
    return scheduler.get_jobs()

# 단독 테스트용 async 함수
async def test_scheduler_async():
    """
    AsyncIOScheduler를 asyncio 이벤트 루프 안에서 테스트합니다.
    """
    print("AsyncIOScheduler 테스트 시작...")
    init_scheduler()
    start_scheduler()
    print("스케줄러가 1분 동안 실행됩니다. 작업을 확인하세요.")
    await asyncio.sleep(60)  # 1분 대기
    shutdown_scheduler()
    print("AsyncIOScheduler 테스트 종료.")

if __name__ == "__main__":
    # 이 파일 단독으로 실행하여 스케줄러 테스트
    print("scheduler.py 단독 실행 테스트...")
    asyncio.run(test_scheduler_async())