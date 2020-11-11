#!/usr/bin/env python3
import rsa

public, private = rsa.newkeys(512)
with open("private_key.txt", "w") as pr:
    pr.write("{} {} {} {} {}".format(private.n, private.e, private.d, private.p, private.q))
with open("public_key.txt", "w") as pub:
    pub.write("{} {}".format(public.n, public.e))
