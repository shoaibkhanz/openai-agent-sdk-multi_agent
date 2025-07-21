from agents import (
    Agent,
    FileSearchTool,
    ModelSettings,
    Runner,
    SQLiteSession,
    WebSearchTool,
)
from src.vector import create_vector_store, upload_pdf_to_vector_store
from typing import Optional
from configs.config import PDF_PATH

from src.prompts import (
    QUERY_TRANSACTION_PROMPT,
    FINANCIAL_AGENT_PROMPT,
    TRIAGE_AGENT_PROMPT,
    INVESTMENT_AGENT_PROMPT,
    WEALTH_AGENT_PROMPT,
)
from src.tools import (
    addition,
    division,
    get_metadata_from_table,
    get_table_columns,
    execute_sql,
    multiplication,
    percent_change,
    subtraction,
)


sql_query_agent = Agent(
    name="sql_query_agent",
    instructions=QUERY_TRANSACTION_PROMPT,
    tools=[WebSearchTool(), get_metadata_from_table, get_table_columns, execute_sql],
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0, tool_choice="required"),
)
financial_agent = Agent(
    name="financial_agent",
    instructions=FINANCIAL_AGENT_PROMPT,
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.2, tool_choice="auto"),
    tools=[
        sql_query_agent.as_tool(
            tool_name="sql_query_agent_tool",
            tool_description="This sql agent as a tool is called for pulling data from tables and aggregation",
        ),
        addition,
        subtraction,
        multiplication,
        division,
        percent_change,
    ],
)

investment_agent = Agent(
    name="investment_agent",
    instructions=INVESTMENT_AGENT_PROMPT,
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.2, tool_choice="required"),
    tools=[
        WebSearchTool(),
        addition,
        subtraction,
        multiplication,
        division,
        percent_change,
    ],
)


vector_store = create_vector_store(store_name="wealth-advice")
file_upload = upload_pdf_to_vector_store(
    pdf_filepath=PDF_PATH, vector_store_id=vector_store["vector_store_id"]
)
wealth_agent = Agent(
    name="wealth_agent",
    instructions=WEALTH_AGENT_PROMPT,
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.2, tool_choice="required"),
    tools=[
        FileSearchTool(vector_store_ids=[vector_store["vector_store_id"]]),
        addition,
        subtraction,
        multiplication,
        division,
        percent_change,
    ],
    handoffs=[financial_agent],
)

# Set the handoffs for financial_agent after sql_query_agent is defined
financial_agent.handoffs = [investment_agent]
investment_agent.handoffs = [financial_agent, wealth_agent]

triage_agent = Agent(
    name="triage_agent",
    instructions=TRIAGE_AGENT_PROMPT,
    handoffs=[financial_agent, investment_agent, wealth_agent],
    model="gpt-4o-mini",
    model_settings=ModelSettings(temperature=0.1, tool_choice="required"),
)


def create_session(session_name: str, **kwargs):
    session = SQLiteSession(session_name, **kwargs)
    return session


async def agent_execution(
    agent: Agent, query: str, session: Optional[SQLiteSession] = None
):
    if session is None:
        new_session = create_session("Agent-Session")
        response = await Runner.run(
            starting_agent=agent, input=query, session=new_session
        )
    else:
        response = await Runner.run(starting_agent=agent, input=query, session=session)

    return response
