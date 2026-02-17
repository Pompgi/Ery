import random

# Trigger responses dictionary
TRIGGERS = [
    {
        "keywords": ["peepeepoopoo"],
        "response": "peepeepoopoo"
    },
    {
        "keywords": ["food"],
        "response": lambda message: f"HMMMM, Very tasky, {message.author.mention}!"
    },
    {
        "keywords": ["im hungry", "i'm hungry"],
        "response": lambda message: f"Hi HUNGRY, I'm DAD {message.author.mention}!"
    },
    {
        "keywords": ["im bak", "i'm bak", "bak", "im back", "i'm back"],
        "response": lambda message: f"Hi BACK, i'm FRONT {message.author.mention}!"
    },
    {
        "keywords": ["talk"],
        "response": lambda message: random.choice([
            f"You are loved, and I'm one of the many people who love you",
            f"Sometime it might not be much, but how you got here is definitely no easy road, and you should be proud of yourself",
            f"Yes tell me how are you today as well, I've missed you",
            f"Have you ever wondered the probability of us meeting? crazy am i right?",
            f"Hey, i'm here!",
            f"Nah, id rather stare into your eyes and listen to your voice"
        ])
    }
]

async def check_triggers(message, content):
    """Check if any triggers match the message content and respond accordingly."""
    responded = False
    
    for trigger in TRIGGERS:
        if not responded and any(keyword in content for keyword in trigger["keywords"]):
            if callable(trigger["response"]):
                response = trigger["response"](message)
            else:
                response = trigger["response"]
            
            await message.channel.send(response)
            responded = True
            
            # Return early for talk trigger to prevent further processing
            if trigger["keywords"] == ["talk"]:
                return True
    
    return responded
