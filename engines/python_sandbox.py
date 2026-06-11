import sys
import io

def run_python_code(code):
    """
    Python code execute karke uska output capture karta hai.
    """
    # Standard output ko divert karne ke liye
    output_capture = io.StringIO()
    original_stdout = sys.stdout
    sys.stdout = output_capture
    
    try:
        # Code run karo
        exec(code)
        result = output_capture.getvalue()
        sys.stdout = original_stdout # Reset
        return {"stdout": result, "error": None}
    except Exception as e:
        sys.stdout = original_stdout # Reset
        return {"stdout": None, "error": str(e)}
