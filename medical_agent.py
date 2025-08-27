from agents import Agent , Runner , RunContextWrapper , function_tool , trace
from connection import config
from pydantic import BaseModel
from dotenv import load_dotenv
import asyncio
import rich

load_dotenv()

# ------------------ Exercise 1 ------------------ #
# Medical Consultation Assistant (Intermediate)
# Requirement: Create a dynamic instructions system for a medical consultation agent 
# that adapts based on user_type.
# Patient: Use simple, non-technical language. Explain medical terms in everyday words. 
# Be empathetic and reassuring. 
# Medical Student: Use moderate medical terminology with explanations. Include learning opportunities. 
# Doctor: Use full medical terminology, abbreviations, and clinical language. Be concise and professional.

class MedicalQuery(BaseModel):
    user_type: str
    question: str
    
medical = MedicalQuery(user_type="name", question="What is blood pressure")    

async def MyPersonalFunction(wrapper: RunContextWrapper[MedicalQuery]):
    return wrapper

@function_tool
def products_info(wrapper: RunContextWrapper[MedicalQuery]):
    print('Checking Context', wrapper)
    return f'{wrapper.context}'

# ------------------ Example of Dynamic Context ------------------ #

class Medical_Consultant(BaseModel):
    user_type: str
    question: str

personOne = Medical_Consultant(
    user_type="patient",
    question="What is hypertension?"
)

async def my_dynamic_instructions(ctx: RunContextWrapper[Medical_Consultant], agent: Agent):
    if ctx.context.user_type == "patient":
        return """
        Hypertension, also called high blood pressure, means the force of blood 
        against your artery walls is too high. This can damage your heart over time. 
        It's important to eat healthy, exercise, and follow your doctor's advice.
        """
    elif ctx.context.user_type == "medical student":
        return """
        Hypertension is defined as persistently elevated arterial blood pressure, 
        usually >140/90 mmHg. It involves increased peripheral resistance and can 
        lead to complications such as LVH, stroke, and nephropathy.
        """
    elif ctx.context.user_type == "doctor":
        return """
        Hypertension (HTN): chronic elevation of arterial BP >140/90. Classified into 
        primary and secondary causes. Requires risk stratification, evaluation for 
        end-organ damage, and guideline-based management.
        """
    else:
        return "Please specify a valid user type: patient, medical student, or doctor."

personal_agent = Agent(
    name="Agent",
    instructions=my_dynamic_instructions,
)

async def main():
    with trace("Learn Dynamic Instructions"):
        result = await Runner.run(
            personal_agent, 
            "What is Hypertension?",
            run_config=config,
            context=personOne  # Local context
        )
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
