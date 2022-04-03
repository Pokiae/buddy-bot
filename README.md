# Buddy Bot    
## What is Buddy Bot ?    
Buddy Bot is a Discord bot which has been created to manage roles attribution in a guild. Therefore it can :    
- **Add or remove** roles when a user react to a message with emojis ;
- Give a **specific role** after receiving the associated **password**.    

All the messages send by the bot will be in French, as it was created for a French speaking guild.

## How do I configure it ?    

### 1. Enter your token (master.py)    

You just have to put your own token here (l.41) :    
```python
client.run(YOUR_TOKEN)
```    

### 2. Put the ID of your guild and the bot ID (config.py)    

Enter the ID of the guild the bot has to manage (l.9) :    
```python
id_guild = YOUR_GUILD_ID
```

/!\ Please note that **the bot can only manage ONE guild** /!\    

You have to put your bot ID too (l.11) :   
```python
moi = YOUR_BOT_ID
```

### 3. Configure the "open" roles attribution (config.py)    
Buddy bot is able to give roles based on a **user reaction to a specific message**. To configure this you will have to (l.2) :    
* Enter the ID of the message you want the user to react in order to have the role ;    
* Associate the emojis to the ID of the role they give access to.    
```python
message_under_watching = {YOUR_MESSAGE_ID: {'YOUR EMOJI': YOUR_ROLE_ID,
                                               '🏠': 00000000000000, #those are examples
                                               '🌍': 00000000000000,
                                               '🎲': 00000000000000,
                                               '🎭': 00000000000000,
                                               '📰': 00000000000000,
                                               '🧑‍⚖️': 00000000000000}}
```
You can of course add several messages the bot will have to watch :    
```python
message_under_watching = {YOUR_MESSAGE_ID_1: {'YOUR EMOJI 1': YOUR_ROLE_ID_1}
                          YOUR_MESSAGE_ID_2: {'YOUR EMOJI 2': YOUR_ROLE_ID_2, #Here the bot will watch 2 messages
                                              'YOUR EMOJI 3': YOUR_ROLE_ID_3}}
```

### 3bis. Configure the entry system (config.py)    
This feature was done espacially to fit the guild it was created for, because of how specific it is, **I do not recommend using this feature** if your guild works differently. The bot will automatically give any new user arriving in the guild a role. This was done so the new user could **only see the rules message** and had to agree to it by **reacting with a specific emoji**. Once they reacted, the *arriving role* would be removed and they would receive a *basic role* which allow them to see the whole guild.    

In order to make this work, you just have to enter the following informations (l.26-30) :    
```python
rules_channel = YOUR_RULE_CHANNEL_ID
entry_message = YOUR_RULE_MESSAGE_ID

arriving_role_id = YOUR_ARRIVING_ROLE_ID
basic_member_role_id = YOUR_BASIC_ROLE_ID
```

**/!\\** The bot has been done a specific way, so the emoji used to approve the rules ***MUST HAVE A NAME WHICH STARTS WITH "coche"* /!\\**    

Other useful informations :    
* When the bot starts, it will automatically check which user accepted the rules and will give to the others the *arriving role* ;
* When a user removes their reaction to the rules message, the bot will give him the the *arriving role* and removes it if the user puts their reaction back.

### 4. Configure the attribution with passwords (config.py variables.py)    
This is to give roles only to the users who have the associatied password (in order to restrain the access to roles with higher permissions for example). To obtain the role, the user will have to **send a private message** to the bot. They must give **one or several** *key words*, the bot will then ask for the password associated to each *key word*.    

#### Enter the key words and the associated role (config.py l.14)    
/!\ The key words must be in **lower case** /!\    
```python
alias_to_roles = {'student': 00000000000000,
                  'teacher': 00000000000000,
                  'cinema': 00000000000000,
                  'YOUR_KEY_WORD': YOUR_ROLE_ID}
```

#### Associate the key word to its password (variables.py l.13)    
```python
passwords = {"student": STUDENT_PASSWORD,
             "teacher": TEACHER_PASSWORD,
             "cinema": CINEMA_PASSWORD,
             'YOUR_KEY_WORD': YOUR_PASSWORD}
```

***/!\ EXTREMELY IMPORTANT : YOUR PASSWORD MUST BE HASHED USING SHA-256, ELSE THE BOT WON'T RECOGNIZE THE PASSWORD EVEN IF IT IS CORRECTLY GIVEN /!\\***     
## Useful links    
* [Link to discord.py docs](https://discordpy.readthedocs.io/en/stable/)
* [Link to dicord developer portal](https://discord.com/developers/docs/intro)
