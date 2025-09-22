
import OpenAI from 'openai';
import { z } from "zod";
import { zodToJsonSchema } from 'zod-to-json-schema';

console.log('Starting data extraction with OpenAI...');

const ContactInformationSchema = z.object({
  sender_name: z.string().optional().describe("name of the email sender"),
  location: z.string().optional().describe("location of the email sender"),
  job_title: z.string().optional().describe("job title for the email sender"),
  company: z.string().optional().describe("company the email sender works for"),
  email: z.string().email().optional().describe("email address of the email sender"),
  phone_number: z.string().optional().describe("phone number of the email sender")
});

console.log('ContactInformation Schema:');
console.log(JSON.stringify(zodToJsonSchema(ContactInformationSchema), null, 2));

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

const systemMessage = "Given an <email> message, you will extract the sender's contact information.";

// Function to extract contact information from email
async function extractContactInformation(email) {
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      { role: "system", content: systemMessage },
      { role: "user", content: `<email>${email}</email>\nJSON:` }
    ],
    response_format: {
      type: 'json_schema',
      json_schema: {
        name: 'ContactInformation',
        schema: zodToJsonSchema(ContactInformationSchema)
      }
    }
  });
  
  
  const structuredOutput = response.choices[0].message.content;

  // You can then parse and validate the output using Zod
  const parsedOutput = ContactInformationSchema.parse(JSON.parse(structuredOutput));
  
  return parsedOutput;
}

// Email examples
const email1 = `Hi Jacob,
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
(312)-555-0182`;

const email2 = `Hi Jacob,

I'm the Director of Customer Experience at Acme Software Solutions.  Thank you for sending 
over the detailed proposal. I've reviewed it with our product and customer-success leads, 
and we're excited about the project.  Please put together an SOW for review so we can get 
things started. We'd like you to travel to our office in Denver, Colorado for the kick off 
meeting.  You can always reach me at (312)-555-0182.  

Thanks again for the thorough proposal.  I'm looking forward to collaborating.

Best regards,

Sarah Whitfield
sarah.whitfield@acmesoft.com`;

// Main execution function
async function main() {
  try {
    // Extract contact information from first email
    console.log('\nExtracting contact information from Email 1...');
    const contactInformation1 = await extractContactInformation(email1);
    
    console.log('\nEmail 1 Contact Information:');
    console.log(JSON.stringify(contactInformation1, null, 2));

    // Extract contact information from second email
    console.log('\nExtracting contact information from Email 2...');
    const contactInformation2 = await extractContactInformation(email2);
    
    console.log('\nEmail 2 Contact Information:');
    console.log(JSON.stringify(contactInformation2, null, 2));

  } catch (error) {
    console.error('Error in main execution:', error);
  }
}

// Run the main function
main();
