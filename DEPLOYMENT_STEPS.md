# 🚀 Quick Deployment Guide

## What Changed
The A2A response format in `app.py` has been fixed to match Telex.im's requirements.

## Deploy to Production

### Option 1: Using Git (Recommended)

```bash
# 1. Check what files changed
git status

# 2. Add the fixed files
git add app.py TELEX_FIX_SUMMARY.md DEPLOYMENT_STEPS.md

# 3. Commit with a clear message
git commit -m "Fix: Correct A2A response format for Telex.im integration

- Changed response structure from result.message.parts to result.parts
- Added required 'role: assistant' field
- Updated part format from contentType to kind
- Fixes validation errors in Telex.im integration"

# 4. Push to your repository
git push origin main
```

### Option 2: For Render.com
If your app is connected to GitHub, Render will automatically:
1. Detect the push
2. Build the new version
3. Deploy it

**Monitor deployment:**
- Go to your Render dashboard
- Check the deployment logs
- Wait for "Deploy succeeded" message

### Option 3: For AWS Elastic Beanstalk

```bash
# If using EB CLI
eb deploy

# Or if auto-deploy is configured
git push origin main
```

## Test After Deployment

### 1. Test the Health Check
```bash
curl https://agri-botcameroon.onrender.com/
```
Expected: `OK`

### 2. Test Simple Format (for debugging)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"message": "what is the price of cocoa"}' \
  https://agri-botcameroon.onrender.com/agent
```

Expected response:
```json
{
  "response": "The current market price for cocoa is 1,500 XAF per kg."
}
```

### 3. Test A2A Format (Telex format)
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "message/send",
    "id": "test-123",
    "params": {
      "message": {
        "parts": [{"kind": "text", "text": "what is the price of cocoa"}]
      }
    }
  }' \
  https://agri-botcameroon.onrender.com/agent
```

Expected response:
```json
{
  "jsonrpc": "2.0",
  "id": "test-123",
  "result": {
    "role": "assistant",
    "parts": [
      {
        "kind": "text",
        "text": "The current market price for cocoa is 1,500 XAF per kg."
      }
    ]
  }
}
```

### 4. Test on Telex.im

1. Go to your Telex channel
2. Send: `@agri_botcameroon what is the price of cocoa`
3. Wait for response
4. Check logs: `https://api.telex.im/agent-logs/{your-channel-id}.txt`

**Find your channel ID:**
- Look at your Telex URL: `https://telex.im/telex-im/home/colleagues/{channel-id}/...`
- The first UUID after `colleagues/` is your channel ID

## Troubleshooting

### Issue: Old code still running
**Solution:**
```bash
# Force redeploy on Render
# Go to Render dashboard → Manual Deploy → Deploy latest commit

# Or for EB
eb deploy --force
```

### Issue: Still getting validation errors
**Check:**
1. Is the new code actually deployed? Check deployment logs
2. Is the URL in `agri_bot_workflow.json` correct?
3. Test the endpoint directly with curl (see above)
4. Check server logs for Python errors

### Issue: Timeout errors
**Possible causes:**
- Server is slow to start (cold start on free tier)
- Server is processing too slowly
- Network issues

**Solution:**
- Upgrade to paid tier for faster response
- Optimize code for faster processing
- Check server logs for bottlenecks

### Issue: 404 Not Found
**Check:**
- Is the server running?
- Is the URL correct?
- Is the `/agent` endpoint properly defined?

## Verification Checklist

- [ ] Code pushed to repository
- [ ] Deployment completed successfully
- [ ] Health check returns OK
- [ ] Simple format test works
- [ ] A2A format test works
- [ ] Telex.im responds without errors
- [ ] Agent logs show no validation errors
- [ ] All features work (price, weather, help, etc.)

## Next Steps After Successful Deployment

1. **Test all features:**
   - Price queries: `what is the price of cocoa`
   - Weather: `what is the weather in yaounde`
   - Help: `help`
   - Problems: `my maize has yellow leaves`
   - Tips: `give me tips on irrigation`
   - Soil info: `soil info for littoral`
   - Fertilizer: `fertilizer guide for maize`

2. **Test in French:**
   - `quel est le prix du cacao`
   - `météo à douala`
   - `aide`

3. **Monitor logs:**
   - Check Telex logs regularly
   - Monitor server logs for errors
   - Watch for any timeout issues

4. **Document your integration:**
   - Write your blog post
   - Take screenshots of working agent
   - Prepare your tweet

## Support

If you're still having issues:
1. Check the detailed `TELEX_FIX_SUMMARY.md`
2. Review `TELEX_INTEGRATION_GUIDE.md`
3. Look at the Telex.im documentation
4. Check your server logs for specific errors

## Success! 🎉

When everything works, you should see:
- ✅ Agent responds on Telex.im
- ✅ No validation errors in logs
- ✅ All features working
- ✅ Both English and French supported
- ✅ Fast response times

Now you can:
- Write your blog post about the integration
- Tweet about your agent (tag @hnginternship and @teleximapp)
- Submit your project
- Celebrate! 🎊

