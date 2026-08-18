import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from prompts.templates import validate_answer, NO_CONTEXT_RESPONSE

t1 = validate_answer("Generally speaking, the capital of France is Paris.", "some pdf context")
print("Test 1 hallucination signal  :", "BLOCKED OK" if t1 == NO_CONTEXT_RESPONSE else "FAILED - " + t1[:60])

t2 = validate_answer("The answer is yes.", "No relevant context found.")
print("Test 2 empty context         :", "BLOCKED OK" if t2 == NO_CONTEXT_RESPONSE else "FAILED - " + t2[:60])

t3 = validate_answer("The revenue was 50 million in 2023.", "revenue was 50 million in 2023")
print("Test 3 valid answer passes   :", "PASSED OK" if t3 != NO_CONTEXT_RESPONSE else "FAILED")

t4 = validate_answer("I don't have information about that in the uploaded documents.", "")
print("Test 4 LLM self-declined     :", "PASSED OK" if t4 == NO_CONTEXT_RESPONSE else "FAILED")

t5 = validate_answer("I typically believe that water is H2O.", "some pdf content here")
print("Test 5 typically keyword     :", "BLOCKED OK" if t5 == NO_CONTEXT_RESPONSE else "FAILED - " + t5[:60])

print("")
print("All validation tests complete!")
