from src.agent import agent_execution
import asyncio
from src.agent import triage_agent, create_session
from dotenv import load_dotenv
from configs.config import ROOT

_ = load_dotenv(override=True)


async def main():
    session = create_session(
        session_name="finance_session", db_path=ROOT / "data" / "session.db"
    )
    full_query = ""
    cur_agent = triage_agent
    while True:
        user_query = input(">>  ")
        if user_query.strip().lower() in {"exit", "quit"}:
            break
        full_query += f"<message_start>{user_query}"
        response = await agent_execution(cur_agent, user_query, session=session)
        full_query += f"<response_start>{response.final_output}"
        cur_agent = response.last_agent

        print(f"{cur_agent.name} response: {response.final_output}")


if __name__ == "__main__":
    asyncio.run(main())
