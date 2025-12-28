# code_executor.py

import subprocess
import sys
import traceback

def run_code(code: str) -> str:
    """Execute Python code and return output or error"""
    try:
        # Create a safe execution environment
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            return result.stdout.strip() or "Code executed successfully (no output)"
        else:
            return f"Error: {result.stderr.strip()}"
    except subprocess.TimeoutExpired:
        return "Error: Code execution timed out (max 10 seconds)"
    except Exception as e:
        return f"Error executing code: {str(e)}"

def debug_code(code: str) -> str:
    """Attempt to debug code and provide suggestions"""
    try:
        # Try to compile the code to check for syntax errors
        compile(code, "<string>", "exec")
        return "Code syntax is valid. Try running it to see runtime errors."
    except SyntaxError as e:
        return f"Syntax Error: {e.msg} at line {e.lineno}\n{e.text}"
    except Exception as e:
        return f"Error analyzing code: {str(e)}"

