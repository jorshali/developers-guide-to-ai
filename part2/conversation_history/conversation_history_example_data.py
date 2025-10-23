conversation_history = [
    {
        "role": "user",
        "content": (
            "You are a helpful Help Desk Representative. Use the following "
            "support article to answer questions. Only use the provided <articles> "
            "and if an answer can't be found, respond with: "
            "\"I'm sorry I can't help with that. Please email customer support at support@acme.com.\"\n\n"
            "<article>\n"
            "To reset your password, follow these simple steps:\n\n"
            "1. Click on the \"Forgot Password\" link on the login page\n"
            "2. Enter your registered email address\n"
            "3. Check your email for a password reset link\n"
            "4. Click the link in the email (valid for 24 hours)\n"
            "5. Create a new password that meets our security requirements:\n"
            "   - At least 8 characters long\n"
            "   - Contains uppercase and lowercase letters\n"
            "   - Includes at least one number\n"
            "   - Has at least one special character\n\n"
            "If you don't receive the reset email within 5 minutes, please check your\n"
            "spam folder or contact our support team.\n\n"
            "For security reasons, your old password will be immediately invalidated\n"
            "once you create a new one.\n"
            "</article>\n\n"
            "Question: I'm having password issues. Can you help me log in?"
        )
    },
    {
        "role": "assistant",
        "content": (
            "To resolve password issues, you can reset your password by following these steps:\n\n"
            "1. Click on the **'Forgot Password'** link on the login page.\n"
            "2. Enter your registered email address.\n"
            "3. Check your email for a password reset link (valid for 24 hours).\n"
            "4. Click the link and create a new password that:\n"
            "   - Is at least 8 characters long\n"
            "   - Contains uppercase and lowercase letters\n"
            "   - Includes at least one number\n"
            "   - Has at least one special character\n\n"
            "If you don't receive the reset email within 5 minutes, check your spam folder or contact our support team.\n\n"
            "For security reasons, your old password will stop working once you create a new one."
        )
    },
    {
        "role": "user",
        "content": (
            "Using the same article:\n\n"
            "<article>\n"
            "To reset your password, follow these simple steps:\n\n"
            "1. Click on the \"Forgot Password\" link on the login page\n"
            "2. Enter your registered email address\n"
            "3. Check your email for a password reset link\n"
            "4. Click the link in the email (valid for 24 hours)\n"
            "5. Create a new password that meets our security requirements:\n"
            "   - At least 8 characters long\n"
            "   - Contains uppercase and lowercase letters\n"
            "   - Includes at least one number\n"
            "   - Has at least one special character\n\n"
            "If you don't receive the reset email within 5 minutes, please check your\n"
            "spam folder or contact our support team.\n\n"
            "For security reasons, your old password will be immediately invalidated\n"
            "once you create a new one.\n"
            "</article>\n\n"
            "Question: I didn't get my reset email after 10 minutes. What should I do?"
        )
    },
    {
        "role": "assistant",
        "content": (
            "If you don't receive your password reset email within 5 minutes, please check your spam folder. "
            "If it's not there, contact our support team for assistance."
        )
    },
    {
        "role": "user",
        "content": (
            "Using the same article:\n\n"
            "<article>\n"
            "To reset your password, follow these simple steps:\n\n"
            "1. Click on the \"Forgot Password\" link on the login page\n"
            "2. Enter your registered email address\n"
            "3. Check your email for a password reset link\n"
            "4. Click the link in the email (valid for 24 hours)\n"
            "5. Create a new password that meets our security requirements:\n"
            "   - At least 8 characters long\n"
            "   - Contains uppercase and lowercase letters\n"
            "   - Includes at least one number\n"
            "   - Has at least one special character\n\n"
            "If you don't receive the reset email within 5 minutes, please check your\n"
            "spam folder or contact our support team.\n\n"
            "For security reasons, your old password will be immediately invalidated\n"
            "once you create a new one.\n"
            "</article>\n\n"
            "Question: Can I reuse my old password?"
        )
    },
    {
        "role": "assistant",
        "content": (
            "I'm sorry I can't help with that. Please email customer support at support@acme.com."
        )
    }
]
