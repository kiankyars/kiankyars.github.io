---
layout: post
title: Github SSH
date: 2025-01-30
categories: software
---

Follow these numbered steps to set up your SSH key for GitHub:

1. **Set permissions**  
   Ensure your private key is accessible only by you:

   ```bash
   chmod 600 ~/.ssh/id_rsa
   chmod 644 ~/.ssh/id_rsa.pub
   ```

   _(Replace `id_rsa` with your key name if different.)_

2. **Start the SSH agent**  
   Launch the agent to manage your keys:

   ```bash
   eval "$(ssh-agent -s)"
   ```

3. **Add your SSH key to the agent**

   ```bash
   ssh-add ~/.ssh/id_rsa
   ```

4. **Verify the key is added**

   ```bash
   ssh-add -l
   ```

   _(Should display your key's fingerprint.)_

5. **Test SSH connection to GitHub**
   ```bash
   ssh -T git@github.com
   ```
   _(You should see a success or authentication message.)_
