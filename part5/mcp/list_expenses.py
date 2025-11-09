import asyncio
from pymongo import AsyncMongoClient
from datetime import datetime
from typing import List, Optional
from bson import ObjectId
from tabulate import tabulate


uri = "mongodb://localhost:27017?directConnection=true"
client = AsyncMongoClient(uri)
print("Connected to MongoDB")

database = client.get_database("test")
expenses = database.get_collection("expenses")


async def list_all_expenses():
    try:
        # Get all expenses
        cursor = expenses.find({})
        list_of_expenses = await cursor.to_list(length=1000)
        
        if not list_of_expenses:
            print("No expenses found.")
            return
        
        # Format expenses for display
        formatted_expenses = []
        for expense in list_of_expenses:
            expense_id = str(expense.get("_id", ""))
            description = expense.get("description", "")
            amount = expense.get("amount", 0)
            date = expense.get("date", None)
            
            # Format date if present
            if date:
                if isinstance(date, datetime):
                    date_str = date.strftime("%Y-%m-%d %H:%M:%S")
                else:
                    date_str = str(date)
            else:
                date_str = "N/A"
            
            formatted_expenses.append({
                "ID": expense_id,
                "Description": description,
                "Amount": f"${amount:.2f}",
                "Date": date_str
            })
        
        # Display in a nice table
        print("\n" + "=" * 100)
        print("EXPENSES LIST")
        print("=" * 100)
        print(tabulate(formatted_expenses, headers="keys", tablefmt="grid", showindex=True))
        print("=" * 100)
        
        # Calculate total
        total = sum(float(expense.get("amount", 0)) for expense in list_of_expenses)
        print(f"\nTotal Expenses: ${total:.2f}")
        print(f"Number of Expenses: {len(list_of_expenses)}")
        print("=" * 100 + "\n")
        
    except Exception as e:
        print(f"Error retrieving expenses: {e}")
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(list_all_expenses())

