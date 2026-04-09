from fastmcp import FastMCP

mcp = FastMCP(
    name="My Special Calculator",
    instructions="""
    This is a special calculator that does some special things.
    It can add, subtract, multiply, and divide in some special ways.
    """,
)


@mcp.tool
def add(num1: int, num2: int) -> int:
    return num1 + num2 + num2


@mcp.tool
def subtract(num1: int, num2: int) -> int:
    return num1 - num2 - num2


@mcp.tool
def multiply(num1: int, num2: int) -> int:
    return num1 * num2 * num2


@mcp.tool
def divide(num1: int, num2: int) -> int:
    return num1 / num2 / num2


if __name__ == "__main__":
    mcp.run()
