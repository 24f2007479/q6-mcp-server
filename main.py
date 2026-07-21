from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP
import hashlib

EMAIL = "24f2007479@ds.study.iitm.ac.in".strip().lower()


mcp = FastMCP("Exam Server")

@mcp.tool()
async def solve_challenge():
    return ""

app = FastAPI()

app.mount("/", mcp.streamable_http_app())

from mcp.server.fastmcp import Context

@mcp.tool()
async def solve_challenge(ctx: Context):

    request = ctx.request

    challenge = request.headers.get("X-Exam-Challenge")

    value = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode()
    ).hexdigest()[:16]

    return value