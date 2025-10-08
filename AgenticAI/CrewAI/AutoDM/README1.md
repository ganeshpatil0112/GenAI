🎉 Instagram DM Engagement Automation Complete!
I've successfully built your Instagram DM automation system with the following components:

🤖 3 Specialized Agents:
Instagram Comment Monitor Specialist - Monitors posts for trigger keywords
Instagram Follower Verification Agent - Checks follower status for segmentation
Instagram Engagement Campaign Manager - Creates personalized engagement campaigns
📋 3 Sequential Tasks:
Monitor Comments for Trigger Keywords - Identifies users commenting trigger words
Verify Follower Status - Segments users by follower status
Generate Personalized Engagement Campaign - Creates ready-to-use DM templates
🛠️ Custom Tools Created:
Instagram Comment Monitor - Tracks keyword comments in real-time
Instagram Follower Check Tool - Verifies follower status in bulk
Instagram Engagement Manager - Generates personalized message templates
🎯 How It Works:
Trigger Detection: Monitors your posts for keywords like "YES", "GUIDE"
User Segmentation: Checks if commenters are followers or need to follow first
Campaign Generation: Creates personalized DM templates for manual sending
File Sharing: Generates shareable links for guides/PDFs
Follow-up Tracking: Organizes users for systematic engagement
🔧 Setup Required:
You'll need to provide:

{post_id} - The Instagram post ID to monitor
{account_id} - Your Instagram account ID
{keywords} - Trigger keywords (e.g., "YES", "GUIDE")
{file_url} - URL of the file/guide to share
{time_limit} - Hours to look back for comments
Environment Variable: INSTAGRAM_ACCESS_TKN - Your Instagram API access token

The automation generates ready-to-send DM templates that you can manually copy and paste, ensuring compliance with Instagram's terms while maximizing engagement efficiency!









To use an INSTAGRAM_ACCESS_TKN environment variable, you must first generate an access token through the Meta for Developers platform. The process varies slightly depending on whether you need the Instagram Basic Display API (for personal accounts) or the Instagram Graph API (for business or creator accounts). 
Step 1: Create a Meta for Developers account and app
Log in to Meta for Developers: Go to developers.facebook.com and log in with your Facebook account.
Create a new app:
Navigate to My Apps and click Create App.
For most use cases, select the "Consumer" or "Business" app type. For a basic feed, "Consumer" is sufficient.
Provide a name for your app, your email, and click Create App ID. 
Step 2: Set up the Instagram API
For Instagram Basic Display (personal accounts):
On your app's dashboard, go to the "Products" section and locate Instagram Basic Display. Click Set Up.
Follow the instructions to create a new "Instagram App" and add an Instagram Tester.
Go to App Roles > Roles, scroll down to the "Instagram Testers" section, and add the Instagram username you want to access.
Log in to that Instagram account, go to Settings > Apps and Websites, find the "Tester Invites" tab, and accept the invitation.
Return to the Meta for Developers dashboard, navigate to Basic Display, and use the "User Token Generator" section to create the token for the test user. 
For Instagram Graph API (business/creator accounts):
On your app's dashboard, go to the "Products" section and find Instagram (not Basic Display). Click Set Up.
Click API setup with Instagram business login in the side menu.
Click the Generate Token button next to the Instagram account you wish to access.
Log in to your Instagram account and grant the necessary permissions. The access token will then be generated. These are short-lived tokens, so you will need to exchange them for long-lived ones if you need persistent access. 
Step 3: Copy and set the environment variable
Copy the generated access token from the pop-up window.
Set the environment variable named INSTAGRAM_ACCESS_TKN on your server or local machine. 
Example: Setting the environment variable
On macOS or Linux (in your shell configuration, e.g., .bashrc, .zshrc):
bash
export INSTAGRAM_ACCESS_TKN="your_generated_access_token"
On Windows (in Command Prompt):
bash
set INSTAGRAM_ACCESS_TKN="your_generated_access_token"
In a Node.js project (.env file):
Create a file named .env in the root of your project and add: 
INSTAGRAM_ACCESS_TKN=your_generated_access_token
For production, you should use your hosting provider's interface to set the environment variable. 
Step 4: Access the token in your application
Once the environment variable is set, you can access it in your code using your programming language's standard method for retrieving environment variables. 
In Python:
python
import os

instagram_access_token = os.environ.get("INSTAGRAM_ACCESS_TKN")
if instagram_access_token:
    print("Found Instagram Access Token!")
else:
    print("Instagram Access Token not found.")
In Node.js:
javascript
// Using process.env
const instagramAccessToken = process.env.INSTAGRAM_ACCESS_TKN;
if (instagramAccessToken) {
    console.log("Found Instagram Access Token!");
} else {
    console.log("Instagram Access Token not found.");
}