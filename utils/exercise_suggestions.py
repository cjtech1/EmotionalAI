"""
Exercise Suggestions - Contains exercises for different mental health states
"""

import random

BREATHING_EXERCISES = [
    {
        "name": "4-7-8 Breathing",
        "description": "Inhale for 4 seconds, hold for 7 seconds, exhale for 8 seconds. Repeat 4 times.",
        "benefits": "Helps reduce anxiety and promote sleep"
    },
    {
        "name": "Box Breathing",
        "description": "Inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds, hold for 4 seconds. Repeat for 2-3 minutes.",
        "benefits": "Reduces stress and improves concentration"
    },
    {
        "name": "Deep Belly Breathing",
        "description": "Place your hand on your belly. Breathe in deeply through your nose for 5 seconds, feeling your hand rise. Exhale slowly through your mouth for 5 seconds. Repeat 10 times.",
        "benefits": "Activates relaxation response and reduces anxiety"
    },
    {
        "name": "Alternate Nostril Breathing",
        "description": "Close your right nostril with your thumb, inhale through left nostril. Close left nostril with ring finger, exhale through right nostril. Repeat, alternating sides for 5 minutes.",
        "benefits": "Balances energy and calms the mind"
    }
]

MINDFULNESS_EXERCISES = [
    {
        "name": "5-4-3-2-1 Grounding",
        "description": "Acknowledge 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste.",
        "benefits": "Helps bring you back to the present moment during anxiety"
    },
    {
        "name": "Body Scan",
        "description": "Lie down and focus your attention on each part of your body, from your toes to your head, noticing any sensations without judgment.",
        "benefits": "Reduces tension and increases body awareness"
    },
    {
        "name": "Mindful Observation",
        "description": "Choose an object and focus on it for 5 minutes. Notice its color, texture, shape, and other details as if seeing it for the first time.",
        "benefits": "Improves focus and presence"
    }
]

JOURNALING_EXERCISES = [
    {
        "name": "Gratitude Journal",
        "description": "Write down 3 things you're grateful for today, no matter how small.",
        "benefits": "Shifts focus to positive aspects of life"
    },
    {
        "name": "Thought Record",
        "description": "Write down a troubling thought, identify the emotion, find evidence for and against it, then create a balanced thought.",
        "benefits": "Helps challenge negative thinking patterns"
    },
    {
        "name": "Stream of Consciousness",
        "description": "Write continuously for 10 minutes without stopping or judging what comes out.",
        "benefits": "Releases mental clutter and provides clarity"
    },
    {
        "name": "Worry Time",
        "description": "Schedule 15 minutes to write down all your worries. When worries arise outside this time, note them for your next scheduled worry time.",
        "benefits": "Contains worries to a specific time instead of all day"
    }
]

PHYSICAL_EXERCISES = [
    {
        "name": "Progressive Muscle Relaxation",
        "description": "Tense and then relax each muscle group in your body, from feet to face.",
        "benefits": "Reduces physical tension and promotes relaxation"
    },
    {
        "name": "Gentle Stretching",
        "description": "Gently stretch your neck, shoulders, arms, and back for 5-10 minutes.",
        "benefits": "Releases physical tension and improves circulation"
    },
    {
        "name": "Quick Walk",
        "description": "Take a 10-minute walk, focusing on your surroundings and the sensation of walking.",
        "benefits": "Boosts mood and provides a mental break"
    }
]

def get_random_exercise(exercise_type=None):
    """
    Return a random exercise suggestion based on type.
    If type is None, returns a random exercise from any category.
    """
    if exercise_type == "breathing":
        return random.choice(BREATHING_EXERCISES)
    elif exercise_type == "mindfulness":
        return random.choice(MINDFULNESS_EXERCISES)
    elif exercise_type == "journaling":
        return random.choice(JOURNALING_EXERCISES)
    elif exercise_type == "physical":
        return random.choice(PHYSICAL_EXERCISES)
    else:
        all_exercises = (BREATHING_EXERCISES + MINDFULNESS_EXERCISES + 
                        JOURNALING_EXERCISES + PHYSICAL_EXERCISES)
        return random.choice(all_exercises)
        
def get_exercise_for_state(mental_state):
    """
    Return appropriate exercise based on detected mental state.
    """
    if mental_state == "anxiety":
        return random.choice(BREATHING_EXERCISES + MINDFULNESS_EXERCISES)
    elif mental_state == "depression":
        return random.choice(PHYSICAL_EXERCISES + JOURNALING_EXERCISES)
    elif mental_state == "burnout":
        return random.choice(BREATHING_EXERCISES + PHYSICAL_EXERCISES)
    else:
        return get_random_exercise()
