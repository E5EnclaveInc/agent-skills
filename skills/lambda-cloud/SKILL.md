---
name: lambda-cloud
description: "Operate Lambda Cloud GPU instances from the CLI: list instance types with live pricing and regional capacity, launch/terminate/restart behind a confirm gate, manage SSH keys and filesystems. Use for evaluation, prototype, or burst GPU work. Credential via the LAMBDA_API_KEY environment variable or ~/.lambda/api_key (mode 600); every mutating command requires --confirm."
license: MIT
compatibility: "Requires a Lambda Cloud account and API key."
metadata:
  version: 1.0.0
---
# Lambda Cloud (GPU) — evaluation / burst lane

Lambda GPU Cloud used as the **evaluation / prototype / burst lane**: the
place workloads go when they need a real GPU for hours, not a home. It is a
burst lane, not a home — nothing critical may depend on this lane surviving;
vendor credits are a subsidy, not architecture.

Console: https://cloud.lambda.ai · API: `https://cloud.lambdalabs.com/api/v1`
(`cloud.lambda.ai` is an alias host; the client uses `cloud.lambdalabs.com`).

## Credential model (machine-minted secret, 600-file pattern)

1. Mint a Cloud API key in the Lambda console (give it a descriptive name)
   and store it at `~/.lambda/api_key` (chmod 600, dir 700). Machine-minted
   shared secrets are handled by the agent; human passwords always go
   through your secret store.
2. `bin/lambda.py` / `bin/lambda_check.py` read `LAMBDA_API_KEY` from the
   environment first, falling back to `~/.lambda/api_key`.
3. Agents read the key only through those clients. **Never** echo it, log
   it, put it in argv, write it elsewhere, or paste it in chat.
   `bin/lambda_check.py` verifies auth any time.

## API surface (grounded in the official spec v1.10.0, recon 2026-09-15)

Auth: `Authorization: Bearer <key>`; HTTP Basic (`curl -u $KEY:`, key as
username, blank password) is also accepted. The API is Cloudflare-fronted
with bot management — a default script User-Agent can draw an HTML 403;
the client sends a browser User-Agent. Rate limits: ~1 req/sec overall;
launch is 1 req / 12 sec or 5 / min (`lambda.py` sleeps 1.2 s between calls).
Success payloads nest under `data`; errors are
`{error: {code, message, suggestion, request_id}}` — match on `code`, not
message text.

| Operation | Method + path |
|---|---|
| List instance types (specs, pricing, regional capacity) | `GET /instance-types` |
| List instances | `GET /instances` |
| Get one instance | `GET /instances/{id}` |
| Launch | `POST /instance-operations/launch` |
| Terminate | `POST /instance-operations/terminate` |
| Restart | `POST /instance-operations/restart` |
| SSH keys: list / add / delete | `GET,POST /ssh-keys` · `DELETE /ssh-keys/{id}` |
| Filesystems: list | `GET /file-systems` |

The wider spec carries more surface (regions, images, audit events,
filesystem create/delete, instance rename). This skill's client uses only
the operations above — every one re-verified against the current public
API documentation during export. Verify any additional endpoint against
the live OpenAPI document before relying on it.

**Launch request** (`InstanceLaunchRequest`) — required: `region_name`,
`instance_type_name`, `ssh_key_names` (**exactly one** key, per the spec).
Optional: `file_system_names`, `file_system_mounts`, `hostname`
(`^[a-z0-9][0-9a-z-]{0,62}$`, ≤63 chars), `name` (≤64 chars), `image`
(defaults to latest Lambda Stack), `user_data` (cloud-init, plain text,
**≤1 MB**), `tags`, `firewall_rulesets`. Notable launch errors:
`provider/insufficient-capacity`, `quota-exceeded`,
`invalid-billing-address`, `filesystem-in-wrong-region`.

**Firewall (measured lesson):** a default workspace global ruleset may
allow ONLY tcp/22 + icmp inbound. Five consecutive GPU runs once failed
identically because inbound tcp/8080 was dropped at the provider edge —
the health probes saw persistent TCP *timeout* (curl rc 28), never
conn-refused, and every setup log died with the box. Any workload that
must be reachable inbound needs a firewall ruleset with the port open,
created in the launch region and attached via `--firewall-rulesets <ids>`
(supported by `bin/lambda.py`). Design rule learned: the box must beacon
OUT (HTTPS) from minute 1 — never depend on inbound reachability for the
boot story.

**Instance types** (`GET /instance-types` is the live price list — always
read it before launch; prices below are a 2026 community snapshot, verify
live): B200 SXM6 180 GB ~$4.99/GPU/hr · H100 SXM 80 GB ~$2.99–3.29 ·
H100 PCIe 80 GB ~$2.49 · GH200 96 GB ~$1.49 · A100 80 GB ~$1.79 ·
A100 40 GB ~$1.29 · A10 24 GB ~$0.75 · A6000 48 GB ~$0.80 ·
V100 16 GB ~$0.55. Billing is pay-per-minute (verify current terms live).

**SSH:** an SSH key must be registered *before* launch. Add via
`lambda.py ssh-keys-add`: either upload your public key (`--public-key`),
or omit it and Lambda **generates a keypair server-side** — the private
key is returned once and saved immediately (0600); **Lambda does not
retain it**. SSH user is `ubuntu`: `ssh -i key.pem ubuntu@<ip>`.
Instances come with Lambda Stack (Ubuntu 22.04, NVIDIA drivers, CUDA,
cuDNN, NCCL, PyTorch, TensorFlow, JupyterLab).

**Filesystems:** persistent NFS mounted at `/lambda/nfs/<name>`; attach
only at launch via `file_system_names`; filesystem region must match the
instance region. Storage bills monthly (check current pricing) — terminate filesystems
too, or they keep billing.

## The sandbox SSH story

If your agent sandbox's egress is HTTPS-only, there is **no SSH from the
sandbox**. This skill's client handles *lifecycle* (launch / list /
terminate / restart), never shell access. Instance command execution goes
through one of:
1. an operator or builder agent with SSH access, or
2. `user_data` cloud-init at launch (preferred for unattended runs —
   bootstrap, run the benchmark, write results to the filesystem or
   push them out; then terminate).

## Common operations

```bash
export LAMBDA_API_KEY=...            # injected from the Secure Vault at runtime
python3 bin/lambda_check.py          # read-only auth check + account snapshot
python3 bin/lambda.py types                    # types, live $/hr, capacity regions
python3 bin/lambda.py types --region us-west-1
python3 bin/lambda.py list
python3 bin/lambda.py get <instance-id>
# preview (sends nothing):
python3 bin/lambda.py launch --region us-west-1 --type gpu_1x_a10 \
    --ssh-key my-builder --name bench-01 --dry-run
# real launch (refuses without --confirm):
python3 bin/lambda.py launch --region us-west-1 --type gpu_1x_a10 \
    --ssh-key my-builder --name bench-01 --confirm
python3 bin/lambda.py terminate <id> --confirm
python3 bin/lambda.py restart <id> --confirm
python3 bin/lambda.py ssh-keys
python3 bin/lambda.py ssh-keys-add --name my-builder --public-key ~/.ssh/id_ed25519.pub
```

Every mutating command requires an explicit `--confirm`; `launch`
additionally prints the burn-cap reminder and refuses to send on
`--dry-run` alone. `launch` checks live capacity and refuses when the
type has no capacity in the requested region.

## Cost stewardship (hard rules)

1. **No launch without a frozen benchmark protocol on file** (the suite:
   multi-step tool calls, long-context recall, vision critique, bpy-code
   loops — with pass criteria) **and a per-run burn cap**: hypothesis,
   cheapest falsifying instance type, max dollars, abort condition.
2. **Cheapest falsifier wins** — always the cheapest type that can answer
   the question. An A10 at $0.75/hr answers most inference questions; an
   H100 is not the default.
3. **Terminate the instant the run ends.** No idle burn, ever. A run's
   last step is `terminate`.
4. **Weekly dollars-to-question ledger** to the operator: what each
   dollar answered.
5. **Never let expiry drive wasteful spend** — a credit expiring unspent
   is fine; burning it on theater is a breach.
6. **No design may depend on the credits persisting.** When they expire,
   your resident infrastructure keeps running without this lane.

## Security

The API key is a bearer secret: env-var only, never in chat, logs, files,
argv, or generated code. Generated SSH private keys are saved 0600 and
backed up off-box. Identifiers (instance ids, key names) are non-secret.

## Ambiguities (recon notes, 2026-09-15)

- **Credit balance has no public API endpoint** (checked the full spec)
  — balance is console-only at https://cloud.lambda.ai/billing.
  `lambda_check.py` proves auth; it cannot report your balance.
- The docs' SSH tutorial example includes `"quantity": 1` in a launch
  body, but `quantity` is **absent from the `InstanceLaunchRequest`
  schema** — unverified; the client sends single-instance launches only.
- Exact `status` string values for instances are not enumerated in the
  spec — treat as opaque, match loosely.
- The `ubuntu` SSH user comes from community skills, not the official
  spec — confirm on first live instance.
