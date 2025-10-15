import argparse
import os
from crewai import Crew, Process
from agents import ArticleAnalysisAgents
from tasks import ArticleAnalysisTasks

def main():
    parser = argparse.ArgumentParser(description="Analyze an article and generate a summary.")
    parser.add_argument("--url", type=str, help="The URL of the article to analyze.", required=True)
    args = parser.parse_args()

    # Initialize the agents and tasks
    agents = ArticleAnalysisAgents()
    tasks = ArticleAnalysisTasks()

    # Inform the user which model is being used
    if os.getenv("OPENROUTER_API_KEY"):
        print("Using OpenRouter model: xai/grok-4-fast")
    else:
        print("Using Ollama model: gpt-oss:20b")

    # Create the agents
    summarizer_agent = agents.summarizer_agent()
    assumptions_agent = agents.assumptions_agent()
    errors_agent = agents.errors_agent()

    # Create the tasks
    summarize_task = tasks.summarize_article(summarizer_agent, args.url)
    assumptions_task = tasks.identify_assumptions(assumptions_agent, args.url)
    errors_task = tasks.identify_errors(errors_agent, args.url)

    # Create the crew
    crew = Crew(
        agents=[summarizer_agent, assumptions_agent, errors_agent],
        tasks=[summarize_task, assumptions_task, errors_task],
        process=Process.sequential,
        verbose=True
    )

    # Execute the crew
    result = crew.kickoff()

    # Print the result
    print("\n\nArticle Analysis Report:")
    print("==========================")
    print(result)

if __name__ == "__main__":
    main()
