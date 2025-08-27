# Fallback question bank (used if LLM JSON parsing fails)
BANK = {
    "python": [
        "Explain list vs tuple. When would you use each?",
        "What are list, set, and dict comprehensions? Give examples.",
        "What is a generator? How does 'yield' work?",
        "How does GIL impact multithreading in Python?",
        "Time complexity of common list and dict operations?",
    ],
    "django": [
        "Explain Django's MVT architecture.",
        "How do migrations work? How do you create and run them?",
        "What are QuerySets? Explain select_related vs prefetch_related.",
        "How do you implement authentication/authorization in Django?",
        "How do you secure a Django app against CSRF and SQL injection?",
    ],
    "javascript": [
        "Explain 'this' binding and arrow functions.",
        "What is event loop? How do microtasks/macrotasks work?",
        "Difference between var, let, and const?",
        "What are closures? Give a practical use case.",
        "How do promises differ from async/await?",
    ],
    "react": [
        "Explain reconciliation and keys in lists.",
        "What are hooks? Explain useEffect dependency traps.",
        "How to optimize performance with memo, useMemo, useCallback?",
        "Controlled vs uncontrolled components?",
        "Client-side routing vs server-side rendering tradeoffs?",
    ],
    "sql": [
        "Explain normalization (1NF-3NF) and denormalization trade-offs.",
        "Inner vs left vs right join with examples.",
        "How does indexing work? Pros and cons.",
        "Detecting and handling slow queries?",
        "ACID properties and transaction isolation levels?",
    ]
}
