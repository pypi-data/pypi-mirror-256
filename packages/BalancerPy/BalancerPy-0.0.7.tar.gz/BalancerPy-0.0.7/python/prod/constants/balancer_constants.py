from decimal import Decimal

ONE_WEI = Decimal('0.000000000000000001')
BONE = Decimal('1')
MIN_BOUND_TOKENS = 2
MAX_BOUND_TOKENS = 8
MIN_FEE = Decimal('0.000001')
MAX_FEE = Decimal('0.1')
EXIT_FEE = 0
MIN_WEIGHT = BONE
MAX_WEIGHT = BONE * Decimal('50')
MAX_TOTAL_WEIGHT = BONE * Decimal('50')
MIN_BALANCE = Decimal('0.000000000001')
INIT_POOL_SUPPLY = BONE * Decimal('100')
MIN_BPOW_BASE = Decimal('0.000000000000000001')
MAX_BPOW_BASE = (Decimal('2') * BONE) - ONE_WEI
BPOW_PRECISION = BONE / Decimal('10000000000')
MAX_IN_RATIO = BONE / Decimal('2')
MAX_OUT_RATIO = (BONE / Decimal('3')) + ONE_WEI
