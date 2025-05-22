# router.py
from fastapi import APIRouter, Request, HTTPException
from pydantic import ValidationError
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

        # ✅ Access tool from internal tool registry
        tool = mcp._tool_registry.get(tool_name)

        if not tool:
            raise HTTPException(status_code=404, detail=f"Tool '{tool_name}' not found")

        result = await tool.invoke(tool_input)
        return {"type": result.type, "content": result.text}

    except ValidationError as ve:
        raise HTTPException(status_code=422, detail=ve.errors())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


