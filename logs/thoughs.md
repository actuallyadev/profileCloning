## 2025-05-29
### Thoughts:
    - Looking at the last commit the work is clear.

    - I will start with the accepting cookie logic.
    
    - The webdriverwait does not really matter for reasons unknown to me
    
    - Cookie accepting logic is working now.
    
    - Next item on the list is between implementing concurrency or captcha finding 
    
    - I have decided on captcha finding as concurrency does not make any sense
    if the warm-up was not effective.
    
    - A 10 minute test will be ran to check for captchas, I need to integrate
    the CaptchaFinder class into my main warm_up script and record captchas
    triggered
    
    - For a 10 minute test we must use profiles that have been warmed up for X time
    and profiles that have not been warmed at all.
    
    - For this we have to change the act_like_a_human function, and make it so
    that there is a sleep between each action, making scrolling 4 times more likely
    to happen than clicking something, executing 25-50 actions instead of the 75-100
    I had planned and make scrolling more realistic: slower and smaller.

    - Implemented these changes in the warm_up.py script, moved set_up_driver to utils.py
    to avoid circular imports. Fixed imports in captcha_finder.py

## 2025-06-01
### Thoughts:
    - Looking at the first commit today, warm up a profile for 10 minutes with X
    elements interacted, scrolling over posts? Then test with the same automation
    settings the warmed up profile and a fresh one.
    - After this we could try to emulate human behaviour better, adding more sleep,
    adding mouse movements, something like that to see the difference in captchas
    triggered
    - Done with the script, testing captchas looks good aswell, have not tested it
    need to go to the gym rn.