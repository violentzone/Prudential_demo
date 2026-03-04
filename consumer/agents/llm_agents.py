from google.adk.agents import LlmAgent
from .agent_tools import calculate_insurance_fee


decide_agent = LlmAgent(
    name='decide_agent',
    description="Decide a person is valuable for reach out for insurance",
    model='gemini-2.5-flash-lite',
    instruction="""You are a sales agent of insurance company, you decide a person is valuable for approaching for selling insurance,
                Evaluate on factors below:
                1. Determine if the person is a 'high_value_target' based on:
                   - GraduateOrNot == 1
                   - AnnualIncome >= 500000
                   - OR Government Sector Worker == 1 (Always High Value)
                2. Update the JSON data: 
                   - Set a field "is_valuable": true/false.
                   - If false, add a "rejection_reason" field.
                3. Pass the entire updated JSON object to the next agent. Do not say goodbye.
                """
)


calculate_fee_agent = LlmAgent(
    name='insurance_fee_calculate_agent',
    description="Calculate a person's best insurance fee",
    model='gemini-2.5-flash-lite',
    instruction="""You are insurance specialist, if the person is not a good client for travel insurance, skip this process, 
    else calculate best travel insurance fee by 'calculate_insurance_fee' tool, creates new information in user's information like below:
    {"Age": 31, "Government Sector Worker": 1, "GraduateOrNot": 1, "AnnualIncome": 400000, "FamilyMembers": 9, "ChronicDiseases": 1, "FrequentFlyer": 0, "EverTravelledAbroad": 0, "TravelInsurance": 0}
    ->  {"Age": 31, "Government Sector Worker": 1, "GraduateOrNot": 1, "AnnualIncome": 400000, "FamilyMembers": 9, "ChronicDiseases": 1, "FrequentFlyer": 0, "EverTravelledAbroad": 0, "TravelInsurance": 0, "fee": 3000}
    """,
    tools=[calculate_insurance_fee]
)

summary_agent = LlmAgent(
    name='summary_and_suggestion_agent',
    description="You are a sales professional, you response client's Determined insurance fee and details if client meets valuable target, if client did not meet requirements valuable target, tell them reason politely",
    model='gemini-2.5-pro',
    instruction="""You are sales manager with top sales skills, your goal is to explain insurance fee and details to client, there are two conditions:
    1. Client is not a valuable target, in this case decline the client politely
    2. Client meets valuable target, explain insurance fee and convince client it's a good deal.
    
    Generate plane text about 200 words of client's insurance proposal or decline to offer insurance regard valuable target or not, in a insurance sales perspective with professional tongue
    """
)
