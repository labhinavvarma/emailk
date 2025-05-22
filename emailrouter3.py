# router.py

from fastapi import APIRouter, Request, HTTPException
from mcpserver import mcp

route = APIRouter()

@route.post("/invoke")
async def invoke_tool(request: Request):
    try:
        payload = await request.json()
        tool_name = payload.get("tool")
        tool_input = payload.get("input", {})

        if not tool_name:
            raise HTTPException(status_code=400, detail="Missing tool name")

        # ✅ Use the official public `mcp.tools` list
        tool = next((t for t in mcp.tools if t.name == tool_name), None)
        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        result = await tool.invoke(tool_input)
        return {"type": result.type, "content": result.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
