import hashlib

from fastmcp import FastMCP
from starlette.requests import Request

EMAIL = "24f2007479@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP("Exam MCP")


@mcp.tool(name="solve_challenge")
async def solve_challenge(request: Request):
    """
    Reads challenge from HTTP headers and returns
    first 16 chars of SHA256(challenge:email)
    """

    challenge = request.headers.get("X-Exam-Challenge")

    if challenge is None:
        return "missing challenge"

    digest = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode()
    ).hexdigest()

    return digest[:16]


app = mcp.streamable_http_app()