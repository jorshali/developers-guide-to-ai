from langchain.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate

system_prompt = SystemMessagePromptTemplate.from_template(
  "Answer the question with company information based on only " + 
  "the following context:\n\n{context}"
)
human_prompt = HumanMessagePromptTemplate.from_template("{question}")

prompt = ChatPromptTemplate.from_messages([system_prompt, human_prompt])

print(prompt.format(context='''To reset your password, follow these simple steps:

1. Click on the "Forgot Password" link on the login page
2. Enter your registered email address
3. Check your email for a password reset link
4. Click the link in the email (valid for 24 hours)
5. Create a new password that meets our security requirements:
   - At least 8 characters long
   - Contains uppercase and lowercase letters
   - Includes at least one number
   - Has at least one special character

If you don't receive the reset email within 5 minutes, please check your 
spam folder or contact our support team.

For security reasons, your old password will be immediately invalidated 
once you create a new one.''',

question="I'm having password issues.  Can you help me login?"))
    