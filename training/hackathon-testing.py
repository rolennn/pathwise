from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List, Optional
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

# Initialize OpenAI client
client = OpenAI()

# Define output schema
class Milestone(BaseModel):
    year: int
    event: str
    amount: Optional[str] = None

class SimulationScenario(BaseModel):
    title: str
    narrative: str
    timeline: List[Milestone]
    tradeoffs: str
    feasibility_notes: str

class SimulationReport(BaseModel):
    default_path: SimulationScenario
    simulated_alternatives: List[SimulationScenario]

# Construct message with detailed system prompt
simulation_messages = [
    {"role": "system", "content": """
You are a financial planning AI for Pathwise, a narrative-driven financial simulation app. 
You help users visualize possible financial futures based on their profile and life goals.

Your output must include:
1. A DEFAULT FUTURE PATH
- Assume the user's current income, spending, and savings behavior continues
- Describe a narrative of their financial future, milestone timeline, and which goals may/may not be reached

2. 2–3 ALTERNATIVE FUTURE PATHS
- Explore different scenarios based on plausible changes (e.g., higher/lower income, goal shifts, life events)
- Each alternative must include a unique narrative, timeline, trade-offs, and feasibility notes

Output must be:
- Empathetic, human, and calming in tone — not overly technical
- Realistic: factor in inflation, market variability, lifestyle changes, and limits to user control
- Use light probabilistic language: "may," "likely," "may need to adjust," etc.
- Include financial, emotional, and behavioral insight in the narratives
    """},
    {"role": "user", "content": """
🧾 BASIC USER PROFILE
Name: Alex Reyes
Age: 27
Country: Philippines
City: Metro Manila
Occupation: Freelance Graphic Designer
Education: Bachelor's Degree
Employment Type: Freelance
Dependents: None (may have a child by 34)

💸 FINANCIAL SNAPSHOT
Monthly Income: PHP 35,000
Savings: PHP 80,000
Investments: PHP 50,000 (mutual funds)
Debts: None
Rent: PHP 10,000
Utilities: PHP 3,500
Transportation: PHP 2,000
Health Costs: PHP 1,500
Lifestyle: Moderate
Estimated Monthly Expenses: PHP 20,000–25,000
Savings Rate: 20–25%

🎯 LIFE GOALS
1. Buy a condo by age 32 (PHP 3.5M) | Flexibility: Medium | Priority: High
2. Retire early by age 55 | Flexibility: Low | Priority: Medium
3. Take a sabbatical at age 40 (PHP 500k) | Flexibility: High | Priority: Low

📅 FUTURE EVENTS
- May have a child by 34
- Might move abroad by 2032

🧭 PREFERENCES / CONSTRAINTS
Willing to take loans: Only if necessary
Investment style: Balanced (medium risk)
Comfort with uncertainty: Medium
Time available to increase income: 5 hrs/week
Values: Financial stability without sacrificing quality of life
    """}
]

try:
    # Use GPT-4o models for structured outputs (NOT O3)
    response = client.beta.chat.completions.parse(
        model="o4-mini",  # Changed from "o3" to supported model
        messages=simulation_messages,
        response_format=SimulationReport,
        temperature=0.7
    )
    
    report = response.choices[0].message.parsed
    print("Generated Financial Simulation Report:")
    print("=" * 60)
    print(f"Default Path: {report.default_path.title}")
    print(f"Narrative:\n{report.default_path.narrative}\n")
    
    print("Timeline Milestones:")
    for milestone in report.default_path.timeline:
        amount_str = f" - {milestone.amount}" if milestone.amount else ""
        print(f"  {milestone.year}: {milestone.event}{amount_str}")
    
    print(f"\nTradeoffs: {report.default_path.tradeoffs}")
    print(f"Feasibility: {report.default_path.feasibility_notes}")
    
    print(f"\nNumber of alternative scenarios: {len(report.simulated_alternatives)}")
    
    for i, alt in enumerate(report.simulated_alternatives, 1):
        print(f"\n--- Alternative {i}: {alt.title} ---")
        print(f"Narrative: {alt.narrative}")
        print(f"Key milestones: {len(alt.timeline)} events")
        print(f"Tradeoffs: {alt.tradeoffs}")
    
    print("\n" + "="*60)
    print("Full JSON Output:")
    print(report.model_dump_json(indent=2))
    
except Exception as e:
    print(f"Error: {e}")
    print("\nDebugging info:")
    print("- Make sure your API key is valid and not revoked")
    print("- Structured outputs only work with GPT-4o models")
    print("- Available models: gpt-4o-2024-08-06, gpt-4o-mini, gpt-4o-2024-11-20")
    print("- O3 models don't support structured parsing yet")
    
    # Alternative: Try without structured parsing
    print("\nTrying alternative approach without structured parsing...")
    try:
        alt_response = client.chat.completions.create(
            model="gpt-4o-mini",  # Fallback to regular completion
            messages=simulation_messages + [{"role": "user", "content": "Please format your response as valid JSON matching the SimulationReport schema."}],
            temperature=0.7
        )
        print("Alternative response received:")
        print(alt_response.choices[0].message.content)
    except Exception as alt_e:
        print(f"Alternative approach also failed: {alt_e}")