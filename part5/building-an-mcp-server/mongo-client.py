import asyncio
from pymongo import AsyncMongoClient
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import Field
from tabulate import tabulate


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
    date: Optional[datetime] = Field(description="The date of the expense")


async def add_expense(data: Expense):
    try:
        print(data.model_dump())
        result = await expenses.insert_one(data.model_dump(mode="json"))
        print(f"Added expense: {result.inserted_id}")
        return result.inserted_id
    except Exception as e:
        raise Exception(
            "Unable to add the expense due to the following error: ", e)


async def find_expenses():
    try:
        query = {"description": "Coffee"}
        list_of_expenses: List[Expense] = await expenses.find(query).to_list(length=100)
        print(tabulate(list_of_expenses, headers="keys",
              tablefmt="simple_grid", showindex="always"))
        return list_of_expenses
    except Exception as e:
        raise Exception(
            "Unable to find the expenses due to the following error: ", e)


async def get_expense_by_id(id: str):
    try:
        expense: Expense = await expenses.find_one({"_id": ObjectId(id)})
        print(expense)
        return expense
    except Exception as e:
        raise Exception(
            "Unable to get the expense by id due to the following error: ", e)


async def count_expenses():
    try:
        count = await expenses.count_documents({})
        print(count)
        return count
    except Exception as e:
        raise Exception(
            "Unable to count the expenses due to the following error: ", e)


async def main():
    try:
        print("-" * 100)
        print("Adding expense")
        new_expense = Expense(description="Coffee",
                              amount=10, date=datetime.now())
        await add_expense(new_expense)
        print(
            f"Added expense: {new_expense.description} - {new_expense.amount} - {new_expense.date}")
        print("-" * 100)
        print("Counting expenses")
        await count_expenses()
        print("-" * 100)
        print("Finding expenses")
        await find_expenses()
        print("-" * 100)
        print("Getting expense by id")
        await get_expense_by_id("690a4ddd3d82a9ff80b3e753")
        print("-" * 100)

    except Exception as e:
        raise Exception(
            "Unable to find the document due to the following error: ", e)

# Run the async function
asyncio.run(main())
