import uvicorn

if __name__ == "__main__":
    print("Starting Telecom Support Triage Agent...")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
