from agents import Runner, trace, gen_trace_id, OpenAIChatCompletionsModel
from search_agent import create_search_agent
from planner_agent import create_planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import create_writer_agent, ReportData
from email_agent import create_email_agent
from openai import AsyncOpenAI
import asyncio
import os
from dotenv import load_dotenv

load_dotenv(override=True)
# GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

class ResearchManager:

    def __init__(self):
        # google_api_key = os.getenv('GOOGLE_API_KEY')
        # gemini_client = AsyncOpenAI(base_url=GEMINI_BASE_URL, api_key=google_api_key)
        # gemini_model = OpenAIChatCompletionsModel(model="gemini-2.0-flash", openai_client=gemini_client)
        self.model = "gpt-4o-mini"
        
        # Create agents with self.model
        self.planner_agent = create_planner_agent(self.model)
        self.search_agent = create_search_agent(self.model)
        self.writer_agent = create_writer_agent(self.model)
        self.email_agent = create_email_agent(self.model)

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            print(f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}")
            yield f"View trace: https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print("Starting research...")
            search_plan = await self.plan_searches(query)
            yield "Searches planned, starting to search..."     
            search_results = await self.perform_searches(search_plan)
            yield "Searches complete, writing report..."
            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."
            await self.send_email(report)
            yield "Email sent, research complete"
            yield report.markdown_report
        

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        print("Planning searches...")
        result = await Runner.run(
            self.planner_agent,
            f"Query: {query}",
        )
        print(f"Will perform {len(result.final_output.searches)} searches")
        return result.final_output_as(WebSearchPlan)

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        print("Searching...")
        num_completed = 0
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]
        results = []
        for task in asyncio.as_completed(tasks):
            result = await task
            if result is not None:
                results.append(result)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")
        print("Finished searching")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """ Perform a search for the query """
        input = f"Search term: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(
                self.search_agent,
                input,
            )
            return str(result.final_output)
        except Exception:
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """ Write the report for the query """
        print("Thinking about report...")
        input = f"Original query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(
            self.writer_agent,
            input,
        )

        print("Finished writing report")
        return result.final_output_as(ReportData)
    
    async def send_email(self, report: ReportData) -> None:
        print("Writing email...")
        result = await Runner.run(
            self.email_agent,
            report.markdown_report,
        )
        print("Email sent")
        return report