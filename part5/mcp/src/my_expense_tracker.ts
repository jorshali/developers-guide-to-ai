import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { MongoClient } from "mongodb";

const MONGO_DB_URL = "mongodb://localhost:27017?directConnection=true";
const MONGO_DB_NAME = "my_db";
const MONGO_DB_COLLECTION_EXPENSES = "my_expenses";
const MONGO_DB_COLLECTION_USERS = "users";

const client = new MongoClient(MONGO_DB_URL);
const db = client.db(MONGO_DB_NAME);
const collection_expenses = db.collection(MONGO_DB_COLLECTION_EXPENSES);
const collection_users = db.collection(MONGO_DB_COLLECTION_USERS);

// Create server instance
const server = new McpServer({
	name: "my_expense_tracker",
	version: "1.0.0",
	capabilities: {
		resources: {},
		tools: {},
	},
});

// RESOURCES
server.resource("list_users", "mongodb://localhost:27017/my_db/users", {
	description: "List all users from the database"
}, async () => {
	let users = await collection_users.find({}).toArray();
	return {
		contents: [{
			uri: "mongodb://localhost:27017/my_db/users",
			text: JSON.stringify(users.map((user) => (`URI: mongodb://localhost:27017/my_db/users/${user._id}\nDescription: ${user.name}`)), null, 2)
		}]
	};
});

// TOOLS
server.tool(
	"add_expense",
	"Add an expense to the database",
	{
		amount: z.number().describe("The amount of the expense"),
		description: z.string().describe("The description of the expense"),
		date: z.string().describe("The date of the expense"),
	},
	async ({ amount, description, date }) => {
		const expense = { amount, description, date };
		await collection_expenses.insertOne(expense);
		return {
			content: [{
				type: "text",
				text: `Expense added: ${description} - ${amount} - ${date}`
			}]
		};
	}
);

server.tool(
	"get_expenses",
	"Get all expenses from the database",
	{},
	async () => {
		const expenses = await collection_expenses.find({}).toArray();
		return {
			content: [{
				type: "text",
				text: `Expenses: ${expenses.map(expense => `${expense.description} - ${expense.amount} - ${expense.date}`).join("\n")}`
			}]
		};
	}
);

async function main() {
	const transport = new StdioServerTransport();
	await server.connect(transport);
	console.error("My Expense Tracker MCP Server running on stdio");
}

main().catch((error) => {
	console.error("Fatal error in main():", error);
	process.exit(1);
});
