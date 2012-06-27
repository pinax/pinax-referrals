import random


def generate_code(referral_class):
    def _generate_code():
        t = "abcdefghijkmnopqrstuvwwxyzABCDEFGHIJKLOMNOPQRSTUVWXYZ1234567890"
        return "".join([random.choice(t) for i in range(40)])
    
    code = _generate_code()
    while referral_class.objects.filter(code=code).exists():
        code = _generate_code()
    return code
