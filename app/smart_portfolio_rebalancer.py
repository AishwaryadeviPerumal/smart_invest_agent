import asyncio
import uuid

from google.genai import types
from google.adk.apps import App, ResumabilityConfig
from google.adk.runners import Runner
from google.adk.memory import InMemoryMemoryService
from google.adk.sessions import InMemorySessionService

from app.authentication.authentication import set_api_key
from app.data.portfolio_data import portfolio_data
from app.human_in_loop.human_approval_agent import get_human_decision
from app.smart_invest_agent import smart_invest_agent
from app.utils.utils import check_for_approval, create_approval_response, print_agent_response

set_api_key()

session_service = InMemorySessionService()

memory_service = (
    InMemoryMemoryService()
)

smart_invest_app = App(
    name="smart_portfolio_rebalancer",
    root_agent=smart_invest_agent,
    resumability_config=ResumabilityConfig(is_resumable=True),
)

smart_invest_runner = Runner(
    app=smart_invest_app,
    session_service=session_service,
    memory_service=memory_service,
)

async def run_rebalance_portfolio(query: str):
    """Runs a rebalance portfolio with approval handling.
    Args:
        query: User's shipping request
    """

    print(f"\n{'='*60}")
    print(f"User > {query}\n")

    session_id = f"session_id_{uuid.uuid4().hex[:8]}"

    session = await session_service.create_session(
        app_name="smart_portfolio_rebalancer", user_id="test_user", session_id=session_id
    )

    await memory_service.add_session_to_memory(session)

    query_content = types.Content(role="user", parts=[types.Part(text=query)])
    events = []

    async for event in smart_invest_runner.run_async(
            user_id="test_user", session_id=session_id, new_message=query_content
    ):
        events.append(event)

    # STEP 2: Loop through all the events generated and check if `adk_request_confirmation` is present.
    approval_info = check_for_approval(events)

    # STEP 3: If the event is present, it's a large order - HANDLE APPROVAL WORKFLOW
    if approval_info:
        print(f"⏸️  Pausing for approval...")
        is_approved=get_human_decision()
        print(f"🤔 Human Decision: {'APPROVED ✅' if is_approved else 'REJECTED ❌'}\n")

        # PATH A: Resume the agent by calling run_async() again with the approval decision
        async for event in smart_invest_runner.run_async(
                user_id="test_user",
                session_id=session_id,
                new_message=create_approval_response(
                    approval_info, is_approved
                ),  # Send human decision here
                invocation_id=approval_info[
                    "invocation_id"
                ],  # Critical: same invocation_id tells ADK to RESUME
        ):
            if event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print(f"Agent > {part.text}")

    # -----------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------
    else:
        # PATH B: If the `adk_request_confirmation` is not present - no approval needed - order completed immediately.
        print_agent_response(events)

    print(f"{'='*60}\n")


    print("✅ Workflow function ready")

if __name__ == "__main__":
    portfolio: list = portfolio_data.keys()
    print('hello')
    asyncio.run(
        run_rebalance_portfolio(
            f"suggest buy/sell order with details to rebalance the portfolio:{portfolio}"
        )
    )
