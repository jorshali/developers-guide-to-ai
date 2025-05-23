from langchain.prompts import PromptTemplate

article = '''To reset your password, follow these simple steps:

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
once you create a new one.'''

prompt_template = PromptTemplate.from_template("""
  You are a helpful Help Desk Representative. Use the following 
  support article to answer questions.  Only use the provided 
  <articles> and if an answer can't be found, respond with:  
  I'm sorry I can't help with that.  Please call customer 
  support at 555-555-1234.
  
<article>
{article}
</article>

Question: {question}""")

question = "I'm having password issues.  Can you help me login?"

prompt = prompt_template.format_prompt(article=article, question=question)