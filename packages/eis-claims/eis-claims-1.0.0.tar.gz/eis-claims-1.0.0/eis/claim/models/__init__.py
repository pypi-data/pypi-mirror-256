# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from eis.claim.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from eis.claim.model.create_claim_request_dto import CreateClaimRequestDto
from eis.claim.model.update_claim_request_dto import UpdateClaimRequestDto
