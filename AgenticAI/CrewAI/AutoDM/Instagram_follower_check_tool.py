"""
Crafting a customized tool for your automation
Create an Instagram Follower Check Tool that can:
1. Check if a specific user is following your Instagram account
2. Use Instagram Basic Display API or Graph API to verify follower status
3. Handle bulk checking of multiple users at once
4. Return follower status for each user checked
5. Include user details like username, user_id, follower_count if available
6. Handle API rate limiting gracefully
7. Use environment variables like INSTAGRAM_ACCESS_TOKEN for authentication

The tool should accept parameters:
- usernames: Single username string or list of usernames to check
- account_id: Your Instagram account ID to check followers against
- include_details: Boolean to include additional user details (default: True)

Return format should be a dictionary with follower status for each user.
Instagram Follower Check Tool created
Checks if specific users are following an Instagram account using Instagram Graph API. 
Supports bulk checking with rate limiting and detailed user information.
"""

from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Union
import requests
import json
import time
from datetime import datetime

class InstagramFollowerCheckRequest(BaseModel):
    """Input schema for Instagram Follower Check Tool."""
    usernames: Union[str, List[str]] = Field(
        ...,
        description="Single username string or list of usernames to check follower status"
    )
    account_id: str = Field(
        ...,
        description="Your Instagram account ID to check followers against"
    )
    include_details: bool = Field(
        default=True,
        description="Boolean to include additional user details like follower count"
    )

class InstagramFollowerCheckTool(BaseTool):
    """Tool for checking if specific users are following an Instagram account using Instagram Graph API."""

    name: str = "Instagram Follower Check Tool"
    description: str = (
        "Checks if specific users are following an Instagram account using Instagram Graph API. "
        "Supports bulk checking with rate limiting and returns detailed follower status information. "
        "Requires INSTAGRAM_ACCESS_TKN environment variable for authentication."
    )
    args_schema: Type[BaseModel] = InstagramFollowerCheckRequest

    def _run(self, usernames: Union[str, List[str]], account_id: str, include_details: bool = True) -> str:
        """
        Check follower status for given usernames against specified Instagram account.
        
        Args:
            usernames: Single username or list of usernames to check
            account_id: Instagram account ID to check followers against
            include_details: Include additional user details in response
            
        Returns:
            JSON string with follower status for each user
        """
        try:
            import os
            access_token = os.getenv('INSTAGRAM_ACCESS_TKN')
            
            if not access_token:
                return json.dumps({
                    "error": "Instagram access token not found. Please set INSTAGRAM_ACCESS_TKN environment variable.",
                    "status": "failed"
                })
            
            # Normalize usernames to list
            if isinstance(usernames, str):
                usernames = [usernames]
            
            results = {}
            
            # First, get the followers of the target account
            followers_data = self._get_account_followers(account_id, access_token)
            
            if "error" in followers_data:
                return json.dumps(followers_data)
            
            follower_usernames = {follower.get('username', '').lower() for follower in followers_data.get('followers', [])}
            follower_details = {follower.get('username', '').lower(): follower for follower in followers_data.get('followers', [])}
            
            # Check each username
            for username in usernames:
                username_lower = username.lower()
                
                try:
                    is_following = username_lower in follower_usernames
                    
                    user_result = {
                        "username": username,
                        "is_following": is_following,
                        "checked_at": datetime.now().isoformat()
                    }
                    
                    if include_details and is_following and username_lower in follower_details:
                        follower_info = follower_details[username_lower]
                        user_result.update({
                            "user_id": follower_info.get('id'),
                            "account_type": follower_info.get('account_type'),
                            "media_count": follower_info.get('media_count')
                        })
                    elif include_details and not is_following:
                        # Try to get user details even if not following
                        user_details = self._get_user_details(username, access_token)
                        if user_details and "error" not in user_details:
                            user_result.update(user_details)
                    
                    results[username] = user_result
                    
                    # Rate limiting - Instagram Graph API allows ~200 requests per hour
                    time.sleep(0.1)  # Small delay between requests
                    
                except Exception as e:
                    results[username] = {
                        "username": username,
                        "error": f"Failed to check user: {str(e)}",
                        "is_following": False,
                        "checked_at": datetime.now().isoformat()
                    }
            
            summary = {
                "total_checked": len(usernames),
                "following_count": sum(1 for result in results.values() if result.get("is_following", False)),
                "results": results,
                "status": "completed"
            }
            
            return json.dumps(summary, indent=2)
            
        except Exception as e:
            return json.dumps({
                "error": f"Tool execution failed: {str(e)}",
                "status": "failed"
            })
    
    def _get_account_followers(self, account_id: str, access_token: str) -> Dict[str, Any]:
        """
        Get followers of the specified Instagram account.
        
        Args:
            account_id: Instagram account ID
            access_token: Instagram access token
            
        Returns:
            Dictionary with followers data or error information
        """
        try:
            # Instagram Graph API endpoint for getting followers
            url = f"https://graph.instagram.com/{account_id}/followers"
            params = {
                'access_token': access_token,
                'fields': 'id,username,account_type,media_count',
                'limit': 100  # Maximum allowed by Instagram API
            }
            
            all_followers = []
            
            while url:
                response = requests.get(url, params=params)
                
                if response.status_code == 429:  # Rate limited
                    time.sleep(60)  # Wait 1 minute before retrying
                    continue
                
                if response.status_code != 200:
                    return {
                        "error": f"Failed to fetch followers. Status: {response.status_code}, Response: {response.text}",
                        "status_code": response.status_code
                    }
                
                data = response.json()
                
                if 'data' not in data:
                    return {
                        "error": f"Unexpected API response format: {data}",
                        "status_code": response.status_code
                    }
                
                all_followers.extend(data['data'])
                
                # Check for pagination
                url = data.get('paging', {}).get('next')
                params = None  # Next URL already contains parameters
                
                # Rate limiting
                time.sleep(0.2)
            
            return {
                "followers": all_followers,
                "total_count": len(all_followers)
            }
            
        except requests.RequestException as e:
            return {
                "error": f"Network error while fetching followers: {str(e)}"
            }
        except Exception as e:
            return {
                "error": f"Unexpected error while fetching followers: {str(e)}"
            }
    
    def _get_user_details(self, username: str, access_token: str) -> Dict[str, Any]:
        """
        Get details for a specific user (if possible).
        Note: Instagram Graph API has limited public user search capabilities.
        
        Args:
            username: Instagram username
            access_token: Instagram access token
            
        Returns:
            Dictionary with user details or empty dict if not accessible
        """
        try:
            # Note: Instagram Graph API doesn't provide public user search
            # This would require the user to grant permissions or be a business account
            # For now, return basic structure
            return {
                "note": "User details not available - user is not following or API limitations",
                "username": username
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get user details: {str(e)}"
            }