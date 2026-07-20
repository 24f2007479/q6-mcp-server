import hashlib

from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP


EMAIL = "24f2007479@ds.study.iitm.ac.in"


# -----------------------------
# MCP SERVER
# -----------------------------

mcp = FastMCP(
    "challenge-server"
)


@mcp.tool()
def solve_challenge():
    """
    Generate SHA256(challenge:email) first 16 chars.
    Challenge comes from HTTP header.
    """

    request = mcp.get_request()

    challenge = request.headers.get(
        "X-Exam-Challenge"
    )

    if not challenge:
        return {
            "type": "text",
            "text": ""
        }


    value = f"{challenge}:{EMAIL}"


    answer = hashlib.sha256(
        value.encode("utf-8")
    ).hexdigest()[:16]


    return {
        "type": "text",
        "text": answer
    }



# -----------------------------
# FASTAPI APP
# -----------------------------

app = FastAPI()



@app.get("/")
def home():
    return {
        "status": "MCP server running"
    }



# IMPORTANT:
# No redirect
# No trailing slash problem

app.mount(
    "/mcp",
    mcp.streamable_http_app()
)