import hashlib
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from mcp.server.fastmcp import FastMCP, Context


EMAIL = "24f2007479@ds.study.iitm.ac.in"


# -------------------------
# MCP SERVER
# -------------------------

mcp = FastMCP(
    "challenge-server"
)


@mcp.tool()
def solve_challenge(ctx: Context):
    """
    Returns first 16 chars of SHA256(challenge:email)
    """

    try:
        request = ctx.request_context.request

        challenge = request.headers.get(
            "X-Exam-Challenge"
        )

        if not challenge:
            return {
                "type": "text",
                "text": ""
            }

        raw = f"{challenge}:{EMAIL}"

        result = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:16]


        return {
            "type": "text",
            "text": result
        }

    except Exception:
        return {
            "type": "text",
            "text": ""
        }



# -------------------------
# FASTAPI APP
# -------------------------

app = FastAPI()



@app.get("/")
def home():
    return {
        "status": "MCP server running"
    }



# Fix Render/FastAPI automatic 307 redirect
# MCP clients call /mcp without trailing slash

@app.api_route(
    "/mcp",
    methods=["GET", "POST"]
)
async def mcp_no_slash():

    return RedirectResponse(
        url="/mcp/",
        status_code=200
    )



# Actual MCP endpoint

app.mount(
    "/mcp/",
    mcp.streamable_http_app()
)