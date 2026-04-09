import asyncio
from pymongo import AsyncMongoClient
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from tabulate import tabulate
from fastmcp import FastMCP

# mcp = FastMCP("My Expense Manager")

mcp = FastMCP(
    name="My Expense Manager",
    instructions="This is a simple expense manager that allows you to add, find, get and count expenses",
)

uri = "mongodb://localhost:27017?directConnection=true"
client = AsyncMongoClient(uri)
print("Connected to MongoDB")

database = client.get_database("test")
print("Database: ", database.name)
expenses = database.get_collection("expenses")
print("Expenses: ", expenses.name)


class Expense(BaseModel):
    _id: Optional[ObjectId] = None
    description: str = Field(description="The description of the expense")
    amount: float = Field(description="The amount of the expense")
    date: Optional[datetime | str] = Field(
        description="The date of the expense", default=None)


@mcp.tool(
    name="add_expense",
    description="Add a new expense",
)
async def add_expense(data: Expense) -> ObjectId:
    try:
        print(data.model_dump())
        result = await expenses.insert_one(data.model_dump(mode="json"))
        print(f"Added expense: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        raise Exception(
            "Unable to add the expense due to the following error: ", e)


@mcp.tool()
async def find_expenses() -> List[Expense]:
    """
    Find all expenses
    Args:
        None
    Returns:
        List[Expense]: A list of expenses
    """
    try:
        list_of_expenses: List[Expense] = await expenses.find().to_list(length=100)
        for expense in list_of_expenses:
            expense["_id"] = str(expense["_id"])
        print(tabulate(list_of_expenses, headers="keys",
              tablefmt="simple_grid", showindex="always"))
        return list_of_expenses
    except Exception as e:
        raise Exception(
            "Unable to find the expenses due to the following error: ", e)


@mcp.tool()
async def count_expenses() -> int:
    """
    Count all expenses
    Args:
        None
    Returns:
        int: The number of expenses
    """
    try:
        count = await expenses.count_documents({})
        print(count)
        return count
    except Exception as e:
        raise Exception(
            "Unable to count the expenses due to the following error: ", e)


if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)
