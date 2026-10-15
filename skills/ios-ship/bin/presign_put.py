# SigV4 presigned PUT for R2 (query auth) — derived, expiring capability; value printed is the URL only
import sys,os,hashlib,hmac,datetime,urllib.parse
AK=os.environ["R2_ACCESS_KEY_ID"];SK=os.environ["R2_SECRET_ACCESS_KEY"]
ACC=os.environ.get("CLOUDFLARE_ACCOUNT_ID") or sys.exit("set CLOUDFLARE_ACCOUNT_ID (no default: your account ID is yours)")
HOST=f"{ACC}.r2.cloudflarestorage.com"
def sign(key,msg):return hmac.new(key,msg.encode(),hashlib.sha256).digest()
def presign_put(bucket,key,expires=14400):
    now=datetime.datetime.utcnow();amz=now.strftime("%Y%m%dT%H%M%SZ");ds=now.strftime("%Y%m%d")
    scope=f"{ds}/auto/s3/aws4_request"
    enc_key="/".join(urllib.parse.quote(s,safe="") for s in key.split("/"))
    uri=f"/{bucket}/{enc_key}"
    q={"X-Amz-Algorithm":"AWS4-HMAC-SHA256","X-Amz-Credential":f"{AK}/{scope}","X-Amz-Date":amz,
       "X-Amz-Expires":str(expires),"X-Amz-SignedHeaders":"host"}
    qs="&".join(f"{urllib.parse.quote(k,safe='')}={urllib.parse.quote(v,safe='')}" for k,v in sorted(q.items()))
    creq=f"PUT\n{uri}\n{qs}\nhost:{HOST}\n\nhost\nUNSIGNED-PAYLOAD"
    sts=f"AWS4-HMAC-SHA256\n{amz}\n{scope}\n{hashlib.sha256(creq.encode()).hexdigest()}"
    k=sign(sign(sign(sign(("AWS4"+SK).encode(),ds),"auto"),"s3"),"aws4_request")
    sig=hmac.new(k,sts.encode(),hashlib.sha256).hexdigest()
    return f"https://{HOST}{uri}?{qs}&X-Amz-Signature={sig}"
print(presign_put(sys.argv[1],sys.argv[2],int(sys.argv[3]) if len(sys.argv)>3 else 14400))
