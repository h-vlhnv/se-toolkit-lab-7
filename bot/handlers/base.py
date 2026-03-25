"""Base command handlers for the LMS Telegram Bot.

Each handler is a pure function that takes input parameters and returns a text response.
"""


def handle_start() -> str:
    """Handle /start command.
    
    Returns:
        Welcome message for new users.
    """
    return (
        "👋 Welcome to the LMS Bot!\n\n"
        "I can help you interact with the Learning Management System.\n\n"
        "Available commands:\n"
        "/help - Show all available commands\n"
        "/health - Check backend system status\n"
        "/labs - List available labs\n"
        "/scores <lab> - Get scores for a specific lab\n\n"
        "You can also ask questions in plain language!"
    )


def handle_help() -> str:
    """Handle /help command.
    
    Returns:
        List of available commands with descriptions.
    """
    return (
        "📚 Available Commands:\n\n"
        "/start - Welcome message and bot introduction\n"
        "/help - Show this help message\n"
        "/health - Check backend system status\n"
        "/labs - List all available labs\n"
        "/scores <lab_name> - Get scores for a specific lab (e.g., /scores lab-04)\n\n"
        "💡 You can also ask questions in plain language:\n"
        "• \"What labs are available?\"\n"
        "• \"Show me my score for lab-04\"\n"
        "• \"Is the backend working?\""
    )


def handle_health() -> str:
    """Handle /health command.
    
    Returns:
        Backend system health status.
    """
    # Placeholder - will be implemented in Task 2
    return "🏥 Backend Status: Checking...\n\n[Backend integration pending - will show real status in next iteration]"


def handle_labs() -> str:
    """Handle /labs command.
    
    Returns:
        List of available labs.
    """
    # Placeholder - will be implemented in Task 2
    return "📋 Available Labs:\n\n[Labs list pending - will fetch from backend in next iteration]"


def handle_scores(lab_name: str | None = None) -> str:
    """Handle /scores command.
    
    Args:
        lab_name: Optional lab name to get scores for.
        
    Returns:
        Scores information for the specified lab or general scores overview.
    """
    if lab_name:
        return f"📊 Scores for {lab_name}:\n\n[Scores pending - will fetch from backend in next iteration]"
    return "📊 Scores Overview:\n\nPlease specify a lab name: /scores <lab_name>\nExample: /scores lab-04"


def handle_text(user_message: str) -> str:
    """Handle plain text messages using LLM for intent routing.
    
    Args:
        user_message: The user's text message.
        
    Returns:
        Response based on detected intent.
    """
    # Placeholder - will be implemented in Task 3 with LLM integration
    return (
        f"💬 I received your message: \"{user_message}\"\n\n"
        "[Natural language processing pending - will use LLM for intent routing in Task 3]"
    )
