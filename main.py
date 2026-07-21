from fastapi import FastAPI
from starlette.routing import Mount
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
import hashlib

EMAIL = "24f2007479@ds.study.iitm.ac.in".strip().lower()

mcp = FastMCP("Exam Server")


@mcp.tool(
    name="solve_challenge",
    description="Solve exam challenge"
)
async def solve_challenge() -> str:
    request = get_http_request()

    challenge = request.headers.get("X-Exam-Challenge", "")

    answer = hashlib.sha256(
        f"{challenge}:{EMAIL}".encode()
    ).hexdigest()[:16]

    return answer


mcp_app = mcp.streamable_http_app(path="/")

app = FastAPI(
    lifespan=mcp_app.lifespan,
    routes=[
        Mount("/", app=mcp_app),
    ],
)