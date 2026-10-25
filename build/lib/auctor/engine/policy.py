class PolicyEngine:
    @staticmethod
    def validate_action(mandate: dict, tool_name: str) -> bool:
        # Check signature (simplified for now)
        # Check tool in capabilities
        tools = mandate.get("capabilities", {}).get("tools", [])
        return tool_name in tools
