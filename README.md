# 🎧 Music Mood Mixer

AI-powered web application that finds the perfect songs based on your mood or emoji input using AWS Bedrock Claude and YouTube.

## ✨ Features

- 🤖 **AI Mood Analysis** - Uses AWS Bedrock Claude 3 Haiku to interpret your mood
- 😊 **Emoji Support** - Works with text moods AND emojis (😊, 😢, 🔥, etc.)
- 🎵 **Real Songs** - Finds actual individual songs (not playlists)
- ▶️ **Direct Playback** - Play full songs directly in the app
- 🎯 **Single Playback** - Only one song plays at a time
- 🚀 **Fast & Lightweight** - 263MB Docker image, ~1.5s response time

## 🛠️ Tech Stack

- **Backend**: Flask, Python 3.12
- **AI**: AWS Bedrock (Claude 3 Haiku)
- **Music**: YouTube Data API v3
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Docker, AWS App Runner
- **Secrets**: AWS Secrets Manager

## 📋 Prerequisites

1. **AWS Account** with:
   - AWS Bedrock access (Claude 3 Haiku enabled in us-east-1)
   - IAM credentials or IAM role

2. **YouTube Data API Key**:
   - Go to [Google Cloud Console](https://console.cloud.google.com)
   - Enable YouTube Data API v3
   - Create API Key

## 🚀 Quick Start

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AI_Project_Part2
```

2. **Set environment variables**
```bash
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
export AWS_REGION="us-east-1"
export YOUTUBE_API_KEY="your-youtube-key"
```

3. **Run with Docker**
```bash
docker build -t music-mood-mixer .
docker run -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID \
  -e AWS_SECRET_ACCESS_KEY \
  -e AWS_REGION \
  -e YOUTUBE_API_KEY \
  music-mood-mixer
```

4. **Open your browser**
```
http://localhost:8080
```

## ☁️ AWS Deployment

### Step 1: Build and Push to ECR

```bash
# Set your AWS account ID
AWS_ACCOUNT_ID="your-account-id"

# Create ECR repository
aws ecr create-repository --repository-name music-mood-mixer --region us-east-1

# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Build and push
docker build -t music-mood-mixer .
docker tag music-mood-mixer:latest \
  $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/music-mood-mixer:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/music-mood-mixer:latest
```

### Step 2: Store YouTube API Key in Secrets Manager

```bash
aws secretsmanager create-secret \
    --name youtube-api-key \
    --secret-string '{"api_key":"your-youtube-api-key"}' \
    --region us-east-1
```

### Step 3: Create IAM Role for App Runner

Create an IAM role with these policies:

**bedrock-policy.json** (attach to AppRunnerInstanceRole)
```bash
aws iam put-role-policy \
    --role-name AppRunnerInstanceRole \
    --policy-name BedrockAccess \
    --policy-document file://bedrock-policy.json
```

**secrets-manager-policy.json** (attach to AppRunnerInstanceRole)
```bash
aws iam put-role-policy \
    --role-name AppRunnerInstanceRole \
    --policy-name SecretsManagerAccess \
    --policy-document file://secrets-manager-policy.json
```

### Step 4: Deploy to App Runner

1. Go to AWS App Runner Console
2. Create a new service
3. Choose "Container registry" → "Amazon ECR"
4. Select your image URI
5. Configure:
   - Port: 8080
   - IAM role: AppRunnerInstanceRole
6. Deploy!

## 📁 Project Structure

```
.
├── app.py                          # Flask application
├── ai_helper.py                    # AWS Bedrock & YouTube integration
├── secrets_helper.py               # AWS Secrets Manager helper
├── templates/
│   └── index.html                  # Frontend UI
├── requirements.txt                # Python dependencies
├── Dockerfile                      # Multi-stage Alpine build
├── bedrock-policy.json            # IAM policy for Bedrock
├── secrets-manager-policy.json    # IAM policy for Secrets Manager
├── .gitignore                     # Git ignore rules
└── README.md                      # This file
```

## 🎮 How to Use

1. **Enter your mood** - Type any mood (happy, sad, energetic, chill, romantic, etc.)
2. **Or use emojis** - Try 😊, 😢, 🔥, 💪, 🌙, etc.
3. **Click "Find Music"** - AI analyzes your mood
4. **Get 5 songs** - Individual songs matching your mood
5. **Click "▶ Play Song"** - Listen directly in the app

## 🔐 Security Notes

- ✅ All secrets stored in AWS Secrets Manager
- ✅ IAM roles used (no hardcoded credentials)
- ✅ `.gitignore` protects sensitive files
- ✅ Sandboxed iframe prevents redirects
- ✅ Environment variables for local dev

## 📊 Performance

- **Response Time**: ~1.5 seconds
- **Docker Image**: 263MB (Alpine-based)
- **Memory Usage**: ~100MB
- **AI Model**: Claude 3 Haiku (fast, cost-effective)

## 🐛 Troubleshooting

### "Access Denied" for Bedrock
- Ensure Claude 3 Haiku is enabled in us-east-1
- Check IAM role has `bedrock:InvokeModel` permission
- Verify the policy is attached to AppRunnerInstanceRole

### "YouTube API quota exceeded"
- YouTube Data API has daily quotas
- Consider requesting quota increase
- Or use caching to reduce API calls

### "Secrets not found"
- Check secret name is `youtube-api-key`
- Verify IAM role has `secretsmanager:GetSecretValue`
- Ensure secret is in the same region (us-east-1)

## 📝 License

MIT License - Feel free to use for personal or educational purposes.

## 🎯 Future Improvements

- [ ] Add caching for frequent mood queries
- [ ] Implement user favorites/history
- [ ] Add more music sources (Spotify API)
- [ ] Support multiple languages
- [ ] Add playlist creation feature

---

**Built with ❤️ using AWS Bedrock AI and YouTube**
