// mcp-server.js
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
// Define the URL where your Express app is running
const EXPRESS_APP_URL = 'http://localhost:3000'; // Make sure this matches your app.js port

async function startMcpServer() {
	const server = new McpServer({
		name: "my_custom_calculator",
		version: "1.0.0",
		description: "Exposes Express API endpoints as MCP tools."
	});

	server.registerResource("get_processed_data", "file://processed", {
		description: "Get processed data."
	}, async () => {
		try {
			const response = await fetch(`${EXPRESS_APP_URL}/data`, {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const data = await response.json();
			return {
				contents: [{
					uri: "data://processed",
					text: JSON.stringify(data, null, 2)
				}]
			};
		} catch (error: any) {
			return {
				contents: [{
					uri: "data://processed",
					text: `Error fetching data: ${error.message}`
				}]
			};
		}
	});

	server.registerTool("special_calculator_add", {
		description: "Adds two numbers together in a special way.",
		inputSchema: {
			number1: z.number().describe("The first number."),
			number2: z.number().describe("The second number."),
		},
		outputSchema: {
			result: z.number().describe("The result of the addition.")
		}
	}, async ({ number1, number2 }: { number1: number, number2: number }) => {
		try {
			const response = await fetch(`${EXPRESS_APP_URL}/sum`, {
				method: 'POST',
				body: JSON.stringify({ number1, number2 }),
				headers: {
					'Content-Type': 'application/json'
				}
			});
			const data = await response.json();
			return {
				content: [
					{
						type: "text",
						text: `special_calculator_add: ${number1} + ${number2} = ${data.result}`
					}
				],
				structuredContent: data
			};
		} catch (error: any) {
			return {
				content: [],
				structuredContent: { result: 0 },
				isError: true
			};
		}
	});

	const transport = new StdioServerTransport();
	await server.connect(transport);
}

startMcpServer().catch(() => {
	// Silent error handling for MCP protocol
});