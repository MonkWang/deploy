import hashlib
from urllib.parse import urlencode

cj_act_id = 1
cj_app_id = 1
cj_user_uuid = 1
coupon_code = 1
mobile = 1
key = 1
arr = dict(
    mobile=mobile,
    cj_app_id=cj_app_id,
    cj_act_id=cj_act_id,
    cj_user_uuid=cj_user_uuid,
    coupon_code=coupon_code,
)
arr = dict(sorted(arr.items(), key=lambda e: e[0]))
arr["key"] = key

m = hashlib.md5()
query = urlencode(arr)
print(query)
m.update(query.encode("utf8"))
sign = m.hexdigest().upper()
print(sign)
