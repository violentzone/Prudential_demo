from google.adk.agents import LlmAgent
from .agent_tools import calculate_insurance_fee, description_adder


decide_agent = LlmAgent(
    name='decide_agent',
    description="Decide a person is valuable for reach out for insurance",
    model='gemini-2.5-flash-lite',
    instruction="""You are a sales agent of insurance company, you decide a person is valuable for approaching for selling insurance,
                Evaluate on factors below:
                1. If the person is not graduated(GraduateOrNot column == 0 ), he/she is not valuable for selling insurance, Note: 1=Yes and 0=No
                2. Evaluate on "AnnualIncome" column, if blow 500000, the person's income is too low for insurance
                3. Despite factors above, if column "Government Sector Worker" == 1, means the person is government worker, which is always high value target
                
                If the person is not valuable for selling insurance, add `description` column using 'description_adder' tool
                """,
    tools=[description_adder]
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
    description="You are a sales professional, you response client's Determined insurance fee and details if client meets valuable target, if client did not meets valuable target, tell them reason politely",
    model='gemini-2.5-pro',
    insturction="""You are sales manager with top sales skills, your goal is to explain insurance fee and details to client, there are two conditions:
    1. Client is not a valuable target, in this case decline the client politely
    2. Client meets valuable target, explain insurance fee and convince client it's a good deal.
    """
)
