# 🎉 Instagram DM Engagement Automation

I've successfully built your Instagram DM automation system with the following components:

## 🤖 3 Specialized Agents
- **Instagram Comment Monitor Specialist**: Monitors posts for trigger keywords
- **Instagram Follower Verification Agent**: Checks follower status for segmentation
- **Instagram Engagement Campaign Manager**: Creates personalized engagement campaigns

## 📋 3 Sequential Tasks
1. **Monitor Comments for Trigger Keywords**: Identifies users commenting trigger words
2. **Verify Follower Status**: Segments users by follower status
3. **Generate Personalized Engagement Campaign**: Creates ready-to-use DM templates

## 🛠️ Custom Tools Created
- **Instagram Comment Monitor**: Tracks keyword comments in real-time
- **Instagram Follower Check Tool**: Verifies follower status in bulk
- **Instagram Engagement Manager**: Generates personalized message templates

## 🎯 How It Works
- **Trigger Detection**: Monitors your posts for keywords like `"YES"`, `"GUIDE"`
- **User Segmentation**: Checks if commenters are followers or need to follow first
- **Campaign Generation**: Creates personalized DM templates for manual sending
- **File Sharing**: Generates shareable links for guides/PDFs
- **Follow-up Tracking**: Organizes users for systematic engagement

## 🔧 Setup Required
You'll need to provide:
- `{post_id}`: The Instagram post ID to monitor
- `{account_id}`: Your Instagram account ID
- `{keywords}`: Trigger keywords (e.g., `"YES"`, `"GUIDE"`)
- `{file_url}`: URL of the file/guide to share
- `{time_limit}`: Hours to look back for comments

**Environment Variable**:
- `INSTAGRAM_ACCESS_TKN`: Your Instagram API access token

---

The automation generates ready-to-send DM templates that you can manually copy and paste, ensuring compliance with Instagram's terms while maximizing engagement efficiency!










from pathlib import Path

# Define the complete README content
readme_content = """# Instagram Access Token Setup Guide

This guide explains how to generate and use the `INSTAGRAM_ACCESS_TKN` environment variable for accessing Instagram APIs via Meta for Developers.

---

## 🔐 Step 1: Create a Meta for Developers Account and App

1. Visit [Meta for Developers](https://developers.facebook.com) and log in with your Facebook account.
2. Navigate to **My Apps** and click **Create App**.
3. Choose the app type:
   - **Consumer**: For personal accounts using Instagram Basic Display API.
   - **Business**: For business or creator accounts using Instagram Graph API.
4. Provide a name for your app, your email, and click **Create App ID**.

---

## ⚙️ Step 2: Set Up the Instagram API

### For Instagram Basic Display (Personal Accounts)

1. In your app dashboard, go to **Products** and click **Set Up** under **Instagram Basic Display**.
2. Follow the instructions to create a new Instagram App and add an Instagram Tester.
3. Go to **App Roles > Roles**, scroll to **Instagram Testers**, and add the Instagram username.
4. Log in to that Instagram account, go to **Settings > Apps and Websites**, and accept the tester invitation.
5. Return to the dashboard and use the **User Token Generator** to create a token for the test user.

### For Instagram Graph API (Business/Creator Accounts)

1. In your app dashboard, go to **Products** and click **Set Up** under **Instagram** (not Basic Display).
2. Click **API Setup with Instagram Business Login** in the side menu.
3. Click **Generate Token** next to the Instagram account you want to access.
4. Log in and grant permissions. A short-lived token will be generated.
5. Exchange it for a long-lived token if persistent access is needed.

---

## 📋 Step 3: Copy and Set the Environment Variable

Copy the generated access token from the pop-up window.

Set the environment variable named `INSTAGRAM_ACCESS_TKN` on your server or local machine.

### Example: Setting the Environment Variable

#### On macOS or Linux (in your shell configuration, e.g., `.bashrc`, `.zshrc`):


export INSTAGRAM_ACCESS_TKN="your_generated_access_token"



## Step 4: Access the Token in Your Application

Once the environment variable is set, you can access it in your code using your programming language's standard method for retrieving environment variables.

### In Python:


```PY
import os

instagram_access_token = os.environ.get("INSTAGRAM_ACCESS_TKN")
if instagram_access_token:
    print("Found Instagram Access Token!")
else:
    print("Instagram Access Token not found.")

```