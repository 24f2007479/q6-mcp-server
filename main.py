import hashlib
from fastapi import FastAPI, Request
from mcp.server.fastmcp import FastMCP


EMAIL = "24f2007479@ds.study.iitm.ac.in"


# MCP server
mcp = FastMCP(
    "challenge-server"
)


@mcp.tool()
def solve_challenge():
    """
    Solves exam challenge using HTTP headers.
    """
    
    # headers MCP request se milenge
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

    result = hashlib.sha256(
        value.encode()
    ).hexdigest()[:16]


    return {
        "type": "text",
        "text": result
    }



app = FastAPI()


@app.get("/")
def home():
    return {
        "status":"MCP server running"
    }


# MCP HTTP endpoint
app.mount(
    "/mcp",
    mcp.streamable_http_app()
)