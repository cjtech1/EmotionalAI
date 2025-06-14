"""
Mental Health Resources - Contains information about mental health resources
"""

# Crisis Resources
CRISIS_RESOURCES = [
    {
        "name": "National Suicide Prevention Lifeline",
        "description": "24/7, free and confidential support for people in distress",
        "contact": "1-800-273-8255",
        "website": "https://suicidepreventionlifeline.org/"
    },
    {
        "name": "Crisis Text Line",
        "description": "Free 24/7 text support for those in crisis",
        "contact": "Text HOME to 741741",
        "website": "https://www.crisistextline.org/"
    }
]

# General Mental Health Resources
GENERAL_RESOURCES = [
    {
        "name": "National Alliance on Mental Illness (NAMI)",
        "description": "Advocacy, education, and support for individuals affected by mental illness",
        "website": "https://www.nami.org/",
        "helpline": "1-800-950-NAMI (6264)"
    },
    {
        "name": "Mental Health America",
        "description": "Promotes mental health and provides resources and screenings",
        "website": "https://www.mhanational.org/"
    },
    {
        "name": "Substance Abuse and Mental Health Services Administration (SAMHSA)",
        "description": "Information and treatment referrals",
        "website": "https://www.samhsa.gov/",
        "helpline": "1-800-662-HELP (4357)"
    }
]

# Apps and Online Resources
ONLINE_RESOURCES = [
    {
        "name": "Headspace",
        "description": "Meditation and mindfulness app",
        "website": "https://www.headspace.com/"
    },
    {
        "name": "Calm",
        "description": "Sleep, meditation and relaxation app",
        "website": "https://www.calm.com/"
    },
    {
        "name": "7 Cups",
        "description": "Online therapy and free emotional support",
        "website": "https://www.7cups.com/"
    },
    {
        "name": "Moodfit",
        "description": "Tools to help your mental health, including mood tracking",
        "website": "https://www.getmoodfit.com/"
    }
]

# Books and Reading Materials
READING_RESOURCES = [
    {
        "name": "The Anxiety and Phobia Workbook",
        "author": "Edmund J. Bourne",
        "description": "Practical guide with exercises for managing anxiety"
    },
    {
        "name": "Feeling Good: The New Mood Therapy",
        "author": "David D. Burns",
        "description": "Classic self-help book using cognitive behavioral therapy principles"
    },
    {
        "name": "The Upward Spiral",
        "author": "Alex Korb",
        "description": "Uses neuroscience to explain how to reverse depression"
    }
]

def get_resources_by_concern(concern_level):
    """
    Return appropriate resources based on concern level
    """
    if concern_level == "critical":
        return {
            "message": "These resources can provide immediate support:",
            "resources": CRISIS_RESOURCES
        }
    elif concern_level == "high":
        return {
            "message": "Here are some helpful mental health resources:",
            "resources": CRISIS_RESOURCES + GENERAL_RESOURCES[:1]
        }
    elif concern_level == "moderate":
        return {
            "message": "These resources might be helpful:",
            "resources": GENERAL_RESOURCES + ONLINE_RESOURCES[:2]
        }
    else:
        return {
            "message": "If you're interested in learning more about mental wellness, check out these resources:",
            "resources": ONLINE_RESOURCES + READING_RESOURCES[:1]
        }
