
__instance = None

class Singleton(object):
    """
    Class used to allow classes to be Singletons.
    """

    @staticmethod
    def instance(cls, *args, **vargs):

        if isinstance(__instance, None):
            __instance = cls(*args, **vargs)
        
        return __instance