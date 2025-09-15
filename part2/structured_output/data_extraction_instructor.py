import logging

# Set logging to DEBUG
logging.basicConfig(level=logging.DEBUG)

import json

from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class ContactInformation(BaseModel):
  sender_name: Optional[str] = Field(default=None, description="name of the email sender")
  location: Optional[str] = Field(default=None, description="location of the email sender")
  job_title: Optional[str] = Field(default=None, description="job title for the email sender")
  company: Optional[str] = Field(default=None, description="company the email sender works for")
  email: EmailStr | None = Field(default=None, description="email address of the email sender")
  phone_number: Optional[str] = Field(default=None, description="phone number of the email sender")

print(json.dumps(ContactInformation.model_json_schema(), indent=2))

import instructor

from openai import OpenAI

client = instructor.from_openai(
  OpenAI(base_url="http://localhost:11434/v1", api_key="none"),
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

email1 = """Hi Jacob,
Thank you for sending over the detailed proposal. I've reviewed it with our product and 
customer-success leads, and we're excited about the project.  Please put together an SOW 
for review so we can get things started.  We'd like you to travel to our office in Denver, 
Colorado for the kick off meeting.

Thanks again for the thorough proposal - I'm looking forward to collaborating.

Best regards,

Sarah Whitfield
Director of Customer Experience
Acme Software Solutions
sarah.whitfield@acmesoft.com
(312)-555-0182"""

contact_information_1 = extract_contact_information(email1)

print('\nEmail 1 Contact Information:\n')
print(contact_information_1.model_dump_json(indent=2))

email2 = """Hi Jacob,

I'm the Director of Customer Experience at Acme Software Solutions.  Thank you for sending 
over the detailed proposal. I've reviewed it with our product and customer-success leads, 
and we're excited about the project.  Please put together an SOW for review so we can get 
things started. We'd like you to travel to our office in Denver, Colorado for the kick off 
meeting.  You can always reach me at (312)-555-0182.  

Thanks again for the thorough proposal.  I'm looking forward to collaborating.

Best regards,

Sarah Whitfield
sarah.whitfield@acmesoft.com"""

contact_information_2 = extract_contact_information(email2)

print('\nEmail 2 Contact Information:\n')
print(contact_information_2.model_dump_json(indent=2))