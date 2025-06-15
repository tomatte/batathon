from fastmcp import FastMCP

from chatbot.mcp.servers import test_mcp, utils_mcp

mcp = FastMCP(name="Hype Server")

mcp.mount("utils", utils_mcp.mcp)

if __name__ == "__main__":
    # This runs the server, defaulting to STDIO transport
    mcp.run()