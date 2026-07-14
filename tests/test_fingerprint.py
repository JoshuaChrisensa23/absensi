from fingerprint.verify import FingerprintVerifier

verify = FingerprintVerifier()
user = verify.wait()
print()
print(user)
