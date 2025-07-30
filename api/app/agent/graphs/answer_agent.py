from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_naver import ChatClovaX
from app.agent.states.basic_state import GraphState
from app.config import get_settings

settings = get_settings()

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "너는 clovaX가 아니라 금융분석조수 fingaroo(핀거루)야. 너의 이름을 말할때는 '저의 이름은 fingaroo입니다.'라고 하면 돼 그리고 사용자에게 답변을 제공하는 agent이기도 해. 사용자에게 답변을 제공해줘. 답변은 한글로 해줘."),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위의 대화 내용을 보고 사용자에게 적절한 답변을 해주세요. 답변을 markdown 형식으로 해줘.",
        ),
    ]
)

def answer_agent(state: GraphState):
    llm = ChatClovaX(
        model=settings.LLM_MODEL_BASE, 
        api_key=settings.CLOVASTUDIO_API_KEY
    )
    chain = prompt | llm
    answer = chain.invoke(state)
    answer.name = "answer_agent"
    return {"answer": answer, "messages": state["messages"] + [answer]}