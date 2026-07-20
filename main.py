import hashlib
from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP, Context


EMAIL = "24f2007479@ds.study.iitm.ac.in"


mcp = FastMCP(
    "challenge-server"
)


@mcp.tool()
def solve_challenge(ctx: Context):
    """
    Returns SHA256(challenge:email) first 16 chars.
    """

    request = ctx.request_context.request

    challenge = request.headers.get(
        "X-Exam-Challenge"
    )

    if not challenge:
        return "missing challenge"


    value = f"{challenge}:{EMAIL}"

    answer = hashlib.sha256(
        value.encode()
    ).hexdigest()[:16]


    return answer



app = FastAPI()


@app.get("/")
def home():
    return {
        "status": "MCP server running"
    }


app.mount(
    "/mcp",
    mcp.streamable_http_app()
)