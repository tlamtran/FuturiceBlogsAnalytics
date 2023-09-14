def get_objectives_with_info(draft: str) -> list[dict]:
    """
    Analyzes the given draft text and produces its communication objectives ( = topics/categories).
    Besides objectives themselves, also produces supporting information that might be good to show
    to user.

    Example of a returned object (one of the list):

        [{
            "name": "Leading edge technology/innovation",

            "median_bounce_rate": 0.65,

            "median_views": 100,

            "rating": 95,
                rating is 0-100, where 100 is the best objective there is, and 0 is worst
                (might be good for e.g. showing it in green/red)

        }, {...}, ...]

    :returns: list of "communication objective" objects.
    """
    return []
