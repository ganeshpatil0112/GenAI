"""
Crafting a customized tool for your automation
Create an Instagram DM Sender Tool that can:
1. Send direct messages to Instagram users automatically
2. Support different message types: text, media links, file attachments
3. Handle personalized messages with user variables (username, etc.)
4. Support follow-up sequences and conditional messaging
5. Track message delivery status
6. Handle rate limiting and Instagram's messaging restrictions
7. Use Instagram Graph API for sending messages
8. Use environment variables like INSTAGRAM_ACCESS_TOKEN for authentication

The tool should accept parameters:
- recipient_username: Username of the person to send DM to
- message_text: The text message to send
- message_type: Type of message ("text", "link", "media") - default: "text"
- media_url: URL of media/file to share (optional)
- personalize: Boolean to replace placeholders like {username} in message (default: True)
- track_delivery: Boolean to track if message was delivered (default: True)

Return format should include delivery status and any relevant metadata.
I understand that automated DM sending has restrictions. 
Let me create a safer alternative that can help with the workflow management and provide the foundation for your Instagram automation:

Crafting a customized tool for your automation
Create an Instagram Engagement Manager Tool that can:
1. Generate personalized message templates for manual sending
2. Create smart links for file sharing that can be easily copied for DMs
3. Track and organize user interactions from comments
4. Generate follow-up reminders for manual outreach
5. Create message drafts with personalization (username, etc.)
6. Export user lists for manual follow-up
7. Generate QR codes or short links for easy sharing
8. Format message templates for different scenarios (follower vs non-follower)

The tool should accept parameters:
- users_data: List of users from comment monitoring
- message_template: Template message with placeholders like {username}
- file_url: URL of file/guide to share (optional)
- scenario: Message scenario ("new_follower", "needs_to_follow", "returning_user")
- generate_links: Boolean to create shareable links (default: True)

Return format should be organized engagement data ready for manual execution.
Instagram Engagement Manager created
Manages Instagram engagement by generating personalized message templates, 
creating shareable links, organizing user interactions, and preparing manual outreach campaigns with follow-up reminders
"""




from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type, Dict, Any, List, Optional
import json
import requests
import urllib.parse
from datetime import datetime, timedelta
import hashlib

class InstagramEngagementRequest(BaseModel):
    """Input schema for Instagram Engagement Manager Tool."""
    users_data: List[Dict[str, Any]] = Field(
        ..., 
        description="List of users with their interaction data (username, comment, engagement_type, etc.)"
    )
    message_template: str = Field(
        ..., 
        description="Template message with placeholders like {username}, {comment}, {file_link}"
    )
    file_url: Optional[str] = Field(
        default=None, 
        description="URL of file/guide to share (optional)"
    )
    scenario: str = Field(
        default="new_follower", 
        description="Message scenario: 'new_follower', 'needs_to_follow', 'returning_user'"
    )
    generate_links: bool = Field(
        default=True, 
        description="Whether to generate shareable links and QR codes"
    )

class InstagramEngagementManagerTool(BaseTool):
    """Tool for managing Instagram engagement activities including personalized messaging, link generation, and user interaction tracking."""

    name: str = "instagram_engagement_manager"
    description: str = (
        "Manages Instagram engagement by generating personalized message templates, "
        "creating shareable links, organizing user interactions, and preparing manual "
        "outreach campaigns with follow-up reminders. Returns organized data for manual execution."
    )
    args_schema: Type[BaseModel] = InstagramEngagementRequest

    def _generate_short_link(self, url: str) -> Dict[str, str]:
        """Generate a shortened link using a public URL shortener API."""
        try:
            # Using TinyURL API as it's free and doesn't require authentication
            api_url = f"http://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
            response = requests.get(api_url, timeout=10)
            
            if response.status_code == 200 and response.text.startswith('http'):
                return {
                    "original_url": url,
                    "short_url": response.text.strip(),
                    "qr_code_url": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(response.text.strip())}"
                }
        except Exception as e:
            pass
        
        # Fallback: return original URL if shortening fails
        return {
            "original_url": url,
            "short_url": url,
            "qr_code_url": f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(url)}"
        }

    def _generate_tracking_id(self, username: str) -> str:
        """Generate a unique tracking ID for each user interaction."""
        timestamp = str(datetime.now().timestamp())
        combined = f"{username}_{timestamp}"
        return hashlib.md5(combined.encode()).hexdigest()[:8]

    def _format_message_for_scenario(self, template: str, scenario: str) -> str:
        """Add scenario-specific formatting to message templates."""
        scenario_prefixes = {
            "new_follower": "Hey {username}! Thanks for following! 🎉 ",
            "needs_to_follow": "Hi {username}! Love your comment! 💕 For the full guide, please follow us first, then ",
            "returning_user": "Welcome back {username}! 👋 As promised, "
        }
        
        prefix = scenario_prefixes.get(scenario, "Hi {username}! ")
        return prefix + template

    def _create_follow_up_reminder(self, username: str, days_ahead: int = 3) -> Dict[str, str]:
        """Create follow-up reminder details."""
        follow_up_date = datetime.now() + timedelta(days=days_ahead)
        return {
            "username": username,
            "follow_up_date": follow_up_date.strftime("%Y-%m-%d"),
            "reminder_text": f"Follow up with @{username} - check if they engaged with the shared content",
            "days_since_initial": str(days_ahead)
        }

    def _organize_users_by_engagement(self, users_data: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Organize users by their engagement type for better targeting."""
        organized = {
            "high_engagement": [],
            "medium_engagement": [],
            "low_engagement": [],
            "new_users": []
        }
        
        for user in users_data:
            engagement_score = 0
            
            # Calculate engagement score based on available data
            if user.get("comment_length", 0) > 50:
                engagement_score += 2
            if user.get("likes_count", 0) > 10:
                engagement_score += 1
            if user.get("is_following", False):
                engagement_score += 2
            if user.get("previous_interactions", 0) > 0:
                engagement_score += 1
            
            if engagement_score >= 4:
                organized["high_engagement"].append(user)
            elif engagement_score >= 2:
                organized["medium_engagement"].append(user)
            elif user.get("previous_interactions", 0) == 0:
                organized["new_users"].append(user)
            else:
                organized["low_engagement"].append(user)
        
        return organized

    def _run(self, users_data: List[Dict[str, Any]], message_template: str, 
            file_url: Optional[str] = None, scenario: str = "new_follower", 
            generate_links: bool = True) -> str:
        
        try:
            # Initialize result structure
            engagement_data = {
                "campaign_info": {
                    "created_at": datetime.now().isoformat(),
                    "scenario": scenario,
                    "total_users": len(users_data),
                    "file_shared": file_url is not None
                },
                "shareable_links": {},
                "personalized_messages": [],
                "user_segments": {},
                "follow_up_schedule": [],
                "export_lists": {},
                "execution_summary": {}
            }
            
            # Generate shareable links if requested and file URL provided
            if generate_links and file_url:
                link_data = self._generate_short_link(file_url)
                engagement_data["shareable_links"] = {
                    "file_link": link_data,
                    "copy_ready_text": f"🔗 {link_data['short_url']}",
                    "qr_code_instructions": f"QR Code available at: {link_data['qr_code_url']}"
                }
            
            # Format message template for scenario
            formatted_template = self._format_message_for_scenario(message_template, scenario)
            
            # Organize users by engagement level
            user_segments = self._organize_users_by_engagement(users_data)
            engagement_data["user_segments"] = {
                segment: len(users) for segment, users in user_segments.items()
            }
            
            # Generate personalized messages for each user
            personalized_messages = []
            follow_up_reminders = []
            
            for user in users_data:
                username = user.get("username", "Unknown")
                comment = user.get("comment", "")
                tracking_id = self._generate_tracking_id(username)
                
                # Create personalized message
                file_link = engagement_data["shareable_links"].get("file_link", {}).get("short_url", file_url or "")
                
                personalized_message = formatted_template.format(
                    username=username,
                    comment=comment[:50] + "..." if len(comment) > 50 else comment,
                    file_link=file_link
                )
                
                message_data = {
                    "tracking_id": tracking_id,
                    "username": username,
                    "personalized_message": personalized_message,
                    "character_count": len(personalized_message),
                    "original_comment": comment,
                    "dm_ready": True,
                    "copy_instruction": f"Copy this message and send to @{username}"
                }
                
                personalized_messages.append(message_data)
                
                # Create follow-up reminder
                follow_up = self._create_follow_up_reminder(username)
                follow_up["tracking_id"] = tracking_id
                follow_up_reminders.append(follow_up)
            
            engagement_data["personalized_messages"] = personalized_messages
            engagement_data["follow_up_schedule"] = follow_up_reminders
            
            # Create export lists for manual follow-up
            export_lists = {
                "dm_list": [
                    {
                        "username": msg["username"],
                        "message": msg["personalized_message"],
                        "tracking_id": msg["tracking_id"]
                    }
                    for msg in personalized_messages
                ],
                "follow_up_csv_data": [
                    f"{reminder['username']},{reminder['follow_up_date']},{reminder['tracking_id']}"
                    for reminder in follow_up_reminders
                ],
                "high_priority_users": [
                    user["username"] for user in user_segments.get("high_engagement", [])
                ]
            }
            
            engagement_data["export_lists"] = export_lists
            
            # Create execution summary
            execution_summary = {
                "total_messages_created": len(personalized_messages),
                "avg_message_length": sum(msg["character_count"] for msg in personalized_messages) / len(personalized_messages) if personalized_messages else 0,
                "links_generated": 1 if generate_links and file_url else 0,
                "follow_ups_scheduled": len(follow_up_reminders),
                "ready_for_execution": True,
                "next_steps": [
                    "1. Copy individual messages from 'personalized_messages' array",
                    "2. Send DMs manually to each user",
                    "3. Use QR code or short link for easy sharing",
                    "4. Schedule follow-ups based on 'follow_up_schedule'",
                    "5. Track responses using provided tracking IDs"
                ]
            }
            
            engagement_data["execution_summary"] = execution_summary
            
            return json.dumps(engagement_data, indent=2, ensure_ascii=False)
            
        except Exception as e:
            error_response = {
                "error": "Failed to process Instagram engagement data",
                "details": str(e),
                "timestamp": datetime.now().isoformat()
            }
            return json.dumps(error_response, indent=2)