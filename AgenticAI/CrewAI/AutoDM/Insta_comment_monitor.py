"""
Crafting a customized tool for your automation
Create an Instagram Comment Monitor Tool that can:
1. Monitor Instagram posts and stories for specific keywords (like "YES", "GUIDE", etc.)
2. Use Instagram Basic Display API or Graph API to fetch comments
3. Return a list of users who commented with the target keywords
4. Include user information like username, user_id, and comment text
5. Filter comments by time range if needed
6. Handle API authentication using environment variables like INSTAGRAM_ACCESS_TOKEN

The tool should accept parameters:
- post_id: The Instagram post ID to monitor
- keywords: List of keywords to look for (default: ["YES", "GUIDE"])
- time_limit: How far back to check comments (in hours, default: 24)

Return format should be a list of dictionaries with user info and comment details.
Instagram Comment Monitor created
Monitors Instagram posts for comments containing specific keywords and returns user information who commented with those keywords
"""


from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, List, Dict, Any
import requests
import json
from datetime import datetime, timedelta

class InstagramCommentMonitorInput(BaseModel):
    """Input schema for Instagram Comment Monitor Tool."""
    post_id: str = Field(..., description="The Instagram post ID to monitor")
    keywords: List[str] = Field(default=["YES", "GUIDE"], description="List of keywords to look for in comments")
    time_limit: int = Field(default=24, description="How far back to check comments (in hours)")

class InstagramCommentMonitorTool(BaseTool):
    """Tool for monitoring Instagram posts and stories for specific keywords in comments."""

    name: str = "instagram_comment_monitor"
    description: str = (
        "Monitors Instagram posts for comments containing specific keywords. "
        "Returns a list of users who commented with the target keywords, "
        "including their username, user_id, and comment text. "
        "Requires INSTAGRAM_ACCESS_TKN environment variable for authentication."
    )
    args_schema: Type[BaseModel] = InstagramCommentMonitorInput

    def _run(self, post_id: str, keywords: List[str] = None, time_limit: int = 24) -> str:
        """
        Monitor Instagram post comments for specific keywords.
        
        Args:
            post_id: The Instagram post ID to monitor
            keywords: List of keywords to look for (default: ["YES", "GUIDE"])
            time_limit: How far back to check comments (in hours, default: 24)
            
        Returns:
            JSON string containing list of matching comments with user info
        """
        try:
            import os
            
            # Get access token from environment variables
            access_token = os.getenv('INSTAGRAM_ACCESS_TKN')
            if not access_token:
                return json.dumps({
                    "error": "INSTAGRAM_ACCESS_TKN environment variable is required",
                    "status": "failed"
                })
            
            # Set default keywords if none provided
            if keywords is None:
                keywords = ["YES", "GUIDE"]
            
            # Calculate time cutoff
            time_cutoff = datetime.now() - timedelta(hours=time_limit)
            
            # Instagram Basic Display API endpoint for media comments
            comments_url = f"https://graph.instagram.com/{post_id}/comments"
            
            # Parameters for the API request
            params = {
                'access_token': access_token,
                'fields': 'id,text,username,timestamp'
            }
            
            # Make request to Instagram API
            response = requests.get(comments_url, params=params, timeout=30)
            
            if response.status_code != 200:
                return json.dumps({
                    "error": f"Instagram API error: {response.status_code} - {response.text}",
                    "status": "failed"
                })
            
            data = response.json()
            
            if 'data' not in data:
                return json.dumps({
                    "error": "No comments data received from Instagram API",
                    "status": "failed"
                })
            
            matching_comments = []
            
            # Process each comment
            for comment in data.get('data', []):
                try:
                    # Parse comment timestamp
                    comment_time = datetime.fromisoformat(comment['timestamp'].replace('Z', '+00:00'))
                    
                    # Check if comment is within time limit
                    if comment_time < time_cutoff:
                        continue
                    
                    # Check if comment contains any of the keywords (case insensitive)
                    comment_text = comment.get('text', '').upper()
                    keywords_upper = [keyword.upper() for keyword in keywords]
                    
                    matching_keywords = [keyword for keyword in keywords_upper if keyword in comment_text]
                    
                    if matching_keywords:
                        matching_comments.append({
                            "comment_id": comment.get('id'),
                            "username": comment.get('username'),
                            "comment_text": comment.get('text'),
                            "timestamp": comment.get('timestamp'),
                            "matching_keywords": matching_keywords,
                            "post_id": post_id
                        })
                        
                except (ValueError, KeyError) as e:
                    # Skip malformed comments
                    continue
            
            # Return results
            result = {
                "status": "success",
                "post_id": post_id,
                "keywords_searched": keywords,
                "time_limit_hours": time_limit,
                "matching_comments": matching_comments,
                "total_matches": len(matching_comments)
            }
            
            return json.dumps(result, indent=2)
            
        except requests.exceptions.RequestException as e:
            return json.dumps({
                "error": f"Network error while accessing Instagram API: {str(e)}",
                "status": "failed"
            })
        except Exception as e:
            return json.dumps({
                "error": f"Unexpected error: {str(e)}",
                "status": "failed"
            })