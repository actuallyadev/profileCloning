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
    - Back from the gym, at the library, I tried running test_captcha.py, I realized
    that some links need you to be logged into an account to actually show any relevant
    content, I asked ChatGPT o3 to give me some relevant links, and I am setting
    elements_over_scrolling to True, with a ratio of 3/2. For every 3 elements clicked,
    2 actions are spent scrolling.
    - Some ChatGPT o3 links where shit, so I had to modify them, I have to modify
    the get_creep_js_output function to return an empty dictionary when there is
    an exception
    - Ran one test of 4 minutes, no difference. I will up the interactions instead
    of 15, to 500.
    - Also realized that clicking buttons with CTAs for logging in or registering
    an account is not the behaviour we want since it will break normal requests
    and just make the driver go off into terms and conditions.
    - For this last point, I have to change logic in get_random_element to call
    my new function: is_not_log_in_or_register_stem, which takes the element text
    (or maybe a concatenation of title, aria-label, text and others attributes).
    - Need to change sleep to == 0, lower threshold + 0
    - Ran the test with these settings, triggered one captcha with the "warmed_up"
    profile, and zero with the "fresh" profile.
    - Maybe a fresh profile works just right, maybe I need to implement selenium concurrency,
    or change frameworks or execute several drivers, idk at this point.
    - The issue is that test_captchas even if it has 500 interactions per site,
    it will only cover the first one, even when the sleep is set to 0
    - Fuck this, imma go read a book, I will be back though