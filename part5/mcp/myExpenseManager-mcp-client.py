import asyncio
from datetime import datetime
from fastmcp import Client
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
from tabulate import tabulate
from pydantic import Field

client = Client("http://localhost:8000/mcp")


class Expense(BaseModel):
    _id: Optional[ObjectId] = None
    description: str = Field(description="The description of the expense")
    amount: float = Field(description="The amount of the expense")
    date: Optional[datetime] = Field(description="The date of the expense")


async def print_tools():
    print("----- TOOLS -----")
    tools = await client.list_tools()
    print(tools)
    print("-" * 100)
    for tool in tools:
        print(f"== Tool Name: {tool.name} == ")
        print(f"Description: {tool.description}")
        print(f"Input Schema: {tool.inputSchema}")
        print(f"Output Schema: {tool.outputSchema}")
        print("-" * 100)


async def find_expenses():
    result = await client.call_tool("find_expenses")
    print("=" * 100)
    print(result.content)
    print("=" * 100)
    print(tabulate(result.data, headers="keys",
                   tablefmt="simple_grid", showindex="always"))
    print("=" * 100)
    print(result.structured_content)
    print("=" * 100)


async def add_expense(expense: Expense):
    print("Adding expense: ", expense.model_dump())
    result = await client.call_tool("add_expense", {"data": expense.model_dump()})
    print("Added expense: ", result.content)


async def count_expenses():
    result = await client.call_tool("count_expenses")
    print("=" * 100)
    print(result.structured_content)
    print("=" * 100)


async def call_tool():
    async with client:
        # await print_tools()
        await find_expenses()
        await add_expense(Expense(description="Test expense", amount=100, date=datetime.now()))
        await find_expenses()
        await count_expenses()

asyncio.run(call_tool())
