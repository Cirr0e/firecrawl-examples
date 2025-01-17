import asyncio
import os
from dotenv import load_dotenv
from api_assistant import APIIntegrationAssistant

load_dotenv()

async def monitor_github():
    """Example of monitoring the GitHub API."""
    assistant = APIIntegrationAssistant(os.getenv("FIRECRAWL_API_KEY"))
    
    # Discover GitHub API endpoints
    api_info = await assistant.discover_api("https://api.github.com/docs")
    print("\nDiscovered API Information:")
    print(f"Base URL: {api_info.base_url}")
    print(f"Auth Method: {api_info.auth_method}")
    print("\nEndpoints:")
    for endpoint in api_info.endpoints[:5]:  # Show first 5 endpoints
        print(f"- {endpoint.method} {endpoint.path}")
        if endpoint.rate_limit:
            print(f"  Rate Limit: {endpoint.rate_limit}")
    
    # Start monitoring
    print("\nStarting API monitoring...")
    await assistant.monitor_api("https://api.github.com")
    
    # Monitor for 5 minutes
    for _ in range(5):
        await asyncio.sleep(60)
        stats = assistant.get_monitoring_stats("https://api.github.com")
        print("\nMonitoring Stats:")
        print(f"Average Response Time: {stats['average_response_time']:.3f}s")
        print(f"Error Count: {stats['error_count']}")
        if stats['recent_errors']:
            print("Recent Errors:")
            for error in stats['recent_errors']:
                print(f"- {error['timestamp']}: {error.get('error', error.get('message', 'Unknown error'))}")
    
    # Stop monitoring
    await assistant.stop_monitoring("https://api.github.com")
    print("\nMonitoring stopped")

if __name__ == "__main__":
    asyncio.run(monitor_github())