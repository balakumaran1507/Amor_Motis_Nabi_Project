# 🚀 CTF WRAPPED - QUICK DEPLOYMENT GUIDE

## ✅ WHAT'S READY:
- ✅ 163 personalized cards generated
- ✅ 163 personalized HTML pages created
- ✅ All files in `/Users/neuxdemorphous/Downloads/wrapped_pages/`
- ✅ Total size: 17MB (well within limits)

---

## 📤 STEP 1: DEPLOY TO NETLIFY (5 minutes)

### Method A: Netlify Drop (Easiest - No account needed)

1. **Open Netlify Drop:**
   - Go to: https://app.netlify.com/drop

2. **Drag & Drop:**
   - Open Finder
   - Navigate to `/Users/neuxdemorphous/Downloads/`
   - Drag the `wrapped_pages` folder onto the Netlify Drop page

3. **Wait for deployment:**
   - Takes ~2 minutes
   - Netlify will show: "Your site is live at: https://random-name-12345.netlify.app"

4. **Copy the URL!**
   - Example: `https://luminous-biscuit-abc123.netlify.app`
   - **SAVE THIS URL!**

5. **Test it:**
   - Open: `https://YOUR-URL.netlify.app/LUFFY.html`
   - Should see LUFFY's wrapped page!

### Method B: Netlify with Account (Better for long-term)

1. Go to: https://app.netlify.com
2. Sign up (free) with GitHub/Email
3. Click "Add new site" → "Deploy manually"
4. Drag `wrapped_pages` folder
5. Once deployed, click "Site settings" → "Change site name"
6. Set name to: `cybercom-ctf-wrapped`
7. Your URL: `https://cybercom-ctf-wrapped.netlify.app`

---

## 🔗 STEP 2: UPDATE SHARE LINKS (5 minutes)

The share buttons currently point to a placeholder URL. Let's fix that:

1. **Edit the generation script:**
   ```bash
   cd "/Users/neuxdemorphous/Downloads/files (2)"
   ```

   Open `generate_html_pages.py` in a text editor

2. **Find line 23:**
   ```python
   BASE_URL = "https://cybercom-ctf-wrapped.netlify.app"
   ```

3. **Replace with YOUR actual Netlify URL:**
   ```python
   BASE_URL = "https://luminous-biscuit-abc123.netlify.app"  # YOUR ACTUAL URL
   ```

4. **Regenerate pages:**
   ```bash
   source ctf_venv/bin/activate
   python3 generate_html_pages.py
   ```

5. **Re-upload to Netlify:**
   - Drag `wrapped_pages` folder to Netlify again
   - It will UPDATE the existing site
   - Wait 1 minute

6. **Test share buttons:**
   - Open any player page
   - Click Twitter share button
   - Verify URL is correct

---

## 📧 STEP 3: SET UP EMAIL SYSTEM (15 minutes)

### Option A: Google Sheets + Apps Script (Recommended)

1. **Create Google Sheet:**
   - Go to: https://sheets.google.com
   - Create new sheet: "CTF Wrapped Email List"

2. **Import player data:**
   - Open `/Users/neuxdemorphous/Downloads/player_data.csv`
   - Copy all data
   - Paste into Google Sheet

3. **Set up Apps Script:**
   - In Google Sheets: Extensions → Apps Script
   - Delete existing code
   - Paste this script:

```javascript
function sendCTFWrapped() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
  var data = sheet.getDataRange().getValues();

  // Start from row 2 (skip header)
  for (var i = 1; i < data.length; i++) {
    var username = data[i][0];  // Column A
    var email = data[i][1];     // Column B
    var archetype = data[i][2]; // Column C

    // IMPORTANT: Replace with YOUR Netlify URL
    var wrappedURL = "https://YOUR-URL.netlify.app/" + username + ".html";

    var subject = "🎉 Your CYBERCOM Valentine's CTF Wrapped is Here!";

    var body = "Hi " + username + ",\n\n" +
      "Thank you for participating in CYBERCOM's Valentine's Day CTF!\n\n" +
      "Your personalized CTF Wrapped is ready:\n\n" +
      "👉 " + wrappedURL + "\n\n" +
      "You've been classified as: " + archetype + "\n\n" +
      "Discover your full stats, download your card, and share your results!\n\n" +
      "See you at the next CTF! 🚀\n\n" +
      "- CYBERCOM Team\n" +
      "#CYBERCOMValentineCTF";

    try {
      MailApp.sendEmail({
        to: email,
        subject: subject,
        body: body
      });

      Logger.log('Sent to: ' + email);
      Utilities.sleep(1000); // 1 second delay between emails
    } catch (e) {
      Logger.log('Error sending to ' + email + ': ' + e);
    }
  }

  Logger.log('All emails sent!');
}
```

4. **IMPORTANT: Update the URL in the script!**
   - Line 12: Replace `YOUR-URL.netlify.app` with your actual Netlify URL

5. **Test with ONE email first:**
   - Modify line 5: `for (var i = 1; i < 2; i++)`
   - This sends only to the first player
   - Click "Run"
   - Authorize Gmail permissions (Google will ask)
   - Check that player's email inbox
   - Did they receive it? Does the link work?

6. **Send to ALL players:**
   - Change back to: `for (var i = 1; i < data.length; i++)`
   - Click "Run"
   - Wait ~3 minutes (163 emails at 1/second)
   - Check logs for any errors

### Option B: Manual Email (if Google Apps Script doesn't work)

You can also send emails manually:
1. Open your email client
2. BCC all 163 emails (copy from player_data.csv)
3. Use this template:

```
Subject: 🎉 Your CYBERCOM Valentine's CTF Wrapped is Here!

Hi there,

Thank you for participating in CYBERCOM's Valentine's Day CTF!

Your personalized CTF Wrapped is ready:
👉 https://YOUR-URL.netlify.app/[USERNAME].html

(Note: Replace [USERNAME] with your CTF username)

Discover your hacker archetype, view your stats, and share your results!

See you at the next CTF! 🚀

- CYBERCOM Team
#CYBERCOMValentineCTF
```

---

## 🎯 STEP 4: LAUNCH! (NOW!)

1. ✅ Confirm Netlify site is live
2. ✅ Test 5 random player pages
3. ✅ Test share buttons work
4. ✅ Test card download works
5. ✅ Send test email to yourself
6. ✅ If all good → Send to all 163 players!

---

## 📊 MONITORING

**After sending emails:**

- **Netlify Analytics:** Check how many people visit
  - Go to your Netlify dashboard
  - Click "Analytics"
  - See page views in real-time

- **Social Media:** Search for #CYBERCOMValentineCTF
  - See who's sharing
  - Repost the best ones
  - Engage with participants

- **Email responses:** Reply to any questions

---

## 🆘 TROUBLESHOOTING

**Problem: Netlify deployment fails**
- **Solution:** Folder might be too large. Try compressing images or splitting deployment.

**Problem: Share buttons don't work**
- **Solution:** Make sure you updated BASE_URL and regenerated pages.

**Problem: Emails not sending**
- **Solution:** Gmail has limits. Wait 1 hour and try again, or use Mailchimp.

**Problem: Player page shows wrong data**
- **Solution:** Check player_data.csv has correct info. Regenerate pages if needed.

**Problem: Images not loading**
- **Solution:** Make sure cards/ folder was uploaded to Netlify with HTML files.

---

## 🎉 SUCCESS METRICS

**Good launch:**
- ✅ 80%+ email delivery rate
- ✅ 50%+ players open their wrapped page
- ✅ 10+ social media shares
- ✅ Positive feedback from participants

**Great launch:**
- ✅ 90%+ email delivery
- ✅ 70%+ open rate
- ✅ 30+ social shares
- ✅ Viral engagement

---

## 📝 POST-LAUNCH

**After 1 week:**
1. Download Netlify analytics
2. Count social media mentions
3. Collect testimonials
4. Take screenshots of best shares
5. Plan improvements for next CTF!

---

## 🔄 UPDATING AFTER LAUNCH

**If you need to fix something:**

1. Make changes to files
2. Re-run generation scripts
3. Drag `wrapped_pages` to Netlify again
4. Netlify automatically updates the site
5. No need to resend emails (links stay the same!)

---

## 🎊 YOU'RE READY!

Everything is set up and ready to launch!

**Total time to complete:** 30 minutes
**Players reached:** 163
**Engagement potential:** High!

**GOOD LUCK! 🚀**

---

*Created: Feb 15, 2026*
*Project: CYBERCOM Valentine's Day CTF Wrapped*
