import dotenv
dotenv.load_dotenv()

from crewai import Crew, Agent, Task
from crewai.project import CrewBase, task, agent, crew
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource
from models import JobList, RankedJobList, ChosenJob
from tools import web_search_tool

# Load resume content directly
with open('knowledge/resume.txt', 'r') as f:
    resume_content = f.read()

resume_knowledge = TextFileKnowledgeSource(
    file_paths=["resume.txt"]
)

@CrewBase
class JobHunterCrew:

    @agent
    def job_search_agent(self):
        return Agent(
            config=self.agents_config["job_search_agent"],
            tools = [web_search_tool],)
    @agent
    def job_matching_agent(self):
        return Agent(config=self.agents_config["job_matching_agent"])
    @agent
    def resume_optimization_agent(self):
        return Agent(config=self.agents_config["resume_optimization_agent"])
    @agent
    def company_research_agent(self):
        return Agent(config=self.agents_config["company_research_agent"],
        tools=[web_search_tool])
    @agent
    def interview_prep_agent(self):
        return Agent(config=self.agents_config["interview_prep_agent"])

    @task
    def job_extraction_task(self):
        return Task(
            config=self.tasks_config["job_extraction_task"],
            output_pydantic=JobList)
    @task
    def job_matching_task(self):
        # Add resume content to the task description
        base_description = self.tasks_config["job_matching_task"]["description"]
        enhanced_description = f"""
        {base_description}
        
        Here is the user's resume for reference:
        
        {resume_content}
        """
        
        task_config = self.tasks_config["job_matching_task"].copy()
        task_config["description"] = enhanced_description
        return Task(
            config=task_config,
            output_pydantic=RankedJobList)
    @task
    def job_selection_task(self):
        return Task(
            config=self.tasks_config["job_selection_task"],
            output_pydantic=ChosenJob)
    @task
    def resume_rewriting_task(self):
        # Add resume content to the task description
        base_description = self.tasks_config["resume_rewriting_task"]["description"]
        enhanced_description = f"""
        {base_description}
        
        Here is the user's actual resume content:
        
        {resume_content}
        
        Use this exact resume content as the source material for rewriting.
        """
        
        task_config = self.tasks_config["resume_rewriting_task"].copy()
        task_config["description"] = enhanced_description
        return Task(config=task_config)
    @task
    def company_research_task(self):
        return Task(
            config=self.tasks_config["company_research_task"],
            context = [
                self.job_selection_task()
            ])
    @task
    def interview_prep_task(self):
        return Task(
            config=self.tasks_config["interview_prep_task"],
            context=[
                self.job_selection_task(),  #job_selection_task의 작업 결과물을 interview_prep_task로 전달
                self.resume_rewriting_task(),
                self.company_research_task()]
            )

    @crew
    def crew(self):
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )

JobHunterCrew().crew().kickoff(inputs={'level':'Full Time', 'position':'Data Scientist', 'location':'Paris'})