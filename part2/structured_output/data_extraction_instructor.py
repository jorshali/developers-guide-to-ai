import logging
import instructor

from typing import Optional
from openai import OpenAI
from pydantic import BaseModel, EmailStr, Field

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

class ContactInformation(BaseModel):
  sender_name: Optional[str] = Field(default=None,
    description="The name of the email sender")
  location: Optional[str] = Field(default=None,
    description="The sentiment of the comment")
  job_title: Optional[str] = Field(default=None,
    description="The category of the comment")
  company: Optional[str] = Field(default=None,
    description="The category of the comment")
  email: EmailStr | None = Field(default=None,
    description="The category of the comment")
  phone_number: Optional[str] = Field(default=None,
    description="The category of the comment")

client = instructor.from_openai(
  OpenAI(base_url="http://localhost:11434/v1"),
  mode=instructor.Mode.TOOLS
)

system_message = "Given an <email> message, you will extract the sender's contact information."

def extract_contact_information(email: str) -> ContactInformation:
  return client.chat.completions.create(
    model="llama3.2",
    messages=[
      {"role": "system", "content": system_message},
      {"role": "user", "content": "<email>{{email}}</email>, JSON:"}
    ],
    response_model=ContactInformation,
    temperature=0,
    context={"email": email}
  )

email = """Hi Jacob,
Thank you for sending over the detailed proposal. I've reviewed it with our product and customer-success leads, and we're excited about the project.  Please put together an SOW for review so we can get things started.  We'd like you to travel to our office in Denver, Colorado for the kick off meeting.

Thanks again for the thorough proposal - I'm looking forward to collaborating.

Best regards,

Sarah Whitfield
Director of Customer Experience
Acme Software Solutions
sarah.whitfield@acmesoft.com
(312)-555-0182"""

contact_information = extract_contact_information(email)

print(contact_information.model_dump_json(indent=2))