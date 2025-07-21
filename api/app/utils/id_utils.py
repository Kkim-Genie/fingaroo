import nanoid


def generate_nanoid(length: int = 21) -> str:
    """
    Generate a nanoid with the specified length.
    Default length is 21 characters (nanoid's default).
    
    Args:
        length: The length of the generated ID
        
    Returns:
        A random string ID
    """
    id = nanoid.generate(alphabet="abcdefghijklmnopqrstuvwxyz0123456789", size=length)  
    return id